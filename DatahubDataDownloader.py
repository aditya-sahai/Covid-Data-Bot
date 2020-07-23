import requests


class DatahubDataDownloader:
    def __init__(self):
        self.DOWNLOAD_URL = "https://datahub.io/core/covid-19/r/countries-aggregated.csv"
        self.OUTPUT_FILE_NAME = "datahub-countries-aggregated-data.csv"

    def download_csv_data(self):
        """Downloads the 'countries-aggregated_csv.csv' data file."""

        headers = {
            "USER-AGENT": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        encoded_data = requests.get(self.DOWNLOAD_URL, headers=headers)
        print(encoded_data.status_code)
        # print(encoded_data.content)

        with open(self.OUTPUT_FILE_NAME, "wb") as write_file:
            write_file.write(encoded_data.content)


if __name__ == "__main__":
    Receiver = DatahubDataDownloader()
    Receiver.download_csv_data()
