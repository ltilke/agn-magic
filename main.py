import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QPushButton,
    QWidget,
)


class WavelengthWidget(QWidget):
    def __init__(self):
        super().__init__()
        outer_layout = QHBoxLayout()
        self.setLayout(outer_layout)

        color_options = ["Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Purple", "Pink", "Brown", "Gray"]

        wavelengths = [["B", color_options.index("Blue")], ["V", color_options.index("Green")],
                       ["R", color_options.index("Red")], ["I", color_options.index("Gray")],
                       ["G", color_options.index("Purple")]]

        wavelength_groups = []

        for wl in wavelengths:
            wl_layout = QVBoxLayout()
            wl_groupbox = QGroupBox(wl[0])
            wl_groupbox.setCheckable(True)
            wl_groupbox.setChecked(False)
            outer_layout.addWidget(wl_groupbox)
            wl_combobox = QComboBox()
            wl_combobox.addItems(color_options)
            wl_combobox.setCurrentIndex(wl[1])
            wl_layout.addWidget(wl_combobox)
            wl_groupbox.setLayout(wl_layout)
            wavelength_groups.append(wl_groupbox)


class DataWidget(QWidget):
    file_list = {}

    def __init__(self):
        super().__init__()
        outer_layout = QVBoxLayout()
        self.setLayout(outer_layout)
        file_table = QTableWidget()
        file_table.setColumnCount(4)
        file_table.setHorizontalHeaderLabels(['File', 'Telescope', 'Symbol', 'Remove'])
        outer_layout.addWidget(file_table)

        def file_dialog():
            dialog = QFileDialog().getOpenFileNames(self, 'Select Files', '', 'Data Files (*.csv *.lc)')
            if dialog.exec_():
                filenames = dialog.selectedFiles()
                for filename in filenames:
                    self.file_list += filename
            print(self.file_list)

        select_files_button = QPushButton("Select Files")
        select_files_button.clicked.connect(file_dialog)
        outer_layout.addWidget(select_files_button)

        def build_rows(file_paths):
            for fp in file_paths:
                row_position = file_table.rowCount()
                file_table.insertRow(row_position)
                telescope_line_edit = QLineEdit()
                symbol_options = ['Point', 'Circle', 'Square', 'Star', 'Plus']
                symbol_combobox = QComboBox()
                symbol_combobox.addItems(symbol_options)
                remove_button = QPushButton("Remove")
                if fp in self.file_list:
                    symbol_combobox.setCurrentText(str(self.file_list[fp["Symbol"]]))

                file_table.setItem(row_position, 0, QTableWidgetItem(str(fp)))
                file_table.setItem(row_position, 1, QTableWidgetItem(telescope_line_edit))
                file_table.setItem(row_position, 2, QTableWidgetItem(symbol_combobox))
                file_table.setItem(row_position, 3, QTableWidgetItem(remove_button))

        def save_info():
            num_rows = file_table.rowCount()
            for row in num_rows:
                file_name = str(file_table.item(row, 0))
                telescope_text = str(file_table.item(row, 1).text()) if file_table.item(row, 1) is QLineEdit \
                    else ""
                symbol_choice = str(file_table.item(row, 1).currentText()) if file_table.item(row, 2) is QComboBox \
                    else ""
                file_dict = {"Telescope": telescope_text, "Symbol": symbol_choice}
                self.file_list[file_name] = file_dict

        def build_table():
            pass

        def delete_row(row):
            file_name = str(file_table.item(row, 0))
            del self.file_list[file_name]
            build_table()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AGN Magic!")

        sources_line_edit = QLineEdit()
        sources_line_edit.setPlaceholderText("Sources are comma-space delimited. "
                                             "Make sure your text matches your data.")

        wavelength_widget = WavelengthWidget()

        data_widget = DataWidget()

        error_bars_checkbox = QCheckBox()

        legend_combobox = QComboBox()
        legend_combobox_options = ["Best", "Top Left", "Top Right", "Bottom Left", "Bottom Right", "None"]
        legend_combobox.addItems(legend_combobox_options)
        legend_combobox.setCurrentIndex(0)

        aspect_ratio_combobox = QComboBox()
        aspect_ratio_combobox_options = ["Portrait", "Landscape", "Square"]
        aspect_ratio_combobox.addItems(aspect_ratio_combobox_options)
        aspect_ratio_combobox.setCurrentIndex(0)

        form_layout = QFormLayout()

        form_layout.addRow("Source(s):", sources_line_edit)
        form_layout.addRow("Wavelengths:", wavelength_widget)
        form_layout.addRow("Add Data:", data_widget)
        form_layout.addRow("Error Bars:", error_bars_checkbox)
        form_layout.addRow("Legend:", legend_combobox)
        form_layout.addRow("Aspect Ratio:", aspect_ratio_combobox)
        form_layout.addRow(QPushButton("Create Graph"), QLabel(""))

        self.setLayout(form_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
