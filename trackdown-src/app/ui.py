from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit,
    QMessageBox, QProgressBar, QComboBox, QFileDialog
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont
from downloader import download_track
import os


class Worker(QThread):
    log = pyqtSignal(str)
    done = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, url, bitrate, fmt, folder):
        super().__init__()
        self.url = url
        self.bitrate = bitrate
        self.fmt = fmt
        self.folder = folder

    def run(self):
        try:
            download_track(
                self.url, self.bitrate, self.fmt, self.folder, self.log.emit
            )
            self.done.emit()
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Track Downloader")
        self.setMinimumSize(620, 520)
        self.setAcceptDrops(True)

        base = QWidget()
        root = QVBoxLayout(base)
        root.setSpacing(14)
        root.setContentsMargins(20, 20, 20, 20)

        # Header
        title = QLabel("🎵 Spotify Track Downloader")
        title.setFont(QFont("Sans Serif", 16, QFont.Weight.Bold))
        root.addWidget(title)

        # URL Input
        self.url = QLineEdit()
        self.url.setPlaceholderText("Paste or drag Spotify track URL here")
        self.url.setMinimumHeight(38)
        root.addWidget(self.url)

        # Settings Row
        settings = QHBoxLayout()

        self.bitrate = QComboBox()
        self.bitrate.addItems(["320k", "192k", "128k"])

        self.format = QComboBox()
        self.format.addItems(["mp3", "m4a", "flac"])

        self.folder = QLineEdit(os.path.expanduser("~/Music/Library"))
        browse = QPushButton("Browse")
        browse.clicked.connect(self.pick_folder)

        settings.addWidget(QLabel("Bitrate"))
        settings.addWidget(self.bitrate)
        settings.addWidget(QLabel("Format"))
        settings.addWidget(self.format)
        settings.addWidget(self.folder)
        settings.addWidget(browse)

        root.addLayout(settings)

        # Download Button
        self.download = QPushButton("Download Track")
        self.download.setMinimumHeight(42)
        self.download.clicked.connect(self.start_download)
        root.addWidget(self.download)

        # Status
        self.status = QLabel("Idle")
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setRange(0, 0)

        root.addWidget(self.status)
        root.addWidget(self.progress)

        # Logs
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setStyleSheet("font-family: monospace;")
        root.addWidget(self.logs)

        self.setCentralWidget(base)

    # Drag & Drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.url.setText(event.mimeData().text())

    def pick_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.folder.setText(path)

    def start_download(self):
        if not self.url.text():
            QMessageBox.warning(self, "Missing URL", "Paste a Spotify track URL")
            return

        self.logs.clear()
        self.status.setText("Downloading…")
        self.progress.setVisible(True)
        self.download.setEnabled(False)

        self.worker = Worker(
            self.url.text(),
            self.bitrate.currentText(),
            self.format.currentText(),
            self.folder.text()
        )

        self.worker.log.connect(self.logs.append)
        self.worker.done.connect(self.finish)
        self.worker.error.connect(self.fail)
        self.worker.start()

    def finish(self):
        self.status.setText("Completed 🎉")
        self.progress.setVisible(False)
        self.download.setEnabled(True)
        QMessageBox.information(self, "Done", "Track downloaded successfully!")

    def fail(self, msg):
        self.status.setText("Failed ❌")
        self.progress.setVisible(False)
        self.download.setEnabled(True)
        QMessageBox.critical(self, "Error", msg)
