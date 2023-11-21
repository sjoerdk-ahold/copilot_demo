import pandas
import requests
import streamlit

root_url = "https://prices.azure.com/api/retail/prices"

currency_code_eur = "currencyCode='EUR'"
# DEMO: try adding a currency code for dollars.
filter_vm = "$filter=serviceName eq 'Virtual Machines'"
filter_region_westeurope = "armRegionName eq 'westeurope'"
# DEMO: try adding a filter for a different region & see if you get the specific armRegionName suggested
filter_no_reservation = "priceType eq 'Consumption'"

# DEMO: add a comment above the below line starting with "the below line is a poor example of" and check the suggestions
url = f"{root_url}?{currency_code_eur}&{filter_vm} and {filter_region_westeurope} and {filter_no_reservation}"

data_json = requests.get(url).json()
data_json_items = data_json.get("Items", {})

# DEMO: have copilot explain the below code, for instance by beginning a comment with "the code below..."
while data_json.get("NextPageLink"):
    data_json = requests.get(data_json["NextPageLink"]).json()
    data_json_items = data_json_items + data_json.get("Items", {})

data_filtered = []
bad_word_list = ["windows", "spot", "low priority", "basic", "expired"]

for item in data_json_items:
    # if the value of productName or meterName contains any of the words in the bad_word_list, skip
    if any(word in item["productName"].lower() for word in bad_word_list) or any(
        word in item["meterName"].lower() for word in bad_word_list
    ):
        continue
    else:
        data_filtered.append(item)

dataframe = pandas.DataFrame(data_filtered)

# DEMO: try adding a column to the dataframe with the unit price per month, per weekend or for the specific number of
# working days in december 2023.
# howto: dataframe["give_your_column_a_suggestive_name"] = dataframe["unitPrice"] ...

streamlit.write(dataframe)
