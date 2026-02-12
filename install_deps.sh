#!/bin/bash
# LockN Score QA - Requirements Installation Script
# Install all required dependencies for qa_metrics.py

python3 -m pip install --user -r requirements.txt

# Validate installation
python3 -c "import numpy; import scipy; import matplotlib; print('All dependencies installed successfully!')"