import argparse

from preprocessing import main as preprocess
from schema_item_classifier import classify_schema
from text2sql_data_generator import generate_text2sql_data

opts = {
    "mode": "test",
    "table_path": "./data/spider/tables.json",
    "input_dataset_path": "./data/spider/dev.json",
    "natsql_dataset_path": "./NatSQL/NatSQLv1_6/train_spider-natsql.json",
    "output_dataset_path": "./data/preprocessed_data/preprocessed_test.json",
    "db_path": "./database",
    "target_type": "sql",
    "batch_size": 8,
    "gradient_descent_step": 4,
    "device": "mps",
    "learning_rate": 3e-5,
    "gamma": 1.0,
    "alpha": 1.0,
    "epochs": 128,
    "patience": 32,
    "seed": 42,
    "save_path": "./models/text2sql_schema_item_classifier",
    "tensorboard_save_path": None,
    "train_filepath": "data/pre-processing/preprocessed_train_spider.json",
    "dev_filepath": "./data/preprocessed_data/preprocessed_test.json",
    "output_filepath": "./data/preprocessed_data/test_with_probs.json",
    "model_name_or_path": "roberta-large",
    "use_contents": True,
    "add_fk_info": True,
}

other_opts = {
    "input_dataset_path": "./data/preprocessed_data/test_with_probs.json",
    "output_dataset_path": "./data/preprocessed_data/resdsql_test.json",
    "topk_table_num": 4,
    "topk_column_num": 5,
    "mode": "test",
    "noise_rate": 0.08,
    "use_contents": True,
    "add_fk_info": True,
    "output_skeleton": True,
    "target_type": "sql"
}




class AttrDict(dict):
    def __getattr__(self, item):
        return self[item]


def parse_option():
    # opt = parser.parse_args()

    return AttrDict(opts)


def main():
    opts = parse_option()
    preprocess(opts)
    classify_schema(opts)
    generate_text2sql_data(AttrDict(other_opts))


if __name__ == '__main__':
    main()
