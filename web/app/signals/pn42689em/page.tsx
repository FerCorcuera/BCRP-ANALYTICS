import type { Metadata } from "next";
import Link from "next/link";

import seriesSnapshot from "@/data/series/PN42689EM.json";

import styles from "./page.module.css";

type Observation = {
  period: string;
  value: number | null;
};

const observations = seriesSnapshot.observations as Observation[];
const availableObservations = observations.filter(
  (observation): observation is { period: string; value: number } =>
    observation.value !== null,
);

const valueFormatter = new Intl.NumberFormat("es-PE", {
  maximumFractionDigits: 0,
});

const dateFormatter = new Intl.DateTimeFormat("es-PE", {
  month: "short",
  year: "numeric",
  timeZone: "UTC",
});

const fullDateFormatter = new Intl.DateTimeFormat("es-PE", {
  day: "numeric",
  month: "long",
  year: "numeric",
  timeZone: "America/Lima",
});

function parsePeriod(period: string) {
  return new Date(`${period}-01T00:00:00Z`);
}

function formatPeriod(period: string) {
  return dateFormatter.format(parsePeriod(period)).replace(".", "");
}

function formatPercent(value: number) {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(1)}%`;
}

function changeBetween(current: number, previous: number) {
  return ((current / previous) - 1) * 100;
}

function buildChart(observationValues: Observation[]) {
  const width = 1000;
  const height = 390;
  const padding = { top: 26, right: 28, bottom: 48, left: 76 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  const numericValues = observationValues
    .map((observation) => observation.value)
    .filter((value): value is number => value !== null);
  const minimum = Math.floor(Math.min(...numericValues) / 1000) * 1000;
  const maximum = Math.ceil(Math.max(...numericValues) / 1000) * 1000;
  const range = maximum - minimum || 1;
  const denominator = Math.max(observationValues.length - 1, 1);

  const pointFor = (observation: Observation, index: number) => {
    if (observation.value === null) {
      return null;
    }

    return {
      x: padding.left + (index / denominator) * chartWidth,
      y:
        padding.top +
        ((maximum - observation.value) / range) * chartHeight,
      value: observation.value,
      period: observation.period,
    };
  };

  const points = observationValues.map(pointFor);
  const segments: Array<Array<NonNullable<ReturnType<typeof pointFor>>>> = [];
  let currentSegment: Array<NonNullable<ReturnType<typeof pointFor>>> = [];

  points.forEach((point) => {
    if (point) {
      currentSegment.push(point);
    } else if (currentSegment.length) {
      segments.push(currentSegment);
      currentSegment = [];
    }
  });
  if (currentSegment.length) {
    segments.push(currentSegment);
  }

  const yTicks = Array.from({ length: 5 }, (_, index) => {
    const value = minimum + ((maximum - minimum) / 4) * index;
    return {
      value,
      y: padding.top + chartHeight - (index / 4) * chartHeight,
    };
  }).reverse();

  const tickIndexes = Array.from(
    new Set([0, 12, 24, observationValues.length - 1]),
  ).filter((index) => index >= 0 && index < observationValues.length);

  return {
    width,
    height,
    padding,
    chartWidth,
    chartHeight,
    segments,
    yTicks,
    xTicks: tickIndexes.map((index) => ({
      x: padding.left + (index / denominator) * chartWidth,
      label: formatPeriod(observationValues[index].period),
    })),
    latestPoint: [...points].reverse().find(Boolean),
  };
}

export const metadata: Metadata = {
  title: "Signal 001 · PN42689EM | BCRP Nowcasting Lab",
  description:
    "Serie realizada del monto total procesado por adquirentes y facilitadores de pago.",
};

export default function Signal001Page() {
  const latest = availableObservations.at(-1)!;
  const previous = availableObservations.at(-2)!;
  const yearAgo = availableObservations.find(
    (observation) =>
      observation.period ===
      `${Number(latest.period.slice(0, 4)) - 1}${latest.period.slice(4)}`,
  );
  const monthlyChange = changeBetween(latest.value, previous.value);
  const annualChange = yearAgo
    ? changeBetween(latest.value, yearAgo.value)
    : null;
  const chart = buildChart(observations);
  const recentObservations = [...availableObservations].reverse().slice(0, 6);

  return (
    <main className={styles.page}>
      <header className={styles.topbar}>
        <Link className={styles.brand} href="/">
          FC<span>/</span>MACRO LAB
        </Link>
        <p>RESEARCH LOG · LIMA, PE</p>
      </header>

      <section className={styles.intro} aria-labelledby="signal-title">
        <div>
          <p className={styles.eyebrow}>
            <span>SIGNAL 001</span>
            Serie realizada
          </p>
          <h1 id="signal-title">{seriesSnapshot.series.display_name}</h1>
          <p className={styles.summary}>
            {seriesSnapshot.series.description} Primera señal del laboratorio,
            publicada antes de incorporar pronósticos experimentales.
          </p>
        </div>

        <dl className={styles.metadata}>
          <div>
            <dt>Código</dt>
            <dd>{seriesSnapshot.series.code}</dd>
          </div>
          <div>
            <dt>Frecuencia</dt>
            <dd>{seriesSnapshot.series.frequency_label}</dd>
          </div>
          <div>
            <dt>Unidad</dt>
            <dd>{seriesSnapshot.series.unit_label}</dd>
          </div>
          <div>
            <dt>Muestra</dt>
            <dd>{seriesSnapshot.observation_count} observaciones</dd>
          </div>
        </dl>
      </section>

      <section className={styles.metrics} aria-label="Resumen de la serie">
        <article>
          <p>Último valor</p>
          <strong>S/ {valueFormatter.format(latest.value)} MM</strong>
          <span>{formatPeriod(latest.period)}</span>
        </article>
        <article>
          <p>Variación mensual</p>
          <strong>{formatPercent(monthlyChange)}</strong>
          <span>respecto al mes anterior</span>
        </article>
        <article>
          <p>Variación anual</p>
          <strong>
            {annualChange === null ? "No disponible" : formatPercent(annualChange)}
          </strong>
          <span>respecto al mismo mes del año previo</span>
        </article>
      </section>

      <section className={styles.chartSection} aria-labelledby="chart-title">
        <div className={styles.sectionHeading}>
          <div>
            <p className={styles.sectionLabel}>OBSERVED TRANSMISSION</p>
            <h2 id="chart-title">Evolución mensual realizada</h2>
          </div>
          <p className={styles.legend}>
            <span aria-hidden="true" />
            BCRPData
          </p>
        </div>

        <figure className={styles.figure}>
          <svg
            viewBox={`0 0 ${chart.width} ${chart.height}`}
            role="img"
            aria-labelledby="series-chart-title series-chart-description"
          >
            <title id="series-chart-title">
              {`Serie mensual ${seriesSnapshot.series.code}`}
            </title>
            <desc id="series-chart-description">
              {`Valores realizados desde ${formatPeriod(
                seriesSnapshot.first_period,
              )} hasta ${formatPeriod(seriesSnapshot.latest_period)}.`}
            </desc>

            {chart.yTicks.map((tick) => (
              <g key={tick.value}>
                <line
                  className={styles.gridLine}
                  x1={chart.padding.left}
                  x2={chart.padding.left + chart.chartWidth}
                  y1={tick.y}
                  y2={tick.y}
                />
                <text
                  className={styles.axisLabel}
                  x={chart.padding.left - 16}
                  y={tick.y + 4}
                  textAnchor="end"
                >
                  {valueFormatter.format(tick.value)}
                </text>
              </g>
            ))}

            {chart.xTicks.map((tick) => (
              <text
                className={styles.axisLabel}
                key={`${tick.x}-${tick.label}`}
                x={tick.x}
                y={chart.height - 12}
                textAnchor="middle"
              >
                {tick.label}
              </text>
            ))}

            {chart.segments.map((segment, index) => (
              <polyline
                className={styles.seriesLine}
                key={index}
                points={segment.map((point) => `${point.x},${point.y}`).join(" ")}
              />
            ))}

            {chart.latestPoint && (
              <g>
                <circle
                  className={styles.latestHalo}
                  cx={chart.latestPoint.x}
                  cy={chart.latestPoint.y}
                  r="11"
                />
                <circle
                  className={styles.latestDot}
                  cx={chart.latestPoint.x}
                  cy={chart.latestPoint.y}
                  r="5"
                />
              </g>
            )}
          </svg>
          <figcaption>
            Valores nominales en millones de soles. Los faltantes, si aparecen
            en futuras actualizaciones, se mostrarán como interrupciones.
          </figcaption>
        </figure>
      </section>

      <div className={styles.lowerGrid}>
        <section className={styles.modelCard} aria-labelledby="models-title">
          <p className={styles.sectionLabel}>MODEL CHANNEL</p>
          <h2 id="models-title">Pronósticos experimentales</h2>
          <p>
            Todavía no se han publicado modelos. Este espacio recibirá el primer
            nowcast únicamente cuando exista una predicción fechada y
            reproducible.
          </p>
          <span>STATUS · AWAITING FIRST MODEL</span>
        </section>

        <section className={styles.tableCard} aria-labelledby="recent-title">
          <p className={styles.sectionLabel}>LATEST OBSERVATIONS</p>
          <h2 id="recent-title">Últimos datos</h2>
          <table>
            <thead>
              <tr>
                <th>Periodo</th>
                <th>Millones S/</th>
              </tr>
            </thead>
            <tbody>
              {recentObservations.map((observation) => (
                <tr key={observation.period}>
                  <td>{formatPeriod(observation.period)}</td>
                  <td>{valueFormatter.format(observation.value)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </div>

      <footer className={styles.sourceNote}>
        <div>
          <p>
            Fuente:{" "}
            <a
              href={seriesSnapshot.series.source_url}
              target="_blank"
              rel="noreferrer"
            >
              BCRPData, serie {seriesSnapshot.series.code}
            </a>
            . Elaboración propia.
          </p>
          <p>
            Datos consultados el{" "}
            {fullDateFormatter.format(new Date(seriesSnapshot.retrieved_at))}.
            Este es un proyecto experimental y no representa al BCRP.
          </p>
        </div>
        <Link href="/">Volver al laboratorio</Link>
      </footer>
    </main>
  );
}
