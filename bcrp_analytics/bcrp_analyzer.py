import pandas as pd
import requests

from bcrp_analytics import build_bcrp_dataset


# TODO: cambiar las funcioens para que devuelvan datafames y no seires, complican mucho las funciones
class BCRP_ANALYZER:
    """
    BCRP_ANALYZER is a tool that:
        - Automates data straction from the BCRP's API
        - Returns plots to analyze how different markets and macroeconomic trends are going
        - Applies useful macroeconomic methods (deflation , exchange rate, etc)
    """

    inflation_bcrp_series = {
        "PN38705PM": "ipc",
        "PN42107PM": "ipc_desestacionalizado",
        "PN01271PM": "inflacion_mensual",
        "PN01272PM": "inflacion_acumulada",
        "PN01273PM": "inflacion_12m",
    }

    df_ipc_series = None

    def __init__(self):

        if BCRP_ANALYZER.df_ipc_series is None:

            print("Loading BCRP data...")

            BCRP_ANALYZER.df_ipc_series = build_bcrp_dataset(
                BCRP_ANALYZER.inflation_bcrp_series
            )

            print("BCRP data loaded!")

        self.df_ipc_series = BCRP_ANALYZER.df_ipc_series.sort_values("period")

    def deflate_series(
        self, monthly_df: pd.DataFrame, period_name: str, series_name: str
    ) -> pd.DataFrame:
        """
        Deflates a nominal series using the IPC series extracted from BCRP data
        It automatically fetchs data using the API.

        Parameters
        ----------
        montly_series: pd.DataFrame of the nominal values to deflate

        """

        merged_df = monthly_df.merge(
            self.df_ipc_series[["period", "ipc"]],
            left_on=period_name,
            right_on="period",
            how="left",
        )

        deflated_name = series_name + "_deflated"
        merged_df[deflated_name] = (merged_df[series_name] / merged_df["ipc"]) * 100

        display(merged_df[[period_name, series_name, "monthly_deflated_series"]])

        return monthly_deflated_series

    def calculate_realmonthly_growth(
        self, monthly_df: pd.DataFrame, period_name: str, series_name: str
    ) -> pd.DataFrame:
        """
        Returns the real monthly growth given a monthly series
        using BCRP inflation series (Fisher equation)

        Parameters
        ----------
        monthly_df  : pd.DataFrame with the nominal series
        period_name : column name of the period (must match BCRP period format)
        series_name : column name of the nominal values to deflate

        """
        monthly_df = monthly_df.sort_values(period_name).reset_index(drop=True)

        monthly_df["nominal_growth"] = monthly_df[series_name].pct_change() * 100

        merged_df = monthly_df.merge(
            self.df_ipc_series[["period", "inflacion_mensual"]],
            left_on=period_name,
            right_on="period",
            how="left",
        )

        merged_df["real_growth"] = (
            (
                (1 + merged_df["nominal_growth"] / 100)
                / (1 + merged_df["inflacion_mensual"] / 100)
            )
            - 1
        ) * 100

        display(merged_df[["period", "nominal_growth", "real_growth"]])

        return merged_df

    def calculate_real_12m_growth(
        self, monthly_df: pd.DataFrame, period_name: str, series_name: str
    ) -> pd.DataFrame:
        """
        Returns the real monthly growth given a monthly serie using BCRP inflation series
        Parameters
        ----------
        monthly_df: pd.DataFrame to calcualte the real yoy growth

        """
        monthly_df = monthly_df.sort_values(period_name).reset_index(drop=True)

        monthly_df["nominal_growth"] = monthly_df[series_name].pct_change(12) * 100

        merged_df = monthly_df.merge(
            self.df_ipc_series[["period", "inflacion_12m"]],
            left_on=period_name,
            right_on="period",
            how="left",
        )

        merged_df[real_growth] = (
            (
                (1 + merged_df["nominal_growth"] / 100)
                / (1 + merged_df["inflacion_12m"] / 100)
            )
            - 1
        ) * 100

        return merged_df
