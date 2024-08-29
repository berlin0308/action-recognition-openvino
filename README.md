# Action Recognition with OpenVINO

This repository contains code and resources for building an action recognition system using TensorFlow, MoviNet, and OpenVINO.

## Project Structure
- **`1-data-preparation/:`** Scripts for recording and annotating video data.
  - Python 3.x
- `2-action-recognition-training/`: Training scripts for action recognition models using Docker.
  - **Environment Requirements**: 
    - Docker (with DevContainer setup)
    - GPU-enabled device for training
- `3-model-conversion-openvino/`: Scripts for converting models to OpenVINO format.
  - **Environment Requirements**: Python 3.x
- `4-edge-inference/`: C++ code for running models on edge devices.
  - **Environment Requirements**: 
    - Edge device with C++ compiler
    - OpenVINO runtime
- `5-view-app/`: A simple C# application for displaying results.
  - **Environment Requirements**: .NET runtime

## Getting Started

### Prerequisites
To work with this repository, you will need the following environments configured:

1. **Python 3.x**: Required for scripts in `1-data-preparation` and `3-model-conversion-openvino`.
   - Install required Python packages using `pip install -r requirements.txt` in each folder.
2. **Docker**: Used for training environment setup in `2-action-recognition-training`.
   - A GPU-enabled device is required for efficient model training.
3. **C++ Compiler and OpenVINO Runtime**: Required for running inference on edge devices in `4-edge-inference`.
   - Ensure OpenVINO is installed
