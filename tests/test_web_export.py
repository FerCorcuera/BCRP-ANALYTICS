import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from scripts import export_web_series

RAW_PAYLOAD = {
    "config": {
        "series": [
            {
                "name": "Official acquisition market series",
                "dec": "0",
            }
        ]
    },
    "periods": [
        {"name": "Feb.2024", "values": ["110.25"]},
        {"name": "Ene.2024", "values": ["100"]},
    ],
}


class WebSeriesExportTests(unittest.TestCase):
    @patch("scripts.export_web_series.get_bcrp_series_payload")
    def test_payload_is_sorted_and_contains_source_metadata(self, mock_retrieve):
        mock_retrieve.return_value = RAW_PAYLOAD

        payload = export_web_series.build_web_series_payload(
            "PN42689EM",
            retrieved_at=datetime(2026, 7, 31, 12, 30, tzinfo=timezone.utc),
        )

        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["series"]["code"], "PN42689EM")
        self.assertEqual(payload["series"]["signal_id"], "signal-001")
        self.assertEqual(payload["first_period"], "2024-01")
        self.assertEqual(payload["latest_period"], "2024-02")
        self.assertEqual(payload["observation_count"], 2)
        self.assertEqual(payload["observations"][0]["value"], 100.0)
        self.assertEqual(payload["retrieved_at"], "2026-07-31T12:30:00Z")
        self.assertIn("PN42689EM", payload["series"]["source_url"])

    def test_only_catalogued_series_can_be_exported(self):
        with self.assertRaisesRegex(ValueError, "Unsupported web series"):
            export_web_series.build_web_series_payload("UNKNOWN")


if __name__ == "__main__":
    unittest.main()
