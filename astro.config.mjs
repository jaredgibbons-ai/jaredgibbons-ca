import { defineConfig } from 'astro/config';
import fixLinks from './src/integrations/fix-links.mjs';

// Static output. Archived URLs keep their .html suffix (build.format: 'file'), so
// /fort-langley.html is emitted as dist/fort-langley.html. The routing Worker (later phase)
// maps incoming paths through the route manifest; see docs/02-architecture.md.
export default defineConfig({
  site: 'https://jaredgibbons.ca',
  output: 'static',
  trailingSlash: 'never',
  build: { format: 'file', inlineStylesheets: 'auto' },
  devToolbar: { enabled: false },
  integrations: [fixLinks()],
});
