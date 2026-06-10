# Text to Audio Converter

A lightweight, object-oriented Python utility that converts raw text strings or study notes into offline, portable MP3 audio files using the `pyttsx3` library ecosystem.

## 📂 Project Structure

The project uses modular components to separate configurations from runtime application loops:
* `config.py`: Stores structural constants such as speech rate, volume scales, and voice profile preferences.
* `converter.py`: Contains the core `TextToAudioConverter` class encapsulation layer managing speech synthesis.
* `main.py`: The primary runtime application loader containing script execution configurations and text data strings.
* `.gitignore`: Excludes volatile tracking parameters and local output audio assets from tracking into Git records.

## ⚡ Key Features
* **Object-Oriented Design:** Wrapped within fully scalable, reusable, and modular class implementations.
* **Granular Parametric Controls:** Allows dynamic manipulation of delivery speed metrics (WPM), voice profile arrays, and gain outputs.
* **Exception Prevention Management:** Features runtime validation loops ensuring empty payloads do not crash translation operations.

## 🛠️ Setup and Execution

1. Initialize project environment setup dependencies:
   ```bash
   pip install pyttsx3