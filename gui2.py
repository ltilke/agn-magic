import sys

import json
from graph import main as graph_main
from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QFileDialog,
    QTableWidget,
    QHeaderView
)


class SourceWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.sources_line = QLineEdit()
        layout.addWidget(self.sources_line)


class FilterWidget(QWidget):
    def __init__(self):
        super().__init__()
        outer_layout = QHBoxLayout()
        self.setLayout(outer_layout)

        color_options = ["Red", "Orange", "Yellow", "Olive", "Green", "Cyan", "Blue", "Purple", "Pink", "Brown", "Gray"]

        wavelengths = [["B", color_options.index("Blue")], ["V", color_options.index("Green")],
                       ["R", color_options.index("Red")], ["I", color_options.index("Gray")],
                       ["G (Unavailable)", color_options.index("Purple")]]

        self.wavelength_groups = {}

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
            self.wavelength_groups[wl_groupbox.title()] = [wl_groupbox, wl_combobox]


class FilesWidget(QWidget):
    files = {}

    def __init__(self):
        super().__init__()
        outer_layout = QVBoxLayout()
        self.setLayout(outer_layout)

        self.file_table = QTableWidget()
        self.file_table.setColumnCount(4)
        self.file_table.setHorizontalHeaderLabels(["File", "Name", "Symbol", "Highlight"])
        file_table_header = self.file_table.horizontalHeader()
        file_table_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        file_table_header.setSectionResizeMode(1, QHeaderView.Stretch)
        file_table_header.setSectionResizeMode(2, QHeaderView.Stretch)
        file_table_header.setSectionResizeMode(3, QHeaderView.Stretch)

        select_files_button = QPushButton("Select Files")
        select_files_button.clicked.connect(self.file_dialog)

        outer_layout.addWidget(self.file_table)
        outer_layout.addWidget(select_files_button)

    def file_dialog(self):
        dialog = QFileDialog()
        file_names, _ = dialog.getOpenFileNames(filter="Data Files (*.csv *.lc)")
        if file_names:
            for file_name in file_names:
                if file_name not in self.files:
                    self.add_file(file_name)
                    self.make_row(file_name)

    def make_row(self, file):
        row_count = self.file_table.rowCount()
        self.file_table.insertRow(row_count)
        self.file_table.setCellWidget(row_count, 0, QLabel(file))
        self.file_table.setCellWidget(row_count, 1, self.files[file][0])
        self.file_table.setCellWidget(row_count, 2, self.files[file][1])
        self.file_table.setCellWidget(row_count, 3, self.files[file][2])

    def add_file(self, file):
        telescope_line = QLineEdit()
        highlight_check = QCheckBox()
        symbols_combobox = QComboBox()
        symbols_combobox_options = ["Point", "Circle", "Triangle", "Square", "Star", "Diamond",
                                    "Plus", "Cross"]
        symbols_combobox.addItems(symbols_combobox_options)
        symbols_combobox.setCurrentIndex(0)
        self.files[file] = [telescope_line, symbols_combobox, highlight_check]


class GridWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.grid_check = QCheckBox("Add Grid?")
        layout.addWidget(self.grid_check)


class ErrorWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.error_check = QCheckBox("Add Error Bars?")
        layout.addWidget(self.error_check)


class LegendWidget(QWidget):
    def __init__(self):
        super().__init__()
        legend_options = ["Best", "Top Left", "Top Right", "Bottom Left", "Bottom Right", "None"]
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.legend_combo = QComboBox()
        self.legend_combo.addItems(legend_options)
        self.legend_combo.setCurrentIndex(0)
        layout.addWidget(self.legend_combo)
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AGN Magic!")

        form_layout = QFormLayout()

        self.sources_line = SourceWidget()
        self.filter_widget = FilterWidget()
        self.files_widget = FilesWidget()
        self.grid_check = GridWidget()
        self.error_check = ErrorWidget()
        self.legend_combo = LegendWidget()
        self.create_graph_button = QPushButton("Create Graph")

        form_layout.addRow("Source(s):", self.sources_line)
        form_layout.addRow("Filter(s):", self.filter_widget)
        form_layout.addRow("Load File(s):", self.files_widget)
        form_layout.addRow("Grid:", self.grid_check)
        form_layout.addRow("Error:", self.error_check)
        form_layout.addRow("Legend:", self.legend_combo)
        form_layout.addRow(self.create_graph_button, QLabel(""))

        self.setLayout(form_layout)


class Controller:
    def __init__(self, view):
        def model():
            self.make_graph()

        self.view = view
        self.view.create_graph_button.clicked.connect(model)

    def write_json(self):
        wavelengths = self.view.filter_widget.wavelength_groups
        checked_wavelengths = {}
        for wl in wavelengths:
            if wavelengths[wl][0].isChecked():
                checked_wavelengths[wl] = str(wavelengths[wl][1].currentText())
        files = self.view.files_widget.files
        files_info = {}
        for file in files:
            files_info[file] = []
            files_info[file].append(files[file][0].text())
            files_info[file].append(files[file][2].isChecked())
            files_info[file].append(files[file][1].currentText())

        out_dict = {"sources": self.view.sources_line.sources_line.text().split(", "),
                    "grid": self.view.grid_check.grid_check.isChecked(),
                    "error": self.view.error_check.error_check.isChecked(),
                    "legend": self.view.legend_combo.legend_combo.currentText(),
                    "wavelengths": checked_wavelengths,
                    "files": files_info
                    }

        with open("config.json", "w") as output:
            json.dump(out_dict, output)

    def make_graph(self):
        self.write_json()
        graph_main("config.json")
        self.view.close()


def main():
    app = QApplication(sys.argv)
    view = Window()
    view.show()
    Controller(view=view)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
