# 🤖 JARVIS AI - Touchless Desktop Controller

A complete AI-powered virtual mouse, keyboard, and assistant system built with **Python** and **Streamlit**.

## ✨ Features

### 🖱️ Section 1: Virtual Mouse (Multi-Gesture)
- **Hand Tracking** using MediaPipe
- **Move Cursor** with index finger
- **Left Click** - quick pinch (thumb + index)
- **Drag & Drop** - hold the pinch, move, release
- **Right Click** - pinch thumb + middle finger
- **Scroll** - index + middle fingers up, move hand up/down
- Real-time camera feed with visual feedback
- Smoothed interpolated movement for fluid control

> 💡 **Use Mouse + Keyboard together:** the sidebar has Start/Stop Mouse and
> Open Virtual Keyboard buttons, so everything stays reachable while the
> mouse is running - no tab switching needed.

### 🚀 Section 2: Quick Actions
- **One-Click App Launcher** - Chrome, VS Code, Notepad, Calculator, and more
- **Custom App Launcher** - type any application name to launch it
- **Virtual Keyboard** opener
- Action history tracking
- Cross-platform support (Windows/Mac/Linux)

### 💬 Section 3: AI Chatbot
- **JARVIS AI** conversational assistant
- Context-aware responses
- Help with gesture controls and quick actions
- Fun interactions (jokes, time, date)

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Webcam

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

Or use the included launchers:
- **Windows:** double-click `run.bat`
- **Mac/Linux:** `./run.sh`

## 📖 Usage Guide

### Virtual Mouse
1. Click **"Start Virtual Mouse"** (sidebar or Section 1)
2. Show your hand to the camera
3. **Index finger** = move cursor
4. **Quick pinch** (thumb+index) = left click
5. **Hold pinch** ~0.5s then move = drag & drop, release to drop
6. **Pinch thumb+middle** = right click
7. **Index+middle up**, move hand up/down = scroll
8. Open the **virtual keyboard** from the sidebar anytime while the mouse runs

### Quick Actions
1. Go to **Section 2: Quick Actions**
2. Click any app button (Chrome, Notepad, VS Code...) to launch it instantly
3. Click **"Open Virtual Keyboard"** to bring up the on-screen keyboard
4. Type any app name in the custom launcher and hit **Launch**

### Virtual Keyboard + Mouse Combo
1. In **Quick Actions**, click **"Open Virtual Keyboard"**
2. The on-screen keyboard appears
3. Switch to **Virtual Mouse** tab
4. Hover over keys with your hand
5. Pinch to "press" each key

### AI Chatbot
1. Go to **Section 3: AI Chatbot**
2. Type your questions or click quick suggestions
3. Get instant help and guidance

## 🛡️ Safety

- **FAILSAFE:** Move mouse to top-left corner to immediately stop
- **Emergency Stop:** Click "Emergency Stop Mouse" in the sidebar
- The virtual mouse runs in a separate thread for smooth performance

## 🏗️ Project Structure

```
Virtual_Mouse_V2.0/
├── app.py                 # Main Streamlit application
├── mouse_controller.py    # Hand tracking & cursor control
├── app_launcher.py        # App launcher & virtual keyboard
├── ai_chatbot.py          # Conversational AI assistant
├── requirements.txt       # Python dependencies
├── run.bat               # Windows launcher
├── run.sh                # Mac/Linux launcher
└── README.md             # This file
```

## 🖥️ Supported Platforms

| Feature | Windows | Mac | Linux |
|---------|---------|-----|-------|
| Virtual Mouse | ✅ | ✅ | ✅ |
| Quick Actions | ✅ | ✅ | ✅ |
| Virtual Keyboard | ✅ | ✅ | ✅ |
| AI Chatbot | ✅ | ✅ | ✅ |

## 🛠️ Tech Stack

- **Streamlit** - Web interface
- **MediaPipe** - Hand landmark detection
- **OpenCV** - Camera capture & image processing
- **PyAutoGUI** - Cursor control & clicks

## 📝 License

Free to use and modify for personal and educational projects.
