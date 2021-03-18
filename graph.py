# Lana Joan Tilke
# Connecticut College Astrophysics Class of 2023
# AGN Magic!

#                 ,,__
#       ..  ..   / o._)
#      /--'/--\  \-'||
#     /        \_/ / |
#   .'\  \__\  __.'.'
#     )\ |  )\ |
#    // \\ // \\
#   ||_  \\|_  \\_
#   '--' '--'' '--'

import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from astropy.table import Table


def get_color(color):  # returns the string that matplotlib understands, from the more human-readable input
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


def get_marker(marker):  # returns the string that matplotlib understands, from the more human-readable input
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


def get_legend_location(config):  # returns the string that matplotlib understands, from the more human-readable input
    legends = {"Best": "best",
               "Top Left": "upper left",
               "Top Right": "upper right",
               "Bottom Left": "lower left",
               "Bottom Right": "lower right",
               "None": "none"
               }

    return legends[config["legend"]]


class DataSet:  # a DataSet is created for each file, each source, and each wavelength combination
    source = ""  # DataSet's source name
    wavelength = ""  # DataSet's wavelength
    file = ""  # DataSet's file

    filetype = ""  # file extension, either .csv or .lc

    telescope = ""  # file's telescope nickname, ie: SRO20 or AAVSO
    marker = ""  # the marker used for the telescope in the graph, as selected within the GUI
    color = ""  # the color used for the wavelength in the graph, as selected within the GUI

    size = 20  # the marker's size
    alpha = 1  # the marker's transparency (1 = opaque, 0 = transparent)

    primary_source = False  # whichever source is listed first is considered the "primary source"
    primary_telescope = False  # if the "highlight" box is checked, it is a "primary telescope"

    time_mjd = []  # data column for time
    y_data = []  # data column for magnitude
    error = []  # data column for error

    label = ""  # the DataSet's label for the graph legend

    is_valid = False

    # initializer, takes source, wavelength, file, and the config json as inputs
    def __init__(self, source, wavelength, file, config):
        self.source = source
        self.wavelength = wavelength
        self.file = file

        self.filetype = os.path.splitext(self.file)[1]  # gets the file extension

        self.telescope = config["files"][self.file][0]  # gets telescope name from config
        self.primary_telescope = config["files"][self.file][1]  # gets value from boolean in config
        self.marker = get_marker(config["files"][self.file][2])  # gets marker from config
        self.color = get_color(config["wavelengths"][self.wavelength])  # gets color from config

        if config["sources"].index(self.source) == 0:  # checks to see if its source was the first listed
            self.primary_source = True  # if it was listed first, it is a "primary source"

        # anything that's not a primary source or telescope is set to gray, small, and 50% opacity
        if not self.primary_telescope or not self.primary_source:
            self.color = "Gray"
            self.size = 5
            self.alpha = 0.5

        if self.filetype == ".csv":  # here's what it does if the file is a .csv
            csv = pd.read_csv(file, skipinitialspace=True)  # reads the csv into a pandas dataframe
            csv = csv.loc[csv["Filter"] == self.wavelength]  # filters the csv for only the dataset's wavelength

            if (self.source + " : Magnitude (Centroid)") in csv:  # checks if source is in file
                time_jd = csv["Timestamp (JD)"]
                time_mjd = [jd - 2450000 for jd in time_jd]  # converts source's timestamp column to MJD
                self.time_mjd = time_mjd   # sets the time array to the MJD array

                mag = csv[self.source + " : Magnitude (Centroid)"]
                self.y_data = mag  # sets the y data array to the source's mag column

                error = csv[self.source + " : Error"]
                self.error = error  # sets the error array to the source's error column
                self.is_valid = True

        elif self.filetype == ".lc":  # special thanks to Nik Korzoun, adapted from AGN Wizard into AGN Magic
            if self.wavelength == "G":
                data = Table.read(file)
                time = data['START']
                time_mjd = (time / 60 / 60 / 24) + 2451910.5 - 2450000
                self.time_mjd = time_mjd
                raw_flux = data['FLUX_100_300000']
                flux = raw_flux * 100000
                self.y_data = flux
                self.error = data['ERROR_100_300000'] * 100000
                self.is_valid = True

        else:  # unrecognized file type, just in case
            print("Unknown file type: " + self.filetype + ".")

        self.label = self.source + " " + self.telescope  # creates label for legend


def make_plot(data: {}, config):  # this is what actually makes the plot, takes a dictionary of wavelength: DataSets
    if len(data) >= 1:  # checks if there is actually data to graph
        # noinspection PyTypeChecker
        fig, axs = plt.subplots(len(data), sharex=True)

        ax_num = 0

        filters = ["B", "V", "R", "I", "G"]
        ordered_data = {k: data[k] for k in filters if k in data}  # makes sure that subplots are stacked consistently

        for wavelength in ordered_data:
            if len(ordered_data) == 1:  # if there is only one plot to graph
                if config["grid"]:  # adds grid if true in config
                    axs.grid(color="tab:gray", which="major", linestyle="--", linewidth=0.25)
                    axs.grid(color="tab:gray", which="minor", linestyle="--", linewidth=0.15)
                    axs.minorticks_on()

                for dataset in ordered_data[wavelength]:  # creates a scatter plot for the wavelength's DataSets
                    axs.scatter(x=dataset.time_mjd,
                                y=dataset.y_data,
                                s=dataset.size,
                                color=dataset.color, marker=dataset.marker, alpha=dataset.alpha,
                                label=dataset.label,
                                )

                    if config["error"]:  # adds error bars if true in config
                        axs.errorbar(x=dataset.time_mjd,
                                     y=dataset.y_data,
                                     yerr=dataset.error,
                                     color=dataset.color, alpha=dataset.alpha,
                                     linestyle="None"
                                     )

                    if dataset.filetype == ".csv":  # for a csv file, y data is measured in mag
                        axs.set_ylabel(wavelength + " [mag]")

                    if dataset.filetype == ".lc":  # units for a lc file
                        axs.set_ylabel(r"Gamma$\ [10^{-5}\ ph\ s^{-1}\ cm^{-2}]$")

                    if get_legend_location(config) != "none":  # sets the legend location from config
                        axs.legend(loc=get_legend_location(config))

                axs.set_xlabel("MJD [JD - 2450000]")  # x axis label
                axs.figure.show()  # shows graph

            else:  # if there's more than one plot to graph, axs --> axs[ax_num], and ax_num increments
                if config["grid"]:  # adds grid if true in config
                    axs[ax_num].grid(color="tab:gray", which="major", linestyle="--", linewidth=0.25)
                    axs[ax_num].grid(color="tab:gray", which="minor", linestyle="--", linewidth=0.15)
                    axs[ax_num].minorticks_on()

                for dataset in ordered_data[wavelength]:  # creates a scatter plot for the wavelength's DataSets
                    axs[ax_num].scatter(x=dataset.time_mjd,
                                        y=dataset.y_data,
                                        s=dataset.size,
                                        color=dataset.color, marker=dataset.marker, alpha=dataset.alpha,
                                        label=dataset.label,
                                        )

                    if config["error"]:  # adds error bars if true in config
                        axs[ax_num].errorbar(x=dataset.time_mjd,
                                             y=dataset.y_data,
                                             yerr=dataset.error,
                                             color=dataset.color, alpha=dataset.alpha,
                                             linestyle="None"
                                             )

                    if dataset.filetype == ".csv":  # for a csv file, y data is measured in mag
                        axs[ax_num].set_ylabel(wavelength + " [mag]")

                    if dataset.filetype == ".lc":  # units for a lc file
                        axs[ax_num].set_ylabel(r"Gamma$\ [10^{-5}\ ph\ s^{-1}\ cm^{-2}]$")

                    if get_legend_location(config) != "none":  # sets the legend location from config
                        axs[ax_num].legend(loc=get_legend_location(config))

                axs[ax_num].set_xlabel("MJD [JD - 2450000]")  # x axis label
                axs[ax_num].figure.show()  # shows graph
                ax_num += 1  # increments ax_num

        for ax in range(ax_num):  # inverts the y axis for any graphs measured in mag
            if "[mag]" in axs[ax].get_ylabel():
                axs[ax].invert_yaxis()

        plt.subplots_adjust(hspace=0)  # gets rid of gap between subplots
        plt.show()  # shows plot

    else:  # prints an error message if there's nothing to graph
        print("No data found! Check source name.")


def main(config_file):  # main, is fed config file from gui.py
    with open(config_file) as json_file:  # opens config file
        config = json.load(json_file)

    data = {}

    for wavelength in config["wavelengths"]:  # for every wavelength selected, adds a key to data dictionary
        data[wavelength] = []
        for source in config["sources"]:  # for every source in source list
            for file in config["files"]:  # for every file in file list
                dataset = DataSet(source, wavelength, file, config)  # creates a DataSet
                if dataset.is_valid:  # checks to make sure we're only plotting valid DataSets
                    data[wavelength].append(dataset)

    # gets rid of any wavelengths that were selected but have no data
    cleaned_data = {k: v for k, v in data.items() if len(v) != 0}
    make_plot(cleaned_data, config)  # makes the plot!
