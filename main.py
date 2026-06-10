from converter import TextToAudioConverter
import config


def main():
    # Instantiate the engine targeting an adaptive voice profile (example  Female)
    app = TextToAudioConverter(rate=180, volume=1.0, voice_index=config.FEMALE_VOICE_INDEX)
    
    # Text asset payload reflecting project credentials
    study_notes = (
        "Object-Oriented Programming (OOP) Core Pillars:\n"
        "1. Encapsulation: Bundling data properties and processing methods together.\n"
        "2. Abstraction: Concealing complex underlying code execution architectures.\n"
        "3. Inheritance: Deriving structural logic footprints from existing base classes.\n"
        "4. Polymorphism: Authorizing unified methods to adopt multiple functional shapes."
    )
    
    # Process conversion deployment loop
    app.save_as_mp3(study_notes, output_filename="oop_review_session.mp3")

if __name__ == "__main__":
    main()