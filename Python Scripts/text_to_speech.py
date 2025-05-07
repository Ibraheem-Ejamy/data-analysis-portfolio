import os
import sys
import pyttsx3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QFileDialog, QComboBox, QLabel,
                             QTextEdit, QMessageBox)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class TextToSpeechConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()

        # Set window properties
        self.setWindowTitle("Text to Speech Converter")
        self.setGeometry(300, 300, 600, 400)

        # Set the dark mode theme with blue accent
        self.set_dark_theme()

        # Create the UI
        self.init_ui()

    def set_dark_theme(self):
        # Set the application palette to dark theme
        dark_palette = QPalette()

        # Define colors
        dark_color = QColor(45, 45, 45)
        disabled_color = QColor(70, 70, 70)
        blue_accent = QColor(42, 130, 218)
        text_color = QColor(255, 255, 255)

        # Set color roles
        dark_palette.setColor(QPalette.Window, dark_color)
        dark_palette.setColor(QPalette.WindowText, text_color)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, dark_color)
        dark_palette.setColor(QPalette.ToolTipBase, blue_accent)
        dark_palette.setColor(QPalette.ToolTipText, text_color)
        dark_palette.setColor(QPalette.Text, text_color)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, disabled_color)
        dark_palette.setColor(QPalette.Button, dark_color)
        dark_palette.setColor(QPalette.ButtonText, text_color)
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, disabled_color)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, blue_accent)
        dark_palette.setColor(QPalette.Highlight, blue_accent)
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        # Apply the palette
        self.setPalette(dark_palette)

    def init_ui(self):
        # Create the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)

        # Create title label
        title_label = QLabel("Text to Speech Converter")
        title_label.setStyleSheet("font-size: 18pt; color: #2a82da; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Create a text area to display the selected file path
        self.file_path_display = QTextEdit()
        self.file_path_display.setPlaceholderText("No file selected...")
        self.file_path_display.setReadOnly(True)
        self.file_path_display.setMaximumHeight(60)
        self.file_path_display.setStyleSheet("border: 1px solid #2a82da; border-radius: 5px;")
        layout.addWidget(self.file_path_display)

        # Browse button
        self.browse_button = QPushButton("Browse Text File")
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a92ea;
            }
        """)
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        # Voice selection
        voice_label = QLabel("Select Voice:")
        voice_label.setStyleSheet("color: white; margin-top: 10px;")
        layout.addWidget(voice_label)

        self.voice_combo = QComboBox()
        self.voice_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #2a82da;
                border-radius: 5px;
                padding: 5px;
                background-color: #303030;
                color: white;
            }
            QComboBox:hover {
                border: 1px solid #3a92ea;
            }
            QComboBox QAbstractItemView {
                background-color: #303030;
                color: white;
                selection-background-color: #2a82da;
            }
        """)
        # Get available voices and add them to the combo box
        self.load_voices()
        layout.addWidget(self.voice_combo)

        # Text preview label
        preview_label = QLabel("Text Preview:")
        preview_label.setStyleSheet("color: white; margin-top: 10px;")
        layout.addWidget(preview_label)

        # Text preview area
        self.text_preview = QTextEdit()
        self.text_preview.setPlaceholderText("Text preview will appear here...")
        self.text_preview.setReadOnly(True)
        self.text_preview.setStyleSheet("border: 1px solid #2a82da; border-radius: 5px;")
        layout.addWidget(self.text_preview)

        # Convert button
        self.convert_button = QPushButton("Convert to Speech")
        self.convert_button.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #3a92ea;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)
        self.convert_button.clicked.connect(self.convert_to_speech)
        self.convert_button.setEnabled(False)  # Disabled until a file is selected
        layout.addWidget(self.convert_button)

    def load_voices(self):
        # Get available voices from the engine
        voices = self.engine.getProperty('voices')
        for voice in voices:
            # Extract just the name of the voice
            name = voice.name
            self.voice_combo.addItem(name, voice.id)

    def browse_file(self):
        # Open file dialog to select a text file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            # Display the selected file path
            self.file_path_display.setText(file_path)

            # Preview the text content (first 500 characters)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    preview = text[:500] + ("..." if len(text) > 500 else "")
                    self.text_preview.setText(preview)

                # Enable the convert button
                self.convert_button.setEnabled(True)

                # Store the full text
                self.current_text = text

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read file: {str(e)}")
                self.convert_button.setEnabled(False)

    def convert_to_speech(self):
        # Check if we have text to convert
        if not hasattr(self, 'current_text') or not self.current_text:
            QMessageBox.warning(self, "Warning", "No text available to convert.")
            return

        # Get selected voice ID
        voice_id = self.voice_combo.currentData()

        # Set the voice
        self.engine.setProperty('voice', voice_id)

        # Prepare the output file path
        input_path = self.file_path_display.toPlainText()
        output_path = os.path.splitext(input_path)[0] + '.mp3'

        try:
            # Show a message that conversion is starting
            QMessageBox.information(self, "Processing", "Converting text to speech.\nThis might take a moment...")

            # Convert text to speech
            self.engine.save_to_file(self.current_text, output_path)
            self.engine.runAndWait()

            # Show completion message with the output location
            QMessageBox.information(self, "Success", f"Conversion complete!\nFile saved to: {output_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert text to speech: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = TextToSpeechConverter()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()