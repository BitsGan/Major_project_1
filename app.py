"""
🤖 JARVIS AI - Virtual Mouse, Keyboard & AI Assistant
====================================================
A touchless desktop control system powered by:
• MediaPipe (Hand Tracking)
• OpenCV (Computer Vision)
• pyautogui (System Control)
• Streamlit (Web Interface)
"""

import streamlit as st
import numpy as np
from PIL import Image
import time
import cv2
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mouse_controller import VirtualMouse
from app_launcher import AppLauncher
from ai_chatbot import AIChatbot

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="JARVIS AI - Touchless Controller",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7b2cbf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .section-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid #2a2a4a;
        margin-bottom: 1rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .status-active {
        background: rgba(0, 255, 136, 0.15);
        color: #00ff88;
        border: 1px solid #00ff88;
    }
    .status-inactive {
        background: rgba(255, 77, 77, 0.15);
        color: #ff4d4d;
        border: 1px solid #ff4d4d;
    }
    .chat-message-user {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.5rem 0;
        max-width: 80%;
        align-self: flex-end;
    }
    .chat-message-bot {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.5rem 0;
        max-width: 80%;
        align-self: flex-start;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #1a1a2e;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00d4ff, #7b2cbf) !important;
        color: white !important;
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .command-history {
        background: #0f0f1a;
        border-radius: 10px;
        padding: 1rem;
        max-height: 300px;
        overflow-y: auto;
        font-family: monospace;
        font-size: 0.9rem;
    }
    .command-item {
        padding: 0.4rem 0;
        border-bottom: 1px solid #2a2a4a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "mouse_running" not in st.session_state:
    st.session_state.mouse_running = False
if "mouse_obj" not in st.session_state:
    st.session_state.mouse_obj = None
if "mouse_frame" not in st.session_state:
    st.session_state.mouse_frame = None
if "mouse_status" not in st.session_state:
    st.session_state.mouse_status = "⏹️ Mouse Inactive"
if "action_history" not in st.session_state:
    st.session_state.action_history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "bot" not in st.session_state:
    st.session_state.bot = AIChatbot()
if "launcher" not in st.session_state:
    st.session_state.launcher = AppLauncher()

# ============================================================
# CALLBACK FUNCTIONS
# ============================================================
def update_mouse_frame(frame):
    """Callback to update mouse frame in session state"""
    st.session_state.mouse_frame = frame

def update_mouse_status(status):
    """Callback to update mouse status"""
    st.session_state.mouse_status = status

def add_action(entry):
    """Add an entry to the quick-action history"""
    st.session_state.action_history.append(entry)


def start_mouse():
    """Start the virtual mouse engine"""
    st.session_state.mouse_obj = VirtualMouse()
    st.session_state.mouse_obj.start(
        frame_callback=update_mouse_frame,
        status_callback=update_mouse_status
    )
    st.session_state.mouse_running = True
    st.session_state.mouse_status = "🟢 Starting..."


def stop_mouse():
    """Stop the virtual mouse engine"""
    if st.session_state.mouse_obj:
        st.session_state.mouse_obj.stop()
    st.session_state.mouse_running = False
    st.session_state.mouse_frame = None
    st.session_state.mouse_status = "⏹️ Mouse Inactive"

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">🤖 JARVIS AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Touchless Desktop Controller • Gesture Mouse • Quick Actions • AI Chatbot</div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    st.markdown("---")

    # Mouse Status
    if st.session_state.mouse_running:
        st.markdown('<span class="status-badge status-active">🖱️ Mouse Active</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-inactive">🖱️ Mouse Inactive</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 System Info")
    st.info(f"**Status:** {st.session_state.mouse_status}")

    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")

    if st.button("🛑 Emergency Stop Mouse", use_container_width=True, type="primary", key="sb_emergency_stop"):
        if st.session_state.mouse_obj:
            st.session_state.mouse_obj.stop()
        st.session_state.mouse_running = False
        st.session_state.mouse_status = "⏹️ Mouse Inactive"
        st.rerun()

    # ---- Mouse & Keyboard always reachable from sidebar ----
    st.markdown("#### 🖱️ Mouse")
    if st.session_state.mouse_running:
        if st.button("⏹️ Stop Virtual Mouse", use_container_width=True, key="sb_stop_mouse"):
            stop_mouse()
            st.rerun()
    else:
        if st.button("▶️ Start Virtual Mouse", use_container_width=True, key="sb_start_mouse"):
            start_mouse()
            time.sleep(1)
            st.rerun()

    st.markdown("#### ⌨️ Keyboard")
    if st.button("⌨️ Open Virtual Keyboard", use_container_width=True, key="sb_open_keyboard"):
        kb_result = st.session_state.launcher.open_virtual_keyboard()
        add_action(kb_result)
        st.success(kb_result)

    st.markdown("---")

    if st.button("🧹 Clear Chat History", use_container_width=True, key="sb_clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("🧹 Clear Action History", use_container_width=True, key="sb_clear_actions"):
        st.session_state.action_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 📖 Instructions")
    st.markdown("""
    **💡 Tip:** Use the sidebar buttons
    above to start the mouse or open
    the keyboard WHILE the mouse runs -
    no tab switching needed!

    **Virtual Mouse:**
    1. Start mouse (sidebar or Section 1)
    2. Show hand to camera
    3. Index finger = move cursor
    4. Pinch index+thumb = click
    5. HOLD pinch = drag & drop

    **Quick Actions:**
    1. Go to Section 2
    2. Click any app button
    3. Apps open instantly
    4. Open the virtual keyboard
    5. Type using the Virtual Mouse

    **AI Chatbot:**
    1. Go to Section 3
    2. Type your message
    3. Get instant AI responses
    """)

# ============================================================
# MAIN TABS - 3 SECTIONS
# ============================================================
tab1, tab2, tab3 = st.tabs(["🖱️ Section 1: Virtual Mouse", "🚀 Section 2: Quick Actions", "💬 Section 3: AI Chatbot"])

# ============================================================
# SECTION 1: VIRTUAL MOUSE
# ============================================================
with tab1:
    st.markdown("## 🖱️ AI Virtual Mouse Controller")
    st.markdown("Control your cursor using hand gestures. No physical mouse needed!")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📹 Camera Feed")

        # Frame display area
        frame_placeholder = st.empty()
        status_placeholder = st.empty()

        # Show current frame if available
        if st.session_state.mouse_frame is not None and st.session_state.mouse_running:
            frame_rgb = cv2.cvtColor(st.session_state.mouse_frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            status_placeholder.info(st.session_state.mouse_status)
        else:
            frame_placeholder.markdown("""
                <div style="background:#0f0f1a; border-radius:15px; height:400px; display:flex; align-items:center; justify-content:center; flex-direction:column;">
                    <div style="font-size:4rem;">📷</div>
                    <div style="color:#888; margin-top:1rem;">Camera feed will appear here</div>
                    <div style="color:#555; font-size:0.9rem;">Click 'Start Virtual Mouse' to begin</div>
                </div>
            """, unsafe_allow_html=True)
            status_placeholder.info(st.session_state.mouse_status)

    with col2:
        st.markdown("### 🎮 Controls")

        if not st.session_state.mouse_running:
            if st.button("▶️ Start Virtual Mouse", use_container_width=True, type="primary", key="t1_start_mouse"):
                start_mouse()
                time.sleep(1)
                st.rerun()
        else:
            if st.button("⏹️ Stop Virtual Mouse", use_container_width=True, type="primary", key="t1_stop_mouse"):
                stop_mouse()
                st.rerun()

        # Keyboard right here - no tab switching while mouse runs
        if st.button("⌨️ Open Virtual Keyboard", use_container_width=True, key="t1_open_keyboard"):
            kb_result = st.session_state.launcher.open_virtual_keyboard()
            add_action(kb_result)
            st.success(kb_result)
            st.info("💡 Keyboard opened! Pinch keys to type.")

        st.markdown("---")
        st.markdown("### 📋 Gesture Guide")
        st.markdown("""
        <div class="section-card">
        <p>👆 <b>Move Cursor</b><br>
        <small>Move index finger tip</small></p>

        <p>👌 <b>Left Click</b><br>
        <small>Quick pinch: thumb + index</small></p>

        <p>🧲 <b>Drag & Drop</b><br>
        <small>HOLD pinch 0.4s, move hand, release</small></p>

        <p>👉 <b>Right Click</b><br>
        <small>Pinch: thumb + middle finger</small></p>

        <p>📜 <b>Scroll</b><br>
        <small>Index + Middle up, move hand up/down</small></p>

        <p>⚡ <b>Smooth Movement</b><br>
        <small>Averaged interpolated mapping</small></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### ⚠️ Safety")
        st.warning("Move mouse to top-left corner to trigger FAILSAFE and stop immediately.")

    # Auto-refresh when mouse is running
    if st.session_state.mouse_running:
        time.sleep(0.15)
        st.rerun()

# ============================================================
# SECTION 2: QUICK ACTIONS
# ============================================================
with tab2:
    st.markdown("## 🚀 Quick Actions & App Launcher")
    st.markdown("Launch applications and open the virtual keyboard instantly with a single click!")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🖥️ Launch Applications")

        app_buttons = [
            ("🌐 Chrome", "chrome"),
            ("📝 Notepad", "notepad"),
            ("🧮 Calculator", "calculator"),
            ("💻 VS Code", "vscode"),
            ("🦊 Firefox", "firefox"),
            ("📊 Excel", "excel"),
            ("📄 Word", "word"),
            ("🎵 Spotify", "spotify"),
        ]

        btn_cols = st.columns(2)
        for i, (label, key) in enumerate(app_buttons):
            with btn_cols[i % 2]:
                if st.button(label, use_container_width=True, key=f"app_{key}"):
                    result = st.session_state.launcher.open_application(key)
                    add_action(result)
                    st.success(result)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("➕ More Apps"):
            more_apps = [
                ("🌐 Edge", "edge"),
                ("📽️ PowerPoint", "powerpoint"),
                ("🖥️ Terminal", "terminal"),
                ("📁 File Manager", "file manager"),
                ("🎨 Paint", "paint"),
                ("⚙️ Settings", "settings"),
            ]
            more_cols = st.columns(2)
            for i, (label, key) in enumerate(more_apps):
                with more_cols[i % 2]:
                    if st.button(label, use_container_width=True, key=f"more_{key}"):
                        result = st.session_state.launcher.open_application(key)
                        add_action(result)
                        st.success(result)

        st.markdown("---")
        st.markdown("### ⌨️ Virtual Keyboard")

        if st.button("⌨️ Open Virtual Keyboard", use_container_width=True, type="primary", key="t2_open_keyboard"):
            result = st.session_state.launcher.open_virtual_keyboard()
            add_action(result)
            st.success(result)
            st.info("💡 Now use the Virtual Mouse to hover over keys and pinch to click them!")

        st.markdown("---")
        st.markdown("### 🔎 Open Any App")
        custom_app = st.text_input("Type an application name...", placeholder="e.g. chrome, spotify, gedit")
        if st.button("🚀 Launch", use_container_width=True, key="t2_launch") and custom_app.strip():
            result = st.session_state.launcher.open_any_app(custom_app)
            add_action(result)
            st.success(result)

    with col2:
        st.markdown("### 📜 Action History")

        if st.session_state.action_history:
            history_html = '<div class="command-history">'
            for item in reversed(st.session_state.action_history[-20:]):
                history_html += f'<div class="command-item">{item}</div>'
            history_html += '</div>'
            st.markdown(history_html, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="command-history" style="display:flex; align-items:center; justify-content:center; color:#555;">
                    No actions yet. Click a button to launch an app!
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 Pro Tip")
    st.info("🎯 Combo Mode: Open the virtual keyboard here, then switch to the Virtual Mouse tab and type by pinching on keys!")

# ============================================================
# SECTION 3: AI CHATBOT
# ============================================================
with tab3:
    st.markdown("## 💬 JARVIS AI Chatbot")
    st.markdown("Your intelligent assistant for desktop control guidance and conversation.")
    st.markdown("---")

    # Chat container
    chat_container = st.container()

    with chat_container:
        # Welcome message on first load
        if not st.session_state.chat_history:
            welcome = st.session_state.bot.get_welcome_message()
            st.session_state.chat_history.append({"role": "bot", "content": welcome})

        # Display chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div style="display:flex; justify-content:flex-end;"><div class="chat-message-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="display:flex; justify-content:flex-start;"><div class="chat-message-bot">{msg["content"]}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Input area
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("💭 Type your message...", key="chat_input", placeholder="Ask me about mouse control, keyboard, quick actions, or just chat!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_clicked = st.button("📤 Send", use_container_width=True, type="primary", key="t3_send")

    # Quick suggestion chips
    st.markdown("### ⚡ Quick Questions")
    chips = st.columns(4)
    chip_texts = ["How does virtual mouse work?", "Open keyboard help", "What apps can I open?", "Tell me a joke"]

    for i, chip in enumerate(chips):
        with chip:
            if st.button(chip_texts[i], use_container_width=True, key=f"chip_{i}"):
                user_input = chip_texts[i]
                send_clicked = True
                # Process immediately
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                response = st.session_state.bot.get_response(user_input)
                st.session_state.chat_history.append({"role": "bot", "content": response})
                st.rerun()

    # Process user input
    if send_clicked and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        response = st.session_state.bot.get_response(user_input)
        st.session_state.chat_history.append({"role": "bot", "content": response})
        st.rerun()

    # Also handle Enter key
    if user_input and user_input != st.session_state.get("last_input", ""):
        st.session_state["last_input"] = user_input

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#555; font-size:0.85rem;">
    🤖 <b>JARVIS AI Desktop Controller</b> | Built with Python, MediaPipe, OpenCV & Streamlit<br>
    Touchless Interaction • Gesture Control • Artificial Intelligence
</div>
""", unsafe_allow_html=True)
