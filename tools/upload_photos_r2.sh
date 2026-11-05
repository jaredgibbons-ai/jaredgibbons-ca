#!/usr/bin/env bash
# Upload the listing photos to the R2 bucket jg-listing-photos (the Worker serves them at /listing-photos/<name>).
# Run once on a computer that is signed in to Cloudflare (`npx wrangler login`), from the folder that holds the .webp files:
#     bash upload_photos_r2.sh /path/to/folder-with-webp-files
# Safe to re-run (it simply uploads again). Uploads 8 at a time; about 10,000 files, roughly 45 minutes.
set -euo pipefail
DIR="${1:?folder with the .webp files}"
BUCKET="${BUCKET:-jg-listing-photos}"
cd "$DIR"
total=$(ls -1 *.webp | wc -l | tr -d ' ')
echo "Uploading $total files to R2 bucket $BUCKET ..."
ls -1 *.webp | xargs -P 8 -I{} sh -c 'npx --yes wrangler@4 r2 object put "'"$BUCKET"'/{}" --file "{}" --content-type image/webp --cache-control "public, max-age=31536000, immutable" --remote >/dev/null 2>&1 && echo "ok {}" || echo "FAILED {}"' | tee /tmp/r2-upload.log | awk '/^FAILED/{f++} /^ok/{o++} {if((o+f)%250==0) printf "%d done, %d failed\n", o+f, f}'
echo "Finished: $(grep -c '^ok' /tmp/r2-upload.log) uploaded, $(grep -c '^FAILED' /tmp/r2-upload.log) failed (see /tmp/r2-upload.log). Re-run to retry failures."
