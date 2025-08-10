from pipe.processor.list_processor import JsonListProcessor
from pipe.processor.printer import DataPrinter


def print_color(text, color="green"):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
    }
    RESET = "\033[0m"
    color_code = colors.get(color.lower(), "")
    print(f"{color_code}{text}{RESET}")


class PrintResults(DataPrinter):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.pre_score = 0
        self.masked = 0
        self.total = 0
        self.total_toks = 0

    def _post_run(self):
        print(f"PreScore: {self.pre_score}/{self.total}")
        print(f"Score: {self.score}/{self.total}")
        print(f"Masked: {self.masked}/{self.total}")
        # print(f"Toks: {self.total_toks}/{self.total}")

    async def _process_row(self, row):
        self.total += 1
        # self.total_toks += row['total_toks']
        exec_acc = row['eval']['acc']
        self.score += exec_acc
        pre_score = row['pre_eval']['acc']
        self.pre_score += pre_score
        # self.masked += row['symbolic']['masked']
        # if exec_acc == 1:
        #     return
        print(f"\nEntry #{self.total}" + "-" * 100)
        print(f"EXEC ACC: {exec_acc}")
        # return
        # print(f"MASKED: {row['symbolic']['masked']}")
        # if "symbolic" in row:
        #     print(f"Masked Question: {row['symbolic']['question']}")
        # print_color(f"Question: {row['question']}", "green")
        # print_color(f"Gold: {row['query']}", "green")
        # print(f"Pred: {row['pred_sql']}")
        # print(f"Conc: {row['concrete_sql']}")
        # print(f"Masked SQL: {row['symbolic']['sql']}")
        # print(f"Schema Items: {row['schema_items']}")
        # print(f"Schema Links: {row['schema_links']}")
        # print(f"Filtered Schema Links: {row['filtered_schema_links']}")
        # print(f"Value Links: {row['value_links']}")
        # print(f"Filtered Value Links: {row['filtered_value_links']}")
        # print("\n")
        # print("RESULTS: ")
        # if row['eval']['acc'] == 0:
        #     print_color(f"GOLD RES: {row['eval']['gold']}", "green")
        #     print_color(f"PRED RES: {row['eval']['pred']}", "red")
        #     print_color(f"PRED ERR: {row['eval']['pred_err']}", "red")
        # print("\n")
        # print("#" * 10)
        # print(f"Schema:\n {row['schema']}")
        # print("#" * 10)
        # print("#" * 10)
        # print(f"Symbolic Schema:\n {row['symbolic']['schema']}")
        # print("#" * 10)
