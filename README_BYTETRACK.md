# YOLOv8 + BYTETrack People Detection System

A comprehensive people detection and tracking system using YOLOv8 with BYTETrack integration for robust multi-object tracking with zone management.

## 🚀 Features

-   **YOLOv8 Detection**: State-of-the-art person detection
-   **BYTETrack Integration**: Robust multi-object tracking that handles occlusions
-   **Unique ID Tracking**: Maintains consistent IDs across frames
-   **Interactive Zone Drawing**: Create polygonal zones on-screen with mouse
-   **Zone Statistics**:
    -   Current count of people in each zone
    -   Total unique visitors per zone
-   **Visual Tracking Trails**: See movement history for each person
-   **Real-time Performance**: Optimized for live video processing
-   **Persistent Configuration**: Save and load zone configurations

## 📋 Requirements

```bash
pip install -r requirements.txt
```

**Dependencies:**

-   ultralytics >= 8.0.0 (includes YOLOv8 + BYTETrack)
-   opencv-python >= 4.8.0
-   numpy >= 1.24.0

## 🎯 Quick Start

### Basic Detection

```bash
python people_detector_bytetrack.py
```

Uses `Camera-Video.mp4` by default

### With Webcam

```bash
python people_detector_bytetrack.py --source 0
```

### Process Video File

```bash
python people_detector_bytetrack.py --source video.mp4 --output result.mp4
```

## 🎨 Interactive Zone Creation

### Method 1: In Detection Program (Recommended)

```bash
python people_detector_bytetrack.py
```

**Controls:**

-   Press **'d'** to toggle drawing mode
-   **Left Click**: Add point to polygon
-   **Right Click**: Complete the zone (min 3 points)
-   **Middle Click**: Remove last point
-   **'c'**: Clear current zone
-   **'s'**: Save zones to JSON
-   **'z'**: Print zone statistics
-   **'q'**: Quit

### Method 2: Standalone Zone Editor

```bash
python zone_manager.py
```

## 📊 Zone Statistics

Each zone displays:

-   **Current Count**: People currently in the zone
-   **Total Visitors**: Unique individuals who entered (tracked by ID)

Press **'z'** during detection to see detailed statistics:

```
=== Zone Statistics ===
Entry Zone:
  Current Count: 2
  Total Visitors: 15
  Visitor IDs: [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
Exit Zone:
  Current Count: 1
  Total Visitors: 8
  Visitor IDs: [5, 7, 13, 19, 21, 25, 27, 29]
=====================
```

## 🎮 All Controls

| Key   | Action                           |
| ----- | -------------------------------- |
| **d** | Toggle zone drawing mode         |
| **s** | Save zones to file               |
| **c** | Clear current zone being drawn   |
| **z** | Print zone statistics to console |
| **q** | Quit application                 |

**Mouse (in drawing mode):**
| Action | Function |
|--------|----------|
| **Left Click** | Add point to zone polygon |
| **Right Click** | Finish and save zone |
| **Middle Click** | Remove last point |

## 📁 Configuration

### zones.json Structure

```json
{
    "zones": [
        {
            "name": "Entry Zone",
            "points": [
                [100, 100],
                [300, 100],
                [300, 300],
                [100, 300]
            ],
            "color": [0, 255, 0],
            "enabled": true
        }
    ]
}
```

## 🔧 Command Line Options

```bash
python people_detector_bytetrack.py [OPTIONS]

Options:
  --source PATH          Video source (0 for webcam, or video file path)
                         Default: Camera-Video.mp4

  --model PATH           YOLOv8 model path
                         Options: yolov8n.pt (fastest), yolov8s.pt, yolov8m.pt,
                                 yolov8l.pt, yolov8x.pt (most accurate)
                         Default: yolov8n.pt

  --zones PATH           Zones configuration file
                         Default: zones.json

  --output PATH          Save output video to path
                         Default: None (display only)

  --no-display          Run without display (headless mode)
```

## 🏃 Examples

### Example 1: Create Zones and Track People

```bash
python people_detector_bytetrack.py --source Camera-Video.mp4
# Press 'd', click to draw zones, press 's' to save
```

### Example 2: Process and Save Video

```bash
python people_detector_bytetrack.py --source input.mp4 --output tracked.mp4
```

### Example 3: High Accuracy Mode

```bash
python people_detector_bytetrack.py --model yolov8x.pt --source video.mp4
```

### Example 4: Monitor Specific Zones

```bash
python people_detector_bytetrack.py --zones custom_zones.json
```

## 🧠 How BYTETrack Works

**BYTETrack** (Built into YOLOv8) provides:

-   **Association Strategy**: Matches detections across frames using Kalman filter + IoU
-   **Two-Step Matching**:
    1. High-confidence detections matched first
    2. Low-confidence detections matched to remaining tracks
-   **Handles Occlusions**: Maintains IDs even when objects temporarily disappear
-   **No Re-ID Model**: Fast and efficient without deep feature extraction

**Key Advantages:**

-   ⚡ Fast (real-time performance)
-   🎯 Robust to occlusions
-   🔄 Maintains consistent IDs
-   📦 Built-in (no extra dependencies)

## 📈 Performance

| Model   | Speed (FPS) | Accuracy  | Use Case          |
| ------- | ----------- | --------- | ----------------- |
| YOLOv8n | ~60         | Good      | Real-time, webcam |
| YOLOv8s | ~45         | Better    | Balanced          |
| YOLOv8m | ~30         | Great     | High quality      |
| YOLOv8l | ~20         | Excellent | Surveillance      |
| YOLOv8x | ~15         | Best      | Maximum accuracy  |

## 🐛 Troubleshooting

**Video not opening:**

```bash
# Check video path
python people_detector_bytetrack.py --source "C:/path/to/video.mp4"
```

**Slow performance:**

-   Use YOLOv8n: `--model yolov8n.pt`
-   Install GPU support: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118`

**Tracking issues:**

-   IDs jumping: Lower confidence threshold or use larger model
-   Lost tracks: Check occlusions, adjust BYTETrack parameters

## 📦 Project Structure

```
Code/
├── people_detector_bytetrack.py  # Main detection with BYTETrack
├── zone_manager.py               # Standalone zone editor
├── zones.json                    # Zone configuration
├── requirements.txt              # Python dependencies
├── README.md                     # Main documentation
└── README_BYTETRACK.md          # This file
```

## 🔜 Coming Soon

-   Multi-camera support
-   Heat map generation
-   Analytics dashboard

## 📝 License

This project uses:

-   YOLOv8 from Ultralytics (AGPL-3.0)
-   BYTETrack (MIT License)
-   OpenCV (Apache 2.0)

## 👤 Author

Part of CrowdCount-Infosys-SpringBoard project

## 🤝 Contributing

Issues and pull requests welcome at: https://github.com/nvmaditya/CroudCount-Infosys-SpringBoard
