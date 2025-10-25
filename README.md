# Real-Time Gesture Recognition with FastDTW

This is a simple Python application that uses classic computer science algorithms to recognize hand-drawn gestures in real-time.
The core of the project is built using Pygame for the interface and **Dynamic Time Warping (DTW)** for the recognition algorithm, demonstrating that powerful pattern recognition is possible without complex neural networks.

This program opens a window where the user can draw a shape (e.g., a circle, square, triangle). Upon releasing the mouse, the application analyzes the drawn path and compares it against a library of pre-defined templates. If a match is found within a certain threshold, it displays the name of the recognized shape.
The application can also learn new gestures. By pressing the 'G' key, the user can save their last drawing as a new template, making the recognizer smarter over time.

Recognizing human-drawn gestures is challenging because every drawing is unique. People draw at different **speeds**, in different **locations** on the screen, and at different **sizes**. This program solves these problems in a two-stage process:

## How it works

### 1. Preprocessing (Spatial Invariance)

Before a gesture can be compared, it must be standardized. The `preprocess` function cleans the raw list of `(x, y)` points by:
  1. **Centering:** The gesture is moved so its center of mass is at `(0, 0)`. This makes the algorithm independent of *where* the shape was drawn.
  2. **Scaling (Normalization):** The gesture is shrunk or enlarged to fit within a standard `[-1, 1]` bounding box. This makes the algorithm independent of the *size* of the drawing.
  3. **Resampling:** The gesture is re-sampled to a fixed number of points (e.g., 64). This ensures that a shape drawn quickly (fewer points) can be compared to one drawn slowly (more points).

### 2. Classification (Temporal Invariance)

After preprocessing, we have two standardized gestures. However, we still have the problem of **speed and timing**. A user might draw the first half of a circle quickly and the second half slowly.
This is solved using **Dynamic Time Warping (DTW)**. DTW is an algorithm that finds the optimal alignment between two time series (in our case, sequences of points). Instead of a rigid, point-for-point comparison (which would fail), DTW flexibly "warps" time, allowing it to find the minimum-cost path to match one shape to another, even if they have non-linear timing differences.
The gesture is classified as the template that has the lowest DTW distance (cost). It runs on FastDTW which is approximation of true DTW algorithm with **O(n) time complexity**.

## Features

* **Real-Time Recognition:** See the classification result instantly after drawing.
* **Dynamic Template Loading:** Automatically loads all `template_*.json` files from the root directory on startup.
* **Learn New Gestures:** Save your own gestures as new templates by simply pressing 'G'.

## Usage

### 1. Requirements

The project requires the following Python libraries:

* `pygame` (for the drawing interface)
* `numpy` (for numerical operations)
* `scipy` (for spatial distance calculations)
* `fastdtw` (for an optimized DTW implementation)

You can install them via pip:
```python
pip install -r requirements.txt
```

### 2. Running the Program

Simply run the script from your terminal: 
```python
python pattern_recognition.py
```

### 3. Controls

* **Hold Left Mouse Button:** Draw your gesture.
* **Release Left Mouse Button:** The program will attempt to recognize the gesture.
* **Press 'G' Key:** After drawing a gesture, press 'G' to save it as a new template. You will be prompted in the **terminal** (not the Pygame window) to provide a name for the gesture.
* **Press 'ESC' Key:** Quit the application.

### 4. Adding New Gestures

1. Run the program.
2. Draw the shape you want to teach (e.g., a "Z" or a "star").
3. Release the mouse.
4. Press the **'G'** key on your keyboard.
5. Switch to your terminal/console.
6. Type the name for your gesture (e.g., `star`) and press Enter.
7. The program will save it as `template_star.json`.
8. The new template is loaded automatically, and you can test its recognition immediately.

## File Structure

* `pattern_recognition.py`: The main application script.
* `template_*.json`: Gesture template files. Each file contains a JSON list of `[x, y]` coordinates representing a single preprocessed gesture. The name of the gesture is taken from the filename (e.g., `template_circle.json` is loaded as "circle").
