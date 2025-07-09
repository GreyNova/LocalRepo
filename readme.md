# CodeZen - Futuristic Competitive Programming Platform 🚀

A modern, minimalistic, and futuristic frontend for a competitive programming platform inspired by Codeforces. Built with vanilla HTML, CSS, and JavaScript featuring glassmorphism design, smooth animations, and an intuitive user experience.

## ✨ Features

### 🎨 **Futuristic Design**
- **Glassmorphism Effects**: Translucent cards with backdrop blur
- **Gradient Accents**: Cyan to purple gradient theme
- **Dark Theme**: Optimized for extended coding sessions
- **Smooth Animations**: Hover effects, page transitions, and micro-interactions
- **Modern Typography**: Inter font family for clean readability

### 🏠 **Homepage Features**
- **Problem Set**: Browse coding problems with difficulty filters
- **Live Contests**: View active, upcoming, and completed contests
- **Global Leaderboard**: Ranking system with user ratings
- **User Profile**: Personal statistics and activity tracking
- **Search & Filter**: Find problems by title, description, or difficulty

### 💻 **Problem Solving Interface**
- **Split Layout**: Problem description alongside code editor
- **Multi-Language Support**: Python, JavaScript, Java, C++
- **Code Editor**: Syntax-aware textarea with monospace font
- **Test Runner**: Execute test cases with detailed feedback
- **Real-time Results**: Instant feedback on submissions

### 📱 **Responsive Design**
- Mobile-first approach
- Adaptive layouts for all screen sizes
- Touch-friendly interfaces
- Optimized navigation for mobile devices

## 🛠️ Technologies Used

- **HTML5**: Semantic markup and modern structure
- **CSS3**: 
  - CSS Grid & Flexbox for layouts
  - CSS Custom Properties (Variables)
  - Backdrop-filter for glassmorphism
  - CSS Animations & Transitions
- **JavaScript (ES6+)**:
  - DOM manipulation
  - Event handling
  - Single Page Application (SPA) navigation
  - Interactive features

## 📁 Project Structure

```
CodeZen/
├── index.html          # Main homepage with navigation
├── problem.html        # Problem solving interface
├── style.css          # Complete styling and animations
├── script.js          # Interactive functionality
└── readme.md          # Project documentation
```

## 🚀 Getting Started

1. **Clone or Download** the project files
2. **Open** `index.html` in your web browser
3. **Explore** the different sections:
   - Problems: Browse and search coding challenges
   - Contests: View competition information
   - Leaderboard: Check global rankings
   - Profile: View user statistics
4. **Click "Solve"** on any problem to access the coding interface

## 🎯 Usage Guide

### Navigation
- Use the top navigation bar to switch between sections
- Active page is highlighted with gradient underline
- Mobile users get a stacked navigation layout

### Problem Solving
1. Click "Solve" on any problem card
2. Read the problem description on the left panel
3. Write your solution in the code editor (right panel)
4. Use the language dropdown to switch between programming languages
5. Click "Run Tests" to execute test cases
6. Click "Submit" to submit your final solution

### Interactive Features
- **Search**: Real-time filtering of problems
- **Difficulty Filter**: Filter problems by Easy/Medium/Hard
- **Hover Effects**: Cards lift and glow on hover
- **Button Ripples**: Material Design-inspired click effects
- **Animated Numbers**: Stats animate when scrolled into view
- **Typing Effect**: Logo subtitle types out on page load

## 🎨 Design Philosophy

### Minimalistic Approach
- Clean, uncluttered layouts
- Generous white space usage
- Focused content presentation
- Essential features only

### Futuristic Aesthetics
- **Color Palette**: Dark backgrounds with cyan/purple accents
- **Typography**: Modern, readable fonts (Inter + JetBrains Mono)
- **Shapes**: Rounded corners and soft edges
- **Effects**: Subtle glows and transparency

### User Experience
- **Intuitive Navigation**: Clear information hierarchy
- **Fast Interactions**: Smooth 60fps animations
- **Accessibility**: High contrast and readable text
- **Performance**: Optimized CSS and JavaScript

## 🌟 Key Components

### CSS Architecture
```css
/* CSS Custom Properties for consistent theming */
:root {
  --accent-primary: #00d4ff;
  --accent-secondary: #7b2cbf;
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
}

/* Glassmorphism effect */
.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
}
```

### JavaScript Features
- **SPA Navigation**: Smooth page transitions without reload
- **Dynamic Content**: Interactive search and filtering
- **Animation Triggers**: Scroll-based animations
- **User Feedback**: Loading states and success messages

## 🎨 Customization

### Color Scheme
Modify the CSS custom properties in `:root` to change the color theme:

```css
:root {
  --accent-primary: #your-color;
  --accent-secondary: #your-color;
  --bg-primary: #your-color;
}
```

### Adding New Problems
Add new problem cards to the `problems-grid` section:

```html
<div class="problem-card">
  <div class="problem-header">
    <h3 class="problem-title">Your Problem</h3>
    <span class="difficulty easy">Easy</span>
  </div>
  <p class="problem-description">Problem description here...</p>
  <div class="problem-stats">
    <span class="stat">👤 1k solved</span>
    <span class="stat">💎 500 pts</span>
  </div>
  <a href="problem.html" class="btn btn-primary btn-small">Solve</a>
</div>
```

## 🔮 Future Enhancements

- **Real Backend Integration**: Connect to actual API
- **User Authentication**: Login/signup functionality
- **Code Syntax Highlighting**: Enhanced editor features
- **Live Contest Timer**: Real-time countdown displays
- **Discussion Forums**: Community interaction features
- **Achievement System**: Badges and milestones
- **Dark/Light Mode Toggle**: Theme switching
- **Progressive Web App**: Offline capabilities

## 🎯 Browser Support

- **Chrome/Chromium**: Full support
- **Firefox**: Full support
- **Safari**: Full support (iOS 12+)
- **Edge**: Full support

*Note: Some advanced CSS features like `backdrop-filter` may have limited support in older browsers.*

## 🤝 Contributing

This is a frontend demonstration project. Feel free to:
- Fork and modify the design
- Add new features or pages
- Improve the responsive layout
- Enhance the animations
- Integrate with real APIs

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for the competitive programming community**

*Ready to code your way to the top? Start your journey with CodeZen!* 🚀