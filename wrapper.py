import requests
import pandas as pd


class PricesAPI(object):
    def __init__(self, user_agent, contact):
        self.base_url = "https://prices.runescape.wiki/api/v1/osrs/"
        self.user_agent = {"User-Agent": user_agent, "From": contact}
        self._mappings = False

        self.times = ["5m", "1h", "3h", "6h", "24h"]

    def latest(self, mapping=False):
        prices = requests.get(self.base_url + "latest", headers=self.user_agent).json()["data"]
        if mapping:
            if not self._mappings:
                self._mappings = self.mapping_df()
            prices = self.__merge_mapping(prices)
        return prices

    def latest_df(self, mapping=False):
        prices = requests.get(self.base_url + "latest", headers=self.user_agent).json()["data"]
        prices = pd.DataFrame.from_dict(prices).T.fillna(0).astype("int").rename_axis("id")
        prices.index = prices.index.astype("int")
        if mapping:
            if not self._mappings:
                self._mappings = self.mapping_df()
            prices = self.__merge_mapping_df(prices)
        return prices

    def volumes(self, mapping=False):
        volumes = requests.get(self.base_url + "volumes", headers=self.user_agent).json()["data"]
        if mapping:
            for key, value in volumes.items():
                value = {"volume": value}
                volumes[key] = value
            if not self._mappings:
                self._mappings = self.mapping_df()
            volumes = self.__merge_mapping(volumes)
        return volumes

    def volumes_df(self, mapping=False):
        volumes = requests.get(self.base_url + "volumes", headers=self.user_agent).json()
        volumes = (
            pd.DataFrame(volumes["data"].items(), columns=["id", "volume"]).fillna(0).astype("int").set_index("id")
        )
        if mapping:
            if not self._mappings:
                self._mappings = self.mapping_df()
            volumes = self.__merge_mapping_df(volumes)
        return volumes

    def prices(self, time, mapping=False):
        if time in self.times:
            prices = requests.get(self.base_url + time, headers=self.user_agent).json()["data"]
            if mapping:
                if not self._mappings:
                    self._mappings = self.mapping_df()
                prices = self.__merge_mapping(prices)
            return prices
        else:
            raise ValueError(f"Invalid timeframe selected, valid options are: {self.times}")

    def prices_df(self, time, mapping=False):
        if time in self.times:
            prices = requests.get(self.base_url + time, headers=self.user_agent).json()["data"]
            prices = pd.DataFrame.from_dict(prices).T.fillna(0).astype("int").rename_axis("id")
            prices.index = prices.index.astype("int")
            if mapping:
                if not self._mappings:
                    self._mappings = self.mapping_df()
                prices = self.__merge_mapping_df(prices)
            return prices
        else:
            raise ValueError(f"Invalid timeframe selected, valid options are: {self.times}")

    def timeseries(self, step, id):
        if step in self.times:
            timeseries = requests.get(
                self.base_url + f"timeseries?timestep={step}&id={id}", headers=self.user_agent
            ).json()["data"]
            return timeseries
        else:
            raise ValueError(f"Invalid timeframe selected, valid options are: {self.times}")

    def timeseries_df(self, step, id):
        if step in self.times:
            timeseries = requests.get(
                self.base_url + f"timeseries?timestep={step}&id={id}", headers=self.user_agent
            ).json()["data"]
            timeseries = pd.DataFrame.from_dict(timeseries).fillna(0).astype("int")
            return timeseries
        else:
            raise ValueError(f"Invalid timeframe selected, valid options are: {self.times}")

    def mapping(self):
        mapping = requests.get(self.base_url + "mapping", headers=self.user_agent).json()
        return mapping

    def mapping_df(self):
        mapping = requests.get(self.base_url + "mapping", headers=self.user_agent).json()
        mapping = (
            pd.DataFrame.from_dict(mapping)
            .fillna(0)
            .set_index("id")
            .sort_index()
            .astype({"lowalch": "int", "limit": "int", "value": "int", "highalch": "int"})
        )
        mapping.index = mapping.index.map(int)
        return mapping

    def __merge_mapping(self, data):
        for key, values in data.items():
            try:
                mappings = self._mappings.loc[int(key)]
                values = {**values, **mappings}
                data[key] = values
            except KeyError:
                pass
        return data

    def __merge_mapping_df(self, data):
        data = data.merge(self._mappings, on="id")
        return data
