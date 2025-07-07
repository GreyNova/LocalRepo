#!/usr/bin/env python3
"""
Advanced Squat Training Application
Features:
- Real-time pose analysis
- Rep counting
- Form scoring
- Session statistics
- Progress tracking
"""

import cv2
import time
import json
import os
from datetime import datetime
from pose_detector import PoseDetector
from squat_analyzer import SquatAnalyzer

class AdvancedSquatTrainer:
    """Advanced squat training system with progress tracking"""
    
    def __init__(self):
        self.pose_detector = PoseDetector()
        self.squat_analyzer = SquatAnalyzer()
        self.running = False
        
        # Session statistics
        self.session_stats = {
            'start_time': None,
            'end_time': None,
            'total_squats': 0,
            'good_reps': 0,
            'form_scores': [],
            'phase_times': {'standing': 0, 'descending': 0, 'bottom': 0, 'ascending': 0},
            'angles_history': {'knee': [], 'hip': [], 'back': []}
        }
        
        # Rep tracking
        self.last_phase = "standing"
        self.current_rep_start = None
        self.rep_form_score = 0
        self.good_feedback_count = 0
        
        # Progress tracking
        self.progress_file = "squat_progress.json"
        self.load_progress()
    
    def load_progress(self):
        """Load previous training sessions"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    self.progress_data = json.load(f)
            except:
                self.progress_data = {'sessions': []}
        else:
            self.progress_data = {'sessions': []}
    
    def save_progress(self):
        """Save current session to progress file"""
        session_data = {
            'date': datetime.now().isoformat(),
            'duration_minutes': (self.session_stats['end_time'] - self.session_stats['start_time']) / 60,
            'total_squats': self.session_stats['total_squats'],
            'good_reps': self.session_stats['good_reps'],
            'success_rate': (self.session_stats['good_reps'] / max(1, self.session_stats['total_squats'])) * 100,
            'avg_form_score': sum(self.session_stats['form_scores']) / max(1, len(self.session_stats['form_scores'])),
            'phase_times': self.session_stats['phase_times']
        }
        
        self.progress_data['sessions'].append(session_data)
        
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2)
    
    def calculate_form_score(self, analysis):
        """Calculate form score based on analysis (0-100)"""
        if not analysis['valid']:
            return 0
        
        score = 0
        total_aspects = 0
        
        # Knee angle scoring
        knee_angles = analysis.get('knee_angles', {})
        for side, angle in knee_angles.items():
            total_aspects += 1
            ideal_min, ideal_max = self.squat_analyzer.ideal_knee_angle_range
            tolerance = self.squat_analyzer.angle_tolerance
            
            if ideal_min - tolerance <= angle <= ideal_max + tolerance:
                if ideal_min <= angle <= ideal_max:
                    score += 25  # Perfect score for ideal range
                else:
                    score += 15  # Good score for tolerance range
        
        # Back angle scoring
        back_angle = analysis.get('back_angle', 0)
        if back_angle > 0:
            total_aspects += 1
            ideal_min, ideal_max = self.squat_analyzer.ideal_back_angle_range
            tolerance = self.squat_analyzer.angle_tolerance
            
            if ideal_min - tolerance <= back_angle <= ideal_max + tolerance:
                if ideal_min <= back_angle <= ideal_max:
                    score += 25
                else:
                    score += 15
        
        # Balance scoring
        balance = analysis.get('balance', {})
        if balance:
            total_aspects += 1
            center_alignment = balance.get('center_alignment', 0)
            if center_alignment <= self.squat_analyzer.balance_tolerance:
                score += 25
            elif center_alignment <= self.squat_analyzer.balance_tolerance * 2:
                score += 15
        
        # Depth scoring
        depth_info = analysis.get('depth', {})
        if depth_info:
            total_aspects += 1
            phase = depth_info.get('phase', 'standing')
            if phase in ['bottom', 'deep_squat']:
                score += 25
            elif phase == 'descending':
                score += 15
        
        # Normalize score
        if total_aspects > 0:
            return min(100, (score / total_aspects))
        return 0
    
    def update_rep_tracking(self, analysis):
        """Update rep counting and form scoring"""
        if not analysis['valid']:
            return
        
        current_phase = analysis['depth']['phase']
        current_time = time.time()
        
        # Track phase timing
        if current_phase != self.last_phase:
            if current_phase == 'descending' and self.last_phase == 'standing':
                # Starting new rep
                self.current_rep_start = current_time
                self.rep_form_score = 0
                self.good_feedback_count = 0
            
            elif current_phase == 'standing' and self.last_phase in ['bottom', 'deep_squat']:
                # Completed rep
                self.session_stats['total_squats'] += 1
                
                # Calculate rep form score
                avg_form_score = self.rep_form_score / max(1, self.good_feedback_count)
                self.session_stats['form_scores'].append(avg_form_score)
                
                # Check if good rep
                if avg_form_score >= 70:  # 70% or higher is considered good
                    self.session_stats['good_reps'] += 1
        
        # Update form score for current rep
        if self.current_rep_start:
            current_form_score = self.calculate_form_score(analysis)
            self.rep_form_score += current_form_score
            self.good_feedback_count += 1
            
            # Track angles
            knee_angles = analysis.get('knee_angles', {})
            if knee_angles:
                avg_knee = sum(knee_angles.values()) / len(knee_angles)
                self.session_stats['angles_history']['knee'].append(avg_knee)
            
            back_angle = analysis.get('back_angle', 0)
            if back_angle > 0:
                self.session_stats['angles_history']['back'].append(back_angle)
        
        self.last_phase = current_phase
    
    def create_detailed_overlay(self, analysis):
        """Create detailed feedback overlay"""
        feedback_lines = ["🏋️ ADVANCED SQUAT TRAINER"]
        
        if analysis['valid']:
            # Basic feedback
            feedback_lines.extend(analysis['feedback'][:4])
            
            # Form score
            current_form_score = self.calculate_form_score(analysis)
            if current_form_score >= 80:
                score_icon = "🟢"
            elif current_form_score >= 60:
                score_icon = "🟡"
            else:
                score_icon = "🔴"
            
            feedback_lines.append(f"{score_icon} Form Score: {current_form_score:.0f}/100")
            
            # Rep info
            if self.current_rep_start:
                rep_duration = time.time() - self.current_rep_start
                feedback_lines.append(f"⏱️  Rep Time: {rep_duration:.1f}s")
        else:
            feedback_lines.append("❌ No pose detected - Step into view")
        
        # Session stats
        feedback_lines.extend([
            "",
            f"📊 Reps: {self.session_stats['total_squats']}",
            f"✅ Good: {self.session_stats['good_reps']}",
            f"📈 Success: {(self.session_stats['good_reps']/max(1, self.session_stats['total_squats'])*100):.1f}%"
        ])
        
        # Average form score
        if self.session_stats['form_scores']:
            avg_score = sum(self.session_stats['form_scores']) / len(self.session_stats['form_scores'])
            feedback_lines.append(f"🎯 Avg Score: {avg_score:.0f}/100")
        
        return feedback_lines
    
    def start_training(self):
        """Start advanced training session"""
        print("🏋️ Advanced Squat Trainer Starting...")
        print("=" * 50)
        
        # Show previous progress
        if self.progress_data['sessions']:
            last_session = self.progress_data['sessions'][-1]
            print(f"📈 Last Session: {last_session['total_squats']} squats, {last_session['success_rate']:.1f}% success")
        
        self.running = True
        self.session_stats['start_time'] = time.time()
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Could not open camera")
            return
        
        print("\n🎯 Training Session Active")
        print("📋 Advanced features enabled:")
        print("   • Real-time form scoring")
        print("   • Detailed rep analysis")
        print("   • Progress tracking")
        print("   • Session statistics")
        print("\n⌨️  Press 'q' to quit, 's' for stats")
        
        frame_count = 0
        
        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Flip for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect and analyze
                processed_frame, landmarks = self.pose_detector.detect_pose(frame)
                analysis = self.squat_analyzer.analyze_pose(landmarks)
                
                # Update rep tracking
                self.update_rep_tracking(analysis)
                
                # Draw landmarks
                if landmarks:
                    processed_frame = self.pose_detector.draw_custom_landmarks(
                        processed_frame, landmarks,
                        joints_to_highlight=['left_knee', 'right_knee', 'left_hip', 'right_hip']
                    )
                
                # Create detailed overlay
                feedback_lines = self.create_detailed_overlay(analysis)
                
                # Add FPS
                fps = self.pose_detector.calculate_fps()
                feedback_lines.append(f"🎥 FPS: {fps:.1f}")
                
                # Add overlay
                processed_frame = self.pose_detector.add_info_overlay(processed_frame, feedback_lines)
                
                # Show frame
                cv2.imshow('Advanced Squat Trainer - Q:Quit S:Stats', processed_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    self.print_live_stats()
        
        except KeyboardInterrupt:
            print("\n⏹️  Training stopped by user")
        
        finally:
            self.session_stats['end_time'] = time.time()
            cap.release()
            cv2.destroyAllWindows()
            self.pose_detector.release()
            self.running = False
            
            # Save and show results
            self.save_progress()
            self.show_detailed_summary()
    
    def print_live_stats(self):
        """Print live statistics to console"""
        print("\n" + "="*30 + " LIVE STATS " + "="*30)
        print(f"⏱️  Session Duration: {(time.time() - self.session_stats['start_time'])/60:.1f} min")
        print(f"📊 Total Squats: {self.session_stats['total_squats']}")
        print(f"✅ Good Reps: {self.session_stats['good_reps']}")
        
        if self.session_stats['form_scores']:
            avg_score = sum(self.session_stats['form_scores']) / len(self.session_stats['form_scores'])
            print(f"🎯 Average Form Score: {avg_score:.1f}/100")
            print(f"📈 Best Score: {max(self.session_stats['form_scores']):.1f}/100")
        
        print("="*72)
    
    def show_detailed_summary(self):
        """Show comprehensive session summary"""
        duration = self.session_stats['end_time'] - self.session_stats['start_time']
        
        print("\n" + "="*60)
        print("🏆 ADVANCED TRAINING SESSION SUMMARY")
        print("="*60)
        
        # Basic stats
        print(f"⏱️  Duration: {duration/60:.1f} minutes")
        print(f"📊 Total Squats: {self.session_stats['total_squats']}")
        print(f"✅ Good Reps: {self.session_stats['good_reps']}")
        print(f"📈 Success Rate: {(self.session_stats['good_reps']/max(1, self.session_stats['total_squats'])*100):.1f}%")
        
        # Form analysis
        if self.session_stats['form_scores']:
            scores = self.session_stats['form_scores']
            print(f"\n🎯 FORM ANALYSIS:")
            print(f"   Average Score: {sum(scores)/len(scores):.1f}/100")
            print(f"   Best Score: {max(scores):.1f}/100")
            print(f"   Worst Score: {min(scores):.1f}/100")
            print(f"   Score Consistency: {100 - (max(scores) - min(scores)):.1f}%")
        
        # Angle analysis
        angles = self.session_stats['angles_history']
        if angles['knee']:
            print(f"\n📐 ANGLE ANALYSIS:")
            print(f"   Avg Knee Angle: {sum(angles['knee'])/len(angles['knee']):.1f}°")
            if angles['back']:
                print(f"   Avg Back Angle: {sum(angles['back'])/len(angles['back']):.1f}°")
        
        # Progress comparison
        if len(self.progress_data['sessions']) > 1:
            prev_session = self.progress_data['sessions'][-2]
            current = self.progress_data['sessions'][-1]
            
            print(f"\n📊 PROGRESS vs LAST SESSION:")
            rep_change = current['total_squats'] - prev_session['total_squats']
            success_change = current['success_rate'] - prev_session['success_rate']
            
            print(f"   Reps: {rep_change:+d} ({current['total_squats']} vs {prev_session['total_squats']})")
            print(f"   Success Rate: {success_change:+.1f}% ({current['success_rate']:.1f}% vs {prev_session['success_rate']:.1f}%)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if self.session_stats['good_reps'] / max(1, self.session_stats['total_squats']) < 0.7:
            print("   • Focus on form quality over quantity")
            print("   • Practice slower, controlled movements")
            print("   • Work on mobility and flexibility")
        else:
            print("   • Excellent form! Consider increasing volume")
            print("   • Try adding variations (pause squats, etc.)")
            print("   • Focus on consistent performance")
        
        print("="*60)
        print(f"📁 Progress saved to: {self.progress_file}")

def main():
    """Main application entry point"""
    trainer = AdvancedSquatTrainer()
    
    print("🎯 Welcome to Advanced Squat Trainer!")
    print("\n🚀 Features:")
    print("   • Real-time pose analysis with mathematical constraints")
    print("   • Advanced form scoring (0-100 scale)")
    print("   • Automatic rep counting and tracking")
    print("   • Progress history and statistics")
    print("   • Detailed session analysis")
    
    input("\n📷 Make sure your camera is connected and press Enter to start...")
    
    trainer.start_training()

if __name__ == "__main__":
    main()