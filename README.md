# Text-to-Audio Converter

A modular, object-oriented Python application that provides a graphical user interface (GUI) to convert raw text strings or study notes into offline, portable MP3 audio files using the `pyttsx3` library.

## 📂 Project Structure

The codebase is split into specific, decoupled files for simple maintenance:
* `config.py`: Stores application-wide settings like default speech rate, volume scales, and voice identifiers.
* `converter.py`: Contains the core `TextToAudioConverter` class handling backend speech synthesis.
* `gui.py`: The main entry point script that builds the interactive desktop interface using Tkinter.
* `.gitignore`: Excludes Python environment caches and compiled audio outputs from cluttering the repository.

## ⚡ Key Features
* **Interactive Tkinter Interface:** Simple, native desktop window for handling user operations seamlessly.
* **Dynamic Voice Selectors:** Real-time toggles to switch speech output profiles between Male and Female options.
* **File Ingestion System:** Allows users to write raw text directly or load plain text (`.txt`) study sheets with a single click.
* **Auto-Play Integration:** Uses system triggers to automatically launch the computer's default media player as soon as audio compilation finishes.

## 🛠️ Setup and Execution

1.  The text-to-speech engine dependency is installed locally:
   ```bash
   pip install pyttsx3