# LockN Score QA - Ping Pong Test Footage

This directory contains test footage and tools for validating the LockN Score ping pong video analysis pipeline.

## Directory Structure

```
tests/qa/
├── footage/          # Downloaded test clips
├── results/          # Pipeline execution results
├── test_manifest.json    # Manifest of all test clips
└── qa_results.json       # Main results from last harness run
```

## Test Footage

The test footage is curated to cover diverse scenarios:

### Categories

- **Professional Matches** - High-quality broadcast footage with skilled players
- **Amateur Play** - Recreational footage with varying skill levels
- **Camera Angles** - Overhead, side-view, and low-angle perspectives
- **Lighting Conditions** - Bright indoor, low-light, and mixed lighting
- **Ball Colors** - White, orange, and red balls for visibility testing

### Difficulty Levels

- **Low** - Well-lit, standard conditions, easy tracking
- **Medium** - Moderate challenges, some occlusion or movement
- **High** - Challenging conditions, fast action, or complex backgrounds

## Usage

### Downloading Test Footage

```bash
# Install requirements
pip install -r requirements.txt

# Download all curated clips
python qa_download.py

# Download specific clips
python qa_download.py --clip-index 0 1 2 3 4

# Dry run to see what would be downloaded
python qa_download.py --dry-run
```

### Running QA Tests

```bash
# Sequential processing
python qa_harness.py

# Parallel processing with 4 workers
python qa_harness.py --parallel --workers 4

# Custom output location
python qa_harness.py --output custom_results.json

# Summary only
python qa_harness.py --summary
```

## Test Manifest

The `test_manifest.json` contains metadata for all test clips:

```json
{
  "created_at": "ISO timestamp",
  "version": "1.0.0",
  "total_clips": 15,
  "clips": [
    {
      "source_url": "https://youtube.com/watch?v=...",
      "start_time": "0:00",
      "end_time": "0:45",
      "duration_seconds": 45,
      "description": "Professional match description",
      "difficulty": "high",
      "tags": ["professional", "broadcast", "good-lighting"],
      "downloaded_filename": "pingpong_...",
      "downloaded_at": "ISO timestamp"
    }
  ],
  "summary": {
    "by_difficulty": {"high": 5, "medium": 6, "low": 4},
    "by_tag": {"professional": 5, "amateur": 4, ...}
  }
}
```

## Pipeline Services

The QA harness interfaces with LockN Score services:

1. **Preprocessing** - Video enhancement and normalization
2. **Detection** - Ball and player detection
3. **Tracking** - Object tracking and path prediction
4. **Analysis** - Game analysis and metrics

## Environment Variables

Configure service endpoints:

- `LOCKN_PREPROCESSING_URL` - Preprocessing service (default: `http://localhost:8001`)
- `LOCKN_DETECTION_URL` - Detection service (default: `http://localhost:8002`)
- `LOCKN_TRACKING_URL` - Tracking service (default: `http://localhost:8003`)
- `LOCKN_ANALYSIS_URL` - Analysis service (default: `http://localhost:8004`)

## Results Format

Results include per-clip pipeline execution data:

```json
{
  "clip_metadata": {...},
  "pipeline_results": {
    "video_path": "...",
    "services": {
      "preprocessing": {"success": true, ...},
      "detection": {"success": true, ...},
      "tracking": {"success": true, ...},
      "analysis": {"success": true, ...}
    },
    "pipeline_status": "completed|partial|failed",
    "duration_seconds": 123.45
  }
}
```

## Adding New Test Clips

To add new test clips:

1. Edit `qa_download.py` and add to `YOUTUBE_TEST_CLIPS` list
2. Include diverse scenarios covering all test categories
3. Run `python qa_download.py --clip-index N` to download the new clip
4. The manifest will automatically update

## Requirements

- Python 3.11+
- yt-dlp
- requests

Install with:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### yt-dlp not found
```bash
pip install yt-dlp
```

### Service connection errors
Ensure LockN Score services are running and accessible at the configured endpoints.

### Download failures
Some videos may be unavailable or region-restricted. Check the URL and try again later.