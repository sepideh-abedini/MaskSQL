from os import pathconf

from openai import files

from src.taxonomy.parse.lexer import reserved
from src.util.json_utils import read_json, write_json


def finder(path1, path2):
    full= read_json(path1)
    category= read_json(path2)
    diff = []
    for items in full:
        if items not in category:
            diff.append(items)
    write_json("data/EA_diff", diff)

    for items in category:
        if items not in full:
            print(items)
    return diff

def analyser(arr):
    path= "data/full/19_RepairSQL.json"
    file = read_json(path)
    res=[]
    for items in arr:
        for records in file:
            if records['question_id'] == items:
                res.append({"id": records['question_id'], 'question': records['question'],"gold": records['SQL'], "pred": records['pred_sql'] })

    write_json("data/EA_sql_diff", res)






def main():
    path1 = "data/full/EA_failures.json"
    path2 = "data/category/EA_failures.json"

    res= finder(path1, path2)
    analyser(res)


if __name__=='__main__':
    main()
