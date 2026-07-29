export default function Home() {
  return (
    <main className="pageShell">
      <div className="horizon" aria-hidden="true" />

      <header className="topbar">
        <p className="brand">
          FC<span>/</span>MACRO LAB
        </p>
        <p className="location">RESEARCH LOG · LIMA, PE</p>
      </header>

      <section className="hero" aria-labelledby="page-title">
        <div className="heroCopy">
          <p className="eyebrow">
            <span>Signal 001</span>
            Peruvian macroeconomic research
          </p>

          <h1 id="page-title">
            BCRP
            <span>Nowcasting</span>
            Lab
          </h1>

          <p className="lead">
            Experimental nowcasting models for Peruvian macroeconomic series.
          </p>
          <p className="description">
            This project tracks model predictions, realized values, and
            forecasting performance as the research evolves.
          </p>

          <div className="statusRow">
            <p className="status" aria-label="Project status">
              <span className="statusDot" aria-hidden="true" />
              Research in progress
            </p>
            <p className="coordinates">PE / UTC−05</p>
          </div>
        </div>

        <aside className="signalCard" aria-label="Research note">
          <p className="signalNumber">01</p>
          <div>
            <p className="signalLabel">Current transmission</p>
            <p className="signalText">
              Tracking signals between data releases.
            </p>
          </div>
        </aside>
      </section>

      <footer>
        <p>Data · Models · Forecasts</p>
        <p>Est. 2026</p>
      </footer>
    </main>
  );
}
