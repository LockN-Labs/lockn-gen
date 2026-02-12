#!/usr/bin/env python3
"""
qa_harness.py - Test harness for LockN Score QA pipeline

Reads test_manifest.json and runs each ping pong clip through the
LockN Score pipeline, collecting results into structured output.

Supports parallel execution for improved performance.
"""

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any
import requests


# Base directory structure
BASE_DIR = Path(__file__).parent
MANIFEST_PATH = BASE_DIR / "tests" / "qa" / "test_manifest.json"
RESULTS_DIR = BASE_DIR / "tests" / "qa" / "results"
DEFAULT_OUTPUT_PATH = RESULTS_DIR / "qa_results.json"


class LockNScorePipeline:
    """Interface to LockN Score pipeline services."""
    
    def __init__(self):
        # Configuration for LockN Score services
        self.services = {
            "preprocessing": {
                "endpoint": os.environ.get("LOCKN_PREPROCESSING_URL", "http://localhost:8001/process"),
                "description": "Video preprocessing and enhancement"
            },
            "detection": {
                "endpoint": os.environ.get("LOCKN_DETECTION_URL", "http://localhost:8002/detect"),
                "description": "Ball and player detection"
            },
            "tracking": {
                "endpoint": os.environ.get("LOCKN_TRACKING_URL", "http://localhost:8003/track"),
                "description": "Object tracking and path prediction"
            },
            "analysis": {
                "endpoint": os.environ.get("LOCKN_ANALYSIS_URL", "http://localhost:8004/analyze"),
                "description": "Game analysis and metrics"
            }
        }
        
        # Check if services are available
        self.services_available = self._check_services()
    
    def _check_service(self, name: str, endpoint: str) -> bool:
        """Check if a service is available."""
        try:
            response = requests.get(f"{endpoint}/health", timeout=5)
            return response.status_code == 200
        except (requests.RequestException, requests.Timeout):
            return False
    
    def _check_services(self) -> dict[str, bool]:
        """Check availability of all services."""
        availability = {}
        for name, config in self.services.items():
            availability[name] = self._check_service(name, config["endpoint"])
            if not availability[name]:
                print(f"⚠️  Service {name} ({config['description']}) not available at {config['endpoint']}")
        return availability
    
    def run_preprocessing(self, video_path: str) -> dict[str, Any]:
        """Run video preprocessing."""
        endpoint = self.services["preprocessing"]["endpoint"]
        try:
            # Upload video file
            with open(video_path, "rb") as f:
                files = {"video": f}
                response = requests.post(
                    f"{endpoint}/preprocess",
                    files=files,
                    timeout=60
                )
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "response": response.json() if response.status_code == 200 else response.text,
                    "service": "preprocessing"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "preprocessing"
            }
    
    def run_detection(self, video_path: str) -> dict[str, Any]:
        """Run ball and player detection."""
        endpoint = self.services["detection"]["endpoint"]
        try:
            with open(video_path, "rb") as f:
                files = {"video": f}
                response = requests.post(
                    f"{endpoint}/detect",
                    files=files,
                    timeout=60
                )
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "response": response.json() if response.status_code == 200 else response.text,
                    "service": "detection"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "detection"
            }
    
    def run_tracking(self, video_path: str) -> dict[str, Any]:
        """Run object tracking."""
        endpoint = self.services["tracking"]["endpoint"]
        try:
            with open(video_path, "rb") as f:
                files = {"video": f}
                response = requests.post(
                    f"{endpoint}/track",
                    files=files,
                    timeout=60
                )
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "response": response.json() if response.status_code == 200 else response.text,
                    "service": "tracking"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "tracking"
            }
    
    def run_analysis(self, video_path: str) -> dict[str, Any]:
        """Run game analysis."""
        endpoint = self.services["analysis"]["endpoint"]
        try:
            with open(video_path, "rb") as f:
                files = {"video": f}
                response = requests.post(
                    f"{endpoint}/analyze",
                    files=files,
                    timeout=60
                )
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "response": response.json() if response.status_code == 200 else response.text,
                    "service": "analysis"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "analysis"
            }
    
    def run_full_pipeline(self, video_path: str) -> dict[str, Any]:
        """Run the complete pipeline on a video."""
        results = {
            "video_path": video_path,
            "started_at": datetime.now().isoformat(),
            "services": {},
            "pipeline_status": "running"
        }
        
        # Run each service in sequence
        pipeline_steps = [
            ("preprocessing", self.run_preprocessing),
            ("detection", self.run_detection),
            ("tracking", self.run_tracking),
            ("analysis", self.run_analysis)
        ]
        
        failed_steps = []
        for step_name, step_func in pipeline_steps:
            if self.services_available.get(step_name, False):
                step_result = step_func(video_path)
                results["services"][step_name] = step_result
                
                if not step_result.get("success", False):
                    failed_steps.append(step_name)
            else:
                results["services"][step_name] = {
                    "skipped": True,
                    "reason": "Service not available",
                    "service": step_name
                }
        
        # Determine overall pipeline status
        if not failed_steps and results["services"]:
            results["pipeline_status"] = "completed"
        elif failed_steps and len(failed_steps) < len(pipeline_steps):
            results["pipeline_status"] = "partial"
        else:
            results["pipeline_status"] = "failed"
        
        results["completed_at"] = datetime.now().isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) - 
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        return results


class QAHarness:
    """Main QA harness class."""
    
    def __init__(self, manifest_path: str, output_dir: str, parallel: bool = False, max_workers: int = 4):
        self.manifest_path = Path(manifest_path)
        self.output_dir = Path(output_dir)
        self.parallel = parallel
        self.max_workers = max_workers
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.individual_results_dir = self.output_dir / "individual"
        self.individual_results_dir.mkdir(exist_ok=True)
        
        # Load manifest
        self.manifest = self._load_manifest()
        
        # Initialize pipeline
        self.pipeline = LockNScorePipeline()
    
    def _load_manifest(self) -> dict[str, Any]:
        """Load the test manifest."""
        try:
            with open(self.manifest_path) as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Manifest not found at {self.manifest_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in manifest: {e}")
            sys.exit(1)
    
    def get_footage_path(self, clip: dict[str, Any]) -> Path | None:
        """Get the local path for a clip's footage."""
        # Extract base directory from manifest or use default
        base_dir = BASE_DIR
        footage_dir = base_dir / "tests" / "qa" / "footage"
        
        filename = clip.get("downloaded_filename", "")
        if filename:
            footage_path = footage_dir / filename
            if footage_path.exists():
                return footage_path
        
        # Fallback: try to find by description
        description = clip.get("description", "")
        safe_description = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" 
                                   for c in description.lower())[:50]
        safe_description = safe_description.replace(" ", "_").strip("_")
        
        existing_files = list(footage_dir.glob(f"pingpong_{safe_description}.*"))
        if existing_files:
            return existing_files[0]
        
        return None
    
    def process_single_clip(self, clip: dict[str, Any], index: int) -> dict[str, Any]:
        """Process a single clip through the pipeline."""
        print(f"[{index}/{len(self.manifest.get('clips', []))}] Processing: {clip.get('description', 'Unknown')[:50]}")
        
        # Get footage path
        footage_path = self.get_footage_path(clip)
        
        if not footage_path or not footage_path.exists():
            return {
                "clip": clip,
                "status": "skipped",
                "reason": "Footage file not found",
                "footage_path": str(footage_path) if footage_path else "None",
                "completed_at": datetime.now().isoformat()
            }
        
        # Run pipeline
        print(f"  Running pipeline on {footage_path.name}...")
        results = self.pipeline.run_full_pipeline(str(footage_path))
        
        # Save individual results
        clip_id = clip.get("source_url", "").split("=")[-1][:11]  # Extract YouTube ID
        safe_description = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" 
                                   for c in clip.get("description", "").lower())[:30]
        safe_description = safe_description.replace(" ", "_").strip("_")
        
        individual_result_path = (
            self.individual_results_dir / 
            f"result_{clip_id}_{safe_description}.json"
        )
        
        individual_result = {
            "clip_metadata": clip,
            "pipeline_results": results,
            "processed_at": datetime.now().isoformat(),
            "harness_version": "1.0.0"
        }
        
        with open(individual_result_path, "w") as f:
            json.dump(individual_result, f, indent=2)
        
        print(f"  ✓ Results saved to {individual_result_path.name}")
        
        return {
            "clip": clip,
            "status": results["pipeline_status"],
            "duration_seconds": results.get("duration_seconds", 0),
            "services_processed": len([s for s in results.get("services", {}).values() 
                                      if not s.get("skipped", False)]),
            "footage_path": str(footage_path),
            "result_file": str(individual_result_path),
            "completed_at": datetime.now().isoformat()
        }
    
    def process_all_clips(self) -> dict[str, Any]:
        """Process all clips in the manifest."""
        clips = self.manifest.get("clips", [])
        total_clips = len(clips)
        
        print(f"Processing {total_clips} test clips...")
        print(f"Parallel execution: {self.parallel}")
        if self.parallel:
            print(f"Max workers: {self.max_workers}")
        print(f"Services available: {[k for k, v in self.pipeline.services_available.items() if v]}")
        
        results = {
            "started_at": datetime.now().isoformat(),
            "manifest_path": str(self.manifest_path),
            "total_clips": total_clips,
            "individual_results": [],
            "summary": {}
        }
        
        if self.parallel:
            # Parallel processing
            print(f"\nStarting parallel processing with {self.max_workers} workers...")
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_index = {
                    executor.submit(self.process_single_clip, clip, i + 1): i 
                    for i, clip in enumerate(clips)
                }
                
                for future in as_completed(future_to_index):
                    result = future.result()
                    results["individual_results"].append(result)
        else:
            # Sequential processing
            print("\nStarting sequential processing...")
            for i, clip in enumerate(clips):
                result = self.process_single_clip(clip, i + 1)
                results["individual_results"].append(result)
        
        # Calculate summary statistics
        completed = [r for r in results["individual_results"] if r["status"] == "completed"]
        partial = [r for r in results["individual_results"] if r["status"] == "partial"]
        failed = [r for r in results["individual_results"] if r["status"] in ("failed", "skipped")]
        
        results["summary"] = {
            "completed": len(completed),
            "partial": len(partial),
            "failed": len(failed),
            "total": total_clips,
            "success_rate": len(completed) / total_clips * 100 if total_clips > 0 else 0,
            "average_duration": sum(r.get("duration_seconds", 0) for r in results["individual_results"]) / total_clips if total_clips > 0 else 0
        }
        
        results["completed_at"] = datetime.now().isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) - 
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        return results
    
    def save_results(self, results: dict[str, Any], output_path: str | None = None) -> Path:
        """Save results to JSON file."""
        output_file = Path(output_path) if output_path else DEFAULT_OUTPUT_PATH
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        return output_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="LockN Score QA Test Harness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python qa_harness.py                              # Process all clips sequentially
  python qa_harness.py --parallel --workers 4      # Process with 4 parallel workers
  python qa_harness.py --manifest custom_manifest.json
  python qa_harness.py --output results/custom.json
        """
    )
    
    parser.add_argument(
        "--manifest",
        type=str,
        default=str(MANIFEST_PATH),
        help=f"Path to test manifest JSON (default: {MANIFEST_PATH})"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT_PATH),
        help=f"Path for output results JSON (default: {DEFAULT_OUTPUT_PATH})"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(RESULTS_DIR),
        help=f"Directory for individual results (default: {RESULTS_DIR})"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Enable parallel execution of clips"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary only"
    )
    
    args = parser.parse_args()
    
    # Validate manifest path
    if not Path(args.manifest).exists():
        print(f"Error: Manifest file not found: {args.manifest}")
        sys.exit(1)
    
    # Create harness and run
    harness = QAHarness(
        manifest_path=args.manifest,
        output_dir=args.output_dir,
        parallel=args.parallel,
        max_workers=args.workers
    )
    
    # Process all clips
    results = harness.process_all_clips()
    
    # Save results
    output_path = harness.save_results(results, args.output)
    
    # Print summary
    summary = results["summary"]
    print("\n" + "="*60)
    print("QA HARNESS RESULTS")
    print("="*60)
    print(f"Manifest: {args.manifest}")
    print(f"Output: {output_path}")
    print(f"Total clips: {summary['total']}")
    print(f"Completed: {summary['completed']}")
    print(f"Partial: {summary['partial']}")
    print(f"Failed/Skipped: {summary['failed']}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    print(f"Total duration: {results['duration_seconds']:.1f} seconds")
    
    if not args.summary:
        print("\nIndividual Results:")
        for i, result in enumerate(results["individual_results"], 1):
            status_icon = "✓" if result["status"] == "completed" else ("⚠️" if result["status"] == "partial" else "✗")
            print(f"  {status_icon} Clip {i}: {result['clip'].get('description', 'Unknown')[:40]}... [{result['status']}]")
    
    # Exit with appropriate code
    if summary["failed"] > 0 and summary["completed"] == 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()