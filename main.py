from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QHBoxLayout, QLabel, QPushButton
from PySide2.QtCore import Qt
import sys

from modules.ImagePreview import ImagePreview, CameraWorker
from modules.Attributes import AttributesPanel


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Pi Photo")

        self.camera = CameraWorker()

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        column_layout = QHBoxLayout()
        main_layout.addLayout(column_layout)

        self.attributes_panel = AttributesPanel(self.camera)
        column_layout.addWidget(self.attributes_panel)
        column_layout.setAlignment(self.attributes_panel, Qt.AlignTop)

        image_preview_layout = QVBoxLayout()
        column_layout.addLayout(image_preview_layout)

        self.preview = ImagePreview()
        image_preview_layout.addWidget(self.preview)
        image_preview_layout.setAlignment(self.preview, Qt.AlignTop)

        # start preview
        self.camera.frame_ready.connect(self.preview.set_image)
        self.camera.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    app.exec_()
