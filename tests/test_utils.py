import unittest
from unittest.mock import Mock, patch

import pandas as pd

from bcrp_analytics import utils

SAMPLE_PAYLOAD = {
    "config": {
        "title": "Sample title",
        "series": [{"name": "Sample series", "dec": "0"}],
    },
    "periods": [
        {"name": "Ene.2024", "values": ["100.5"]},
        {"name": "Feb.2024", "values": ["n.d."]},
    ],
}


class BCRPSeriesRetrieverTests(unittest.TestCase):
    @patch("bcrp_analytics.utils.requests.get")
    def test_payload_uses_range_and_timeout(self, mock_get):
        response = Mock()
        response.json.return_value = SAMPLE_PAYLOAD
        mock_get.return_value = response

        payload = utils.get_bcrp_series_payload(
            " PN42689EM ",
            start_period="2024-1",
            end_period="2024-2",
            timeout=7,
        )

        mock_get.assert_called_once_with(
            "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/"
            "PN42689EM/json/2024-1/2024-2",
            timeout=7,
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(payload, SAMPLE_PAYLOAD)

    def test_end_period_requires_start_period(self):
        with self.assertRaisesRegex(ValueError, "requires start_period"):
            utils.get_bcrp_series_payload("PN42689EM", end_period="2024-2")

    @patch("bcrp_analytics.utils.requests.get")
    def test_invalid_payload_is_rejected(self, mock_get):
        response = Mock()
        response.json.return_value = {"config": {}}
        mock_get.return_value = response

        with self.assertRaisesRegex(ValueError, "periods list"):
            utils.get_bcrp_series_payload("PN42689EM")

    @patch("bcrp_analytics.utils.get_bcrp_series_payload")
    def test_get_series_preserves_api_columns(self, mock_payload):
        mock_payload.return_value = SAMPLE_PAYLOAD

        result = utils.get_bcrp_series("PN42689EM")

        self.assertEqual(result.columns.tolist(), ["name", "values"])
        self.assertEqual(len(result), 2)


class BCRPSeriesCleaningTests(unittest.TestCase):
    def test_monthly_period_is_parsed(self):
        self.assertEqual(
            utils.parse_bcrp_period("May.2026"), pd.Timestamp("2026-05-01")
        )

    def test_values_are_numeric_and_missing_values_are_preserved(self):
        raw = pd.DataFrame(SAMPLE_PAYLOAD["periods"])

        result = utils.clean_bcrp_series(raw)

        self.assertEqual(result.loc[0, "value"], 100.5)
        self.assertTrue(pd.isna(result.loc[1, "value"]))
        self.assertEqual(result.loc[0, "period"], pd.Timestamp("2024-01-01"))

    def test_required_columns_are_validated(self):
        with self.assertRaisesRegex(ValueError, "missing required columns"):
            utils.clean_bcrp_series(pd.DataFrame({"name": ["Ene.2024"]}))


if __name__ == "__main__":
    unittest.main()
