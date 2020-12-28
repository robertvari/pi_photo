from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, \
    QFileDialog, QGroupBox, QSpinBox, QLabel, QComboBox, QCheckBox
import os


class AttributesPanel(QWidget):
    def __init__(self, camera):
        super(AttributesPanel, self).__init__()
        main_layout = QVBoxLayout(self)
        self.setMinimumWidth(400)

        self.camera = camera

        # image attributes
        image_format_box = QGroupBox("Image Attributes")
        image_format_layout = QVBoxLayout(image_format_box)
        main_layout.addWidget(image_format_box)

        res_layout = QHBoxLayout()
        image_format_layout.addLayout(res_layout)
        resolution_lbl = QLabel("Output resolution:")
        self.resolution_field = QComboBox()
        self.resolution_field.addItems([
            "640x480", "1024x768", "1280x960", "1920x1440", "2048x1536", "3200x2400"
        ])

        res_layout.addWidget(resolution_lbl)
        res_layout.addWidget(self.resolution_field)

        self.rotated_checkbx = QCheckBox("Rotete 180")
        self.rotated_checkbx.stateChanged.connect(self.rotate_image)
        image_format_layout.addWidget(self.rotated_checkbx)

        # save frame
        save_frame_box = QGroupBox("Capture Frame")
        save_box_layout = QVBoxLayout(save_frame_box)
        main_layout.addWidget(save_frame_box)

        save_path_layout = QHBoxLayout()
        save_box_layout.addLayout(save_path_layout)
        self.path_field = QLineEdit()
        self.path_field.setPlaceholderText("Image path...")
        browse_bttn = QPushButton("Browse")
        browse_bttn.clicked.connect(self._get_folder_path)

        save_path_layout.addWidget(self.path_field)
        save_path_layout.addWidget(browse_bttn)

        save_bttn = QPushButton("Save current Frame")
        save_bttn.clicked.connect(self.save_frame)
        save_box_layout.addWidget(save_bttn)

        # timelapse
        timelapse_box = QGroupBox("Timelapse")
        timelapse_box_layout = QVBoxLayout(timelapse_box)
        main_layout.addWidget(timelapse_box)

        timelapse_folder_layout = QHBoxLayout()
        timelapse_box_layout.addLayout(timelapse_folder_layout)

        self.timelapse_folder = QLineEdit()
        self.timelapse_folder.setPlaceholderText("Export path...")

        timelapse_folder_bttn = QPushButton("Browse...")
        timelapse_folder_layout.addWidget(self.timelapse_folder)
        timelapse_folder_layout.addWidget(timelapse_folder_bttn)

        time_layout = QHBoxLayout()
        timelapse_box_layout.addLayout(time_layout)

        time_lbl = QLabel("Max time (sec):")
        self.timelapse_time = QSpinBox()
        self.timelapse_time.setMinimum(1)
        time_layout.addWidget(time_lbl)
        time_layout.addWidget(self.timelapse_time)

        interval_layout = QHBoxLayout()
        timelapse_box_layout.addLayout(interval_layout)

        interval_lbl = QLabel("Interval (sec):")
        self.interval_field = QSpinBox()
        self.interval_field.setMinimum(1)
        interval_layout.addWidget(interval_lbl)
        interval_layout.addWidget(self.interval_field)

        start_timelapse_bttn = QPushButton("Start Timelapse...")
        timelapse_box_layout.addWidget(start_timelapse_bttn)

    def save_frame(self):
        if not self.path_field.text():
            return

        self.camera.save_frame(
            {
                "path": self.path_field.text(),
                "resolution": self.resolution
            }
        )

    def rotate_image(self):
        self.camera.set_rotate(self.rotated_checkbx.isChecked())

    def _get_folder_path(self):
        fname = QFileDialog.getExistingDirectory(self, "Select folder")
        self.path_field.setText(os.path.join(fname, "image1.jpg"))

    @property
    def resolution(self):
        return [int(i) for i in self.resolution_field.currentText().split("x")]

    @property
    def frame_path(self):
        return self.path_field.text()