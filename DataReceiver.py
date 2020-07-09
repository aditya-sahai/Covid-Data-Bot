import requests
import json

class DataReceiver:

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    }

    def __init__(self):
        """Initialize the DataReceiver class."""
        self.DATAURL = "https://covid.ourworldindata.org/data/owid-covid-data.json"
        self.DATAFILENAME = "covid-data.json"

    def download_json_data(self):
        """Makes a file called covid-data.json containing the covid data and return a dictionary."""

        response = requests.get(self.DATAURL, headers=DataReceiver.headers)
        print(f"Got response code: {response.status_code}")
        covid_data = json.loads(response.content.decode())

        with open(self.DATAFILENAME, "w") as data_file:
            json.dump(covid_data, data_file, indent=4)

        print(type(covid_data))
        return covid_data


if __name__ == "__main__":
    obj = DataReceiver()
    obj.download_json_data()
