"""
🚀 App Launcher & System Quick Actions
======================================
Cross-platform application launcher and
virtual keyboard opener.
"""

import subprocess
import platform
import os


class AppLauncher:
    """Launch applications and system tools with one click."""

    def __init__(self):
        self.os_type = platform.system()

        # App mapping for different OS
        self.app_map = {
            "chrome":     {"Windows": "chrome",        "Darwin": "open -a Google\ Chrome",           "Linux": "google-chrome"},
            "firefox":    {"Windows": "firefox",       "Darwin": "open -a Firefox",                 "Linux": "firefox"},
            "edge":       {"Windows": "msedge",        "Darwin": "open -a Microsoft\ Edge",        "Linux": "microsoft-edge"},
            "notepad":    {"Windows": "notepad",       "Darwin": "open -a TextEdit",                "Linux": "gedit"},
            "calculator": {"Windows": "calc",          "Darwin": "open -a Calculator",              "Linux": "gnome-calculator"},
            "word":       {"Windows": "winword",       "Darwin": "open -a Microsoft\ Word",        "Linux": "libreoffice --writer"},
            "excel":      {"Windows": "excel",         "Darwin": "open -a Microsoft\ Excel",       "Linux": "libreoffice --calc"},
            "powerpoint": {"Windows": "powerpnt",      "Darwin": "open -a Microsoft\ PowerPoint",  "Linux": "libreoffice --impress"},
            "vscode":     {"Windows": "code",          "Darwin": "open -a Visual\ Studio\ Code",  "Linux": "code"},
            "spotify":    {"Windows": "spotify",       "Darwin": "open -a Spotify",                 "Linux": "spotify"},
            "terminal":   {"Windows": "cmd",           "Darwin": "open -a Terminal",                "Linux": "gnome-terminal"},
            "file manager": {"Windows": "explorer",    "Darwin": "open .",                          "Linux": "nautilus"},
            "paint":      {"Windows": "mspaint",       "Darwin": "open -a Paintbrush",              "Linux": "gimp"},
            "settings":   {"Windows": "start ms-settings:", "Darwin": "open /System/Library/PreferencePanes", "Linux": "gnome-control-center"},
        }

        # Friendly display names
        self.display_names = {
            "chrome": "Google Chrome", "firefox": "Firefox", "edge": "Microsoft Edge",
            "notepad": "Notepad", "calculator": "Calculator", "word": "Microsoft Word",
            "excel": "Microsoft Excel", "powerpoint": "Microsoft PowerPoint",
            "vscode": "VS Code", "spotify": "Spotify", "terminal": "Terminal",
            "file manager": "File Manager", "paint": "Paint", "settings": "Settings",
        }

    def open_application(self, app_key):
        """Open an application by its key name."""
        app_key = app_key.lower().strip()
        if app_key not in self.app_map:
            return f"❌ Unknown app: {app_key}"

        command = self.app_map[app_key].get(self.os_type)
        if not command:
            return f"❌ {app_key} is not supported on {self.os_type}"

        try:
            subprocess.Popen(command, shell=True)
            name = self.display_names.get(app_key, app_key.title())
            return f"✅ Opened {name}"
        except Exception as e:
            return f"❌ Failed to open {app_key}: {str(e)}"

    def open_virtual_keyboard(self):
        """Open the system virtual / on-screen keyboard."""
        try:
            if self.os_type == "Windows":
                subprocess.Popen("osk.exe", shell=True)
                return "✅ Virtual Keyboard opened (Windows OSK)"
            elif self.os_type == "Darwin":
                subprocess.Popen(
                    "open -a /System/Library/Input Methods/KeyboardViewer.app",
                    shell=True
                )
                return "✅ Keyboard Viewer opened"
            else:  # Linux
                for cmd in ("onboard", "florence", "xvkbd"):
                    try:
                        subprocess.Popen(cmd, shell=True)
                        return f"✅ Virtual keyboard opened ({cmd})"
                    except Exception:
                        continue
                return "❌ No virtual keyboard found. Try: sudo apt install onboard"
        except Exception as e:
            return f"❌ Failed to open virtual keyboard: {str(e)}"

    def open_any_app(self, query):
        """Best-effort launcher for any app name typed by the user."""
        query = query.strip()
        if not query:
            return "❌ Please type an application name."

        key = query.lower()
        if key in self.app_map:
            return self.open_application(key)

        # Try a direct launch attempt on the current OS
        try:
            if self.os_type == "Darwin":
                subprocess.Popen(f"open -a '{query}'", shell=True)
            elif self.os_type == "Windows":
                subprocess.Popen(f"start {query}", shell=True)
            else:
                subprocess.Popen(f"{query} &", shell=True, executable="/bin/bash")
            return f"✅ Launch attempt sent for '{query}'"
        except Exception as e:
            return f"❌ Could not launch '{query}': {str(e)}"
