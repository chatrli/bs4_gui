from PySide6 import QtCore, QtWidgets
import sys
import tags
from bs4 import BeautifulSoup as bs
import requests


class ScrapWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # URL field
        self.input_field = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("SCRAP")

        # URL row layout
        url_layout = QtWidgets.QHBoxLayout()
        url_label = QtWidgets.QLabel('URL: ')
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.input_field)

        # Add the URL row layout
        self.layout.addLayout(url_layout)

        # Radio buttons for choosing between HTML tags and CSS selectors
        self.radio_layout = QtWidgets.QHBoxLayout()
        self.html_radio = QtWidgets.QRadioButton('HTML Tags')
        self.css_radio = QtWidgets.QRadioButton('CSS Selectors')
        self.radio_group = QtWidgets.QButtonGroup(self)
        self.radio_group.addButton(self.html_radio)
        self.radio_group.addButton(self.css_radio)
        self.radio_layout.addWidget(self.html_radio)
        self.radio_layout.addWidget(self.css_radio)

        # Add the radio button layout
        self.layout.addLayout(self.radio_layout)

        # Select field
        self.select_label = QtWidgets.QLabel('Select Tag/Selector: ')

        self.select_combo = QtWidgets.QComboBox()
        if self.html_radio.isChecked():
            for i in tags.html_tags:
                self.select_combo.addItem(i)
        elif self.css_radio.isChecked():
            for i in tags.css_selectors:
                self.select_combo.addItem(i)

        # Add the select row layout
        select_layout = QtWidgets.QHBoxLayout()
        select_layout.addWidget(self.select_label)
        select_layout.addWidget(self.select_combo)

        # Add the select layout to the main layout
        self.layout.addLayout(select_layout)

        # Output label
        self.output_label = QtWidgets.QLabel()

        # Add the output label
        self.layout.addWidget(self.output_label)

        # Submit button
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        input_text = self.input_field.text()
        selected_option = self.select_combo.currentText()

        if self.html_radio.isChecked():
            selected_type = "HTML TAG"
        else:
            selected_type = "CSS SELECTOR"

        if input_text and selected_option:
            self.output_label.setText(
                f"URL: {input_text}, {selected_type}: {selected_option}")

        req = requests.get(input_text)
        soup = bs(req.content, 'html.parser').find_all(f'{selected_option}')
        print(soup)
        print(f"bs(req.content, 'html.parser').find_all(f'{selected_option}')")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = ScrapWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
