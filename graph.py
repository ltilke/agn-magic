import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

config = {
  "source": "OJ287",
  "wavelengths": {"V": "Purple",
                  "R": "Red",
                  },
  "files": {os.path.normpath("C:/Users/lanat/OneDrive/Desktop/Astro/OJ 287/OJ287 Photometry V+R.csv"): ["Point", "SRO20"],
            os.path.normpath("C:/Users/lanat/OneDrive/Desktop/Astro/OJ 287/OJ287 AAVSO.csv"): ["Diamond", "AAVSO"],
            },
  "error bars": False,
  "legend": "Top Right"
}


class GraphDataframe:
    dataframe = pd.DataFrame
    wavelength = ""
    file = os.path
    color = ""
    marker = ""

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

        color = config["wavelengths"][self.wavelength]
        marker = config["files"][self.file][0]

        self.color = colors[color]
        self.marker = markers[marker]


def make_dataframes():
    dataframes = []
    for wavelength in config["wavelengths"].keys():
        for file in config["files"].keys():
            cols = [
                "Timestamp (JD)",
                "Filter",
                config["source"] + " : Magnitude (Centroid)"
            ]
            df = pd.read_csv(file, skipinitialspace=True, usecols=cols)

            clean_df = df.loc[df["Filter"] == wavelength]
            if not clean_df.empty:
                dataframe = GraphDataframe(clean_df, wavelength, file)
                dataframes.append(dataframe)

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
                axs[ax_num].scatter(x=df.dataframe["Timestamp (JD)"],
                                    y=df.dataframe[config["source"] + " : Magnitude (Centroid)"],
                                    s=20,
                                    color=df.color, marker=df.marker,
                                    label=config["files"][df.file][1] + " " + df.wavelength,
                                    )
                axs[ax_num].set_xlabel("Timestamp (JD)")
                axs[ax_num].set_ylabel("Magnitude (Centroid)")
                axs[ax_num].legend()
                axs[ax_num].invert_yaxis()
                axs[ax_num].figure.show()

    plt.show()


make_graph()
