import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import re
import datetime
import os


class SubtitleSynchronizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Arabic-English Subtitle Synchronizer")
        self.root.geometry("800x600")

        self.english_file_path = None
        self.arabic_file_path = None
        self.english_lines = []
        self.arabic_lines = []
        self.output_format = tk.StringVar(value="srt")
        self.subtitle_duration = tk.DoubleVar(value=3.0)
        self.start_time = tk.StringVar(value="00:00:00,000")

        self.create_widgets()

    def create_widgets(self):
        # File selection frame
        file_frame = ttk.LabelFrame(self.root, text="File Selection")
        file_frame.pack(fill="x", padx=10, pady=10)

        # English file selection
        ttk.Label(file_frame, text="English Subtitle File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.english_file_label = ttk.Label(file_frame, text="No file selected")
        self.english_file_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.select_english_file).grid(row=0, column=2, padx=5, pady=5)

        # Arabic file selection
        ttk.Label(file_frame, text="Arabic Subtitle File:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.arabic_file_label = ttk.Label(file_frame, text="No file selected")
        self.arabic_file_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.select_arabic_file).grid(row=1, column=2, padx=5, pady=5)

        # Timing and format frame
        timing_frame = ttk.LabelFrame(self.root, text="Timing and Format Settings")
        timing_frame.pack(fill="x", padx=10, pady=10)

        # Start time
        ttk.Label(timing_frame, text="Start Time (HH:MM:SS,mmm):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(timing_frame, textvariable=self.start_time, width=20).grid(row=0, column=1, sticky="w", padx=5,
                                                                             pady=5)

        # Subtitle duration
        ttk.Label(timing_frame, text="Subtitle Duration (seconds):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Spinbox(timing_frame, from_=1, to=10, increment=0.5, textvariable=self.subtitle_duration, width=5).grid(
            row=1, column=1, sticky="w", padx=5, pady=5)

        # Format selection
        ttk.Label(timing_frame, text="Output Format:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        format_frame = ttk.Frame(timing_frame)
        format_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(format_frame, text="SRT", variable=self.output_format, value="srt").pack(side="left", padx=5)
        ttk.Radiobutton(format_frame, text="ASS", variable=self.output_format, value="ass").pack(side="left", padx=5)

        # Preview frame
        preview_frame = ttk.LabelFrame(self.root, text="Preview")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a notebook with tabs for viewing the files
        self.notebook = ttk.Notebook(preview_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # English preview tab
        self.english_preview = ttk.Frame(self.notebook)
        self.notebook.add(self.english_preview, text="English Subtitles")
        self.english_text = tk.Text(self.english_preview, wrap="word")
        self.english_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Arabic preview tab
        self.arabic_preview = ttk.Frame(self.notebook)
        self.notebook.add(self.arabic_preview, text="Arabic Subtitles")
        self.arabic_text = tk.Text(self.arabic_preview, wrap="word")
        self.arabic_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Combined preview tab
        self.combined_preview = ttk.Frame(self.notebook)
        self.notebook.add(self.combined_preview, text="Combined Preview")
        self.combined_text = tk.Text(self.combined_preview, wrap="word")
        self.combined_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Preview Combination", command=self.synchronize).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Combine & Create Subtitle File", command=self.combine_and_save, width=25).pack(
            side="left", padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side="right", padx=5)

    def select_english_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.english_file_path = file_path
            self.english_file_label.config(text=os.path.basename(file_path))
            self.load_english_file()

    def select_arabic_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.arabic_file_path = file_path
            self.arabic_file_label.config(text=os.path.basename(file_path))
            self.load_arabic_file()

    def load_english_file(self):
        try:
            with open(self.english_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.english_text.delete(1.0, tk.END)
                self.english_text.insert(tk.END, content)
                self.english_lines = [line.strip() for line in content.split('\n') if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load English file: {e}")

    def load_arabic_file(self):
        try:
            with open(self.arabic_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.arabic_text.delete(1.0, tk.END)
                self.arabic_text.insert(tk.END, content)
                self.arabic_lines = [line.strip() for line in content.split('\n') if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Arabic file: {e}")

    def parse_time(self, time_str):
        try:
            # Parse time string in format HH:MM:SS,mmm
            hours, minutes, rest = time_str.split(':')
            seconds, milliseconds = rest.split(',')
            return datetime.timedelta(
                hours=int(hours),
                minutes=int(minutes),
                seconds=int(seconds),
                milliseconds=int(milliseconds)
            )
        except Exception as e:
            messagebox.showerror("Time Format Error",
                                 "Please enter time in format HH:MM:SS,mmm (e.g. 00:00:00,000)")
            return datetime.timedelta(0)

    def synchronize(self):
        if not self.english_lines or not self.arabic_lines:
            messagebox.showerror("Error", "Please load both English and Arabic files first.")
            return

        if len(self.english_lines) != len(self.arabic_lines):
            result = messagebox.askyesno("Warning",
                                         f"The number of lines in English ({len(self.english_lines)}) does not match Arabic ({len(self.arabic_lines)}).\n"
                                         "Do you want to continue anyway?")
            if not result:
                return

        # Create combined preview
        self.combined_text.delete(1.0, tk.END)

        max_lines = min(len(self.english_lines), len(self.arabic_lines))
        combined_lines = []

        # Parse start time and duration
        try:
            start_time_delta = self.parse_time(self.start_time.get())
            duration = self.subtitle_duration.get()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid time format: {e}")
            return

        # Generate timestamps for preview
        for i in range(max_lines):
            current_start = start_time_delta + datetime.timedelta(seconds=i * duration)
            current_end = current_start + datetime.timedelta(seconds=duration - 0.1)

            start_time_str = self.format_time(current_start)
            end_time_str = self.format_time(current_end)

            if self.output_format.get() == "srt":
                subtitle = f"{i + 1}\n{start_time_str} --> {end_time_str}\n{self.english_lines[i]}\n{self.arabic_lines[i]}\n\n"
            else:  # ASS format
                subtitle = f"Dialogue: 0,{start_time_str},{end_time_str},Default,,0,0,0,,{self.english_lines[i]}\\N{self.arabic_lines[i]}\n"

            combined_lines.append(subtitle)

        self.combined_text.insert(tk.END, "".join(combined_lines))
        self.notebook.select(self.combined_preview)

        messagebox.showinfo("Success",
                            "Preview generated successfully! Review the combined subtitles and adjust timing if needed.")

    def format_time(self, time_delta):
        if isinstance(time_delta, datetime.timedelta):
            total_seconds = time_delta.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            milliseconds = int((total_seconds % 1) * 1000)

            if self.output_format.get() == "srt":
                return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
            else:  # ASS format
                centiseconds = milliseconds // 10
                return f"{hours:d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
        else:
            # For backwards compatibility
            return time_delta

    def combine_and_save(self):
        # First synchronize to ensure combined text is up to date
        self.synchronize()

        if not hasattr(self, 'combined_text') or not self.combined_text.get(1.0, tk.END).strip():
            messagebox.showerror("Error", "Please generate a preview first.")
            return

        file_ext = ".srt" if self.output_format.get() == "srt" else ".ass"
        output_file = filedialog.asksaveasfilename(
            defaultextension=file_ext,
            filetypes=[(f"{self.output_format.get().upper()} Files", f"*{file_ext}"), ("All Files", "*.*")]
        )

        if output_file:
            try:
                content = self.combined_text.get(1.0, tk.END)

                # Add ASS header if needed
                if self.output_format.get() == "ass":
                    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
                    content = ass_header + content

                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(content)

                messagebox.showinfo("Success", f"Subtitle file created successfully!\nSaved to: {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save output: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleSynchronizer(root)
    root.mainloop()