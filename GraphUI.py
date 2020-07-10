import matplotlib.pyplot as plt
import numpy as np
import json


class GraphUI:

    def __init__(self):
        """Initialize the DataReceiver class."""

        self.DATAFILENAME = "covid-data.json"

        with open(self.DATAFILENAME, "r") as data_file:
            self.covid_data = json.load(data_file)

    def plot_single_country_deaths(self, country_abbr, color, number_of_days=21):
        """Plots the deaths data of a single country BUT DOES NOT CALL SHOW FUNCTION."""

        country_deaths_list, dates_list = [], []

        for country_data in self.covid_data[country_abbr.strip().upper()]["data"][-number_of_days:]:
            country_deaths_list.append(int(country_data["total_deaths"]))
            dates_list.append(country_data["date"])

        plt.plot(dates_list, country_deaths_list, color=color)

    def format_and_show_graph(self):
        """Rotates, sets the x and y labels and shows the graph."""

        plt.xlabel(f"Date")
        plt.ylabel("Number Of Deaths")

        plt.xticks(rotation=30, size=10)
        plt.show()


if __name__ == "__main__":
    GraphObj = GraphUI()
    GraphObj.plot_single_country_deaths("IND", (1, 0, 0), number_of_days=50)
    GraphObj.plot_single_country_deaths("CHN", (0, 1, 0), number_of_days=50)
    GraphObj.format_and_show_graph()
