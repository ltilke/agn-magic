import matplotlib as plt
import numpy as np

config = {
  "sources": ["OJ287"],
  "wavelengths": {"V": "Purple",
                  "R": "Red"
                  },
  "files": {"C:/Users/lanat/OneDrive/Desktop/Astro/OJ 287/OJ287 Photometry V+R.csv": "Point",
            "C:/Users/lanat/OneDrive/Desktop/Astro/OJ 287/OJ287 V+R AAVSO.csv": "Diamond"},
  "error bars": True,
  "legend": "Top Right",
  "aspect ratio": "Portrait"
}


def make_graph():
    data = []
    plots = []
    for file in config["files"]:
        for source in config["sources"]:
            data_from_csv = np.genfromtxt(file, delimeter=",", names=["Timestamp (JD)",
                                                                      source + " : Magnitude (Centroid)"])
            data.append(data_from_csv)
            plots.append(plt.plot(data_from_csv["Timestamp (JD)"], data_from_csv[source + " : Magnitude (Centroid)"]))
    for plot in plots:
        plot.show()
