import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import threading
import time
from collections import deque

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01


class VirtualMouse:
    """
    AI Virtual Mouse with multi-gesture support:

    • Index finger ............... Move cursor
    • Quick pinch (index+thumb) .. Left click
    • HOLD pinch (index+thumb) ... Drag & drop
    • Pinch (middle+thumb) ....... Right click
    • Index + Middle up .......... Scroll mode (move hand up/down)
    """

    def __init__(self, smooth_frames=5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.screen_w, self.screen_h = pyautogui.size()
        self.running = False
        self.cap = None
        self.frame_callback = None
        self.status_callback = None
        self.frame_w, self.frame_h = 640, 480

        # Cursor smoothing buffer
        self.pos_history = deque(maxlen=smooth_frames)

        # Gesture state
        self.pinch_start = None        # when the current index-thumb pinch began
        self.dragging = False
        self.prev_pinch = False
        self.prev_mid_pinch = False
        self.last_click_time = 0
        self.last_rclick_time = 0
        self.scroll_prev_y = None

        # Tunables
        self.CLICK_DIST = 45           # px distance for a pinch
        self.DRAG_HOLD = 0.4           # seconds of holding pinch before drag starts
        self.CLICK_COOLDOWN = 0.35     # min seconds between clicks

    def start(self, frame_callback=None, status_callback=None):
        self.frame_callback = frame_callback
        self.status_callback = status_callback
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.dragging:
            try:
                pyautogui.mouseUp()
            except Exception:
                pass
            self.dragging = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    # ------------------------------------------------------------
    def _fingers_up(self, lm):
        """Return [index, middle, ring, pinky] True/False (up = tip above pip)."""
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        return [lm[tip].y < lm[pip].y for tip, pip in zip(tips, pips)]

    def _move_cursor(self, x, y, w, h):
        """Map camera coords -> screen coords with smoothing."""
        padding = 100
        interp_x = np.interp(x, (padding, w - padding), (0, self.screen_w))
        interp_y = np.interp(y, (padding, h - padding), (0, self.screen_h))
        self.pos_history.append((interp_x, interp_y))
        sx = sum(p[0] for p in self.pos_history) / len(self.pos_history)
        sy = sum(p[1] for p in self.pos_history) / len(self.pos_history)
        pyautogui.moveTo(sx, sy)

    def _release_pinch_state(self):
        """Safely cancel any in-progress pinch/drag."""
        if self.dragging:
            try:
                pyautogui.mouseUp()
            except Exception:
                pass
            self.dragging = False
        self.pinch_start = None
        self.prev_pinch = False

    # ------------------------------------------------------------
    def _run_loop(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_h)

        if self.status_callback:
            self.status_callback("🟢 Virtual Mouse Active - Multi-gesture mode enabled")

        while self.running and self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_img)

            status_text = "Index=Move | Pinch=Click | Hold pinch=Drag | Middle+Thumb=Right click | 2 fingers=Scroll"
            mode_color = (255, 255, 255)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    lm = hand_landmarks.landmark

                    ix, iy = int(lm[8].x * w),  int(lm[8].y * h)   # index tip
                    tx, ty = int(lm[4].x * w),  int(lm[4].y * h)   # thumb tip
                    mx, my = int(lm[12].x * w), int(lm[12].y * h)  # middle tip

                    index_up, middle_up, ring_up, pinky_up = self._fingers_up(lm)

                    pinch_dist = math.hypot(ix - tx, iy - ty)
                    mid_pinch_dist = math.hypot(mx - tx, my - ty)
                    pinch = pinch_dist < self.CLICK_DIST
                    mid_pinch = mid_pinch_dist < self.CLICK_DIST
                    now = time.time()

                    # ---------- Mode selection ----------
                    if index_up and middle_up and not ring_up and not pinky_up:
                        mode = "SCROLL"
                    elif pinch:
                        mode = "PINCH"
                    elif mid_pinch:
                        mode = "RIGHT"
                    else:
                        mode = "MOVE"

                    # ---------- SCROLL MODE ----------
                    if mode == "SCROLL":
                        if self.scroll_prev_y is not None:
                            dy = self.scroll_prev_y - iy
                            if abs(dy) > 3:
                                pyautogui.scroll(int(dy * 1.5))
                        self.scroll_prev_y = iy
                        self._release_pinch_state()
                        status_text = "📜 SCROLL MODE - move hand UP/DOWN to scroll"
                        mode_color = (255, 200, 0)
                        cv2.circle(frame, (ix, iy), 10, (255, 200, 0), -1)
                        cv2.circle(frame, (mx, my), 10, (255, 200, 0), -1)

                    # ---------- PINCH MODE (click / drag) ----------
                    elif mode == "PINCH":
                        self.scroll_prev_y = None
                        if not self.prev_pinch:
                            self.pinch_start = now

                        held = now - (self.pinch_start or now)

                        if not self.dragging and held >= self.DRAG_HOLD:
                            self.dragging = True
                            pyautogui.mouseDown()

                        if self.dragging:
                            self._move_cursor(ix, iy, w, h)
                            status_text = "🧲 DRAGGING - keep pinching & move, release to drop"
                            mode_color = (0, 165, 255)
                        else:
                            status_text = f"👌 Pinching {held:.1f}s - HOLD to drag, release to click"
                            mode_color = (0, 240, 255)

                        cv2.circle(frame, (ix, iy), 10, (0, 255, 0), -1)
                        cv2.circle(frame, (tx, ty), 10, (0, 0, 255), -1)
                        cv2.line(frame, (ix, iy), (tx, ty), (255, 255, 0), 2)
                        cv2.putText(frame, f"{int(pinch_dist)}px", (int((ix+tx)/2)+10, int((iy+ty)/2)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, mode_color, 2)

                    # ---------- MOVE / RIGHT-CLICK / release ----------
                    else:
                        # Pinch just released?
                        if self.prev_pinch:
                            if self.dragging:
                                pyautogui.mouseUp()
                                self.dragging = False
                                status_text = "✅ Drop!"
                                mode_color = (0, 255, 0)
                            elif now - self.last_click_time > self.CLICK_COOLDOWN:
                                pyautogui.click()
                                self.last_click_time = now
                                status_text = "✅ Left Click!"
                                mode_color = (0, 255, 0)
                        self.pinch_start = None
                        self.scroll_prev_y = None

                        if mode == "RIGHT":
                            if (not self.prev_mid_pinch and
                                    now - self.last_rclick_time > self.CLICK_COOLDOWN):
                                pyautogui.rightClick()
                                self.last_rclick_time = now
                                status_text = "✅ Right Click!"
                                mode_color = (0, 255, 0)
                            cv2.circle(frame, (mx, my), 10, (255, 0, 255), -1)
                            cv2.circle(frame, (tx, ty), 10, (0, 0, 255), -1)
                            cv2.line(frame, (mx, my), (tx, ty), (255, 255, 0), 2)
                        else:
                            # MOVE cursor smoothly
                            self._move_cursor(ix, iy, w, h)
                            cv2.circle(frame, (ix, iy), 10, (0, 255, 0), -1)

                    self.prev_pinch = pinch
                    self.prev_mid_pinch = mid_pinch

            cv2.putText(frame, "AI Virtual Mouse - Multi-Gesture | STOP to exit", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, mode_color, 2)

            if self.frame_callback:
                self.frame_callback(frame)
            if self.status_callback:
                self.status_callback(status_text)

        self.cap.release()
        cv2.destroyAllWindows()
