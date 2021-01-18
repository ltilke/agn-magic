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
        file_table.setHorizontalHeaderLabels(["File", "Telescope", "Symbol", "Remove"])
        outer_layout.addWidget(file_table)

        def file_dialog():
            dialog = QFileDialog()
            file_names, _ = dialog.getOpenFileNames(filter="Data Files (*.csv *.lc)")
            if file_names:
                print(file_names)

        select_files_button = QPushButton("Select Files")
        select_files_button.clicked.connect(file_dialog)
        outer_layout.addWidget(select_files_button)


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