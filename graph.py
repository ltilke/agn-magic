import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

config = {
  "source": "OJ287",
  "wavelengths": {"V": "Purple",
                  "R": "Red",
                  },
  "files": {"C:/Users/lanat/OneDrive/Desktop/Astro/OJ 287/OJ287 Photometry V+R.csv": ["Point", "SRO20"],
            "C:/Users/lanat/OneDrive/Desktop/Astro/OJ 287/OJ287 V+R AAVSO.csv": ["Diamond", "AAVSO"],
            },
  "error bars": False,
  "legend": "Top Right"
}


class GraphDataframe:
    dataframe = pd.DataFrame
    wavelength = ""
    file = ""
    format_string = ""

    def __init__(self, dataframe, wavelength, file):
        self.dataframe = dataframe
        self.wavelength = wavelength
        self.file = file

        def make_format_string():
            markers = {"Point": ".",
                       "Circle": "o",
                       "Triangle": "v",
                       "Square": "s",
                       "Star": "*",
                       "Diamond": "d",
                       "Plus": "+",
                       "Cross": "x",
                       }
            colors = {"Red": "r",
                      "Yellow": "y",
                      "Green": "g",
                      "Cyan": "c",
                      "Blue": "b",
                      "Magenta": "m",
                      "Black": "k"
                      }

            marker = config["wavelengths"][self.wavelength]
            color = config["files"][self.file][0]

            return str(markers[marker] + colors[color])

        self.format_string = make_format_string()


def make_dataframes():
    dataframes = []
    for wavelength in config["wavelengths"]:
        for file in config["files"]:
            cols = [
                "Timestamp (JD)",
                "Filter",
                config["source"] + " : Magnitude (Centroid)"
            ]
            df = pd.read_csv(file, skipinitialspace=True, names=cols)
            clean_df = df.loc[df["Filter"] is wavelength]
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
    plt.figure()
    # for wavelength in config["wavelengths"]:
    #     plt.subplot()
    #     legend_loc = get_legend_location()
    #     if legend_loc is not "none":
    #         legend = plt.legend(loc=legend_loc)
    #     for df in dataframes:
    #         plt.plot(df, fmt=df.format_string)
    legend_location = get_legend_location()
    for wavelength in config["wavelengths"]:
        plt.subplot()
        for dataframe in dataframes:
            pass


make_dataframes()
