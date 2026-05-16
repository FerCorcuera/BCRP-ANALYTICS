import warnings

import pandas as pd
import requests

# TODO: add the other parameters to get_brp_series function and edge cases (handling errors)


def get_bcrp_series(series_code: str, start_period=None, end_period=None) -> pd.Series:
    """
    Returns BCRP series data as a pandas DataFrame.
    Parameters
    ------------
    - series_code: Str, The oficial BCRP series code, example: PN42683EM
    - start_period: Str, The selected start period fo the serie, exmample: 2013-1
    - end_period: Str, the selectes end period to the serie

    Returns: a pandas.Series with the period and the selected serie with the column name "value"
    """

    if not isinstance(series_code, str):
        raise TypeError(f"The series code {series_code} must be a string")

    base_url = "https://estadisticas.bcrp.gob.pe/" "estadisticas/series/api"
    url = f"{base_url}/{series_code}/json"

    if start_period and end_period:

        url = f"{url}/{start_period}/{end_period}"

    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["periods"])

    return df


MONTH_MAP = {
    "Ene": "Jan",
    "Feb": "Feb",
    "Mar": "Mar",
    "Abr": "Apr",
    "May": "May",
    "Jun": "Jun",
    "Jul": "Jul",
    "Ago": "Aug",
    "Sep": "Sep",
    "Oct": "Oct",
    "Nov": "Nov",
    "Dic": "Dec",
}


def parse_bcrp_period(periodo: str):
    """
    Applies a transformation to the "period" original column from BCRP.
    In order to have a pandas.date_time format (month,year)
    """
    mes, anio = periodo.split(".")

    mes_en = MONTH_MAP[mes]

    return pd.to_datetime(f"{mes_en}-{anio}", format="%b-%Y")


def clean_bcrp_series(df: pd.DataFrame):
    """
    Cleans the imported BCRP series:
    1. Applies the pandas date format for the period column
    2. Converts the "value" column of the serie into float
    """
    df = df.copy()
    df.columns = ["period", "value"]
    df["value"] = df["value"].str[0].astype(float)

    df["period"] = df["period"].apply(parse_bcrp_period)

    return df


def get_bcrp_clean_series(
    series_code, name_serie: str, start_period=None, end_period=None
):
    """
    Pipeline to get BCRP data cleaned in a pandas dataframe format,
    paramteres:
    - series_code: the oficial BCRP code for that serie
    - name_serie: the name of the serie that you are retrieven (must be short and with one str)
    - start_period (optional)
    - end_period (optional)

    if periods are not provided the function will retrieve all the available data
    """

    df_bcrp_series = get_bcrp_series(series_code, start_period, end_period)

    clean_df_bcrp_series = clean_bcrp_series(df_bcrp_series).sort_values(
        "period", ascending=False
    )

    clean_df_bcrp_series[name_serie] = clean_df_bcrp_series["value"]

    clean_df_bcrp_series = clean_df_bcrp_series.drop(columns=["value"])

    return clean_df_bcrp_series


# TODO: Improve the functionto consider other parametrs like periods
def build_bcrp_dataset(names_codes: dict) -> pd.DataFrame:
    """
    Function to create a whole dataset (in pd.dataframe format) given a dictionary with the codes and names
    ---------
    Parameters:

    - names_codes: a dictionary with the codes and their respective names that will be used as headers

        names_codes = {1235BFD:'test_serie'}

    -------
    Notes:
    Series with different data ranges are merged using an outer join. Missing observations are representend as NaN values

    """
    if not isinstance(names_codes, dict):

        raise TypeError("The 'names_codes' parameters must be a dictionary")

    if not names_codes:

        raise ValueError("The dictionary 'names_codes' can not be empty")

    df_bcrp_dataset = None

    for code, name in names_codes.items():

        if df_bcrp_dataset is None:

            df_bcrp_dataset = get_bcrp_clean_series(code, name)

        else:

            df_bcrp_new_serie = get_bcrp_clean_series(code, name)

            df_bcrp_dataset = pd.merge(
                df_bcrp_dataset, df_bcrp_new_serie, on="period", how="outer"
            )

    df_bcrp_dataset = df_bcrp_dataset.sort_values(
        "period", ascending=False
    ).reset_index(drop=True)

    if df_bcrp_dataset.isna().values.any():

        warnings.warn(
            "Warning: Some series contain missing ovservations due to selecting series with different data ranges"
        )

    return df_bcrp_dataset
