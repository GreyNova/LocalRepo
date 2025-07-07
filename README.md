# Real-Time Squat Pose Analysis & Training System

A comprehensive computer vision system that provides real-time feedback on squat form using mathematical analysis and pose detection.

## 🎯 Features

- **Real-time pose detection** using MediaPipe
- **Mathematical analysis** of squat form with angle calculations
- **Instant feedback** on what's right and wrong with your squat
- **Automatic rep counting** and progress tracking
- **Form scoring** (0-100 scale) for objective assessment
- **Session statistics** and progress history
- **Customizable parameters** for different body types

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Test Your Setup

```bash
python demo_squat_analyzer.py
```

### Step 3: Start Training

```bash
python squat_trainer_app.py
```

## 📁 File Structure

```
├── squat_analyzer.py          # Core squat analysis with mathematical rules
├── pose_detector.py           # MediaPipe pose detection wrapper
├── demo_squat_analyzer.py     # Simple demo script
├── squat_trainer_app.py       # Advanced training application
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 How It Works

### 1. Mathematical Analysis

The system uses mathematical constraints to evaluate squat form:

#### Angle Analysis
- **Knee Angles**: Calculated using hip → knee → ankle points
  - Ideal range: 80°-100° (optimal squat depth)
  - Tolerance: ±10°

- **Hip Angles**: Calculated using shoulder → hip → knee points
  - Ideal range: 70°-90°

- **Back Angle**: Torso angle from vertical
  - Ideal range: 15°-30° (slight forward lean is normal)

#### Balance Assessment
- **Center of mass alignment**: Hip center vs ankle center
- **Foot symmetry**: Equal weight distribution

#### Depth Tracking
- **Phase detection**: Standing → Descending → Bottom → Ascending
- **Depth ratio**: Hip position relative to knee position

### 2. Real-Time Feedback

The system provides instant feedback on:
- ✅ **Good form aspects** (green checkmarks)
- ❌ **Form corrections needed** (red X with specific advice)
- 💡 **Phase guidance** (what to do next)
- 📐 **Angle measurements** (exact degrees)

### 3. Form Scoring

Each squat is scored 0-100 based on:
- Knee angle accuracy (25 points per leg)
- Back posture (25 points)
- Balance/stability (25 points)
- Squat depth (25 points)

## 🏋️ Using the Applications

### Demo Script (`demo_squat_analyzer.py`)
- Simple real-time analysis
- Basic feedback and rep counting
- Good for testing setup

### Advanced Trainer (`squat_trainer_app.py`)
- Comprehensive form analysis
- Progress tracking across sessions
- Detailed statistics and recommendations
- Form scoring with history

## 📊 Squat Form Guidelines

### ✅ Proper Squat Form

1. **Stance**: Feet shoulder-width apart, toes slightly turned out
2. **Descent**: Push hips back and down, keep chest up
3. **Depth**: Hip crease below knee cap (if mobility allows)
4. **Knees**: Track over toes, don't cave inward
5. **Back**: Maintain natural spine curve, slight forward lean OK
6. **Weight**: Evenly distributed on feet, not on toes

### ❌ Common Mistakes Detected

- **Knee valgus** (knees caving inward)
- **Excessive forward lean** (back angle too high)
- **Insufficient depth** (not going low enough)
- **Poor balance** (weight not centered)
- **Asymmetry** (unequal angles between sides)

## ⚙️ Customization

### Adjusting Parameters

You can modify the analysis criteria in `squat_analyzer.py`:

```python
# Ideal angle ranges (degrees)
self.ideal_knee_angle_range = (80, 100)
self.ideal_hip_angle_range = (70, 90)
self.ideal_back_angle_range = (15, 30)

# Tolerances
self.angle_tolerance = 10  # ±degrees
self.balance_tolerance = 0.1  # normalized units
```

### Camera Setup Tips

1. **Distance**: Stand 3-4 feet from camera
2. **Height**: Camera at hip/waist level if possible
3. **Lighting**: Ensure good, even lighting
4. **Background**: Plain background works best
5. **Clothing**: Contrasting colors help detection

## 🔬 Mathematical Approach vs Training Data

This system uses **mathematical rules** rather than machine learning because:

### Advantages of Mathematical Approach:
- **Objective standards**: Based on biomechanics research
- **Explainable**: You know exactly why something is flagged
- **Consistent**: Same criteria every time
- **Customizable**: Easy to adjust for different needs
- **No training data needed**: Works immediately
- **Transparent**: Clear feedback on specific angles/measurements

### When You Might Want Training Data:
- **Subtle form variations**: ML could catch nuanced patterns
- **Personal adaptation**: Learning your specific movement patterns
- **Advanced exercise variations**: Complex movements beyond basic squats

## 📈 Progress Tracking

The advanced trainer automatically saves:
- Session duration and rep counts
- Form scores and consistency metrics
- Average angles and improvements over time
- Success rate trends
- Personalized recommendations

Progress is saved to `squat_progress.json` for long-term tracking.

## 🛠️ Troubleshooting

### Camera Issues
```bash
# Test different camera indices
cap = cv2.VideoCapture(1)  # Try 1, 2, etc. if 0 doesn't work
```

### Poor Detection
- Ensure good lighting
- Check that full body is visible
- Try different clothing (contrasting colors)
- Adjust camera angle/distance

### Performance Issues
- Lower camera resolution in code if needed
- Adjust MediaPipe confidence thresholds
- Close other applications using camera

## 🎓 Exercise Science Background

### Ideal Squat Biomechanics

The mathematical constraints are based on:
- **Knee angle**: 80-100° represents functional squat depth
- **Hip hinge pattern**: Proper hip flexion before knee flexion
- **Spinal neutrality**: Slight forward lean (15-30°) is biomechanically normal
- **Force distribution**: Balanced weight prevents injury

### Progression Recommendations

1. **Beginners**: Focus on form over depth
2. **Intermediate**: Work toward 90° knee angles
3. **Advanced**: Add variations while maintaining form

## 🤝 Contributing

To add new exercises or improve analysis:

1. **Fork the repository**
2. **Add new analyzer classes** following the same pattern
3. **Implement mathematical constraints** for the new exercise
4. **Test thoroughly** with different body types
5. **Submit pull request** with documentation

## 📜 License

This project is open source. Feel free to use, modify, and distribute.

## 🆘 Support

If you encounter issues:
1. Check this README for troubleshooting
2. Ensure all dependencies are installed correctly
3. Test with the simple demo first
4. Verify camera is working with other applications

---

**Ready to improve your squat form? Start with the demo script and work your way up to the advanced trainer!** 🏋️‍♀️