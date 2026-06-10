import os
import pyttsx3
import config

class TextToAudioConverter:
    def __init__(self, rate=config.DEFAULT_SPEED_WPM, volume=config.DEFAULT_VOLUME, voice_index=config.MALE_VOICE_INDEX):
        # Initialize the native pyttsx3 conversion engine
        self.engine = pyttsx3.init()
        
        # Apply configurations passed on instantiation
        self.set_rate(rate)
        self.set_volume(volume)
        self.set_voice(voice_index)

    def set_rate(self, rate):
        """Modulates speech delivery pace in words per minute (WPM)."""
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """Sets engine amplification profile. Expects a float from 0.0 to 1.0."""
        if 0.0 <= volume <= 1.0:
            self.engine.setProperty('volume', volume)
        else:
            print("[Warning] Requested volume out of bounds. Keeping defaults.")

    def set_voice(self, voice_index):
        """Switches voice identities based on local system availability registry."""
        voices = self.engine.getProperty('voices')
        if voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
        else:
            print(f"[Warning] Voice profile index {voice_index} unavailable. Using default.")

    def save_as_mp3(self, text, output_filename="output.mp3"):
        """Compiles raw text data strings cleanly into structural MP3 audio blocks."""
        if not text or not text.strip():
            print("[Error] Conversion failed: Raw text content parameter cannot be empty.")
            return False

        try:
            print(f"Compiling raw text timeline into {output_filename}...")
            
            # Queue text execution payload to save asset locally
            self.engine.save_to_file(text, output_filename)
            
            # Flush processing array stacks and process blocking commands
            self.engine.runAndWait()
            
            print(f"[Success] Audio stream saved cleanly: {os.path.abspath(output_filename)}")
            return True
        except Exception as e:
            print(f"[Error] Pipeline processing error encountered: {e}")
            return False