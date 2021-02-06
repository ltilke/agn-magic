import matplotlib.pyplot as plt
# from astropy.table import Table
import os
import json
import pandas as pd

with open("config.json") as json_file:
    config = json.load(json_file)


class GraphDataframe:
    dataframe = pd.DataFrame
    wavelength = ""
    file = os.path
    color = ""
    marker = ""
    size = 20
    alpha = 1

    def __init__(self, dataframe, wavelength, file):
        self.dataframe = dataframe
        self.wavelength = wavelength
        self.file = file

        markers = {"Point": ".",
                   "Circle": "o",
                   "Triangle": "v",
                   "Square": "s",
                   "Star": "*",
                   "Diamond": "d",
                   "Plus": "+",
                   "Cross": "x",
                   }
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

        if config["files"][self.file][2] is True:
            color = config["wavelengths"][self.wavelength]
        else:
            color = "Gray"
            self.size = 5
            self.alpha = 0.5
        marker = config["files"][self.file][0]

        self.color = colors[color]
        self.marker = markers[marker]


def make_dataframes():
    dataframes = []
    for wavelength in config["wavelengths"].keys():
        for file in config["files"].keys():
            if os.path.splitext(file)[1] == ".csv":
                cols = [
                    "Timestamp (JD)",
                    "Filter",
                    config["source"] + " : Magnitude (Centroid)",
                    config["source"] + " : Error"
                ]
                df = pd.read_csv(file, skipinitialspace=True, usecols=cols)
                df.insert(1, "Timestamp (MJD)", df["Timestamp (JD)"] - 2400000.5)

                clean_df = df.loc[df["Filter"] == wavelength]
                if not clean_df.empty:
                    dataframe = GraphDataframe(clean_df, wavelength, file)
                    dataframes.append(dataframe)
            elif os.path.splitext(file)[1] == ".lc":
                if "G" in config["wavelengths"]:
                    print(".lc files are not yet supported.")
                    # # @author: Nikolas Korzoun
                    # data = Table.read(file)
                    # date = data['START']
                    # date = (date / 60 / 60 / 24) + 2451910.5 - 2450000
                    # flux = data['FLUX_100_300000'] * 100000
                    # if config["error bars"]:
                    #     error = data['ERROR_100_300000'] * 100000
                    # else:
                    #     error = 0
                else:
                    del(config["files"][file])
            else:
                print("Unknown file type (" + os.path.splitext(file)[1] + ")")

    return dataframes


def get_legend_location():
    legends = {"Best": "best",
               "Top Left": "upper left",
               "Top Right": "upper right",
               "Bottom Left": "lower left",
               "Bottom Right": "lower right",
               }

    if config["legend"] in legends:
        return legends[config["legend"]]

    return "none"


def make_graph():
    dataframes = make_dataframes()
    wavelengths = []
    for df in dataframes:
        wavelengths.append(df.wavelength) if df.wavelength not in wavelengths else wavelengths

    fig, axs = plt.subplots(len(wavelengths), sharex=True)
    fig.suptitle(config["source"])

    for wavelength in wavelengths:
        ax_num = wavelengths.index(wavelength)
        for df in dataframes:
            if df.wavelength == wavelength:
                axs[ax_num].scatter(x=df.dataframe["Timestamp (MJD)"],
                                    y=df.dataframe[config["source"] + " : Magnitude (Centroid)"],
                                    s=df.size,
                                    color=df.color, marker=df.marker, alpha=df.alpha,
                                    label=config["files"][df.file][1] + " " + df.wavelength,
                                    )
                if config["error bars"] is True:
                    axs[ax_num].errorbar(x=df.dataframe["Timestamp (MJD)"],
                                         y=df.dataframe[config["source"] + " : Magnitude (Centroid)"],
                                         yerr=df.dataframe[config["source"] + " : Error"],
                                         color=df.color, alpha=df.alpha,
                                         linestyle="None"
                                         )
                axs[ax_num].set_xlabel("Timestamp (MJD)")
                axs[ax_num].set_ylabel("Magnitude (Centroid)")
                axs[ax_num].legend(loc=get_legend_location())
                axs[ax_num].invert_yaxis()
                axs[ax_num].figure.show()

    plt.show()


make_graph()
