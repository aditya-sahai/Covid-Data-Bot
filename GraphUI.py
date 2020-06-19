import json


class GraphUI:

    def __init__(self):
        """Initialize the DataReceiver class."""
        self.DATAFILENAME = "temp.json"

        with open(self.DATAFILENAME, "r") as data_file:
            self.covid_data = json.load(data_file)

        # print(self.covid_data)
        for data in self.covid_data["AFG"]:
            print(data, end="\n\n")


if __name__ == "__main__":
    GrapgObj = GraphUI()
