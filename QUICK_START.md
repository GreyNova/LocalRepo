# 🚀 Quick Start: Squat Pose Analysis System

## 🎯 What This Is
A real-time squat form analyzer that uses **mathematical rules** (not machine learning) to provide instant feedback on your squat technique.

## ⚡ 30-Second Setup

```bash
# 1. Install basic dependencies
pip install opencv-python numpy matplotlib

# 2. Try the demo (works without camera!)
python demo_alternative_squat.py
```

## 🎮 What You'll See

### Simulated Squat Analysis
- Animated stick figure doing squats
- Real-time angle measurements
- Instant feedback on form
- Rep counting and scoring

### Sample Feedback:
```
✅ Left Knee: Good angle (92.3°)
✅ Right Knee: Good angle (88.7°)
✅ Back: Good posture (25.1°)
❌ Balance: Weight not centered
💡 Bottom position - Drive through heels to stand
```

## 📊 Key Features Demonstrated

1. **Mathematical Analysis**: See angle calculations in action
2. **Real-time Feedback**: Watch feedback change with movement
3. **Rep Counting**: Automatic squat detection
4. **Form Scoring**: 0-100 scoring system
5. **Progress Tracking**: Session statistics

## 🎯 Next Steps

### For Real Camera Input:
```bash
# Install MediaPipe
pip install mediapipe

# Run with real pose detection
python demo_squat_analyzer.py
```

### For Advanced Features:
```bash
# Full training application
python squat_trainer_app.py
```

## 🔧 Customize Analysis

Edit `squat_analyzer.py` to adjust:
- Ideal angle ranges
- Tolerance levels
- Feedback messages
- Scoring criteria

## 📚 Learn More

- **Full Guide**: See `STEP_BY_STEP_GUIDE.md`
- **Technical Details**: See `README.md`
- **Troubleshooting**: Check the guides above

## 🤔 Why This Approach?

### Mathematical Rules vs Machine Learning:
- ✅ **Explainable**: You know why feedback is given
- ✅ **Customizable**: Easy to adjust for your needs
- ✅ **Immediate**: No training data required
- ✅ **Consistent**: Same standards every time
- ✅ **Scientific**: Based on biomechanics research

---

**🎯 Ready to improve your squat form? Start the demo and see the math in action!**

```bash
python demo_alternative_squat.py
```