set -euo pipefail

source .venv/bin/activate

mkdir -p out

python3 NatSQL/table_transform.py \
--in_file ./data/tables.json \
--out_file ./data/resd/test_tables_for_natsql.json \
--correct_col_type \
--remove_start_table \
--analyse_same_column \
--table_transform \
--correct_primary_keys \
--use_extra_col_types \
--db_path ./data/databases

python3 preprocessing.py \
--mode "test" \
--table_path ./data/tables.json \
--input_dataset_path ./data/1_input.json \
--output_dataset_path ./data/resd/preprocessed_test.json \
--db_path ./data/databases \
--target_type "sql"

python3 schema_item_classifier.py \
--batch_size 32 \
--device mps \
--seed 42 \
--save_path "./resdsql/models/text2sql_schema_item_classifier" \
--dev_filepath "./data/resd/preprocessed_test.json" \
--output_filepath "./data/resd/test_with_probs.json" \
--use_contents \
--add_fk_info \
--mode "test"

python3 text2sql_data_generator.py \
--input_dataset_path "./data/resd/test_with_probs.json" \
--output_dataset_path "./data/resd_output.json" \
--topk_table_num 4 \
--topk_column_num 5 \
--mode "test" \
--use_contents \
--add_fk_info \
--output_skeleton \
--target_type "sql"
