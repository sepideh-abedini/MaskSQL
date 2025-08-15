set -euo pipefail

source .venv/bin/activate

mkdir -p out

python3 NatSQL/table_transform.py \
--in_file ../msc/data/dev/dev_tables.json \
--out_file ./out/test_tables_for_natsql.json \
--correct_col_type \
--remove_start_table \
--analyse_same_column \
--table_transform \
--correct_primary_keys \
--use_extra_col_types \
--db_path ../msc/data/dev/dev_databases

python3 preprocessing.py \
--mode "test" \
--table_path ../msc/data/dev/dev_tables.json \
--input_dataset_path ../msc/data/dev/dev.json \
--output_dataset_path ./out/preprocessed_test.json \
--db_path ../msc/data/dev/dev_databases \
--target_type "sql"

python3 schema_item_classifier.py \
--batch_size 32 \
--device mps \
--seed 42 \
--save_path "./models/text2sql_schema_item_classifier" \
--dev_filepath "./out/preprocessed_test.json" \
--output_filepath "./out/test_with_probs.json" \
--use_contents \
--add_fk_info \
--mode "test"

python3 text2sql_data_generator.py \
--input_dataset_path "./out/test_with_probs.json" \
--output_dataset_path "./out/resdsql_test.json" \
--topk_table_num 4 \
--topk_column_num 5 \
--mode "test" \
--use_contents \
--add_fk_info \
--output_skeleton \
--target_type "sql"
