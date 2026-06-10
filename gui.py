import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
from converter import TextToAudioConverter
import config

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Audio Converter")
        self.root.geometry("550x550")
        self.root.config(bg="#f4f4f6")
        
        self.converter = TextToAudioConverter()
        
        # Fetch available system voices to show true accents installed 
        self.system_voices = self.converter.engine.getProperty('voices')
        
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="TTS Audio Synthesizer", font=("Arial", 14, "bold"), bg="#f4f4f6", fg="#333333")
        title.pack(pady=(15, 10))

        # 1. Voice & Accent Dropdown Section
        voice_frame = tk.LabelFrame(self.root, text=" Select Voice / Accent ", font=("Arial", 10, "bold"), bg="#f4f4f6", padx=10, pady=5)
        voice_frame.pack(pady=10, fill="x", padx=20)

        # Create human-readable names for the dropdown
        voice_options = []
        for index, v in enumerate(self.system_voices):
            # Cleans up the system name to show something readable like "Voice 1 (English)"
            lang = "English/Native" if "EN" in v.id.upper() else "System Voice"
            voice_options.append(f"Profile {index + 1} - {v.name} ({lang})")

        self.voice_dropdown = ttk.Combobox(voice_frame, values=voice_options, state="readonly", width=50)
        self.voice_dropdown.current(0) # Default to the first available voice
        self.voice_dropdown.pack(pady=5, padx=5)

        # 2. Dynamic Speed Configuration Slider
        speed_frame = tk.LabelFrame(self.root, text=" Adjust Speed (Words Per Minute) ", font=("Arial", 10, "bold"), bg="#f4f4f6", padx=10, pady=5)
        speed_frame.pack(pady=10, fill="x", padx=20)

        # Pyttsx3 default speed is usually around 200. We allow low (100) to fast (300).
        self.speed_slider = tk.Scale(speed_frame, from_=100, to=300, orient=tk.HORIZONTAL, bg="#f4f4f6", highlightthickness=0)
        self.speed_slider.set(config.DEFAULT_SPEED_WPM) # Starts at your config default (175)
        self.speed_slider.pack(fill="x", padx=5, pady=5)

        # 3. Text Content Input Box
        input_frame = tk.Frame(self.root, bg="#f4f4f6")
        input_frame.pack(pady=10, fill="both", expand=True, padx=20)

        self.text_box = tk.Text(input_frame, height=6, font=("Arial", 10), wrap=tk.WORD, bd=1, relief="solid")
        self.text_box.pack(fill="both", expand=True, pady=5)

        # 4. Action Buttons
        btn_frame = tk.Frame(self.root, bg="#f4f4f6")
        btn_frame.pack(pady=15)

        load_btn = tk.Button(btn_frame, text="📂 Load file (.txt/.docx)", font=("Arial", 10), command=self.import_text_file, bg="#ffffff", relief="groove", padx=10)
        load_btn.grid(row=0, column=0, padx=10)

        generate_btn = tk.Button(btn_frame, text="🔊 Convert & Play Audio", font=("Arial", 10, "bold"), command=self.handle_generation, bg="#007ACC", fg="white", relief="flat", padx=15, pady=5)
        generate_btn.grid(row=0, column=1, padx=10)

    def import_text_file(self):
        target_path = filedialog.askopenfilename(
            filetypes=[("Text & Word Documents", "*.txt *.docx"), ("Text Documents", "*.txt"), ("Word Documents", "*.docx")]
        )
        if target_path:
            try:
                if target_path.endswith('.docx'):
                    import docx
                    doc = docx.Document(target_path)
                    file_contents = "\n".join([p.text for p in doc.paragraphs])
                else:
                    with open(target_path, "r", encoding="utf-8") as raw_file:
                        file_contents = raw_file.read()
                        
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert("1.0", file_contents)
            except Exception as error:
                messagebox.showerror("Read Failure", f"Could not load data file: {error}")

    def handle_generation(self):
        raw_input = self.text_box.get("1.0", tk.END).strip()
        
        # Get values dynamically from user configurations right from the GUI
        chosen_voice_index = self.voice_dropdown.current()
        chosen_speed = self.speed_slider.get()

        if not raw_input:
            messagebox.showwarning("Missing Payload", "Please type or import some text details first.")
            return

        worker_thread = threading.Thread(target=self.run_conversion_backend, args=(raw_input, chosen_voice_index, chosen_speed))
        worker_thread.start()

    def run_conversion_backend(self, raw_input, chosen_voice_index, chosen_speed):
        target_filename = "gui_output.mp3"

        # Pass the customized GUI slider and dropdown values safely to the converter engine
        self.converter.apply_settings(rate=chosen_speed, volume=config.DEFAULT_VOLUME, voice_index=chosen_voice_index)
        
        print(f"Processing text-to-speech at {chosen_speed} WPM using voice profile {chosen_voice_index}...")
        is_successful = self.converter.save_as_mp3(raw_input, output_filename=target_filename)

        if is_successful:
            messagebox.showinfo("Success", "Audio compiled cleanly! Launching media player.")
            os.system(f"start {target_filename}")
        else:
            messagebox.showerror("Pipeline Exception", "The internal compilation engine failed to create audio.")

if __name__ == "__main__":
    app_root = tk.Tk()
    app_instance = AudioConverterApp(app_root)
    app_root.mainloop()