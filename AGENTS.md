# Collaboration rules

These instructions apply to automated coding agents working in this
repository.

## Ownership and scope

- The notebooks, research code, datasets, estimations, and existing project
  structure belong to the repository owner.
- Do not modify, move, delete, reorganize, or refactor research work unless the
  owner explicitly requests it.
- Web work should remain inside `web/` unless a small supporting change outside
  that directory is explicitly approved.
- Changes to `bcrp_analytics/` must be requested or directly necessary for an
  approved data workflow. Keep them backward compatible when practical.

## Git workflow

- Start meaningful web work in a short-lived branch named `codex/web-*`.
- Codex may create local commits after validating the relevant work.
- Keep commits focused and use clear messages.
- Preserve the owner's configured Git name and email.
- Add `Assisted-by: Codex` to commits created by Codex.
- Do not push unless the owner explicitly authorizes that push.
- Do not push directly to `main`.
- The owner publishes branches, opens pull requests, reviews previews, and
  decides when to merge.
- Never merge a pull request on the owner's behalf unless separately and
  explicitly authorized.

## Web product rules

- The web application is an experimental research interface, not an official
  BCRP product.
- Never present estimated, illustrative, or placeholder values as observed
  data.
- Clearly distinguish realized values from forecasts and nowcasts.
- Every published BCRP series must show its code, frequency, unit, source link,
  and data-as-of date.
- Attribute reproduced data to BCRPData and label transformations as the
  author's own work.
- Do not imply BCRP sponsorship, endorsement, or affiliation.
- Ask before adding a database, authentication, API service, analytics,
  external UI library, or other significant dependency.
- Keep secrets and credentials out of source control and conversation output.

## Quality and communication

- Explain material architectural choices before making them.
- Prefer the smallest useful implementation that can grow with the research.
- Preserve accessibility and responsive behavior.
- Run relevant tests and a production build before committing web changes.
- Report limitations honestly, especially short samples, revisions, missing
  observations, and experimental model status.
