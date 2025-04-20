# frontend.py - GUI implementation

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                            QLabel, QLineEdit, QPushButton, QSpinBox, 
                            QHBoxLayout, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from backend import generate_qr_code, save_qr_code
from languages import get_translation

class QRCodeGeneratorApp(QMainWindow):
    def __init__(self, lang="en"):
        super().__init__()
        self.lang = lang
        self.translations = get_translation(lang)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(self.translations["window_title"])
        self.setFixedSize(500, 600)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Content input
        content_label = QLabel(self.translations["content_label"])
        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("https://example.com or any text")
        
        # Size selection
        size_layout = QHBoxLayout()
        size_label = QLabel(self.translations["size_label"])
        self.size_input = QSpinBox()
        self.size_input.setRange(100, 1000)
        self.size_input.setValue(400)
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_input)
        
        # Buttons
        self.generate_button = QPushButton(self.translations["generate_button"])
        self.generate_button.clicked.connect(self.generate_qr)
        self.save_button = QPushButton(self.translations["save_button"])
        self.save_button.clicked.connect(self.save_qr)
        self.save_button.setEnabled(False)
        
        # QR code display
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setMinimumSize(300, 300)
        
        # Add widgets to layout
        layout.addWidget(content_label)
        layout.addWidget(self.content_input)
        layout.addLayout(size_layout)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.qr_label)
        layout.addWidget(self.save_button)
        
    def generate_qr(self):
        """Generate and display the QR code"""
        content = self.content_input.text().strip()
        if not content:
            QMessageBox.critical(
                self,
                self.translations["error_title"],
                self.translations["error_empty"]
            )
            return
            
        size = self.size_input.value()
        self.qr_image = generate_qr_code(content, size)
        
        # Convert PIL image to QPixmap
        qimage = QImage(
            self.qr_image.tobytes(), 
            self.qr_image.size[0], 
            self.qr_image.size[1], 
            QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(qimage)
        self.qr_label.setPixmap(pixmap)
        self.save_button.setEnabled(True)
        
    def save_qr(self):
        """Save the generated QR code to a file"""
        if not hasattr(self, 'qr_image'):
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self,
            self.translations["save_title"],
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
        )
        
        if filename:
            try:
                save_qr_code(self.qr_image, filename)
                QMessageBox.information(
                    self,
                    self.translations["success_title"],
                    self.translations["success_message"]
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    self.translations["error_title"],
                    f"Error saving file: {str(e)}"
                )

def main():
    app = QApplication(sys.argv)
    
    # You can change the language here ('en' or 'ru')
    window = QRCodeGeneratorApp(lang="en")
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()