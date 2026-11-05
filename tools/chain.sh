# Full content chain (generators -> dedupe -> builds -> uniqueness gate -> tests). Run from anywhere: sh tools/chain.sh
set -e
cd /home/claude/jaredgibbons-rebuild
for s in build_snapstats_layers build_community_pages build_snapstats_layers build_type_pages build_condo_pages build_brentwood build_gap_pages build_poco_55plus link_communities build_muse_faq build_sold_layer build_55plus_notes build_typenotes build_acreages build_mobilehomes build_duplex build_nearby build_nearby_buildings build_uniqueness build_mls55 build_muse_faq scrub_research_wording build_sold_layer; do
  echo "== $s"; python3 -I tools/$s.py 2>&1 | tail -2
done
python3 -I tools/apply_archive_rewrites.py 2>&1 | tail -1
python3 -I tools/build_area_thoughts.py --apply 2>&1 | tail -1
python3 -I tools/build_area_near.py 2>&1 | tail -1
python3 -I tools/build_type_near.py 2>&1 | tail -2
python3 -I tools/build_neighbour_compare.py 2>&1 | tail -3
python3 -I tools/build_search_pages.py 2>&1 | tail -2
python3 -I tools/build_new_construction.py 2>&1 | tail -2
python3 -I tools/build_new_construction_subareas.py 2>&1 | tail -2
python3 -I tools/build_idx_embeds.py 2>&1 | head -1
python3 -I tools/dedupe_generated.py 2>&1 | tail -2
python3 -I tools/build_breadcrumbs.py 2>&1 | tail -1
python3 -I tools/build_explore.py 2>&1 | tail -1
npm run build >/tmp/b1.log 2>&1; tail -2 /tmp/b1.log
python3 -I tools/link_pages.py 2>&1 | tail -1
npm run build >/tmp/b2.log 2>&1
python3 -I tools/assign_reviews.py 2>&1 | tail -1
npm run build >/tmp/b3.log 2>&1
python3 -I tools/uniqueness.py --write-gate 2>&1 | tail -3
npm run build >/tmp/b4.log 2>&1; tail -3 /tmp/b4.log
npm test 2>&1 | tail -15
