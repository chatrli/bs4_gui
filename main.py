from PySide6 import QtCore, QtWidgets
import sys
import tags
import core


class ScrapWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # URL field
        self.input_field = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("SCRAP")

        # URL layout
        url_layout = QtWidgets.QHBoxLayout()
        url_label = QtWidgets.QLabel('URL: ')
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.input_field)

        # Add the URL layout
        self.layout.addLayout(url_layout)

        # Radio buttons for choosing between HTML tags and CSS selectors
        self.radio_layout = QtWidgets.QHBoxLayout()
        self.html_radio = QtWidgets.QRadioButton('HTML Tags')
        self.html_radio.setChecked(True)
        self.css_radio = QtWidgets.QRadioButton('CSS Selectors')
        self.radio_group = QtWidgets.QButtonGroup(self)
        self.radio_group.addButton(self.html_radio)
        self.radio_group.addButton(self.css_radio)
        self.radio_layout.addWidget(self.html_radio)
        self.radio_layout.addWidget(self.css_radio)

        # Add the radio button layout
        self.layout.addLayout(self.radio_layout)

        # Tag select field
        self.select_label = QtWidgets.QLabel('Select Tag/Selector:')
        self.select_combo = QtWidgets.QComboBox()
        if self.html_radio.isChecked():
            for i in tags.html_tags:
                self.select_combo.addItem(i)
        elif self.css_radio.isChecked():
            for i in tags.css_selectors:
                self.select_combo.addItem(i)

        # Add the tag select layout
        select_layout = QtWidgets.QHBoxLayout()
        select_layout.addWidget(self.select_label)
        select_layout.addWidget(self.select_combo)

        # Add the tag select layout to the main layout
        self.layout.addLayout(select_layout)

        # Input field for CSS Selector
        self.css_input_label = QtWidgets.QLabel('CSS Selector:')
        self.css_input_field = QtWidgets.QLineEdit()
        self.css_input_label.hide()
        self.css_input_field.hide()

        # Add CSS Selector input layout
        css_input_layout = QtWidgets.QHBoxLayout()
        css_input_layout.addWidget(self.css_input_label)
        css_input_layout.addWidget(self.css_input_field)
        self.layout.addLayout(css_input_layout)

        # Search select field
        self.search_label = QtWidgets.QLabel('Filters:')
        self.search_combo = QtWidgets.QComboBox()
        for i in tags.filters:
            self.search_combo.addItem(i)

        # Add search select layout
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_combo)

        # Add search select layout to the main layout
        self.layout.addLayout(search_layout)

        # Output label
        self.output_label = QtWidgets.QLabel()

        # Add the output label
        self.layout.addWidget(self.output_label)

        # Submit button
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)

        # Output text widget
        self.output_text = QtWidgets.QTextEdit()
        self.layout.addWidget(self.output_text)
        self.output_text.setReadOnly(True)

        # Connect radio buttons to slot
        self.html_radio.toggled.connect(self.update_select_combo)
        self.css_radio.toggled.connect(self.update_select_combo)
        self.css_radio.toggled.connect(self.toggle_css_input)
        self.css_radio.toggled.connect(self.toggle_filter_elements)

    @QtCore.Slot()
    def magic(self):
        input_text = self.input_field.text()
        selected_option = self.select_combo.currentText()
        selected_filter = self.search_combo.currentText()

        if self.html_radio.isChecked():
            output = core.scrap_with_filter(input_text, selected_filter, selected_option)
        elif self.css_radio.isChecked():
            css_selector = self.css_input_field.text()
            output = core.scrap_with_css(input_text, selected_option, css_selector)
        self.output_text.setPlainText(str(output))

    # Dynamically populate select_combo
    @QtCore.Slot(bool)
    def update_select_combo(self, checked):
        self.select_combo.clear()
        if checked and self.html_radio.isChecked():
            for i in tags.html_tags:
                self.select_combo.addItem(i)
        elif checked and self.css_radio.isChecked():
            for i in tags.css_selectors:
                self.select_combo.addItem(i)

    @QtCore.Slot(bool)
    def toggle_css_input(self, checked):
        self.css_input_label.setVisible(checked)
        self.css_input_field.setVisible(checked)

    # Slot to toggle visibility of filter label and combo box
    @QtCore.Slot(bool)
    def toggle_filter_elements(self, checked):
        self.search_label.setVisible(not checked)
        self.search_combo.setVisible(not checked)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = ScrapWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
