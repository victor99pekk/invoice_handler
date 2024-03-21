from GUI import DragDropWidget
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def main():
    app = QApplication(sys.argv)
    window = DragDropWidget()
    window.setWindowTitle("Faktura Sammanställare")
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


