AGN Magic - by Lana Tilke
Last Updated: March 16, 2021

How to Use:
    Essentially, you provide the input to the GUI, and the GUI writes that input to a config.json file, which is then
    fed into the graphing application.

    .csv
        Required headers:   source + " : Magnitude (Centroid)"
                            source + " : Error"
                            "Timestamp (JD)"

    GUI
        List source names exactly as they appear in your data files, and if you would like to list multiple,
        separate each source with a ", ".

        Toggle whichever filter bands you'd like, and assign a plotting color in the dropdown menu.

        Click "Select Files," then load in however many files you want. Then, fill out the "Name" section,
        with the name you'd like to assign to the telescope (for example, "SRO20," or even "Nina"). Then, pick
        the symbol you'd like to be used as a datapoint marker in the plot. Finally, the "Highlight" toggles
        whether or not a file should be used as a "primary telescope." Anything that is not a "primary telescope"
        will have its points on the plot grayed out. A good use of this, for example, is highlighting the file for
        SRO20 data, but not highlighting the file for AAVSO data, so that in publishing we can show that our data
        does follow the larger set, while remaining clear about which data is ours and which is not.

        Toggle whether or not you'd like to add a grid.

        Toggle whether or not you'd like to add error bars.

        Pick where you would like the legend to be located, or "None."

        Create Graph!

        "Reload Config" allows you to open the GUI, press that button, and the GUI will be populated with whatever
        the last sets of inputs were. This is great for saving time while playing around with different options.

    config.json
        {
          "sources": [
            "source1",
            "source2"
          ],

          "wavelengths": {
            "WL1": "Color1",
            "WL2": "Color2"
          },

          "files": {
            "C:\\*\\file1.csv": ["Telescope1", true/false, "Symbol1"],
            "C:\\*\\file2.csv": ["Telescope2", true/false, "Symbol2"]
          },

          "grid": true/fals,
          "error": true/fals,
          "legend": "LegendLocation"
        }

        Note: the true/false in config["files"][file][1] is the indicator for whether or not that file is highlighted
        / a "primary telescope."
