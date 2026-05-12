import pandas as pd
import requests


def get_bcrp_series(series_code, start_period=None, end_period=None):
    """
    Returns BCRP series data as a pandas DataFrame, it can accept optional start and end period params
    """
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

    mes, anio = periodo.split(".")

    mes_en = MONTH_MAP[mes]

    return pd.to_datetime(f"{mes_en}-{anio}", format="%b-%Y")


def clean_bcrp_series(df: pd.DataFrame):

    df = df.copy()
    df.columns = ["period", "value"]
    df["value"] = df["value"].str[0].astype(float)

    df["period"] = df["period"].apply(parse_bcrp_period)

    return df
