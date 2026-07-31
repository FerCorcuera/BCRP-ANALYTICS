import warnings
from typing import Any

import pandas as pd
import requests

BCRP_API_BASE_URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
DEFAULT_REQUEST_TIMEOUT = 20.0


def get_bcrp_series_payload(
    series_code: str,
    start_period: str | None = None,
    end_period: str | None = None,
    timeout: float = DEFAULT_REQUEST_TIMEOUT,
) -> dict[str, Any]:
    """
    Retrieve the raw JSON payload for one BCRPData series.

    Parameters
    ----------
    series_code:
        Official BCRPData series code, for example ``PN42689EM``.
    start_period:
        Optional first period using the BCRP API format, for example ``2024-1``.
    end_period:
        Optional last period. It can only be provided together with
        ``start_period``.
    timeout:
        Maximum number of seconds to wait for the API response.

    Returns
    -------
    dict
        The validated BCRPData JSON payload, including ``config`` and
        ``periods``.
    """
    if not isinstance(series_code, str):
        raise TypeError(f"The series code {series_code} must be a string")

    series_code = series_code.strip()
    if not series_code:
        raise ValueError("The series code can not be empty")

    if end_period is not None and start_period is None:
        raise ValueError("end_period requires start_period")

    url_parts = [BCRP_API_BASE_URL, series_code, "json"]
    if start_period is not None:
        if not isinstance(start_period, str) or not start_period.strip():
            raise ValueError("start_period must be a non-empty string")
        url_parts.append(start_period.strip())

    if end_period is not None:
        if not isinstance(end_period, str) or not end_period.strip():
            raise ValueError("end_period must be a non-empty string")
        url_parts.append(end_period.strip())

    response = requests.get("/".join(url_parts), timeout=timeout)
    response.raise_for_status()

    try:
        data = response.json()
    except ValueError as exc:
        raise ValueError("BCRPData returned an invalid JSON response") from exc

    if not isinstance(data, dict) or not isinstance(data.get("periods"), list):
        raise ValueError("BCRPData response does not contain a periods list")

    return data


def get_bcrp_series(
    series_code: str,
    start_period: str | None = None,
    end_period: str | None = None,
    timeout: float = DEFAULT_REQUEST_TIMEOUT,
) -> pd.DataFrame:
    """
    Retrieve one BCRPData series in its original period/value representation.

    The returned DataFrame preserves the API fields ``name`` and ``values`` so
    existing cleaning helpers and notebooks remain compatible.
    """
    data = get_bcrp_series_payload(
        series_code=series_code,
        start_period=start_period,
        end_period=end_period,
        timeout=timeout,
    )

    return pd.DataFrame(data["periods"])


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
    if not isinstance(periodo, str):
        raise TypeError("BCRP period must be a string")

    try:
        mes, anio = periodo.split(".", maxsplit=1)
        mes_en = MONTH_MAP[mes]
    except (KeyError, ValueError) as exc:
        raise ValueError(f"Unsupported BCRP monthly period: {periodo}") from exc

    return pd.to_datetime(f"{mes_en}-{anio}", format="%b-%Y")


def clean_bcrp_series(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the imported BCRP series:
    1. Applies the pandas date format for the period column
    2. Converts the "value" column of the serie into float
    """
    required_columns = {"name", "values"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"BCRP series data is missing required columns: {missing}")

    df = df.copy()
    first_values = df["values"].map(
        lambda values: values[0] if isinstance(values, list) and values else values
    )

    clean_df = pd.DataFrame(
        {
            "period": df["name"].map(parse_bcrp_period),
            "value": pd.to_numeric(first_values, errors="coerce"),
        }
    )

    return clean_df


def get_bcrp_clean_series(
    series_code: str,
    name_serie: str,
    start_period: str | None = None,
    end_period: str | None = None,
    timeout: float = DEFAULT_REQUEST_TIMEOUT,
) -> pd.DataFrame:
    """
    Pipeline to get BCRP data cleaned in a pandas dataframe format,
    paramteres:
    - series_code: the oficial BCRP code for that serie
    - name_serie: the name of the serie that you are retrieven (must be short and with one str)
    - start_period (optional)
    - end_period (optional)

    if periods are not provided the function will retrieve all the available data
    """
    if not isinstance(name_serie, str):
        raise TypeError("The series name must be a string")
    if not name_serie.strip():
        raise ValueError("The series name can not be empty")

    df_bcrp_series = get_bcrp_series(
        series_code=series_code,
        start_period=start_period,
        end_period=end_period,
        timeout=timeout,
    )

    clean_df_bcrp_series = clean_bcrp_series(df_bcrp_series).sort_values(
        "period", ascending=False
    )

    clean_df_bcrp_series[name_serie.strip()] = clean_df_bcrp_series["value"]

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
