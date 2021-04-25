import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


class GetBlockChainInfo:
    def __init__(self, get_or_load="Nothing"):
        ##########################################
        #   get_network_activity gets the newest network activity data from blockchain.com;
        #   save_network_activity_data_dataframes will save the network activity dataframes
        #   gathered from blockchain.com not to request the data again;
        #   load_local_network_activity_data_dataframes will load the saved network activity dataframes
        #   into the network_activity_data variable;
        ##########################################
        self.stored_path_of_dataframes = HERE YOUR PATH WHERE TO STORE THE DATA LOCALLY AS A STRING LIKE "C:/Users/.../"
        self.chart_base_url_begin = "https://api.blockchain.info/charts/"
        self.chart_base_url_end = "?timespan=all&sampled=true&metadata=false&cors=true&format=json"

        self.data_division_names = ["network_activity", "wallet_activity", "market_signals", "mining_information"]

        self.network_activity_variables_and_urls = [["unique_adresses_used", "n-unique-addresses"],
                                           ["confirmed_transactions_per_day", "n-transactions"],
                                           ["confirmed_payments_per_day", "n-payments"],
                                           ["transaction_rate_per_second", "transactions-per-second"],
                                           ["output_value_per_day", "output-volume"],
                                           ["mempool_transaction_count", "mempool-count"],
                                           ["mempool_size_growth", "mempool-growth"],
                                           ["mempool_size_bytes", "mempool-size"],
                                           ["unspent_transaction_outputs", "utxo-count"],
                                           ["transactions_excluding_popular_adresses", "n-transactions-excluding-popular"],
                                           ["estimated_transaction_value_BTC", "estimated-transaction-volume"],
                                           ["estimated_transaction_value_USD", "estimated-transaction-volume-usd"]]

        self.wallet_activity_variables_and_urls = [["blockchain.com_wallets", "my-wallet-n-users"]]

        self.market_signals_variables_and_urls = [["market_value_to_realized_value", "mvrv"],
                                                  ["network_value_to_transactions", "nvt"]]

        self.mining_information_variables_and_urls = [["total_hash_rate_in_TH_per_s", "hash-rate"],
                                               ["network_difficulty", "difficulty"],
                                               ["miners_revenue_USD", "miners-revenue"],
                                               ["total_transaction_fees_BTC", "transaction-fees"],
                                               ["total_transaction_fees_USD", "transaction-fees-usd"],
                                               ["fees_per_transaction_USD", "fees-usd-per-transaction"],
                                               ["cost_percent_of_transaction_volume", "cost-per-transaction-percent"],
                                               ["cost_of_transaction", "cost-per-transaction"]]

        self.network_activity_data = {}
        self.wallet_activity_data = {}
        self.market_signals_data = {}
        self.mining_information_data = {}

        while True:
            if get_or_load == "Nothing":
                get_or_load = float(input("Download new data from blockchain.com (Option: 'get') or load downloaded, local saved data (Option: 'load'): "))
            if get_or_load == "get":
                self.get_all_data()
                self.save_all_data_dataframes()
                break
            elif get_or_load == "load":
                self.load_all_local_data_dataframes()
                break

    def get_network_activity(self):
        for i in self.network_activity_variables_and_urls:
            url = self.chart_base_url_begin + i[1] + self.chart_base_url_end
            df = pd.DataFrame(requests.get(url).json()["values"])
            df["x"] = pd.to_datetime(df["x"], unit="s")
            df.set_index("x", inplace=True)
            self.network_activity_data["{}".format(i[0])] = [i[1], df]

    def get_wallet_activity(self):
        for i in self.wallet_activity_variables_and_urls:
            url = self.chart_base_url_begin + i[1] + self.chart_base_url_end
            df = pd.DataFrame(requests.get(url).json()["values"])
            df["x"] = pd.to_datetime(df["x"], unit="s")
            df.set_index("x", inplace=True)
            self.wallet_activity_data["{}".format(i[0])] = [i[1], df]

    def get_market_signals(self):
        for i in self.market_signals_variables_and_urls:
            url = self.chart_base_url_begin + i[1] + self.chart_base_url_end
            df = pd.DataFrame(requests.get(url).json()["values"])
            df["x"] = pd.to_datetime(df["x"], unit="s")
            df.set_index("x", inplace=True)
            self.market_signals_data["{}".format(i[0])] = [i[1], df]

    def get_mining_information(self):
        for i in self.mining_information_variables_and_urls:
            url = self.chart_base_url_begin + i[1] + self.chart_base_url_end
            df = pd.DataFrame(requests.get(url).json()["values"])
            df["x"] = pd.to_datetime(df["x"], unit="s")
            df.set_index("x", inplace=True)
            self.mining_information_data["{}".format(i[0])] = [i[1], df]

    def get_all_data(self):
        print("Getting fresh data...")
        self.get_network_activity()
        print("Got network activity data...")
        self.get_wallet_activity()
        print("Got wallet activity data...")
        self.get_market_signals()
        print("Got market signals data...")
        self.get_mining_information()
        print("Got mining information data...")
        print("-Got all data-")

    def save_network_activity_data_dataframes(self):
        for i in self.network_activity_variables_and_urls:
            self.network_activity_data[i[0]][1].to_json(self.stored_path_of_dataframes + "network_activity_data_dataframe{}.json".format("_" + i[0]))

    def save_wallet_activity_data_dataframes(self):
        for i in self.wallet_activity_variables_and_urls:
            self.wallet_activity_data[i[0]][1].to_json(self.stored_path_of_dataframes + "wallet_activity_data_dataframe{}.json".format("_" + i[0]))

    def save_market_signals_data_dataframes(self):
        for i in self.market_signals_variables_and_urls:
            self.market_signals_data[i[0]][1].to_json(self.stored_path_of_dataframes + "market_signals_data_dataframe{}.json".format("_" + i[0]))

    def save_mining_information_data_dataframes(self):
        for i in self.mining_information_variables_and_urls:
            self.mining_information_data[i[0]][1].to_json(self.stored_path_of_dataframes + "mining_information_data_dataframe{}.json".format("_" + i[0]))

    def save_all_data_dataframes(self):
        print("Save the new data locally...")
        self.save_network_activity_data_dataframes()
        self.save_wallet_activity_data_dataframes()
        self.save_market_signals_data_dataframes()
        self.save_mining_information_data_dataframes()
        print("-Saved the new data locally-")

    def load_local_network_activity_data_dataframes(self):
        for i in self.network_activity_variables_and_urls:
            df = pd.read_json(self.stored_path_of_dataframes + "network_activity_data_dataframe{}.json".format("_" + i[0]))
            self.network_activity_data["{}".format(i[0])] = [i[1], df]

    def load_local_wallet_activity_data_dataframes(self):
        for i in self.wallet_activity_variables_and_urls:
            df = pd.read_json(self.stored_path_of_dataframes + "wallet_activity_data_dataframe{}.json".format("_" + i[0]))
            self.wallet_activity_data["{}".format(i[0])] = [i[1], df]

    def load_local_market_signals_data_dataframes(self):
        for i in self.market_signals_variables_and_urls:
            df = pd.read_json(self.stored_path_of_dataframes + "market_signals_data_dataframe{}.json".format("_" + i[0]))
            self.market_signals_data["{}".format(i[0])] = [i[1], df]

    def load_local_mining_information_data_dataframes(self):
        for i in self.mining_information_variables_and_urls:
            df = pd.read_json(self.stored_path_of_dataframes + "mining_information_data_dataframe{}.json".format("_" + i[0]))
            self.mining_information_data["{}".format(i[0])] = [i[1], df]

    def load_all_local_data_dataframes(self):
        print("Load local saved data...")
        self.load_local_network_activity_data_dataframes()
        print("Loaded network activity data...")
        self.load_local_wallet_activity_data_dataframes()
        print("Loaded wallet activity data...")
        self.load_local_market_signals_data_dataframes()
        print("Loaded market signals data...")
        self.load_local_mining_information_data_dataframes()
        print("Loaded mining information data...")
        print("-Loaded all data-")

    def visualize_charts_of_data(self, which_data_to_visualize):
        data_variable_names_and_urls = getattr(self, which_data_to_visualize + "_variables_and_urls")
        to_be_visualized_data = getattr(self, which_data_to_visualize + "_data")
        for x in data_variable_names_and_urls:
            plt.plot(to_be_visualized_data[x[0]][1].index, to_be_visualized_data[x[0]][1]["y"])
            plt.title(str(which_data_to_visualize).upper() + " - " + str(x[0]))
            plt.show()


if __name__ == "__main__":
    data = GetBlockChainInfo(get_or_load="load")
    print(data.network_activity_data)
    for i in ["network_activity", "wallet_activity", "market_signals", "mining_information"]:
        data.visualize_charts_of_data(i)