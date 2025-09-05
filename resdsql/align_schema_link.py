import argparse
import asyncio
import json
import os
from typing import List

import tqdm.asyncio as tqdm
from openai import AsyncClient
from pydantic import BaseModel

DATA_DIR = "data"

PROMPT = """
I give you a NL question, and a list of database schema items ranked by their relevance to the given NL question.
Generate a mapping in the given format that maps n-grams in the question that reference a schema item.
Each schema item is of the form table_name.column_name of the underlying database.
Schema items are sorted in descending order of relevance to the question. 
First we sort the most relevant tables and then we sort the most relevant columns within each table.
We include the top 4 tables and top 5 columns within each table.
So, we include the columns of the first table (the most relevant table), followed by the columns of the second table
and so on. Columns of the first table are sorted in descending order of relevance to the question.
Each mapping item should be in the following format:
'table_name.column_name="n-gram in the question that references the schema item"'
Example:

Input:
NL: "Count the number of stores the chain South has"
SQL: "SELECT count(*) FROM department_stores AS T1 JOIN department_store_chain AS T2 ON T1.dept_store_chain_id  =  T2.dept_store_chain_id WHERE T2.dept_store_chain_name  =  \"South\""
SchemaItems: [ 
      "department_stores.*",
      "department_stores.dept_store_chain_id",
      "department_stores.dept_store_id",
      "department_stores.store_name",
      "department_stores.department_name",
      "department_store_chain.dept_store_chain_name",
      "department_store_chain.dept_store_chain_id",
      "departments_store_chain.*",
      "addresses.address_details",
      "addresses.address_id",
      "addresses.*",
      "products.product_type_code",
      "products.product_name",
      "products.product_price",
      "products.product_id",
      "products.*",
]

Hint:
Database Schema: 
addresses:
  address_details: text
  address_id: number
customers:
  customer_address: text
  customer_id: number
  customer_name: text
department_store_chain:
  dept_store_chain_id: number
  dept_store_chain_name: text
department_stores:
  dept_store_chain_id:
    foreign_key: department_store_chain.dept_store_chain_id
    type: number
  dept_store_id: number
  store_address: text
  store_email: text
  store_name: text
  store_phone: text
departments:
  department_id: number
  department_name: text
  dept_store_id:
    foreign_key: department_stores.dept_store_id
    type: number
products:
  product_id: number
  product_name: text
  product_price: number
  product_type_code: text
supplier_addresses:
  address_id:
    foreign_key: addresses.address_id
    type: number
  date_from: time
  date_to: time
  supplier_id:
    foreign_key: suppliers.supplier_id
    type: number
suppliers:
  supplier_id: number
  supplier_name: text
  supplier_phone: text
  
Output:
Mapping: ['department_stores.*="number of stores"', 'department_store_chain.dept_stor_chain_name="chain South"']

In this example, in addition to the NL question and ranked schema items, we also included the database schema and the 
SQL query to help you better understand the task. However, these hints are not available for further questions.
In the given example, we have a total of 8 tables in the database. However, we selected the tables 'department_stores',
'department_store_chain', 'addresses', and 'products' as the most relevant tables to the question in order of the highest 
relevance to the question. We always pick top 4 tables but in this example we only need the first two tables.  
So, we might include some tables that are not used in the question at all.
This is the same for columns as well. We also pick the top 5 columns within each table. So, again we might 
include some columns that are not relevant to the question.
In the SchemaItems list, first columns of the 'department_stores', 'department_store_chain', 'addresses', and 'products' 
followed by 'departments_store_chain.*', 'addresses.*', and 'products.*'. 
The first five items are columns of 'department_stores'.
These columns are then sorted in descending order of relevance to the question too.
Note that, columns are sorted for each table and not across the tables.
For instance, "department_stores.dept_store_id" listed before "department_store_chain.dept_store_chain_name" not because 
it has more relevance probability but because it is a column of 'department_stores' table and 
all columns of 'department_stores' table are listed before 'department_store_chain' table.

Now, find the schema linking as the given format for the following NL question, SQL query and DB schema:
NL: {}
SchemaItems: {}
"""


class ResdSQLOutput(BaseModel):
    db_id: str
    question: str
    tc_original: List[str]


async def apply_async(fun, items, desc=""):
    semaphore = asyncio.Semaphore(10)

    async def sem_task(item):
        async with semaphore:
            return await fun(item)

    tasks = [asyncio.create_task(sem_task(item)) for item in items]
    results = await tqdm.tqdm.gather(*tasks, total=len(items), desc=desc)
    return results


async def get_schema_link(entry: ResdSQLOutput) -> str:
    client = AsyncClient(
        organization=os.getenv("OPENAI_GROUP_ID"),
        project=os.getenv("OPENAI_PROJ_ID"),
        timeout=int(os.getenv("OPENAI_TIMEOUT", 60))
    )
    msg = PROMPT.format(entry.question, entry.tc_original)
    with open("out/prompts.txt", "a") as f:
        f.write("######################\n" + msg + "\n")
    response = await client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "user",
                "content": msg,
            },
        ],
    )
    return response.choices[0].message.content


async def gen(input, output):
    with open(input) as f:
        data = json.load(f)
    open("out/prompts.txt", "w").close()
    entries = []
    aligned_output = []
    for entry in tqdm.tqdm(data, total=len(data)):
        entry = ResdSQLOutput.model_validate(entry)
        entries.append(entry)

    aligned_output = await apply_async(get_schema_link, entries, desc="Schema linking")
    # aligned_schema_link = await get_schema_link(entry)
    # aligned_output.append(aligned_schema_link)
    with open(output, "w") as f:
        f.write("\n".join(aligned_output))


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()
    await gen(args.input, args.output)


if __name__ == '__main__':
    asyncio.run(main())
