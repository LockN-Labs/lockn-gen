# LockN Score QA - Test Footage Downloader and Harness

## Overview

This solution provides a complete system for downloading and testing ping pong footage for LockN Score QA, as specified in LOC-381.

## Files Created

1. **qa_download.py** - Downloads curated ping pong clips from YouTube
2. **qa_harness.py** - Runs clips through the LockN Score pipeline
3. **requirements.txt** - Python dependencies
4. **tests/qa/README.md** - Comprehensive documentation
5. **tests/qa/.gitignore** - Git ignore rules for generated files

## Key Features

### qa_download.py
- Downloads 15+ curated YouTube clips with diverse scenarios
- Supports multiple categories: professional/amateur, camera angles, lighting conditions, ball colors
- Trims clips to 30-60 second segments using yt-dlp's `--download-sections`
- Saves metadata JSON per clip (source URL, duration, description, difficulty)
- Creates comprehensive `test_manifest.json` with statistics
- Supports parallel execution, dry-run mode, and selective clip downloads

### qa_harness.py
- Reads `test_manifest.json` to process clips
- Runs clips through all LockN Score pipeline services:
  - Preprocessing (video enhancement)
  - Detection (ball and player detection)
  - Tracking (object tracking)
  - Analysis (game metrics)
- Supports `--parallel` flag for concurrent execution with configurable workers
- Collects structured results with per-clip and summary statistics
- Generates individual result files and comprehensive summary

### Directory Structure
```
tests/qa/
├── footage/          # Downloaded test clips (generated)
├── results/          # Pipeline execution results (generated)
├── README.md         # Usage documentation
├── .gitignore        # Git ignore rules
├── test_manifest.json    # Clip metadata (generated)
└── qa_results.json       # Main results (generated)
```

## Usage Examples

### Download Test Footage
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

### Run QA Tests
```bash
# Sequential processing
python qa_harness.py

# Parallel processing with 4 workers
python qa_harness.py --parallel --workers 4

# Custom output location
python qa_harness.py --output results/custom.json
```

## Test Coverage

### Categories
1. **Professional Matches** - High-quality broadcast footage
2. **Amateur Play** - Recreational footage with varying skill levels
3. **Camera Angles** - Overhead, side-view, and low-angle perspectives
4. **Lighting Conditions** - Bright indoor, low-light, and mixed lighting
5. **Ball Colors** - White, orange, and red balls

### Difficulty Levels
- **Low**: Well-lit, standard conditions, easy tracking
- **Medium**: Moderate challenges, some occlusion or movement
- **High**: Challenging conditions, fast action, or complex backgrounds

## Requirements

- Python 3.11+
- yt-dlp (video downloading)
- requests (HTTP client for pipeline services)

Install with:
```bash
pip install -r requirements.txt
```

## Environment Variables

Configure LockN Score service endpoints:
- `LOCKN_PREPROCESSING_URL` - Preprocessing service (default: `http://localhost:8001`)
- `LOCKN_DETECTION_URL` - Detection service (default: `http://localhost:8002`)
- `LOCKN_TRACKING_URL` - Tracking service (default: `http://localhost:8003`)
- `LOCKN_ANALYSIS_URL` - Analysis service (default: `http://localhost:8004`)

## Output Format

### Test Manifest
```json
{
  "created_at": "ISO timestamp",
  "version": "1.0.0",
  "total_clips": 15,
  "clips": [...],
  "summary": {
    "by_difficulty": {"high": 5, "medium": 6, "low": 4},
    "by_tag": {"professional": 5, "amateur": 4, ...}
  }
}
```

### Results
```json
{
  "started_at": "ISO timestamp",
  "total_clips": 15,
  "individual_results": [...],
  "summary": {
    "completed": 12,
    "partial": 2,
    "failed": 1,
    "total": 15,
    "success_rate": 80.0,
    "average_duration": 45.5
  }
}
```

## Validation

Both Python files have been validated for correct syntax:
- `qa_download.py`: Syntax verified with `python3 -m py_compile`
- `qa_harness.py`: Syntax verified with `python3 -m py_compile`

## Next Steps

1. Run `pip install -r requirements.txt` to install dependencies
2. Run `python qa_download.py` to download test footage
3. Ensure LockN Score services are running on configured endpoints
4. Run `python qa_harness.py` to execute the test pipeline
5. Review results in `tests/qa/results/qa_results.json`