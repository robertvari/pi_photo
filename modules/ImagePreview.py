from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPainter, QImage
from PySide2.QtCore import QPoint, QThread, Signal
import cv2, time
import qimage2ndarray


class ImagePreview(QWidget):
    def __init__(self):
        super(ImagePreview, self).__init__()

        self._width = 640
        self._height = 480
        self.setMinimumSize(self._width, self._height)
        self.setMaximumSize(self._width, self._height)

        self.image = None

        self.worker = CaptureWorker(self._width, self._height)
        self.worker.finished.connect(self.set_image)
        self.worker.start()

    def set_image(self, image):
        self.image = image
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()


class ImageCapture(QThread):
    exited = Signal()

    def __init__(self):
        super(ImageCapture, self).__init__()
        self.path = None
        self._width = 2048
        self._height = 1536

    def set_size(self, width, height):
        self._width = width
        self._height = height

    def set_path(self, path):
        self.path = path

    def run(self):
        if not self.path:
            print("Path not set!")
            self.exited.emit()
            return

        print("Saving image...")
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)

        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        cv2.imwrite(self.path, frame)
        cap.release()
        print("Image saved.")
        self.exited.emit()


class CaptureWorker(QThread):
    finished = Signal(QImage)
    exited = Signal()

    def __init__(self, width, height):
        super(CaptureWorker, self).__init__()
        self.capturing = False
        self._width = width
        self._height = height

    def stop(self):
        self.capturing = False

    def run(self):
        print("Starting review.")
        self.capturing = True

        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)

        while self.capturing:
            ret, frame = cap.read()
            im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rotated = cv2.rotate(im_rgb, cv2.ROTATE_180)
            image = qimage2ndarray.array2qimage(rotated)

            self.finished.emit(image)

        print("Exiting preview.")
        cap.release()
        self.exited.emit()
