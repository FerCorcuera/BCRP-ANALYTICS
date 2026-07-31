"""Export approved BCRPData series to versioned JSON files for the web app."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from bcrp_analytics.utils import clean_bcrp_series, get_bcrp_series_payload

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIRECTORY = REPOSITORY_ROOT / "web" / "data" / "series"

SERIES_CATALOG = {
    "PN42689EM": {
        "signal_id": "signal-001",
        "display_name": "Monto total del mercado de adquirencia",
        "description": (
            "Monto total de operaciones procesadas por los adquirentes y "
            "facilitadores de pago."
        ),
        "frequency": "monthly",
        "frequency_label": "Mensual",
        "unit": "millions_of_soles",
        "unit_label": "Millones de soles",
    }
}


def build_web_series_payload(
    series_code: str,
    retrieved_at: datetime | None = None,
) -> dict[str, Any]:
    """Build the stable JSON contract consumed by the Next.js application."""
    if series_code not in SERIES_CATALOG:
        supported = ", ".join(sorted(SERIES_CATALOG))
        raise ValueError(
            f"Unsupported web series {series_code}. Supported series: {supported}"
        )

    raw_payload = get_bcrp_series_payload(series_code)
    cleaned = clean_bcrp_series(pd.DataFrame(raw_payload["periods"])).sort_values(
        "period"
    )
    if cleaned.empty:
        raise ValueError(f"BCRPData returned no observations for {series_code}")

    series_config = SERIES_CATALOG[series_code]
    api_config = raw_payload.get("config", {})
    api_series = api_config.get("series", [])
    official_name = (
        api_series[0].get("name")
        if api_series and isinstance(api_series[0], dict)
        else series_config["display_name"]
    )

    retrieval_time = retrieved_at or datetime.now(timezone.utc)
    if retrieval_time.tzinfo is None:
        retrieval_time = retrieval_time.replace(tzinfo=timezone.utc)
    retrieval_time = retrieval_time.astimezone(timezone.utc).replace(microsecond=0)

    observations = [
        {
            "period": row.period.strftime("%Y-%m"),
            "value": None if pd.isna(row.value) else float(row.value),
        }
        for row in cleaned.itertuples(index=False)
    ]

    return {
        "schema_version": 1,
        "series": {
            "code": series_code,
            "signal_id": series_config["signal_id"],
            "display_name": series_config["display_name"],
            "official_name": official_name,
            "description": series_config["description"],
            "frequency": series_config["frequency"],
            "frequency_label": series_config["frequency_label"],
            "unit": series_config["unit"],
            "unit_label": series_config["unit_label"],
            "source": "BCRPData",
            "source_url": (
                "https://estadisticas.bcrp.gob.pe/estadisticas/series/"
                f"mensuales/resultados/{series_code}/html"
            ),
        },
        "retrieved_at": retrieval_time.isoformat().replace("+00:00", "Z"),
        "first_period": observations[0]["period"],
        "latest_period": observations[-1]["period"],
        "observation_count": len(observations),
        "observations": observations,
    }


def write_web_series(
    series_code: str,
    output_directory: Path = DEFAULT_OUTPUT_DIRECTORY,
) -> Path:
    """Retrieve one approved series and write its web JSON artifact."""
    payload = build_web_series_payload(series_code)
    output_directory.mkdir(parents=True, exist_ok=True)
    output_path = output_directory / f"{series_code}.json"
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export an approved BCRPData series for the web app."
    )
    parser.add_argument(
        "series_code",
        nargs="?",
        default="PN42689EM",
        choices=sorted(SERIES_CATALOG),
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=DEFAULT_OUTPUT_DIRECTORY,
    )
    args = parser.parse_args()

    output_path = write_web_series(args.series_code, args.output_directory)
    print(f"Wrote {output_path.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
    main()
