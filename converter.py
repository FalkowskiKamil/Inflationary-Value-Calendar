"""import pandas as pd
data = pd.read_csv("DUPA.csv", usecols=["Name", "Symbol", "Country"])
data_pol = pd.read_csv("wig.csv", encoding='iso-8859-2')
data_amex = pd.read_csv("amex.csv", usecols=["Name", "Symbol", "Country"])
data_nyse = pd.read_csv("nyse.csv", usecols=["Name", "Symbol", "Country"])
frames = [data, data_nyse, data_amex, data_pol]
data2 = pd.concat(frames)
data2 = data2.drop_duplicates(subset="Symbol")
data2 = data2.sort_values(by="Symbol")
data2.to_csv("stock_listed.csv", index=False)
"""
