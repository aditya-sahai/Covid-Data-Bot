from datetime import date
from calendar import month_name
import matplotlib.pyplot as plt
import numpy as np
import json


class GraphUI:

    def __init__(self):
        """Initialize the DataReceiver class."""

        self.day_today = date.today().day
        self.current_month = month_name[date.today().month]
        self.current_year = date.today().year
        self.DATAFILENAME = "covid-data.json"

        with open(self.DATAFILENAME, "r") as data_file:
            self.covid_data = json.load(data_file)

    def plot_single_country_total_deaths_data(self, country_abbr, color):
        """Plots the data of a single country on the graph but does not show it."""

        deaths_list = []
        dates_list = []

        for data in self.covid_data[country_abbr.upper().strip()]["data"][-7:]:
            deaths_list.append(int(data["total_deaths"]))
            dates_list.append(int(data["date"].split("-")[-1]))
            print(f'Date: {data["date"]}; Deaths: {data["total_deaths"]}')

        self.deaths_array = np.array(deaths_list)
        date_array = np.array(dates_list)

    def plot_on_dates(self, country_abbr, color):
        deaths_list = []
        dates_list = []

        for data in self.covid_data[country_abbr.upper().strip()]["data"][-21:]:
            deaths_list.append(int(data["total_deaths"]))
            dates_list.append(data["date"])
            print(f'Date: {data["date"]}; Deaths: {data["total_deaths"]}')

        self.deaths_array = np.array(deaths_list)
        date_array = np.array(dates_list)

        plt.xlabel(f"Date")
        plt.ylabel("Number Of Deaths")

        fig, ax = plt.subplots()
        ax.xaxis.set_tick_params(rotation=30, labelsize=10)

        plt.plot(dates_list, self.deaths_array)
        plt.show()

    def show_total_deaths_single_country(self, country_abbr, color):
        """Displays the total deaths of a single country."""

        plt.xlabel(f"Date({self.current_year}-{self.current_month})")
        plt.ylabel("Number Of Deaths")
        self.plot_single_country_total_deaths_data(country_abbr, color)

        y_min = (self.deaths_array.min() // 100) * 100
        y_max = (self.deaths_array.max() // 100 + 1) * 100

        plt.axis([self.day_today - 21, self.day_today, y_min, y_max])
        plt.show()

    def show_all_country_total_deaths(self):
        """Displays the total deaths of all countries in a graph."""

        plt.xlabel(f"Date({self.current_year}-{self.current_month})")
        plt.ylabel("Number Of Deaths")

        for abbr in self.covid_data:
            if abbr == "OWID_WRL":
                break

            if self.covid_data[abbr][0].get("total_deaths") != None:
                self.plot_single_country_total_deaths_data(abbr, (0, 0, 1))

        plt.axis([self.day_today - 7, self.day_today - 0.5, 0, 5000])
        plt.show()



if __name__ == "__main__":
    GraphObj = GraphUI()
    # GraphObj.show_total_deaths_single_country("IND", (0, 1, 0))
    GraphObj.plot_on_dates("IND", (1, 0, 0))
