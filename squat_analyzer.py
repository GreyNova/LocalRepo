import numpy as np
import cv2
from typing import Dict, List, Tuple, Optional
import math

class SquatAnalyzer:
    """
    Advanced squat pose analyzer with mathematical constraints
    for real-time feedback on squat form
    """
    
    def __init__(self):
        # Define ideal squat parameters
        self.ideal_knee_angle_range = (80, 100)  # degrees
        self.ideal_hip_angle_range = (70, 90)    # degrees
        self.ideal_ankle_angle_range = (70, 90)  # degrees
        self.ideal_back_angle_range = (15, 30)   # degrees from vertical
        
        # Feedback thresholds
        self.angle_tolerance = 10  # degrees
        self.balance_tolerance = 0.1  # normalized units
        
        # Pose state tracking
        self.squat_phase = "standing"  # standing, descending, bottom, ascending
        self.rep_count = 0
        self.current_feedback = []
        
    def calculate_angle(self, point1: Tuple[float, float], 
                       point2: Tuple[float, float], 
                       point3: Tuple[float, float]) -> float:
        """Calculate angle between three points"""
        try:
            # Convert to numpy arrays
            p1 = np.array(point1)
            p2 = np.array(point2)  # vertex
            p3 = np.array(point3)
            
            # Calculate vectors
            v1 = p1 - p2
            v2 = p3 - p2
            
            # Calculate angle
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            cos_angle = np.clip(cos_angle, -1.0, 1.0)  # Handle numerical errors
            angle = np.arccos(cos_angle)
            
            return np.degrees(angle)
        except:
            return 0.0
    
    def get_joint_positions(self, landmarks) -> Dict[str, Tuple[float, float]]:
        """Extract key joint positions from pose landmarks"""
        try:
            joints = {}
            
            # Key landmarks for squat analysis
            landmark_map = {
                'nose': 0,
                'left_shoulder': 11,
                'right_shoulder': 12,
                'left_hip': 23,
                'right_hip': 24,
                'left_knee': 25,
                'right_knee': 26,
                'left_ankle': 27,
                'right_ankle': 28,
                'left_heel': 29,
                'right_heel': 30,
                'left_foot_index': 31,
                'right_foot_index': 32
            }
            
            for joint_name, landmark_idx in landmark_map.items():
                if landmark_idx < len(landmarks.landmark):
                    landmark = landmarks.landmark[landmark_idx]
                    joints[joint_name] = (landmark.x, landmark.y)
            
            return joints
        except:
            return {}
    
    def analyze_knee_angles(self, joints: Dict) -> Dict[str, float]:
        """Analyze knee angles for both legs"""
        angles = {}
        
        # Left knee angle (hip -> knee -> ankle)
        if all(k in joints for k in ['left_hip', 'left_knee', 'left_ankle']):
            angles['left_knee'] = self.calculate_angle(
                joints['left_hip'], joints['left_knee'], joints['left_ankle']
            )
        
        # Right knee angle
        if all(k in joints for k in ['right_hip', 'right_knee', 'right_ankle']):
            angles['right_knee'] = self.calculate_angle(
                joints['right_hip'], joints['right_knee'], joints['right_ankle']
            )
        
        return angles
    
    def analyze_hip_angles(self, joints: Dict) -> Dict[str, float]:
        """Analyze hip angles for both legs"""
        angles = {}
        
        # Left hip angle (shoulder -> hip -> knee)
        if all(k in joints for k in ['left_shoulder', 'left_hip', 'left_knee']):
            angles['left_hip'] = self.calculate_angle(
                joints['left_shoulder'], joints['left_hip'], joints['left_knee']
            )
        
        # Right hip angle
        if all(k in joints for k in ['right_shoulder', 'right_hip', 'right_knee']):
            angles['right_hip'] = self.calculate_angle(
                joints['right_shoulder'], joints['right_hip'], joints['right_knee']
            )
        
        return angles
    
    def analyze_back_angle(self, joints: Dict) -> float:
        """Analyze back angle from vertical"""
        try:
            # Calculate torso angle using shoulders and hips
            if all(k in joints for k in ['left_shoulder', 'right_shoulder', 'left_hip', 'right_hip']):
                # Average shoulder and hip positions
                shoulder_center = (
                    (joints['left_shoulder'][0] + joints['right_shoulder'][0]) / 2,
                    (joints['left_shoulder'][1] + joints['right_shoulder'][1]) / 2
                )
                hip_center = (
                    (joints['left_hip'][0] + joints['right_hip'][0]) / 2,
                    (joints['left_hip'][1] + joints['right_hip'][1]) / 2
                )
                
                # Calculate angle from vertical
                dx = shoulder_center[0] - hip_center[0]
                dy = shoulder_center[1] - hip_center[1]
                
                angle_from_horizontal = math.atan2(dy, dx)
                angle_from_vertical = abs(90 - abs(math.degrees(angle_from_horizontal)))
                
                return angle_from_vertical
        except:
            pass
        
        return 0.0
    
    def analyze_balance(self, joints: Dict) -> Dict[str, float]:
        """Analyze balance and weight distribution"""
        balance_metrics = {}
        
        try:
            # Check foot position symmetry
            if all(k in joints for k in ['left_ankle', 'right_ankle']):
                left_foot = joints['left_ankle']
                right_foot = joints['right_ankle']
                
                # Horizontal symmetry
                foot_distance = abs(left_foot[0] - right_foot[0])
                balance_metrics['foot_symmetry'] = foot_distance
                
            # Check center of mass alignment
            if all(k in joints for k in ['left_hip', 'right_hip', 'left_ankle', 'right_ankle']):
                hip_center_x = (joints['left_hip'][0] + joints['right_hip'][0]) / 2
                ankle_center_x = (joints['left_ankle'][0] + joints['right_ankle'][0]) / 2
                
                balance_metrics['center_alignment'] = abs(hip_center_x - ankle_center_x)
                
        except:
            pass
        
        return balance_metrics
    
    def evaluate_squat_depth(self, joints: Dict) -> Dict[str, any]:
        """Evaluate squat depth and phase"""
        depth_info = {'depth_ratio': 0.0, 'phase': 'standing'}
        
        try:
            if all(k in joints for k in ['left_hip', 'left_knee', 'left_ankle']):
                hip_y = joints['left_hip'][1]
                knee_y = joints['left_knee'][1]
                ankle_y = joints['left_ankle'][1]
                
                # Calculate relative positions (normalized)
                thigh_length = abs(hip_y - knee_y)
                shin_length = abs(knee_y - ankle_y)
                
                if thigh_length > 0:
                    # Depth ratio: how low the hips are relative to knees
                    depth_ratio = (knee_y - hip_y) / thigh_length
                    depth_info['depth_ratio'] = max(0, depth_ratio)
                    
                    # Determine squat phase
                    if depth_ratio < 0.1:
                        depth_info['phase'] = 'standing'
                    elif depth_ratio < 0.3:
                        depth_info['phase'] = 'descending'
                    elif depth_ratio < 0.6:
                        depth_info['phase'] = 'bottom'
                    else:
                        depth_info['phase'] = 'deep_squat'
                        
        except:
            pass
        
        return depth_info
    
    def generate_feedback(self, analysis_results: Dict) -> List[str]:
        """Generate real-time feedback based on analysis"""
        feedback = []
        
        # Knee angle feedback
        knee_angles = analysis_results.get('knee_angles', {})
        for side, angle in knee_angles.items():
            if angle < self.ideal_knee_angle_range[0] - self.angle_tolerance:
                feedback.append(f"❌ {side.replace('_', ' ').title()}: Too bent ({angle:.1f}°) - Don't go too low")
            elif angle > self.ideal_knee_angle_range[1] + self.angle_tolerance:
                feedback.append(f"❌ {side.replace('_', ' ').title()}: Not bent enough ({angle:.1f}°) - Go deeper")
            else:
                feedback.append(f"✅ {side.replace('_', ' ').title()}: Good angle ({angle:.1f}°)")
        
        # Back angle feedback
        back_angle = analysis_results.get('back_angle', 0)
        if back_angle > self.ideal_back_angle_range[1] + self.angle_tolerance:
            feedback.append(f"❌ Back: Leaning too forward ({back_angle:.1f}°) - Keep chest up")
        elif back_angle < self.ideal_back_angle_range[0] - self.angle_tolerance:
            feedback.append(f"❌ Back: Too upright ({back_angle:.1f}°) - Slight forward lean is OK")
        else:
            feedback.append(f"✅ Back: Good posture ({back_angle:.1f}°)")
        
        # Balance feedback
        balance = analysis_results.get('balance', {})
        if balance.get('center_alignment', 0) > self.balance_tolerance:
            feedback.append("❌ Balance: Weight not centered - Shift weight to center")
        else:
            feedback.append("✅ Balance: Good weight distribution")
        
        # Depth feedback
        depth_info = analysis_results.get('depth', {})
        phase = depth_info.get('phase', 'standing')
        depth_ratio = depth_info.get('depth_ratio', 0)
        
        if phase == 'standing':
            feedback.append("💡 Ready to squat - Begin descent")
        elif phase == 'descending':
            feedback.append("💡 Descending - Keep going deeper")
        elif phase == 'bottom':
            feedback.append("✅ Good depth - Hold briefly then push up")
        elif phase == 'deep_squat':
            feedback.append("✅ Excellent depth - Drive through heels to stand")
        
        return feedback
    
    def analyze_pose(self, landmarks) -> Dict:
        """Main analysis function"""
        if not landmarks:
            return {'feedback': ['No pose detected'], 'angles': {}, 'valid': False}
        
        # Extract joint positions
        joints = self.get_joint_positions(landmarks)
        
        if not joints:
            return {'feedback': ['Unable to detect key joints'], 'angles': {}, 'valid': False}
        
        # Perform all analyses
        results = {}
        results['knee_angles'] = self.analyze_knee_angles(joints)
        results['hip_angles'] = self.analyze_hip_angles(joints)
        results['back_angle'] = self.analyze_back_angle(joints)
        results['balance'] = self.analyze_balance(joints)
        results['depth'] = self.evaluate_squat_depth(joints)
        
        # Generate feedback
        results['feedback'] = self.generate_feedback(results)
        results['joints'] = joints
        results['valid'] = True
        
        return results