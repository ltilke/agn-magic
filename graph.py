import json
import os
import pandas as pd
import matplotlib.pyplot as plt


def get_color(color):
    colors = {"Red": "tab:red",
              "Orange": "tab:orange",
              "Yellow": "tab:yellow",
              "Olive": "tab:olive",
              "Green": "tab:green",
              "Cyan": "tab:cyan",
              "Blue": "tab:blue",
              "Purple": "tab:purple",
              "Pink": "tab:pink",
              "Brown": "tab:brown",
              "Gray": "tab:gray",
              }

    return colors[color]


def get_marker(marker):
    markers = {"Point": ".",
               "Circle": "o",
               "Triangle": "v",
               "Square": "s",
               "Star": "*",
               "Diamond": "d",
               "Plus": "+",
               "Cross": "x",
               }

    return markers[marker]


class DataSet:
    source = ""
    wavelength = ""
    file = ""

    filetype = ""

    telescope = ""
    marker = ""
    color = ""

    size = 20
    alpha = 1

    primary_source = False
    primary_telescope = False

    time_mjd = []
    y_data = []
    error = []

    label = ""

    is_valid = False

    def __init__(self, source, wavelength, file, config):
        self.source = source
        self.wavelength = wavelength
        self.file = file

        self.filetype = os.path.splitext(self.file)[1]

        self.telescope = config["files"][self.file][0]
        self.primary_telescope = config["files"][self.file][1]
        self.marker = get_marker(config["files"][self.file][2])

        self.color = get_color(config["wavelengths"][self.wavelength])

        if config["sources"].index(self.source) == 0:
            self.primary_source = True

        if not self.primary_telescope or not self.primary_source:
            self.color = "Gray"
            self.size = 5
            self.alpha = 0.5

        if self.filetype == ".csv":
            csv = pd.read_csv(file, skipinitialspace=True)
            csv = csv.loc[csv["Filter"] == self.wavelength]

            if (self.source + " : Magnitude (Centroid)") in csv:
                time_jd = csv["Timestamp (JD)"]
                time_mjd = [jd - 2450000 for jd in time_jd]
                self.time_mjd = time_mjd

                mag = csv[self.source + " : Magnitude (Centroid)"]
                self.y_data = mag

                error = csv[self.source + " : Error"]
                self.error = error

                self.is_valid = True

        elif self.filetype == ".lc":
            print(".lc files are not yet supported.")

        else:
            print("Unknown file type: " + self.filetype + ".")

        self.label = self.source + " " + self.telescope + " " + self.wavelength


def get_legend_location(config):
    legends = {"Best": "best",
               "Top Left": "upper left",
               "Top Right": "upper right",
               "Bottom Left": "lower left",
               "Bottom Right": "lower right",
               }

    if config["legend"] in legends:
        return legends[config["legend"]]

    return "none"


def make_plot(data: {}, config):

    if len(data) >= 1:
        # noinspection PyTypeChecker
        fig, axs = plt.subplots(len(data), sharex=True)
    else:
        print("No data found. Check source name.")

    ax_num = 0

    filters = ["B", "V", "R", "I", "G"]
    ordered_data = {k: data[k] for k in filters if k in data}

    for wavelength in ordered_data:
        if len(ordered_data) == 1:
            axs.grid(color="tab:gray", which="both", linestyle="--", linewidth=0.25)
            for dataset in ordered_data[wavelength]:
                axs.scatter(x=dataset.time_mjd,
                            y=dataset.y_data,
                            s=dataset.size,
                            color=dataset.color, marker=dataset.marker, alpha=dataset.alpha,
                            label=dataset.label,
                            )

                if config["error"]:
                    axs.errorbar(x=dataset.time_mjd,
                                 y=dataset.y_data,
                                 yerr=dataset.error,
                                 color=dataset.color, alpha=dataset.alpha,
                                 linestyle="None"
                                 )

                if dataset.filetype == ".csv":
                    axs.set_ylabel(wavelength + " [mag]")

                if get_legend_location(config) != "none":
                    axs.legend(loc=get_legend_location(config))

            axs.set_xlabel("MJD [JD - 2450000]")
            axs.figure.show()

        else:
            if config["grid"]:
                axs[ax_num].grid(color="tab:gray", which="major", linestyle="--", linewidth=0.25)
                axs[ax_num].grid(color="tab:gray", which="minor", linestyle="--", linewidth=0.08)
                axs[ax_num].minorticks_on()

            for dataset in ordered_data[wavelength]:
                axs[ax_num].scatter(x=dataset.time_mjd,
                                    y=dataset.y_data,
                                    s=dataset.size,
                                    color=dataset.color, marker=dataset.marker, alpha=dataset.alpha,
                                    label=dataset.label,
                                    )

                if config["error"]:
                    axs[ax_num].errorbar(x=dataset.time_mjd,
                                         y=dataset.y_data,
                                         yerr=dataset.error,
                                         color=dataset.color, alpha=dataset.alpha,
                                         linestyle="None"
                                         )

                if dataset.filetype == ".csv":
                    axs[ax_num].set_ylabel(wavelength + " [mag]")

                if get_legend_location(config) != "none":
                    axs[ax_num].legend(loc=get_legend_location(config))

            axs[ax_num].set_xlabel("MJD [JD - 2450000]")
            axs[ax_num].figure.show()
            ax_num += 1

    for ax in range(ax_num):
        if "[mag]" in axs[ax].get_ylabel():
            axs[ax].invert_yaxis()
    plt.subplots_adjust(hspace=0)
    plt.show()


def main(config_file):
    with open(config_file) as json_file:
        config = json.load(json_file)

    data = {}

    for wavelength in config["wavelengths"]:
        data[wavelength] = []
        for source in config["sources"]:
            for file in config["files"]:
                dataset = DataSet(source, wavelength, file, config)
                if dataset.time_mjd:  # change to if dataset.is_valid: (not working?) !TODO
                    data[wavelength].append(dataset)

    cleaned_data = {k: v for k, v in data.items() if len(v) != 0}
    make_plot(cleaned_data, config)
