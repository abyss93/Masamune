from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow


class UI:

    def render(self, headers):
        x = headers
        rows = 0
        for i, v in enumerate(x):
            rows += len(v)

        app = QApplication([])

        window = QMainWindow()
        window.setWindowTitle('Orc')
        window.setWindowIcon(QIcon('../logo/orc.png'))
        window.setGeometry(100, 100, 500, 500)
        window.setWindowIcon(QIcon('../logo/orc.png'))
        table_widget = QTableWidget(window)
        window.setCentralWidget(table_widget)

        table_widget.setColumnCount(2)
        table_widget.setMinimumSize(500, 500)
        table_widget.setRowCount(rows)
        vertical_header = table_widget.verticalHeader()
        
        vertical_header.setVisible(False)

        r = 0
        for h in headers:
            table_widget.setItem(r, 0, QTableWidgetItem(h[0]))
            table_widget.setItem(r, 1, QTableWidgetItem(h[1]))
            r += 1

        table_widget.resizeColumnsToContents()
        table_widget.resizeRowsToContents()
        window.show()
        app.exec()
