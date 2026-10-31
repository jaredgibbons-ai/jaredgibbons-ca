-- Lead storage for the forms Worker (src/worker/forms.js). Apply with:
--   wrangler d1 migrations apply <database-name>   (after the D1 database is created and bound as LEADS_DB)
CREATE TABLE IF NOT EXISTS leads (
  id          TEXT PRIMARY KEY,
  kind        TEXT NOT NULL,
  received_at TEXT NOT NULL,
  page        TEXT NOT NULL DEFAULT '',
  fields      TEXT NOT NULL            -- JSON of the validated fields
);
CREATE INDEX IF NOT EXISTS leads_received ON leads (received_at);
