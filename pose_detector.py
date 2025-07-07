import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple
import time

class PoseDetector:
    """
    Real-time pose detection using MediaPipe
    """
    
    def __init__(self, 
                 min_detection_confidence=0.5, 
                 min_tracking_confidence=0.5):
        """
        Initialize MediaPipe pose detection
        
        Args:
            min_detection_confidence: Minimum confidence for pose detection
            min_tracking_confidence: Minimum confidence for pose tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
    def detect_pose(self, image: np.ndarray) -> Tuple[np.ndarray, Optional[object]]:
        """
        Detect pose landmarks in an image
        
        Args:
            image: Input BGR image from OpenCV
            
        Returns:
            Tuple of (processed_image, pose_landmarks)
        """
        # Convert BGR to RGB (MediaPipe expects RGB)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Disable writeable flag for performance
        rgb_image.flags.writeable = False
        
        # Detect pose
        results = self.pose.process(rgb_image)
        
        # Re-enable writeable flag
        rgb_image.flags.writeable = True
        
        # Convert back to BGR
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        
        return bgr_image, results.pose_landmarks
    
    def draw_landmarks(self, image: np.ndarray, landmarks) -> np.ndarray:
        """
        Draw pose landmarks on image
        
        Args:
            image: Input image
            landmarks: Pose landmarks from MediaPipe
            
        Returns:
            Image with landmarks drawn
        """
        if landmarks:
            # Draw pose landmarks
            self.mp_drawing.draw_landmarks(
                image, 
                landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
        return image
    
    def draw_custom_landmarks(self, image: np.ndarray, landmarks, 
                            joints_to_highlight: list = None) -> np.ndarray:
        """
        Draw custom landmarks with specific joints highlighted
        
        Args:
            image: Input image
            landmarks: Pose landmarks
            joints_to_highlight: List of joint names to highlight
            
        Returns:
            Image with custom landmarks
        """
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
            # Left leg
            ('left_hip', 'left_knee'),
            ('left_knee', 'left_ankle'),
            # Right leg
            ('right_hip', 'right_knee'),
            ('right_knee', 'right_ankle'),
            # Torso
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
        """
        Add information overlay to image
        
        Args:
            image: Input image
            info_text: List of text lines to display
            
        Returns:
            Image with info overlay
        """
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
        """Release MediaPipe resources"""
        self.pose.close()