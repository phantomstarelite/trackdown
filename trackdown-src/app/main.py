import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui import MainWindow

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("app/assets/trackdown.png"))

app.setStyleSheet("""
    QMainWindow {
        background-color: #121212;
        color: #e0e0e0;
    }
    QLineEdit, QComboBox, QTextEdit, QPushButton {
        background: #1f1f1f;
        border-radius: 8px;
        padding: 6px;
    }
    QPushButton:hover {
        background: #2a2a2a;
    }
""")



window = MainWindow()
window.show()
sys.exit(app.exec())
