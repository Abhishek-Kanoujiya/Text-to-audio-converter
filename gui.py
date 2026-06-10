import os
import tkinter as tk
from tkinter import messagebox, filedialog
import threading  #  Prevents Windows from hanging by handling the audio in the background
from converter import TextToAudioConverter
import config

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Audio Converter")
        self.root.geometry("520x480")
        self.root.config(bg="#f4f4f6")
        
        # Link backend class instance
        self.converter = TextToAudioConverter()
        
        # Build out the visual layout
        self.setup_ui()

    def setup_ui(self):
        # Header Label
        title = tk.Label(self.root, text="TTS Audio Synthesizer", font=("Arial", 14, "bold"), bg="#f4f4f6", fg="#333333")
        title.pack(pady=(15, 10))

        # 1. Voice Preference Selector
        voice_frame = tk.LabelFrame(self.root, text=" Choose Voice Profile ", font=("Arial", 10, "bold"), bg="#f4f4f6", padx=10, pady=5)
        voice_frame.pack(pady=10, fill="x", padx=20)

        self.voice_var = tk.IntVar(value=config.MALE_VOICE_INDEX)
        
        tk.Radiobutton(voice_frame, text="Male Voice Configuration", variable=self.voice_var, value=config.MALE_VOICE_INDEX, bg="#f4f4f6").pack(anchor="w", pady=2)
        tk.Radiobutton(voice_frame, text="Female Voice Configuration", variable=self.voice_var, value=config.FEMALE_VOICE_INDEX, bg="#f4f4f6").pack(anchor="w", pady=2)

        # 2. Text Content Input Box
        input_frame = tk.Frame(self.root, bg="#f4f4f6")
        input_frame.pack(pady=10, fill="both", expand=True, padx=20)

        tk.Label(input_frame, text="Type text or import study material notes below:", font=("Arial", 10), bg="#f4f4f6", fg="#555555").pack(anchor="w", pady=(0, 5))
        
        self.text_box = tk.Text(input_frame, height=8, font=("Arial", 10), wrap=tk.WORD, bd=1, relief="solid")
        self.text_box.pack(fill="both", expand=True, pady=5)

        # 3. Action Buttons
        btn_frame = tk.Frame(self.root, bg="#f4f4f6")
        btn_frame.pack(pady=15)

        load_btn = tk.Button(btn_frame, text="📂 Load text file (.txt)", font=("Arial", 10), command=self.import_text_file, bg="#ffffff", relief="groove", padx=10)
        load_btn.grid(row=0, column=0, padx=10)

        generate_btn = tk.Button(btn_frame, text="🔊 Convert & Play Audio", font=("Arial", 10, "bold"), command=self.handle_generation, bg="#007ACC", fg="white", relief="flat", padx=15, pady=5)
        generate_btn.grid(row=0, column=1, padx=10)

    def import_text_file(self):
        """Opens a file dialog window allowing users to load text directly into the application."""
        target_path = filedialog.askopenfilename(filetypes=[("Text Documents", "*.txt")])
        if target_path:
            try:
                with open(target_path, "r", encoding="utf-8") as raw_file:
                    file_contents = raw_file.read()
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert("1.0", file_contents)
            except Exception as error:
                messagebox.showerror("Read Failure", f"Could not load data file: {error}")

    def handle_generation(self):
        """Validates input, then creates a background thread to prevent the UI from freezing."""
        raw_input = self.text_box.get("1.0", tk.END).strip()
        chosen_voice = self.voice_var.get()

        if not raw_input:
            messagebox.showwarning("Missing Payload", "Please type or import some text details first.")
            return

        # Fire the conversion process on a background worker thread
        worker_thread = threading.Thread(target=self.run_conversion_backend, args=(raw_input, chosen_voice))
        worker_thread.start()

    def run_conversion_backend(self, raw_input, chosen_voice):
        """Runs the actual heavy processing safely on a separate thread."""
        target_filename = "gui_output.mp3"

        # Apply audio specifications to the engine
        self.converter.set_rate(config.DEFAULT_SPEED_WPM)
        self.converter.set_volume(config.DEFAULT_VOLUME)
        self.converter.set_voice(chosen_voice)
        
        print("Processing conversion on a separate background thread...")
        is_successful = self.converter.save_as_mp3(raw_input, output_filename=target_filename)

        # Once the background task finishes, bring up the alert and play the file
        if is_successful:
            messagebox.showinfo("Success", "Audio compiled cleanly! Launching media player.")
            os.system(f"start {target_filename}")
        else:
            messagebox.showerror("Pipeline Exception", "The internal compilation engine failed to create audio.")

if __name__ == "__main__":
    app_root = tk.Tk()
    app_instance = AudioConverterApp(app_root)
    app_root.mainloop()