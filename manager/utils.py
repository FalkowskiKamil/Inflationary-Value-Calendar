import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import mpld3

from manager.database import get_database_currency_rate_to_dollar
from manager.single_info import finding_country_by_currency


def concat_dataframe_with_inflation(inflation: pd.DataFrame, dataframe: pd.DataFrame) -> pd.DataFrame:
    start_date, end_date = unify_dataframes_date(inflation, dataframe)
    inflation = inflation[start_date:end_date]
    dataframe = dataframe[start_date:end_date]
    dataframe = pd.DataFrame({f"{dataframe.columns[0]} with inflation": dataframe.iloc[:, 0] / inflation.iloc[:, 0]})
    return dataframe


def concat_dataframe_with_exchange_rate(main_dataframe: pd.DataFrame, exchange_dataframe: pd.DataFrame) -> pd.DataFrame:
    start_date, end_date = unify_dataframes_date(main_dataframe, exchange_dataframe)
    main_dataframe = main_dataframe[start_date:end_date]
    exchange_dataframe = exchange_dataframe[start_date:end_date]
    main_column = main_dataframe.iloc[:, 0].astype(float)
    exchange_column = exchange_dataframe.iloc[:, 0].astype(float)
    exchange_dataframe_name = exchange_column.name
    if "dollar" in main_column.name:
        main_dataframe_name = main_column.name.split(" in")[0].replace("dollar", exchange_dataframe_name)
        dataframe = pd.DataFrame({main_dataframe_name: main_column * exchange_column})
    elif "cents" in main_column.name:
        main_dataframe_name = main_column.name.split(" in")[0].replace("cents", exchange_dataframe_name)
        dataframe = pd.DataFrame({main_dataframe_name: main_column/100 * exchange_column})
    else:
        main_dataframe_name = main_column.name
        dataframe = pd.DataFrame({main_dataframe_name: main_column * exchange_column})

    return dataframe


def convert_currency_to_usd(from_currency: str, start_dataframe_date: date, end_dataframe_date: date) -> pd.DataFrame:
    country = finding_country_by_currency(from_currency)
    dataframe = get_database_currency_rate_to_dollar(country, start_dataframe_date, end_dataframe_date)
    dataframe[dataframe.columns[0]] = 1 / dataframe.iloc[:, 0]
    return dataframe


def convert_currency_to_other_currency(from_dataframe: pd.DataFrame, to_dataframe: pd.DataFrame) -> pd.DataFrame:
    start_date, end_date = unify_dataframes_date(from_dataframe, to_dataframe)
    dataframe = to_dataframe.iloc[:, 0] / from_dataframe.iloc[:, 0]
    dataframe = dataframe[start_date:end_date]
    return dataframe


def finding_exchanging_rate(from_currency: str, to_currency: str, start_dataframe_date: date, end_dataframe_date: date) -> pd.DataFrame:
    if from_currency == to_currency:
        date_range = pd.date_range(start=start_dataframe_date, end=end_dataframe_date, freq='MS', normalize=True)
        dataframe = pd.DataFrame(index=date_range, columns=[f'{from_currency}'])
        dataframe[from_currency] = ['1']*len(date_range)
        dataframe = pd.DataFrame(dataframe)
        return dataframe

    elif from_currency != "USD" and to_currency == "USD":
        dataframe = convert_currency_to_usd(from_currency, start_dataframe_date, end_dataframe_date)
        return dataframe

    elif from_currency == "USD" and to_currency != "USD":
        country = finding_country_by_currency(to_currency)
        dataframe = get_database_currency_rate_to_dollar(country, start_dataframe_date, end_dataframe_date)
        return dataframe

    elif from_currency != "USD" and to_currency != "USD":
        from_country = finding_country_by_currency(from_currency)
        to_country = finding_country_by_currency(to_currency)
        from_country_dataframe = get_database_currency_rate_to_dollar(from_country, start_dataframe_date, end_dataframe_date)
        to_country_dataframe = get_database_currency_rate_to_dollar(to_country, start_dataframe_date, end_dataframe_date)
        dataframe = convert_currency_to_other_currency(from_country_dataframe, to_country_dataframe)
        return pd.DataFrame(dataframe, columns=[to_currency])


def indexing_on_start_date(dataframe: pd.DataFrame) -> pd.DataFrame:
    denominator_of_values = dataframe.iloc[0].values[0]
    name_of_columns = dataframe.columns[0]
    dataframe[f'{name_of_columns} indexed on {dataframe.index[0].date()}'] = 1 + (dataframe.iloc[:, 0] - denominator_of_values) / dataframe.iloc[:, 0]
    dataframe.drop(dataframe.columns[0], axis=1, inplace=True)
    return dataframe


def plotting_dataframe(dataframe: pd.DataFrame) -> plt:
    fig, ax1 = plt.subplots()
    if dataframe.columns[0] == "Inflation":
        # Part with index
        lines1 = ax1.plot(dataframe.index, dataframe.drop("Inflation", axis=1))
        ax1.set_xlabel("Data")
        ax1.set_ylabel("Index Value", color="tab:green")
        ax1.tick_params(axis="y", labelcolor="tab:green")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha="right")

        # Inflation Part
        ax2 = ax1.twinx()
        lines2 = ax2.plot(dataframe.index, dataframe["Inflation"], color="tab:red", linestyle="'--'")
        ax2.set_ylabel(f"Inflation framed on {dataframe.iloc[0].name.strftime('%Y-%m-%d')}", color="tab:red")
        ax2.tick_params(axis="y", labelcolor="tab:red")

        # Fixing Legend
        lines = lines2 + lines1
        labels = [x for x in dataframe.columns]
        ax1.legend(handles=lines, labels=[x for x in labels], loc="upper left")
        ax2.axhline(y=1, color="red", linestyle="'--'", linewidth=1)
        plt.title(f"{dataframe.columns[1]} from {dataframe.index[0].date()}")
    else:
        # If the first column is not "Inflation," plot the entire DataFrame on the left y-axis
        ax1.plot(dataframe)
        ax1.tick_params(axis="y", labelcolor="tab:blue")
        plt.title(dataframe.columns[0].replace("_", " "))
    html_plot = mpld3.fig_to_html(fig)

    # Close the Matplotlib figure to release resources
    plt.close(fig)

    return html_plot


def unify_dataframes_date(dataframe_1, dataframe_2) -> [str, str]:
    start_date = max(dataframe_1.index[0], dataframe_2.index[0])
    end_date = min(dataframe_1.index[-1], dataframe_2.index[-1])
    return [start_date, end_date]
