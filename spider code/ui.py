import sys
from PyQt5 import QtCore,QtWidgets

app=QtWidgets.QApplication(sys.argv)
widget=QtWidgets.QWidget()
widget.resize(400,100)
widget.setWindowTitle("this is s demo for PyQt Widget.")
widget.show()

exit(app.exec_())