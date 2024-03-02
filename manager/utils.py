import pandas as pd
import yfinance as yf
from data.currency_country import currency_dict
import matplotlib.pyplot as plt
from datetime import date
import mpld3


def concat_database_with_inflation(inflation_database: pd.DataFrame, multi_data: pd.DataFrame) -> pd.DataFrame:
    start_date = max(inflation_database.index[0], multi_data.index[0])
    end_date = min(inflation_database.index[-1], multi_data.index[-1])
    value_with_inflation_database = pd.concat([inflation_database[start_date:end_date], multi_data[start_date:end_date]], axis=1)
    for index in multi_data.columns:
        value_with_inflation_database[f"Value of {index} including inflation"] = value_with_inflation_database[index] / (value_with_inflation_database["Inflation"])
    return value_with_inflation_database


def convert_country_to_currency(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.rename(columns={dataframe.columns[0]: f"{currency_dict[dataframe.columns[0]]}"})


def convert_currency_to_country(currency: str) -> str:
    country = list(currency_dict.keys())[list(currency_dict.values()).index(currency)].replace(" ", "_")
    return country


def indexing_on_start_date(database: pd.DataFrame) -> pd.DataFrame:
    denominator_of_values = database.iloc[0].values[0]
    name_of_columns = database.columns[0]
    database[f'{name_of_columns} indexed on {database.index[0].date()}'] = (database.iloc[:, 0] - denominator_of_values) / database.iloc[:, 0] * 100
    database.drop(database.columns[0], axis=1, inplace=True)
    return database


def convert_usd_to_other_currency(dataframe: pd.DataFrame, country: str, start_date: date = 0, end_date: date = -1) -> pd.DataFrame:
    from manager.database import get_database_currency_rate_to_dollar
    dataframe_rate = get_database_currency_rate_to_dollar(country, start_date, end_date)
    name_of_stock = dataframe.columns[0]
    name_of_currency = dataframe_rate.columns[0]
    dataframe[f"{name_of_stock} in {name_of_currency}"] = dataframe[name_of_stock] * dataframe_rate[name_of_currency]
    dataframe = dataframe.drop(name_of_stock, axis=1)
    return dataframe


def plotting_database(database: pd.DataFrame) -> plt:
    fig, ax1 = plt.subplots()
    if database.columns[0] == "Inflation":
        # Part with index
        lines1 = ax1.plot(database.index, database.drop("Inflation", axis=1))
        ax1.set_xlabel("Data")
        ax1.set_ylabel("Index Value", color="tab:green")
        ax1.tick_params(axis="y", labelcolor="tab:green")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha="right")

        # Inflation Part
        ax2 = ax1.twinx()
        lines2 = ax2.plot(database.index, database["Inflation"], color="tab:red", linestyle="'--'")
        ax2.set_ylabel(f"Inflation based on {database.iloc[0].name.strftime('%Y-%m-%d')}", color="tab:red")
        ax2.tick_params(axis="y", labelcolor="tab:red")

        # Fixing Legend
        lines = lines2 + lines1
        labels = [x for x in database.columns]
        ax1.legend(handles=lines, labels=[x for x in labels], loc="upper left")
        ax2.axhline(y=1, color="red", linestyle="'--'", linewidth=1)
        plt.title(f"{database.columns[1]} from {database.index[0].date()}")
    else:
        # If the first column is not "Inflation," plot the entire DataFrame on the left y-axis
        ax1.plot(database)
        ax1.tick_params(axis="y", labelcolor="tab:blue")
        plt.title(database.columns[0])
    html_plot = mpld3.fig_to_html(fig)

    # Close the Matplotlib figure to release resources
    plt.close(fig)

    return html_plot


def validation_date(dataframe, start_date: date = 0, end_date: date = -1):
    if not isinstance(start_date, int) and not isinstance(end_date, int):
        if dataframe.index[0].date() <= start_date:
            if dataframe.index[-1].date() >= end_date:
                dataframe = dataframe[start_date:end_date]
            else:
                end_date = dataframe.index[-1]
                dataframe = dataframe[start_date: end_date]
        else:
            start_date = dataframe.index[0].date()
            dataframe = dataframe[start_date:end_date]
    return dataframe


def validation_null_value(dataframe: pd.DataFrame):
    if dataframe.empty or dataframe.isna().any().any():
        return "Error in database"
    else:
        return dataframe


def validate_stock(func):
    def wrapper(stock):
        if 'country' in yf.Ticker(stock).info.keys():
            return func(stock)
        else:
            return "No stock info"
    return wrapper
