from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
import sys

class ImageMarkerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Responsive Resim İşaretleme")
        self.setGeometry(100, 100, 800, 600)

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Görsel bileşenler
        self.label = QLabel("Bir resim yükleyin ve tıklayın")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Koordinat Giriş Alanları
        self.input_x = QLineEdit(self)
        self.input_x.setPlaceholderText("X Koordinatı")
        self.layout.addWidget(self.input_x)

        self.input_y = QLineEdit(self)
        self.input_y.setPlaceholderText("Y Koordinatı")
        self.layout.addWidget(self.input_y)

        # Düğmeler
        self.load_button = QPushButton("Resim Yükle", self)
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.mark_button = QPushButton("Konumu İşaretle", self)
        self.mark_button.clicked.connect(self.mark_location_from_input)
        self.layout.addWidget(self.mark_button)

        # Resim ve işaretleme için gerekli değişkenler
        self.image_path = None
        self.pixmap = None
        self.markers = []

    def load_image(self):
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(self, "Resim Yükle", "", "Image Files (*.png *.jpg *.bmp)")
        if self.image_path:
            self.pixmap = QPixmap(self.image_path)
            self.label.setPixmap(self.pixmap)
            self.markers = []  # Yeni resimde işaretleri sıfırla

    def mousePressEvent(self, event):
        if self.image_path and self.label.pixmap() and event.button() == Qt.LeftButton:
            label_x = self.label.x()
            label_y = self.label.y()
            x = event.x() - label_x
            y = event.y() - label_y
            self.input_x.setText(str(x))
            self.input_y.setText(str(y))
            self.mark_location(x, y)

    def mark_location(self, x, y):
        painter = QPainter(self.pixmap)
        pen = QPen(Qt.red)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawEllipse(x - 5, y - 5, 10, 10)
        painter.end()
        self.label.setPixmap(self.pixmap)

    def mark_location_from_input(self):
        try:
            x = int(self.input_x.text())
            y = int(self.input_y.text())
            self.mark_location(x, y)
        except ValueError:
            self.label.setText("Geçerli bir koordinat giriniz!")

# Uygulamayı çalıştır
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageMarkerApp()
    window.show()
    sys.exit(app.exec_())
