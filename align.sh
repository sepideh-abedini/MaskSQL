set -euo pipefail

source .venv/bin/activate

python3 align_schema_link.py \
--input "./out/resdsql_test.json" \
--output "./out/schema_links.txt"
