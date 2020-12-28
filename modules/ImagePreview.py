from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPainter, QImage
from PySide2.QtCore import QPoint, QThread, Signal
import cv2
import qimage2ndarray


class ImagePreview(QWidget):
    def __init__(self):
        super(ImagePreview, self).__init__()

        self._width = 640
        self._height = 480
        self.setMinimumSize(self._width, self._height)
        self.setMaximumSize(self._width, self._height)

        self.image = None

    def set_image(self, image):
        self.image = image
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()


class CameraWorker(QThread):
    frame_ready = Signal(QImage)
    stopped = Signal()

    def __init__(self):
        super(CameraWorker, self).__init__()
        self.running = False
        self.rotated = False

        self._capture = None

        self._width = 640
        self._height = 480

    def set_size(self, width, height):
        self._width = width
        self._height = height

    def set_rotate(self, value):
        self.rotated = value

    def save_frame(self, parameters):
        print("Saving image...")
        self.stop()

        width = parameters.get("resolution")[0]
        height = parameters.get("resolution")[1]
        self._capture = cv2.VideoCapture(0)

        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        image = self._get_image()
        image.save(parameters.get("path"))

        print("Save finished.")

        self.start()

    def stop(self):
        self.running = False

    def _get_image(self):
        ret, frame = self._capture.read()
        im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if self.rotated:
            im_rgb = cv2.rotate(im_rgb, cv2.ROTATE_180)
        return qimage2ndarray.array2qimage(im_rgb)

    def run(self):
        print("Starting camera....")
        self.running = True

        self._capture = cv2.VideoCapture(0)

        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)

        while self.running:
            self.frame_ready.emit(self._get_image())

        print("Exiting camera.")
        self._capture.release()
        self.stopped.emit()
