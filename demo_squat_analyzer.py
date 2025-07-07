#!/usr/bin/env python3
"""
Demo script for squat pose analysis system
Run this to test the system with your camera
"""

import cv2
import time
from pose_detector import PoseDetector
from squat_analyzer import SquatAnalyzer

def main():
    print("🎯 Squat Pose Analysis Demo")
    print("=" * 40)
    
    # Initialize components
    pose_detector = PoseDetector(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    squat_analyzer = SquatAnalyzer()
    
    # Test camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    print("✅ Camera connected successfully!")
    print("\n📍 Instructions:")
    print("   • Stand 3-4 feet away from camera")
    print("   • Make sure your full body is visible")
    print("   • Start doing squats")
    print("   • Press 'q' to quit")
    print("\n🎬 Starting demo...")
    
    # Statistics
    frame_count = 0
    start_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect pose
            processed_frame, landmarks = pose_detector.detect_pose(frame)
            
            # Analyze squat
            analysis = squat_analyzer.analyze_pose(landmarks)
            
            # Draw landmarks
            if landmarks:
                processed_frame = pose_detector.draw_custom_landmarks(
                    processed_frame, landmarks,
                    joints_to_highlight=['left_knee', 'right_knee', 'left_hip', 'right_hip']
                )
            
            # Prepare feedback
            if analysis['valid']:
                feedback_lines = ["SQUAT ANALYSIS:"] + analysis['feedback'][:6]
            else:
                feedback_lines = ["SQUAT ANALYSIS:", "❌ No pose detected - Step into view"]
            
            # Add FPS
            if frame_count % 30 == 0:  # Update every 30 frames
                fps = frame_count / (time.time() - start_time)
                feedback_lines.append(f"🎥 FPS: {fps:.1f}")
            
            # Add overlay
            processed_frame = pose_detector.add_info_overlay(processed_frame, feedback_lines)
            
            # Show frame
            cv2.imshow('Squat Pose Analyzer - Press Q to quit', processed_frame)
            
            # Print detailed analysis every 60 frames
            if frame_count % 60 == 0 and analysis['valid']:
                print(f"\n📊 Frame {frame_count} Analysis:")
                knee_angles = analysis.get('knee_angles', {})
                for side, angle in knee_angles.items():
                    print(f"   📐 {side.replace('_', ' ').title()}: {angle:.1f}°")
                
                back_angle = analysis.get('back_angle', 0)
                print(f"   📐 Back angle: {back_angle:.1f}°")
                
                depth_info = analysis.get('depth', {})
                print(f"   📏 Phase: {depth_info.get('phase', 'Unknown')}")
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n⏹️  Demo stopped by user")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        pose_detector.release()
        
        # Show summary
        duration = time.time() - start_time
        print(f"\n📈 Demo Summary:")
        print(f"   ⏱️  Duration: {duration:.1f} seconds")
        print(f"   📹 Frames processed: {frame_count}")
        print(f"   🎥 Average FPS: {frame_count/duration:.1f}")
        print("\n✅ Demo completed!")

if __name__ == "__main__":
    main()