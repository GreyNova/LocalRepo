import cv2
import numpy as np
from typing import Optional, Tuple
import time
import math

class MockLandmark:
    """Mock landmark class to simulate MediaPipe landmarks"""
    def __init__(self, x, y, z=0.0, visibility=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.visibility = visibility

class MockPoseLandmarks:
    """Mock pose landmarks to simulate MediaPipe results"""
    def __init__(self, landmarks):
        self.landmark = landmarks

class AlternativePoseDetector:
    """
    Alternative pose detection using basic computer vision
    This is a simplified version for demonstration purposes
    """
    
    def __init__(self, 
                 min_detection_confidence=0.5, 
                 min_tracking_confidence=0.5):
        """
        Initialize alternative pose detector
        """
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        # For demo purposes, we'll create a mock person
        self.mock_person_state = "standing"
        self.animation_frame = 0
        
    def create_mock_landmarks(self, frame_height, frame_width, squat_phase="standing"):
        """
        Create mock landmarks that simulate a person doing squats
        This demonstrates the mathematical analysis without requiring MediaPipe
        """
        # Normalize coordinates (MediaPipe uses normalized coordinates)
        center_x = 0.5
        center_y = 0.5
        
        # Simulate squat motion
        if squat_phase == "standing":
            knee_bend = 0.0
            hip_drop = 0.0
        elif squat_phase == "descending":
            knee_bend = 0.1
            hip_drop = 0.05
        elif squat_phase == "bottom":
            knee_bend = 0.2
            hip_drop = 0.15
        elif squat_phase == "ascending":
            knee_bend = 0.15
            hip_drop = 0.1
        else:
            knee_bend = 0.0
            hip_drop = 0.0
        
        # Create landmarks based on MediaPipe pose model
        landmarks = []
        
        # Add all 33 landmarks (MediaPipe pose has 33 landmarks)
        # We'll define key ones and set others to default positions
        landmark_positions = {
            0: (center_x, center_y - 0.3),  # nose
            11: (center_x - 0.15, center_y - 0.2),  # left_shoulder
            12: (center_x + 0.15, center_y - 0.2),  # right_shoulder
            23: (center_x - 0.1, center_y + hip_drop),  # left_hip
            24: (center_x + 0.1, center_y + hip_drop),  # right_hip
            25: (center_x - 0.1, center_y + 0.2 + knee_bend),  # left_knee
            26: (center_x + 0.1, center_y + 0.2 + knee_bend),  # right_knee
            27: (center_x - 0.1, center_y + 0.4 + knee_bend * 0.5),  # left_ankle
            28: (center_x + 0.1, center_y + 0.4 + knee_bend * 0.5),  # right_ankle
            29: (center_x - 0.1, center_y + 0.45 + knee_bend * 0.5),  # left_heel
            30: (center_x + 0.1, center_y + 0.45 + knee_bend * 0.5),  # right_heel
            31: (center_x - 0.1, center_y + 0.42 + knee_bend * 0.5),  # left_foot_index
            32: (center_x + 0.1, center_y + 0.42 + knee_bend * 0.5),  # right_foot_index
        }
        
        # Create all 33 landmarks
        for i in range(33):
            if i in landmark_positions:
                x, y = landmark_positions[i]
                landmarks.append(MockLandmark(x, y))
            else:
                # Default position for other landmarks
                landmarks.append(MockLandmark(center_x, center_y))
        
        return MockPoseLandmarks(landmarks)
    
    def detect_pose(self, image: np.ndarray) -> Tuple[np.ndarray, Optional[object]]:
        """
        Detect pose landmarks in an image
        For this demo, we'll create mock landmarks that change over time
        """
        # Simulate squat motion cycle
        self.animation_frame += 1
        cycle_position = (self.animation_frame % 120) / 120.0  # 120 frame cycle
        
        if cycle_position < 0.25:
            squat_phase = "standing"
        elif cycle_position < 0.5:
            squat_phase = "descending"
        elif cycle_position < 0.75:
            squat_phase = "bottom"
        else:
            squat_phase = "ascending"
        
        # Create mock landmarks
        landmarks = self.create_mock_landmarks(
            image.shape[0], image.shape[1], squat_phase
        )
        
        return image, landmarks
    
    def draw_landmarks(self, image: np.ndarray, landmarks) -> np.ndarray:
        """Draw pose landmarks on image"""
        if not landmarks:
            return image
        
        h, w, _ = image.shape
        
        # Draw basic pose structure
        connections = [
            (11, 12),  # shoulders
            (11, 23),  # left shoulder to hip
            (12, 24),  # right shoulder to hip
            (23, 24),  # hips
            (23, 25),  # left hip to knee
            (24, 26),  # right hip to knee
            (25, 27),  # left knee to ankle
            (26, 28),  # right knee to ankle
        ]
        
        # Draw connections
        for start_idx, end_idx in connections:
            if start_idx < len(landmarks.landmark) and end_idx < len(landmarks.landmark):
                start = landmarks.landmark[start_idx]
                end = landmarks.landmark[end_idx]
                
                start_point = (int(start.x * w), int(start.y * h))
                end_point = (int(end.x * w), int(end.y * h))
                
                cv2.line(image, start_point, end_point, (0, 255, 0), 2)
        
        return image
    
    def draw_custom_landmarks(self, image: np.ndarray, landmarks, 
                            joints_to_highlight: list = None) -> np.ndarray:
        """Draw custom landmarks with specific joints highlighted"""
        if not landmarks:
            return image
        
        h, w, _ = image.shape
        
        # Key joints for squat analysis
        key_joints = {
            'left_hip': 23,
            'right_hip': 24,
            'left_knee': 25,
            'right_knee': 26,
            'left_ankle': 27,
            'right_ankle': 28,
            'left_shoulder': 11,
            'right_shoulder': 12
        }
        
        # Draw connections first
        connections = [
            ('left_hip', 'left_knee'),
            ('left_knee', 'left_ankle'),
            ('right_hip', 'right_knee'),
            ('right_knee', 'right_ankle'),
            ('left_shoulder', 'left_hip'),
            ('right_shoulder', 'right_hip'),
            ('left_shoulder', 'right_shoulder'),
            ('left_hip', 'right_hip')
        ]
        
        # Draw connections
        for start_joint, end_joint in connections:
            if start_joint in key_joints and end_joint in key_joints:
                start_idx = key_joints[start_joint]
                end_idx = key_joints[end_joint]
                
                if (start_idx < len(landmarks.landmark) and 
                    end_idx < len(landmarks.landmark)):
                    
                    start_landmark = landmarks.landmark[start_idx]
                    end_landmark = landmarks.landmark[end_idx]
                    
                    start_point = (int(start_landmark.x * w), int(start_landmark.y * h))
                    end_point = (int(end_landmark.x * w), int(end_landmark.y * h))
                    
                    cv2.line(image, start_point, end_point, (0, 255, 0), 2)
        
        # Draw joints
        for joint_name, landmark_idx in key_joints.items():
            if landmark_idx < len(landmarks.landmark):
                landmark = landmarks.landmark[landmark_idx]
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                
                # Highlight specific joints
                if joints_to_highlight and joint_name in joints_to_highlight:
                    cv2.circle(image, (x, y), 8, (0, 0, 255), -1)  # Red for highlighted
                    cv2.circle(image, (x, y), 10, (255, 255, 255), 2)  # White border
                else:
                    cv2.circle(image, (x, y), 5, (255, 0, 0), -1)  # Blue for normal
                
                # Add joint label
                cv2.putText(image, joint_name.replace('_', ' '), (x + 10, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        
        return image
    
    def calculate_fps(self) -> float:
        """Calculate current FPS"""
        self.fps_counter += 1
        
        if self.fps_counter >= 10:  # Update every 10 frames
            current_time = time.time()
            self.current_fps = self.fps_counter / (current_time - self.fps_start_time)
            self.fps_counter = 0
            self.fps_start_time = current_time
        
        return self.current_fps
    
    def add_info_overlay(self, image: np.ndarray, info_text: list) -> np.ndarray:
        """Add information overlay to image"""
        # Create semi-transparent overlay
        overlay = image.copy()
        h, w = image.shape[:2]
        
        # Calculate text area
        text_height = len(info_text) * 25 + 20
        cv2.rectangle(overlay, (10, 10), (w - 10, text_height), (0, 0, 0), -1)
        
        # Blend overlay
        alpha = 0.7
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
        
        # Add text
        for i, text in enumerate(info_text):
            y_pos = 35 + i * 25
            cv2.putText(image, text, (20, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return image
    
    def release(self):
        """Release resources"""
        pass  # No resources to release in this mock version