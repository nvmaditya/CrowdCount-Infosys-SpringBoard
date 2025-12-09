"""
YOLOv8 People Detection with Tracking and Zone Management
Detects people in video, assigns unique IDs, and manages polygonal zones
"""

import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
import json
from pathlib import Path


class PeopleDetector:
    def __init__(self, model_path='yolov8n.pt', zones_file='zones.json'):
        """
        Initialize the people detector with YOLOv8
        
        Args:
            model_path: Path to YOLOv8 model weights
            zones_file: Path to zones configuration JSON file
        """
        self.model = YOLO(model_path)
        self.zones_file = zones_file
        self.zones = self.load_zones()
        
        # Track history for smooth tracking
        self.track_history = defaultdict(lambda: [])
        
        # Zone statistics: track unique IDs that entered each zone
        self.zone_visitors = defaultdict(set)  # {zone_name: set(track_ids)}
        self.zone_current_count = defaultdict(int)  # {zone_name: current_count}
        
        # Interactive zone drawing
        self.drawing_mode = False
        self.current_zone_points = []
        
        # Colors for visualization
        self.colors = self.generate_colors(100)
        
    def generate_colors(self, n):
        """Generate n distinct colors for visualization"""
        colors = []
        for i in range(n):
            hue = int(180 * i / n)
            col = cv2.cvtColor(np.uint8([[[hue, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
            colors.append((int(col[0]), int(col[1]), int(col[2])))
        return colors
    
    def load_zones(self):
        """Load zones from JSON file"""
        zones_path = Path(self.zones_file)
        if zones_path.exists():
            with open(zones_path, 'r') as f:
                return json.load(f)
        return {"zones": []}
    
    def save_zones(self):
        """Save zones to JSON file"""
        with open(self.zones_file, 'w') as f:
            json.dump(self.zones, f, indent=2)
    
    def draw_zones(self, frame):
        """Draw all defined zones on the frame with statistics"""
        overlay = frame.copy()
        
        for zone in self.zones.get('zones', []):
            if not zone.get('enabled', True):
                continue
                
            points = np.array(zone['points'], dtype=np.int32)
            color = tuple(zone.get('color', [0, 255, 0]))
            zone_name = zone.get('name', 'Unnamed')
            
            # Draw filled polygon with transparency
            cv2.fillPoly(overlay, [points], color)
            
            # Draw polygon border
            cv2.polylines(frame, [points], True, color, 2)
            
            # Draw zone statistics
            centroid = points.mean(axis=0).astype(int)
            current = self.zone_current_count.get(zone_name, 0)
            total = len(self.zone_visitors.get(zone_name, set()))
            
            # Zone name
            cv2.putText(frame, zone_name, (centroid[0], centroid[1] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Statistics: Current count / Total unique
            stats_text = f"Current: {current} | Total: {total}"
            cv2.putText(frame, stats_text, (centroid[0], centroid[1] + 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Blend overlay with frame for transparency effect
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame
    
    def point_in_zone(self, point, zone_points):
        """Check if a point is inside a polygon zone"""
        return cv2.pointPolygonTest(np.array(zone_points, dtype=np.int32), point, False) >= 0
    
    def get_person_zone(self, bbox_center):
        """Determine which zone(s) a person is in"""
        zones_detected = []
        for zone in self.zones.get('zones', []):
            if not zone.get('enabled', True):
                continue
            if self.point_in_zone(bbox_center, zone['points']):
                zones_detected.append(zone.get('name', 'Unnamed'))
        return zones_detected
    
    def update_zone_statistics(self, detections):
        """Update zone visitor counts and statistics"""
        # Reset current counts
        self.zone_current_count.clear()
        
        # Count current people in each zone and track unique visitors
        for det in detections:
            track_id = det['id']
            zones = det['zones']
            
            for zone_name in zones:
                # Increment current count
                self.zone_current_count[zone_name] = self.zone_current_count.get(zone_name, 0) + 1
                
                # Add to unique visitors set
                self.zone_visitors[zone_name].add(track_id)
    
    def print_zone_statistics(self):
        """Print detailed zone statistics"""
        print("\n=== Zone Statistics ===")
        for zone in self.zones.get('zones', []):
            if not zone.get('enabled', True):
                continue
            zone_name = zone.get('name', 'Unnamed')
            current = self.zone_current_count.get(zone_name, 0)
            total = len(self.zone_visitors.get(zone_name, set()))
            print(f"{zone_name}:")
            print(f"  Current Count: {current}")
            print(f"  Total Visitors: {total}")
            if total > 0:
                visitor_ids = sorted(list(self.zone_visitors[zone_name]))
                print(f"  Visitor IDs: {visitor_ids}")
        print("=====================\n")
    
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events for interactive zone drawing"""
        if not self.drawing_mode:
            return
            
        if event == cv2.EVENT_LBUTTONDOWN:
            # Add point to current zone
            self.current_zone_points.append([x, y])
            print(f"Point added: ({x}, {y}) - Total points: {len(self.current_zone_points)}")
            
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Finish current zone
            if len(self.current_zone_points) >= 3:
                self.finish_zone()
            else:
                print("Need at least 3 points to create a zone!")
        
        elif event == cv2.EVENT_MBUTTONDOWN:
            # Remove last point
            if len(self.current_zone_points) > 0:
                removed = self.current_zone_points.pop()
                print(f"Removed last point: {removed}")
    
    def finish_zone(self):
        """Finish creating the current zone and add it to zones list"""
        print("\nEnter zone name (or press Enter for default): ", end='', flush=True)
        zone_name = f"Zone_{len(self.zones['zones']) + 1}"
        
        # Get color for this zone
        zone_colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        color_idx = len(self.zones['zones']) % len(zone_colors)
        color = zone_colors[color_idx]
        
        # Create zone dictionary
        new_zone = {
            'name': zone_name,
            'points': self.current_zone_points,
            'color': list(color),
            'enabled': True
        }
        
        self.zones['zones'].append(new_zone)
        print(f"\nZone '{zone_name}' created with {len(self.current_zone_points)} points")
        
        # Reset current zone
        self.current_zone_points = []
    
    def draw_current_zone(self, frame):
        """Draw the zone currently being created"""
        if len(self.current_zone_points) > 0:
            # Draw points
            for point in self.current_zone_points:
                cv2.circle(frame, tuple(point), 5, (0, 255, 255), -1)
            
            # Draw lines connecting points
            if len(self.current_zone_points) > 1:
                points = np.array(self.current_zone_points, dtype=np.int32)
                cv2.polylines(frame, [points], False, (0, 255, 255), 2)
        
        return frame
    
    def detect_people(self, frame):
        """
        Detect people in frame using YOLOv8 with tracking
        
        Args:
            frame: Input video frame
            
        Returns:
            annotated_frame: Frame with detections drawn
            detections: List of detection dictionaries
        """
        # Run YOLOv8 tracking (tracks across frames)
        results = self.model.track(frame, persist=True, classes=[0], verbose=False)
        
        detections = []
        annotated_frame = frame.copy()
        
        # Draw zones first (background layer)
        annotated_frame = self.draw_zones(annotated_frame)
        
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            confidences = results[0].boxes.conf.cpu().numpy()
            
            for box, track_id, conf in zip(boxes, track_ids, confidences):
                x1, y1, x2, y2 = box.astype(int)
                
                # Calculate center point
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                center = (center_x, center_y)
                
                # Check which zone(s) person is in
                zones = self.get_person_zone(center)
                
                # Store detection info
                detection = {
                    'id': int(track_id),
                    'bbox': [x1, y1, x2, y2],
                    'center': center,
                    'confidence': float(conf),
                    'zones': zones
                }
                detections.append(detection)
                
                # Get color for this ID
                color = self.colors[track_id % len(self.colors)]
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw ID and confidence
                label = f'ID:{track_id} ({conf:.2f})'
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                
                # Draw label background
                cv2.rectangle(annotated_frame,
                            (x1, y1 - label_size[1] - 10),
                            (x1 + label_size[0], y1),
                            color, -1)
                
                # Draw label text
                cv2.putText(annotated_frame, label, (x1, y1 - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Draw zone information
                if zones:
                    zone_text = f"Zone: {', '.join(zones)}"
                    cv2.putText(annotated_frame, zone_text, (x1, y2 + 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Draw center point
                cv2.circle(annotated_frame, center, 4, color, -1)
                
                # Update track history
                self.track_history[track_id].append(center)
                if len(self.track_history[track_id]) > 30:
                    self.track_history[track_id].pop(0)
                
                # Draw tracking trail
                points = np.array(self.track_history[track_id], dtype=np.int32)
                cv2.polylines(annotated_frame, [points], False, color, 2)
        
        # Update zone statistics after all detections
        self.update_zone_statistics(detections)
        
        # Draw current zone being created (if in drawing mode)
        if self.drawing_mode:
            annotated_frame = self.draw_current_zone(annotated_frame)
        
        return annotated_frame, detections
    
    def process_video(self, video_source=0, output_path=None, display=True):
        """
        Process video from source (file or camera)
        
        Args:
            video_source: Video file path or camera index (0 for webcam)
            output_path: Optional path to save output video
            display: Whether to display the video
        """
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            print(f"Error: Cannot open video source {video_source}")
            return
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        
        # Setup video writer if output path specified
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        print(f"Processing video: {video_source}")
        print(f"Resolution: {width}x{height} @ {fps} FPS")
        print("\n=== Controls ===")
        print("Press 'q' to quit")
        print("Press 's' to save zones")
        print("Press 'd' to toggle drawing mode")
        print("  - Left Click: Add point to zone")
        print("  - Right Click: Finish zone")
        print("  - Middle Click: Remove last point")
        print("Press 'c' to clear current zone")
        print("Press 'z' to print zone statistics")
        print("================\n")
        
        window_name = 'YOLOv8 People Detection'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.mouse_callback)
        
        frame_count = 0
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Detect people
                annotated_frame, detections = self.detect_people(frame)
                
                # Add frame info
                info_text = f"Frame: {frame_count} | People: {len(detections)}"
                cv2.putText(annotated_frame, info_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Add drawing mode indicator
                if self.drawing_mode:
                    mode_text = f"DRAWING MODE | Points: {len(self.current_zone_points)}"
                    cv2.putText(annotated_frame, mode_text, (10, 60),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Display detections info
                if len(detections) > 0 and frame_count % 30 == 0:  # Print every 30 frames to reduce clutter
                    print(f"Frame {frame_count}: {len(detections)} people detected")
                    for det in detections:
                        zone_info = f" in {det['zones']}" if det['zones'] else ""
                        print(f"  - ID {det['id']}: conf={det['confidence']:.2f}{zone_info}")
                
                # Write frame to output
                if writer:
                    writer.write(annotated_frame)
                
                # Display frame
                if display:
                    cv2.imshow(window_name, annotated_frame)
                    
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        print("Quitting...")
                        break
                    elif key == ord('s'):
                        self.save_zones()
                        print("Zones saved!")
                    elif key == ord('d'):
                        self.drawing_mode = not self.drawing_mode
                        mode = "ON" if self.drawing_mode else "OFF"
                        print(f"Drawing mode: {mode}")
                    elif key == ord('c'):
                        self.current_zone_points = []
                        print("Current zone cleared")
                    elif key == ord('z'):
                        self.print_zone_statistics()
                        print("Zones saved!")
        
        finally:
            cap.release()
            if writer:
                writer.release()
            if display:
                cv2.destroyAllWindows()
            
            print(f"\nProcessing complete. Total frames: {frame_count}")


def main():
    """Main function to run people detection"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YOLOv8 People Detection with Zone Management')
    parser.add_argument('--source', type=str, default='Camera-Video.mp4',
                       help='Video source (0 for webcam, or path to video file)')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                       help='YOLOv8 model path (yolov8n.pt, yolov8s.pt, etc.)')
    parser.add_argument('--zones', type=str, default='zones.json',
                       help='Path to zones configuration file')
    parser.add_argument('--output', type=str, default=None,
                       help='Path to save output video')
    parser.add_argument('--no-display', action='store_true',
                       help='Disable video display')
    
    args = parser.parse_args()
    
    # Convert source to int if it's a number (camera index)
    try:
        video_source = int(args.source)
    except ValueError:
        video_source = args.source
    
    # Initialize detector
    detector = PeopleDetector(model_path=args.model, zones_file=args.zones)
    
    # Process video
    detector.process_video(
        video_source=video_source,
        output_path=args.output,
        display=not args.no_display
    )


if __name__ == '__main__':
    main()
