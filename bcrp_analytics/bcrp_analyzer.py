import pandas as pd
import requests

from bcrp_analytics import build_bcrp_dataset


class BCRP_ANALYZER:

    inflation_bcrp_series = {"PN38705PM": "ipc", "PN42107PM": "ipc_desestacionalizado"}

    def __init__(self):

        self.df_ipc_series = None

        print("starting inflation analyzer")

    def deflate_series(monthly_series: pd.Series):

        if self.df_ipc_series is None:

            self.df_ipc_series = _load_ipc_series()

        monthly_deflated_series = (monthly_series / self.df_ipc_series["ipc"]) * 100

        return monthly_series

    def _load_ipc_series(self):

        df_ipc_series = build_bcrp_dataset(inflation_bcrp_series)

        return df_ipc_series
