import os
import pyttsx3

class TextToAudioConverter:
    def __init__(self):
        # Initialize the native Windows text-to-speech engine
        self.engine = pyttsx3.init()

    def apply_settings(self, rate, volume, voice_index):
        """Applies configuration parameters dynamically right before rendering."""
        # 1. Update the speaking speed rate
        self.engine.setProperty('rate', rate)
        
        # 2. Update the volume scalar safely
        if 0.0 <= volume <= 1.0:
            self.engine.setProperty('volume', volume)
            
        # 3. Route the correct voice accent profile index
        voices = self.engine.getProperty('voices')
        if voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)

    def save_as_mp3(self, text, output_filename="gui_output.mp3"):
        """Compiles raw input text strings safely into an offline MP3 audio file."""
        if not text or not text.strip():
            print("[Error] Text block payload is empty. Conversion aborted.")
            return False

        try:
            print(f"Compiling raw text timeline into {output_filename}...")
            self.engine.save_to_file(text, output_filename)
            self.engine.runAndWait()
            print(f"[Success] Audio stream saved cleanly: {os.path.abspath(output_filename)}")
            return True
        except Exception as e:
            print(f"[Error] Thread execution pipeline exception: {e}")
            return False