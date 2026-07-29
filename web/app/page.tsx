export default function Home() {
  return (
    <main>
      <section className="hero" aria-labelledby="page-title">
        <p className="eyebrow">Peruvian macroeconomic research</p>
        <h1 id="page-title">BCRP Nowcasting Lab</h1>
        <p className="lead">
          Experimental nowcasting models for Peruvian macroeconomic series.
        </p>
        <p className="description">
          This project tracks model predictions, realized values, and
          forecasting performance as the research evolves.
        </p>
        <div className="status" aria-label="Project status">
          <span className="statusDot" aria-hidden="true" />
          Research in progress
        </div>
      </section>
    </main>
  );
}
