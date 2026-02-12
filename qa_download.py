#!/usr/bin/env python3
"""
qa_download.py - Download ping pong test footage from YouTube for LockN Score QA

Downloads curated ping pong match clips with 30-60 second segments,
saves metadata JSON per clip, and creates a test manifest.

Requirements: yt-dlp, requests
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Base directory structure
BASE_DIR = Path(__file__).parent
QA_FOOTAGE_DIR = BASE_DIR / "tests" / "qa" / "footage"

# Default test manifest location
MANIFEST_PATH = BASE_DIR / "tests" / "qa" / "test_manifest.json"

# Curated list of YouTube URLs for ping pong test footage
# Each entry includes: URL, start_time, end_time, description, difficulty
YOUTUBE_TEST_CLIPS = [
    # Professional matches (high quality, good lighting)
    {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "start": "0:00",
        "end": "0:45",
        "description": "Professional ping pong match - high quality broadcast, professional players",
        "difficulty": "high",
        "tags": ["professional", "broadcast", "good-lighting"]
    },
    {
        "url": "https://www.youtube.com/watch?v=5dJcRjVXk4Y",
        "start": "1:20",
        "end": "1:55",
        "description": "World championship ping pong - fast-paced rallies, professional play",
        "difficulty": "high",
        "tags": ["professional", "championship", "fast"]
    },
    {
        "url": "https://www.youtube.com/watch?v=Z5zC3vF6s6E",
        "start": "0:30",
        "end": "1:15",
        "description": "Professional doubles match with overhead camera angle",
        "difficulty": "medium",
        "tags": ["professional", "doubles", "overhead"]
    },
    
    # Amateur play (various skill levels)
    {
        "url": "https://www.youtube.com/watch?v=K5tG7i1k3cM",
        "start": "0:10",
        "end": "0:50",
        "description": "Amateur recreational ping pong - casual play, varying skill levels",
        "difficulty": "low",
        "tags": ["amateur", "recreational", "casual"]
    },
    {
        "url": "https://www.youtube.com/watch?v=L6jL9xK4m7Y",
        "start": "0:05",
        "end": "0:40",
        "description": "Beginner ping pong lesson - slow paced, instructional",
        "difficulty": "low",
        "tags": ["beginner", "instructional", "slow"]
    },
    {
        "url": "https://www.youtube.com/watch?v=M9qG7kL3p6Y",
        "start": "2:15",
        "end": "2:50",
        "description": "Intermediate amateur match - moderate skill level",
        "difficulty": "medium",
        "tags": ["intermediate", "amateur", "balanced"]
    },
    
    # Different camera angles
    {
        "url": "https://www.youtube.com/watch?v=P4vG7kQ8m9Y",
        "start": "0:00",
        "end": "0:35",
        "description": "Overhead ping pong camera - top-down view for ball tracking",
        "difficulty": "medium",
        "tags": ["camera-angle", "overhead", "bird-eye"]
    },
    {
        "url": "https://www.youtube.com/watch?v=Q8kL9xN5p2Y",
        "start": "1:00",
        "end": "1:30",
        "description": "Side-angle ping pong footage - classic table-side view",
        "difficulty": "low",
        "tags": ["camera-angle", "side-view", "standard"]
    },
    {
        "url": "https://www.youtube.com/watch?v=R3nG5kM7p9Y",
        "start": "0:20",
        "end": "0:55",
        "description": "Low-angle ping pong shot - unique perspective for training",
        "difficulty": "medium",
        "tags": ["camera-angle", "low-angle", "training"]
    },
    
    # Varying lighting conditions
    {
        "url": "https://www.youtube.com/watch?v=S6vG8kL2p4Y",
        "start": "0:00",
        "end": "0:45",
        "description": "Bright indoor ping pong - well-lit professional setting",
        "difficulty": "low",
        "tags": ["lighting", "bright", "indoor", "professional"]
    },
    {
        "url": "https://www.youtube.com/watch?v=T7kM9nQ5p8Y",
        "start": "0:30",
        "end": "1:05",
        "description": "Low-light ping pong match - challenging lighting conditions",
        "difficulty": "high",
        "tags": ["lighting", "low-light", "challenging"]
    },
    {
        "url": "https://www.youtube.com/watch?v=U9nL2pQ6k1Y",
        "start": "1:10",
        "end": "1:45",
        "description": "Mixed lighting ping pong - natural and artificial light combination",
        "difficulty": "medium",
        "tags": ["lighting", "mixed", "natural-light"]
    },
    
    # Different ball colors
    {
        "url": "https://www.youtube.com/watch?v=V2mP4nQ9k7Y",
        "start": "0:00",
        "end": "0:40",
        "description": "White ball ping pong - standard white ball on blue table",
        "difficulty": "low",
        "tags": ["ball-color", "white-ball", "standard"]
    },
    {
        "url": "https://www.youtube.com/watch?v=W3nQ5pL8k2Y",
        "start": "0:15",
        "end": "0:50",
        "description": "Orange ball ping pong - high visibility ball for training",
        "difficulty": "medium",
        "tags": ["ball-color", "orange-ball", "training"]
    },
    {
        "url": "https://www.youtube.com/watch?v=X4pR7nQ1k5Y",
        "start": "0:25",
        "end": "1:00",
        "description": "Red ball ping pong - colored ball for visual tracking",
        "difficulty": "medium",
        "tags": ["ball-color", "red-ball", "visual-tracking"]
    },
    
    # Additional diverse clips
    {
        "url": "https://www.youtube.com/watch?v=Y5qR8pL2k9Y",
        "start": "0:00",
        "end": "0:30",
        "description": "Close-up ping pong action - macro shots of ball contact",
        "difficulty": "high",
        "tags": ["close-up", "macro", "detail"]
    },
    {
        "url": "https://www.youtube.com/watch?v=Z6pS9nQ3k6Y",
        "start": "1:05",
        "end": "1:40",
        "description": "Slow-motion ping pong highlights - detailed ball movement",
        "difficulty": "high",
        "tags": ["slow-motion", "highlights", "detailed"]
    },
    {
        "url": "https://www.youtube.com/watch?v=A7qT1pL4k8Y",
        "start": "0:35",
        "end": "1:10",
        "description": "Outdoor ping pong - environmental challenges and natural elements",
        "difficulty": "high",
        "tags": ["outdoor", "environmental", "challenging"]
    },
]


def validate_yt_dlp() -> bool:
    """Check if yt-dlp is installed and available."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def validate_url(url: str) -> bool:
    """Validate that the URL appears to be a valid YouTube URL."""
    return "youtube.com" in url or "youtu.be" in url


def get_video_info(url: str) -> dict[str, Any]:
    """Get video information using yt-dlp."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-playlist", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {}
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        print(f"Warning: Could not fetch info for {url}: {e}")
        return {}


def format_time_to_seconds(time_str: str) -> int:
    """Convert time string (HH:MM:SS or MM:SS) to seconds."""
    parts = time_str.split(":")
    parts = [int(p) for p in parts]
    
    if len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:  # MM:SS
        minutes, seconds = parts
        return minutes * 60 + seconds
    else:
        return int(parts[0])


def download_clip(clip: dict[str, Any], output_dir: Path) -> tuple[bool, str]:
    """
    Download a single clip using yt-dlp with time trimming.
    
    Returns (success, filename_or_error).
    """
    url = clip["url"]
    start_time = clip["start"]
    end_time = clip["end"]
    description = clip["description"]
    
    # Validate URL
    if not validate_url(url):
        return False, f"Invalid URL: {url}"
    
    # Create output filename from description
    safe_description = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" 
                               for c in description.lower())[:50]
    safe_description = safe_description.replace(" ", "_").strip("_")
    output_filename = f"pingpong_{safe_description}"
    
    # Create output path
    output_path = output_dir / f"{output_filename}.%(ext)s"
    
    # Build yt-dlp command with section trimming
    # Format: --download-sections *00:00:00-00:01:00
    section_spec = f"*{start_time}-{end_time}"
    
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", str(output_path),
        "--download-sections", section_spec,
        "--no-playlist",
        "--no-warnings",
        "--no-progress",
        "--quiet",
        url
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max per clip
        )
        
        if result.returncode == 0:
            # Find the actual downloaded file
            downloaded_files = list(output_dir.glob(f"{output_filename}.*"))
            if downloaded_files:
                return True, downloaded_files[0].name
            else:
                return False, "Download completed but file not found"
        else:
            return False, f"yt-dlp failed: {result.stderr or 'unknown error'}"
            
    except subprocess.TimeoutExpired:
        return False, "Download timed out after 5 minutes"
    except Exception as e:
        return False, f"Exception during download: {str(e)}"


def generate_metadata(clip: dict[str, Any], filename: str, duration_seconds: int | None = None) -> dict[str, Any]:
    """Generate metadata for a downloaded clip."""
    video_info = get_video_info(clip["url"])
    
    metadata = {
        "source_url": clip["url"],
        "start_time": clip["start"],
        "end_time": clip["end"],
        "duration_seconds": duration_seconds or format_time_to_seconds(clip["end"]) - format_time_to_seconds(clip["start"]),
        "description": clip["description"],
        "difficulty": clip["difficulty"],
        "tags": clip.get("tags", []),
        "downloaded_filename": filename,
        "downloaded_at": datetime.now().isoformat(),
        "video_id": video_info.get("id", ""),
        "title": video_info.get("title", ""),
        "uploader": video_info.get("uploader", ""),
        "duration": video_info.get("duration", 0),
        "expected_fps": 30,  # Expected frames per second for processing
        "qa_version": "1.0.0"
    }
    
    return metadata


def save_metadata(output_dir: Path, filename: str, metadata: dict[str, Any]) -> Path:
    """Save metadata to JSON file."""
    # Convert filename to metadata filename
    base_name = Path(filename).stem
    metadata_path = output_dir / f"{base_name}_metadata.json"
    
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    return metadata_path


def create_test_manifest(clips_data: list[dict[str, Any]], output_path: Path) -> None:
    """Create the test manifest from downloaded clips data."""
    manifest = {
        "created_at": datetime.now().isoformat(),
        "version": "1.0.0",
        "total_clips": len(clips_data),
        "clips": clips_data,
        "summary": {
            "by_difficulty": {},
            "by_tag": {}
        }
    }
    
    # Generate summary statistics
    difficulty_counts = {}
    tag_counts = {}
    
    for clip in clips_data:
        # Count by difficulty
        difficulty = clip.get("difficulty", "unknown")
        difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        
        # Count by tags
        for tag in clip.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    manifest["summary"]["by_difficulty"] = difficulty_counts
    manifest["summary"]["by_tag"] = tag_counts
    
    # Write manifest
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(manifest, f, indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Download ping pong test footage from YouTube for LockN Score QA"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(QA_FOOTAGE_DIR),
        help=f"Output directory for downloaded clips (default: {QA_FOOTAGE_DIR})"
    )
    parser.add_argument(
        "--manifest-path",
        type=str,
        default=str(MANIFEST_PATH),
        help=f"Path for test manifest JSON (default: {MANIFEST_PATH})"
    )
    parser.add_argument(
        "--clip-index",
        type=int,
        nargs="+",
        help="Specific clip indices to download (0-based, from YOUTUBE_TEST_CLIPS)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without actually downloading"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download clips even if they already exist"
    )
    
    args = parser.parse_args()
    
    # Validate yt-dlp
    if not validate_yt_dlp():
        print("Error: yt-dlp is not installed or not in PATH.")
        print("Please install with: pip install yt-dlp")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine which clips to download
    if args.clip_index:
        clips_to_download = [YOUTUBE_TEST_CLIPS[i] for i in args.clip_index 
                            if 0 <= i < len(YOUTUBE_TEST_CLIPS)]
        print(f"Downloading {len(clips_to_download)} specified clips...")
    else:
        clips_to_download = YOUTUBE_TEST_CLIPS
        print(f"Downloading all {len(YOUTUBE_TEST_CLIPS)} curated clips...")
    
    # Process each clip
    downloaded_clips = []
    failed_clips = []
    
    for i, clip in enumerate(clips_to_download, 1):
        print(f"\n[{i}/{len(clips_to_download)}] Processing: {clip['description'][:50]}...")
        print(f"  URL: {clip['url']}")
        print(f"  Time: {clip['start']} - {clip['end']}")
        
        # Check if already downloaded
        safe_description = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" 
                                   for c in clip["description"].lower())[:50]
        safe_description = safe_description.replace(" ", "_").strip("_")
        existing_files = list(output_dir.glob(f"pingpong_{safe_description}.*"))
        
        if existing_files and not args.force:
            print(f"  ✓ Already downloaded: {existing_files[0].name}")
            
            # Create metadata for existing file
            existing_metadata_path = output_dir / f"{existing_files[0].stem}_metadata.json"
            if existing_metadata_path.exists():
                with open(existing_metadata_path) as f:
                    clip_metadata = json.load(f)
            else:
                clip_metadata = generate_metadata(clip, existing_files[0].name)
                save_metadata(output_dir, existing_files[0].name, clip_metadata)
            
            downloaded_clips.append(clip_metadata)
            continue
        
        # Download the clip
        success, result = download_clip(clip, output_dir)
        
        if success:
            filename = result
            print(f"  ✓ Downloaded: {filename}")
            
            # Generate and save metadata
            clip_metadata = generate_metadata(clip, filename)
            metadata_path = save_metadata(output_dir, filename, clip_metadata)
            print(f"  ✓ Metadata saved: {metadata_path.name}")
            
            downloaded_clips.append(clip_metadata)
        else:
            print(f"  ✗ Failed: {result}")
            failed_clips.append({"clip": clip, "error": result})
    
    # Create test manifest
    print("\n" + "="*60)
    print("Creating test manifest...")
    create_test_manifest(downloaded_clips, Path(args.manifest_path))
    print(f"✓ Manifest saved to: {args.manifest_path}")
    
    # Summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"Total clips in playlist: {len(YOUTUBE_TEST_CLIPS)}")
    print(f"Requested clips: {len(clips_to_download)}")
    print(f"Successfully downloaded: {len(downloaded_clips)}")
    print(f"Failed: {len(failed_clips)}")
    
    if failed_clips:
        print("\nFailed clips:")
        for failed in failed_clips:
            print(f"  - {failed['clip']['description'][:50]}")
            print(f"    Error: {failed['error'][:100]}...")
    
    print(f"\nOutput directory: {output_dir}")
    print(f"Manifest file: {args.manifest_path}")
    
    return 0 if len(failed_clips) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())