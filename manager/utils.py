import pandas as pd
from data.currency_country import currency_dict
import matplotlib.pyplot as plt


def convert_index_to_DatetimeIndex(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['datetime'] = pd.to_datetime(dataframe.index)
    dataframe.set_index('datetime', inplace=True)
    return dataframe


def concat_database_with_inflation(inflation_database: pd.DataFrame, multi_data: pd.DataFrame) -> pd.DataFrame:
    first_index = multi_data.columns[0]
    value_with_inflation_database = pd.concat([inflation_database, multi_data], axis=1)
    value_with_inflation_database[f'{first_index}*Inf'] = value_with_inflation_database[first_index] * value_with_inflation_database["Inflation"]/100
    if len(multi_data.columns) == 2:
        second_index = multi_data.columns[1]
        value_with_inflation_database[f'{second_index}*Inf'] = value_with_inflation_database[second_index] * value_with_inflation_database["Inflation"]/100
    return value_with_inflation_database


def convert_country_to_currency(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.rename(columns={dataframe.columns[0]: f'{currency_dict[dataframe.columns[0]]}'})


def plotting_database(database):
    database.plot()
    plt.title(str.join(",", database.columns))
    plt.show()

