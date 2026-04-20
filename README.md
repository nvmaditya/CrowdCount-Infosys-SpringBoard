# YOLOv8 People Detection with Zone Management

A comprehensive people detection system using YOLOv8 that tracks individuals with unique IDs and supports configurable polygonal zones for area monitoring.

## Features

-   **Real-time People Detection**: Uses YOLOv8 for accurate person detection
-   **Unique ID Tracking**: Assigns and maintains unique IDs for each detected person across frames
-   **Bounding Box Visualization**: Clear visual representation with color-coded boxes
-   **Tracking Trails**: Shows movement history for each person
-   **Polygonal Zones**: Define custom detection zones with any polygon shape
-   **On-Screen Zone Drawing**: Create zones directly on the video feed with mouse clicks
-   **Zone Statistics**: Track current count and total unique visitors per zone
-   **Zone Monitoring**: Tracks which zone(s) each person is in
-   **Interactive Zone Editor**: Visual tool to create and edit zones
-   **Persistent Configuration**: Zones saved in JSON format for reuse
-   **Video Output**: Save processed video with detections and zones

## Installation

### 1. Clone or download this repository

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Download YOLOv8 model (optional - will auto-download on first run)

The system uses YOLOv8n (nano) by default. Other models available:

-   `yolov8n.pt` - Nano (fastest, recommended for real-time)
-   `yolov8s.pt` - Small
-   `yolov8m.pt` - Medium
-   `yolov8l.pt` - Large
-   `yolov8x.pt` - Extra Large (most accurate)

## Usage

### People Detection

#### Basic usage with webcam:

```bash
python people_detector.py
```

#### Process a video file:

```bash
python people_detector.py --source video.mp4
```

#### Save output video:

```bash
python people_detector.py --source video.mp4 --output output.mp4
```

#### Use different YOLOv8 model:

```bash
python people_detector.py --model yolov8s.pt
```

#### Custom zones file:

```bash
python people_detector.py --zones custom_zones.json
```

#### Run without display (headless):

```bash
python people_detector.py --source video.mp4 --output output.mp4 --no-display
```

### Zone Management

#### Interactive zone editor (standalone tool):

```bash
python zone_manager.py
```

#### Use video file for zone creation:

```bash
python zone_manager.py --source video.mp4
```

#### List existing zones:

```bash
python zone_manager.py --mode list
```

#### Draw zones directly in the main detector:

```bash
python people_detector.py
# Press 'd' to enable drawing mode, then click to create polygon zones
```

## Controls

### Main Detector Controls

When running `people_detector.py`:

-   **'d' key**: Toggle drawing mode (create zones on-screen)
-   **Left Click** (in drawing mode): Add point to current zone
-   **Right Click** (in drawing mode): Finish current zone (minimum 3 points)
-   **Middle Click** (in drawing mode): Remove last point
-   **'c' key**: Clear current zone being drawn
-   **'s' key**: Save zones to file
-   **'z' key**: Print zone statistics to console
-   **'q' key**: Quit

### Zone Editor Controls

When running `zone_manager.py`:

-   **Left Click**: Add point to current zone
-   **Right Click**: Finish current zone (minimum 3 points)
-   **Middle Click**: Remove last point
-   **'s' key**: Save zones to file
-   **'c' key**: Clear current zone being drawn
-   **'d' key**: Delete a zone (prompts for index)
-   **'t' key**: Toggle zone on/off (prompts for index)
-   **'l' key**: List all zones
-   **'q' key**: Quit

## Configuration

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

### Zone Properties:

-   **name**: Descriptive name for the zone
-   **points**: Array of [x, y] coordinates defining the polygon
-   **color**: RGB color values [R, G, B] (0-255)
-   **enabled**: Boolean to activate/deactivate zone

## How It Works

### People Detection

1. YOLOv8 processes each frame and detects people (class 0)
2. Built-in tracking assigns unique IDs that persist across frames
3. Each person gets:
    - Unique color-coded bounding box
    - ID number displayed on box
    - Confidence score
    - Center point marker
    - Movement trail (last 30 positions)
    - Zone information (if in any zone)

### Zone Management

1. Zones are defined as polygons with any number of vertices
2. System checks if person's center point is inside zone polygons
3. Multiple zones can overlap - persons can be in multiple zones
4. Zones are drawn as semi-transparent overlays
5. Zone configuration persists in JSON file
6. **Zone Statistics**: Each zone displays:
    - **Current Count**: Number of people currently in the zone
    - **Total Visitors**: Total unique individuals who have entered the zone (tracked by ID)

## Examples

### Example 1: Create Zones While Detecting

```bash
# Run detector and press 'd' to enable drawing mode
python people_detector.py
# Click on screen to draw polygon zones
# Right-click to complete each zone
# Press 's' to save zones
```

### Example 2: Monitor Entry/Exit Points with Statistics

```bash
# Create zones for doorways using zone manager
python zone_manager.py --source Camera-Video.mp4

# Run detection and press 'z' to see statistics
python people_detector.py
```

### Example 3: Process Surveillance Video

```bash
# Process video with existing zones
python people_detector.py --source surveillance.mp4 --output monitored.mp4
```

### Example 4: Restrict Area Monitoring

```bash
# Edit zones.json to define restricted areas
# Run detection to see who enters restricted zones
python people_detector.py --zones restricted_zones.json
```

## Output Information

The detector prints detailed information every 30 frames:

```
Frame 42: 3 people detected
  - ID 1: conf=0.89 in ['Entry Zone']
  - ID 2: conf=0.94
  - ID 5: conf=0.87 in ['Exit Zone', 'Restricted Area']
```

Press 'z' to see detailed zone statistics:

```
=== Zone Statistics ===
Entry Zone:
  Current Count: 2
  Total Visitors: 5
  Visitor IDs: [1, 3, 5, 7, 9]
Exit Zone:
  Current Count: 1
  Total Visitors: 3
  Visitor IDs: [5, 7, 9]
=====================
```

## Performance Tips

1. **Use YOLOv8n** for real-time performance
2. **GPU acceleration**: Install PyTorch with CUDA support
3. **Lower resolution**: Resize input frames if needed
4. **Reduce trail length**: Modify `track_history` max length in code
5. **Disable zones**: Set `"enabled": false` for unused zones

## Troubleshooting

### Camera not detected:

-   Try different camera indices: `--source 1`, `--source 2`, etc.
-   Check camera permissions

### Slow performance:

-   Use smaller YOLOv8 model (yolov8n.pt)
-   Reduce video resolution
-   Ensure GPU drivers are installed

### No detections:

-   Check lighting conditions
-   Verify camera is working
-   Try different YOLOv8 model
-   Ensure people are clearly visible

## Requirements

-   Python 3.8+
-   OpenCV
-   Ultralytics YOLOv8
-   NumPy
-   (Optional) CUDA-capable GPU for faster processing

## File Structure

```
.
├── people_detector.py    # Main detection script
├── zone_manager.py       # Zone creation and editing tool
├── zones.json           # Zone configuration file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## License

This project uses YOLOv8 from Ultralytics (AGPL-3.0 license).

## Credits

-   YOLOv8 by Ultralytics
-   OpenCV for computer vision operations
