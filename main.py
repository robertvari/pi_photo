from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QHBoxLayout, QLabel, QPushButton
from PySide2.QtCore import Qt
import sys

from modules.ImagePreview import ImagePreview, ImageCapture
from modules.Attributes import AttributesPanel


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Pi Photo")

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        column_layout = QHBoxLayout()
        main_layout.addLayout(column_layout)

        self.attributes_panel = AttributesPanel()
        column_layout.addWidget(self.attributes_panel)
        column_layout.setAlignment(self.attributes_panel, Qt.AlignTop)

        image_preview_layout = QVBoxLayout()
        column_layout.addLayout(image_preview_layout)

        self.image_display = ImagePreview()
        image_preview_layout.addWidget(self.image_display)
        image_preview_layout.setAlignment(self.image_display, Qt.AlignTop)

        self.capture = ImageCapture()
        self.attributes_panel.save_frame.connect(self.capture_image)

    def capture_image(self):
        if not self.attributes_panel.frame_path:
            return

        self.capture.path = self.attributes_panel.frame_path
        resolution = self.attributes_panel.resolution
        self.capture.set_size(resolution[0], resolution[1])

        self.image_display.worker.stop()
        self.image_display.worker.exited.connect(self.capture.start)
        self.capture.exited.connect(self.image_display.worker.start)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    app.exec_()
