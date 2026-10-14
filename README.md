# Air Canvas: Real-Time Hand Gesture Drawing Interface

An interactive computer vision application that enables touchless digital drawing via webcam hand tracking, built with OpenCV and MediaPipe.

---

## Features
- **Real-Time Hand Tracking:** Employs MediaPipe Hands with a confidence threshold of 0.85 to minimize drawing jitter.
- **Dual-Finger Gesture Modes:**
  - **Selection Mode:** Raise both Index and Middle fingers to pick palette colors or select the eraser.
  - **Drawing Mode:** Raise only the Index finger to render smooth strokes on the canvas.
- **On-Screen Color Palette:** Interactive top header with selection targets for Red, Green, Blue, and Eraser.
- **Seamless Alpha Blending:** Uses inverse binary thresholding to overlay drawings onto the live webcam stream.

---

## Installation & Setup

\\\ash
# 1. Clone repository
git clone https://github.com/Prakharsingh05-Git/Air_Canvas_Painting.git
cd Air_Canvas_Painting

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run application
python air_canvas.py
\\\

---

## Controls
- **Index + Middle Fingers UP:** Selection Mode (Choose color / eraser)
- **Only Index Finger UP:** Drawing Mode
- **Key 'q':** Quit application
