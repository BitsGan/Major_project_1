import re
import random
import datetime


class AIChatbot:
    """
    AI Virtual Assistant Chatbot with rule-based intelligence
    and contextual responses for desktop control assistance.
    """

    def __init__(self):
        self.user_name = "User"
        self.context = []
        self.max_context = 5

        # Knowledge base for responses
        self.knowledge = {
            "greeting": [
                "Hello! I'm JARVIS, your AI desktop controller. How can I assist you today?",
                "Greetings! Ready to control your computer hands-free?",
                "Hey there! I'm your AI assistant. Need help with gesture control or quick actions?"
            ],
            "farewell": [
                "Goodbye! Feel free to chat with me anytime you need assistance.",
                "See you later! Keep controlling your desktop like a pro!",
                "Until next time! Remember: pinch to click, gestures to glide."
            ],
            "help": [
                """🤖 **JARVIS AI Assistant - Help Menu**

**Virtual Mouse:**
• Show your hand to the camera
• Move index finger to control cursor
• Pinch index finger + thumb to click

**Quick Actions:**
• One-click app launcher (Chrome, VS Code, Notepad, etc.)
• Open the virtual keyboard with a single click

**Chat with me:**
• Ask about system features
• Get tips on gesture control
• General conversation

What would you like to try first?"""
            ],
            "mouse_help": [
                """🖱️ **Virtual Mouse Guide:**

1. **Move Cursor** - Move index finger tip
2. **Left Click** - Quick pinch (thumb + index)
3. **Drag & Drop** - HOLD the pinch ~0.5s, move hand, release
4. **Right Click** - Pinch thumb + middle finger
5. **Scroll** - Raise index + middle fingers, move hand up/down
6. **Tips:**
   - Keep hand within camera frame
   - Good lighting helps detection
   - Pinch distance < 45px
   - Move mouse to top-left corner = emergency stop"""
            ],
            "keyboard_help": [
                """⌨️ **Virtual Keyboard Guide:**

1. Go to the **Quick Actions** tab
2. Click **"Open Virtual Keyboard"**
3. The on-screen keyboard will appear
4. Use your Virtual Mouse to hover over keys
5. Pinch (index+thumb) to press a key
6. Works with any text field!

**Supported Platforms:**
• Windows: On-Screen Keyboard (OSK)
• Mac: Keyboard Viewer
• Linux: Onboard"""
            ],
            "app_open": [
                "I can open applications for you! Go to the Quick Actions tab and click any app button.",
                "Use the Quick Actions tab - one click opens Chrome, Notepad, VS Code, Calculator and more.",
                "Try the Quick Actions tab! Every app there launches instantly with a single click."
            ],
            "creator": [
                "I am JARVIS, an AI desktop controller built with Python, MediaPipe, and Streamlit.",
                "I'm powered by computer vision and gesture recognition technology.",
                "I was created to provide touchless computer interaction using AI."
            ],
            "time": [
                lambda: f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}.",
                lambda: f"It's {datetime.datetime.now().strftime('%H:%M')} right now."
            ],
            "date": [
                lambda: f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}.",
                lambda: f"The date today is {datetime.datetime.now().strftime('%d/%m/%Y')}."
            ],
            "joke": [
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "Why did the AI go to therapy? It had too many neural issues! 🧠",
                "I told my computer I needed a break. Now it won't stop sending me Kit-Kats! 🍫",
                "Why was the mouse cold? Because it left its Windows open! 🪟"
            ],
            "thanks": [
                "You're welcome! Happy to help control your desktop.",
                "Anytime! That's what I'm here for.",
                "No problem! Let me know if you need anything else."
            ],
            "default": [
                "Interesting! Tell me more, or try asking about 'mouse', 'keyboard', 'apps', or 'help'.",
                "I'm not sure I understood that. Try 'help' for available features.",
                "Hmm, I specialize in desktop control. Ask me about virtual mouse, keyboard, or quick actions!"
            ]
        }

        # Pattern matching for intent detection
        self.patterns = {
            "greeting": r"\b(hello|hi|hey|greetings|howdy|hola)\b",
            "farewell": r"\b(bye|goodbye|see you|later|exit|quit)\b",
            "help": r"\b(help|assist|support|guide|how to|how do)\b",
            "mouse_help": r"\b(mouse|cursor|hand|gesture|move|click|pinch)\b",
            "keyboard_help": r"\b(keyboard|type|typing|keys|onscreen|osk)\b",
            "app_open": r"\b(open app|launch|start app|run program|application|chrome|notepad|vscode|calculator|spotify|excel|word)\b",
            "creator": r"\b(who are you|what are you|your name|created|built|maker)\b",
            "time": r"\b(time|clock|hour|what time)\b",
            "date": r"\b(date|day|today|month|year)\b",
            "joke": r"\b(joke|funny|humor|laugh|lol)\b",
            "thanks": r"\b(thanks|thank you|appreciate|grateful)\b"
        }

    def get_response(self, user_input):
        """Get AI response based on user input"""
        user_input = user_input.lower().strip()
        self.context.append(user_input)
        if len(self.context) > self.max_context:
            self.context.pop(0)

        # Check patterns
        for intent, pattern in self.patterns.items():
            if re.search(pattern, user_input):
                response = random.choice(self.knowledge[intent])
                # Handle lambda responses (time/date)
                if callable(response):
                    return response()
                return response

        # Context-aware fallback
        if len(self.context) >= 2:
            last_topic = self.context[-2]
            if "mouse" in last_topic and "how" in user_input:
                return random.choice(self.knowledge["mouse_help"])
            if "keyboard" in last_topic and "how" in user_input:
                return random.choice(self.knowledge["keyboard_help"])

        return random.choice(self.knowledge["default"])

    def get_welcome_message(self):
        return """👋 **Welcome to JARVIS AI Desktop Controller!**

I'm your intelligent assistant for touchless computer control.

**What I can do:**
🖱️ Control the mouse with hand gestures
🚀 Launch apps instantly from Quick Actions
⌨️ Open the virtual keyboard for typing
💬 Chat with me for help

Type **'help'** to see all features, or explore the tabs above!
"""
