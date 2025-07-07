#!/usr/bin/env python3
"""
Alternative Squat Analysis Demo
This demo uses simulated pose data to showcase the mathematical analysis
when MediaPipe is not available.
"""

import cv2
import time
import numpy as np
from alternative_pose_detector import AlternativePoseDetector
from squat_analyzer import SquatAnalyzer

def main():
    print("🎯 Alternative Squat Pose Analysis Demo")
    print("=" * 50)
    print("📝 This demo simulates a person doing squats to showcase")
    print("   the mathematical analysis system.")
    print("🔬 Watch how the system analyzes angles and provides feedback!")
    print("=" * 50)
    
    # Initialize components
    pose_detector = AlternativePoseDetector()
    squat_analyzer = SquatAnalyzer()
    
    print("✅ Alternative pose detector initialized!")
    print("✅ Squat analyzer with mathematical rules ready!")
    print("\n📊 Analysis Parameters:")
    print(f"   • Ideal knee angles: {squat_analyzer.ideal_knee_angle_range[0]}°-{squat_analyzer.ideal_knee_angle_range[1]}°")
    print(f"   • Ideal back angle: {squat_analyzer.ideal_back_angle_range[0]}°-{squat_analyzer.ideal_back_angle_range[1]}° from vertical")
    print(f"   • Angle tolerance: ±{squat_analyzer.angle_tolerance}°")
    
    print("\n🎬 Starting simulation... Press 'q' to quit, 's' for stats")
    
    # Create a blank canvas to simulate camera feed
    frame_width, frame_height = 640, 480
    
    # Statistics
    frame_count = 0
    start_time = time.time()
    rep_count = 0
    last_phase = "standing"
    good_reps = 0
    total_scores = []
    
    try:
        while True:
            # Create a blank frame (simulating camera input)
            frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
            
            # Add background gradient for visual appeal
            for y in range(frame_height):
                intensity = int(50 + (y / frame_height) * 30)
                frame[y, :] = [intensity, intensity//2, intensity//3]
            
            frame_count += 1
            
            # Detect pose (this will create animated mock landmarks)
            processed_frame, landmarks = pose_detector.detect_pose(frame)
            
            # Analyze squat
            analysis = squat_analyzer.analyze_pose(landmarks)
            
            # Count reps and calculate scores
            if analysis['valid']:
                current_phase = analysis['depth']['phase']
                
                # Rep counting
                if last_phase in ['bottom', 'deep_squat'] and current_phase == 'standing':
                    rep_count += 1
                    
                    # Calculate rep quality score
                    good_feedback_count = sum(1 for f in analysis['feedback'] if '✅' in f)
                    total_feedback = len(analysis['feedback'])
                    
                    if good_feedback_count >= total_feedback * 0.6:  # 60% good feedback
                        good_reps += 1
                    
                    # Store angle measurements
                    knee_angles = analysis.get('knee_angles', {})
                    if knee_angles:
                        avg_knee_angle = sum(knee_angles.values()) / len(knee_angles)
                        total_scores.append(avg_knee_angle)
                
                last_phase = current_phase
            
            # Draw landmarks
            if landmarks:
                processed_frame = pose_detector.draw_custom_landmarks(
                    processed_frame, landmarks,
                    joints_to_highlight=['left_knee', 'right_knee', 'left_hip', 'right_hip']
                )
            
            # Create comprehensive feedback
            feedback_lines = ["🤖 SIMULATED SQUAT ANALYSIS"]
            
            if analysis['valid']:
                feedback_lines.extend(analysis['feedback'][:6])
                
                # Add angle details
                knee_angles = analysis.get('knee_angles', {})
                for side, angle in knee_angles.items():
                    feedback_lines.append(f"📐 {side.replace('_', ' ').title()}: {angle:.1f}°")
                
                back_angle = analysis.get('back_angle', 0)
                if back_angle > 0:
                    feedback_lines.append(f"📐 Back angle: {back_angle:.1f}°")
                
            else:
                feedback_lines.append("❌ No pose data")
            
            # Add statistics
            feedback_lines.extend([
                "",
                f"📊 Reps: {rep_count}",
                f"✅ Good Reps: {good_reps}",
                f"📈 Success Rate: {(good_reps/max(1, rep_count)*100):.1f}%"
            ])
            
            # Add performance info
            if frame_count % 30 == 0:  # Update every 30 frames
                fps = frame_count / (time.time() - start_time)
                feedback_lines.append(f"🎥 FPS: {fps:.1f}")
            
            # Add cycle info
            cycle_pos = (pose_detector.animation_frame % 120) / 120.0
            current_sim_phase = "Unknown"
            if cycle_pos < 0.25:
                current_sim_phase = "Standing"
            elif cycle_pos < 0.5:
                current_sim_phase = "Descending"
            elif cycle_pos < 0.75:
                current_sim_phase = "Bottom Position"
            else:
                current_sim_phase = "Ascending"
            
            feedback_lines.append(f"🎭 Simulation: {current_sim_phase}")
            
            # Add overlay
            processed_frame = pose_detector.add_info_overlay(processed_frame, feedback_lines)
            
            # Add title
            cv2.putText(processed_frame, "SQUAT ANALYSIS SIMULATION", 
                       (frame_width//2 - 200, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            
            # Show frame
            cv2.imshow('Squat Analysis Demo - Press Q to quit, S for stats', processed_frame)
            
            # Print detailed analysis every 60 frames
            if frame_count % 60 == 0 and analysis['valid']:
                print(f"\n📊 Frame {frame_count} Analysis:")
                knee_angles = analysis.get('knee_angles', {})
                for side, angle in knee_angles.items():
                    ideal_min, ideal_max = squat_analyzer.ideal_knee_angle_range
                    status = "✅ GOOD" if ideal_min <= angle <= ideal_max else "❌ NEEDS WORK"
                    print(f"   📐 {side.replace('_', ' ').title()}: {angle:.1f}° {status}")
                
                back_angle = analysis.get('back_angle', 0)
                if back_angle > 0:
                    ideal_min, ideal_max = squat_analyzer.ideal_back_angle_range
                    status = "✅ GOOD" if ideal_min <= back_angle <= ideal_max else "❌ NEEDS WORK"
                    print(f"   📐 Back angle: {back_angle:.1f}° {status}")
                
                depth_info = analysis.get('depth', {})
                print(f"   📏 Phase: {depth_info.get('phase', 'Unknown')}")
                print(f"   📏 Depth ratio: {depth_info.get('depth_ratio', 0):.2f}")
            
            # Handle key presses
            key = cv2.waitKey(30) & 0xFF  # 30ms delay for smooth animation
            if key == ord('q'):
                break
            elif key == ord('s'):
                print_live_stats(frame_count, start_time, rep_count, good_reps, total_scores)
    
    except KeyboardInterrupt:
        print("\n⏹️  Demo stopped by user")
    
    finally:
        cv2.destroyAllWindows()
        pose_detector.release()
        
        # Show final summary
        show_demo_summary(frame_count, start_time, rep_count, good_reps, total_scores, squat_analyzer)

def print_live_stats(frame_count, start_time, rep_count, good_reps, total_scores):
    """Print live statistics"""
    duration = time.time() - start_time
    print(f"\n" + "="*40 + " LIVE STATS " + "="*40)
    print(f"⏱️  Demo Duration: {duration:.1f} seconds")
    print(f"📹 Frames Processed: {frame_count}")
    print(f"🎥 Average FPS: {frame_count/duration:.1f}")
    print(f"📊 Total Reps: {rep_count}")
    print(f"✅ Good Reps: {good_reps}")
    print(f"📈 Success Rate: {(good_reps/max(1, rep_count)*100):.1f}%")
    
    if total_scores:
        avg_knee_angle = sum(total_scores) / len(total_scores)
        print(f"📐 Average Knee Angle: {avg_knee_angle:.1f}°")
    
    print("="*90)

def show_demo_summary(frame_count, start_time, rep_count, good_reps, total_scores, squat_analyzer):
    """Show comprehensive demo summary"""
    duration = time.time() - start_time
    
    print(f"\n" + "="*60)
    print("🏆 SQUAT ANALYSIS DEMO SUMMARY")
    print("="*60)
    
    # Performance stats
    print(f"⏱️  Demo Duration: {duration:.1f} seconds")
    print(f"📹 Frames Processed: {frame_count}")
    print(f"🎥 Average FPS: {frame_count/duration:.1f}")
    
    # Analysis stats
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"   Total Reps Detected: {rep_count}")
    print(f"   Good Form Reps: {good_reps}")
    print(f"   Success Rate: {(good_reps/max(1, rep_count)*100):.1f}%")
    
    # Angle analysis
    if total_scores:
        avg_angle = sum(total_scores) / len(total_scores)
        min_angle = min(total_scores)
        max_angle = max(total_scores)
        
        print(f"\n📐 ANGLE ANALYSIS:")
        print(f"   Average Knee Angle: {avg_angle:.1f}°")
        print(f"   Angle Range: {min_angle:.1f}° - {max_angle:.1f}°")
        
        ideal_min, ideal_max = squat_analyzer.ideal_knee_angle_range
        print(f"   Ideal Range: {ideal_min}° - {ideal_max}°")
        
        in_range_count = sum(1 for angle in total_scores if ideal_min <= angle <= ideal_max)
        print(f"   Angles in Ideal Range: {in_range_count}/{len(total_scores)} ({(in_range_count/len(total_scores)*100):.1f}%)")
    
    # Mathematical approach explanation
    print(f"\n🔬 MATHEMATICAL ANALYSIS APPROACH:")
    print(f"   This demo showcases how the system uses mathematical")
    print(f"   constraints to analyze squat form:")
    print(f"   • Angle calculations using vector mathematics")
    print(f"   • Real-time pose tracking and analysis")
    print(f"   • Objective feedback based on biomechanics")
    print(f"   • No training data required - pure mathematical rules")
    
    # Next steps
    print(f"\n🚀 NEXT STEPS:")
    print(f"   1. Install MediaPipe for real pose detection:")
    print(f"      pip install mediapipe")
    print(f"   2. Run the real-time trainer:")
    print(f"      python squat_trainer_app.py")
    print(f"   3. Customize analysis parameters in squat_analyzer.py")
    print(f"   4. Try with your own camera and real squats!")
    
    print("="*60)
    print("✅ Demo completed successfully!")

if __name__ == "__main__":
    main()