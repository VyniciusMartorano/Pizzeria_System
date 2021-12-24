from sistema.functions import Functions
from PyQt5.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)
janela = Functions()
janela.show()
sys.exit(app.exec_())