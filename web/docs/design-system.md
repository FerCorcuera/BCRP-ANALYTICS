# BCRP Nowcasting Lab — product and design system

## Purpose

BCRP Nowcasting Lab is a public research log for experimental nowcasting of
Peruvian macroeconomic and payment-system time series. It will document:

- realized values published through BCRPData;
- predictions produced before the corresponding realization is known;
- model versions and prediction dates;
- forecasting performance as evidence accumulates; and
- methodological notes and limitations.

The site is not an official BCRP product and must not imply endorsement or
affiliation.

## Current product scope

The current milestone is intentionally narrow:

1. Maintain a simple landing page.
2. Publish one realized monthly series as `Signal 001`.
3. Show the latest observation and transparent metadata.
4. Reserve a clearly labeled area for future experimental models.
5. Add forecasts only after a real prediction artifact exists.

No database, authentication, live model endpoint, or automated pipeline is
required for this milestone.

## Visual direction

The identity combines quantitative research with restrained
science-fiction/anime editorial cues. Inspiration should be expressed through
typography, composition, signal labels, timestamps, and technical metadata—not
through copied characters, logos, or artwork.

### Palette

| Token | Value | Use |
| --- | --- | --- |
| Cream | `#f3f0e8` | Primary background |
| Paper | `#fbfaf6` | Cards and raised surfaces |
| Ink | `#172238` | Primary text |
| Muted | `#6d7788` | Secondary text and metadata |
| Signal blue | `#176bff` | Primary accent and realized series |
| Deep blue | `#16488f` | Supporting accent |
| Pale blue | `#dce9ff` | Quiet emphasis and chart guides |
| Line | `#d4d9e1` | Borders and dividers |

### Typography

- Zilla Slab is the primary family.
- Large headings may use italic weight selectively for an editorial,
  time-travel-inspired character.
- Labels such as `SIGNAL 001`, series codes, frequencies, and timestamps use
  compact uppercase styling.
- Body copy should remain calm and highly readable.

### Layout principles

- Prefer generous whitespace and a strong information hierarchy.
- Use blue sparingly so it retains meaning.
- Avoid generic dashboard chrome until multiple signals genuinely require it.
- Technical motifs must remain subtle and never reduce readability.
- Mobile layouts must preserve the series title, latest value, chart, and
  source attribution.

## Data presentation rules

For every realized series, display:

- official series name;
- BCRPData series code;
- frequency and unit;
- first and latest available period;
- data-as-of or retrieval date;
- a direct link to the official source; and
- `Fuente: BCRPData. Elaboración propia.`

Observed data uses a solid signal-blue line. Future predictions will use
visually distinct dashed lines and must identify the model, target period, and
prediction date.

Missing values must appear as gaps. They must not be silently interpolated.
Revised observations should retain enough metadata to distinguish the latest
available value from a value known at an earlier prediction date.

## Signal 001

The first published series is:

- Code: `PN42689EM`
- Name: Monto total de operaciones procesadas por los adquirentes y
  facilitadores de pago
- Frequency: Monthly
- Unit: Millions of soles
- Source: BCRPData

The first version shows realized observations only. The models section must say
that no experimental forecasts have been published yet.

## Future prediction record

Each stored prediction should eventually include:

- `series_code`
- `model_id`
- `model_version`
- `prediction_date`
- `target_period`
- `predicted_value`
- `realized_value`
- `realized_vintage`

This prevents predictions from being rewritten after the realized value becomes
known and supports honest performance tracking.

## Delivery roadmap

1. Realized `Signal 001` page.
2. Reproducible Python export from `bcrp_analytics`.
3. First manually published prediction.
4. Realized-versus-predicted overlay.
5. Prediction history and error metrics.
6. Scheduled retrieval and inference.
7. Additional series and model comparison.
