[Go home](./Readme.md)

# MaskSQL Pipeline

Here, we explain each of the pipeline stages used in MaskSQL.

## LimitJson

This stage filters the data entries based on `START` and `LIMIT` variables. For
instance, if `START=50` and `LIMIT=10`, then we filter out the data entries to
retain only entries 50,51,...,59.

## AddResd

This stage receives the `resd_path` as input, which is the path to the output file
of the RESDSQL. Then, it adds the property `tc_original` to each entry that is a
A list of schema items ranked by relevance.

## RankSchemaResd

This stage just changes the format of the schema items from the previous stage by
prefixing them with `COLUMN:`. We also add items of the form `TABLE:` for each
The table is included in the schema items. Moreover, all table and column names are
wrapped in `[]` to prevent problems with column or table names that include
whitespace.

## AddFilteredSchema

This stage adds a YAML representation of the schema based on filtering the items
to only those that are filtered based on the RESDSQL output. This representation
includes the type of columns as well as the foreign key and primary key
information.

## AddSymbolicTable

This stage adds a symbol table to each entry; the symbol table includes a
`to_symbol` dictionary, which maps each schema item to a unique symbolic name. We
use `C1`,`C2` for column names and `T1`,`T2` for table names. A reverse mapping
named `to_name` is also recorded, which maps each symbol to its original value.
These two mappings are then stored in the `symbolic` property of each entry.

## DetectValues

This stage is a prompt-based stage. The arguments specify the property that
should be set in the entry and the type of language model to use. This step creates
a prompt using the schema items from the previous step and the natural language
question. The output of the prompt, which is a list of values, is then set to
property of `values` in each entry.

## LinkValues

This stage uses the `schema_items`, `question`, and `values` to create a prompt.
Then it asks SLM to find the linking information for the literal values in the
question by generating a dictionary with keys being the question terms and values
being the schema items. The result is set to the `value_links` property of the
entries.

## LinkSchema

Similar to the `LinkValue` stage, the goal of this stage is to generate the
linking information for the references to a database other than literal values.
So, we create a prompt using `question`, `schema_items`, and `values` from the
previous step. We include the `values` to exclude them from the output of this
stage. After receiving the output of the LM, we filter out the dictionary by
removing any schema item that is invalid. The result is then set to the property
`schema_links` of the entries.

## AddSymbolicSchema

This step generates the symbolic YAML representation of the `schema` based on
The symbol table that was generated previously. The symbolic schema is then
stored in the property `symbolic.schema` of each entry.

## AddSymbolicQuestion

In this stage, the symbol table, `schema_links`, and `value_links` are used to
generate a symbolic version of the `question`.

To do so, we iterate over the key values in `schema_links` and `value_links`
where keys are terms in the question and values are schema items. Then we look up
each schema item in the symbol table and replace the question term with the
specified symbol.

We record each replaced term in a list and store it in the
`symbolic.masked_terms` property. The symbolic question is stored in the
`symbolic.question` property.

## GenerateSymbolcSql

In this stage, we create a prompt using the `symbolic.question` and
`symbolic.schema`, which is the YAML representation of the symbolic schema. Then
We ask LLM to generate an SQL for the given question. We then store the output
of LLM in the property `symbolic.sql`.

## RepairSymbolicSql

In this stage, we repair the SQL generated in the previous step by prompting the
LLM again with the `symbolic.question`, `symbolic.schema`, and `symbolic.sql`.
Then we ask LLM to detect and repair any errors in the generated SQL. We store
The result of this step is in the `symbolic.repaired_sql` property.

## AddConcreteSql

This stage restores the concrete SQL from the `symbolic.repaired_sql` generated
in the previous step. To do so, we use the reverse symbol table generated in the
previous steps, and then we replace each symbolic token with its original column
name, table name, or literal value. We store the result in the `concrete_sql`
property of each entry.

## ExecuteConcreteSql

This stage executes the `concrete_sql` generated in the previous step on the
database identified by the `db_id` property. We then recorded the result of the
execution, which can be either a result set or an error message in the
`pre_eval.pred_res` property of each entry.

## RepairSql

In this stage, we repair the concrete SQL. To do so, we prompt an SLM with
`question`, `schema`, `concrete_sql`, and the execution result from the previous
step. We ask SLM to inspect the `concrete_sql` and its execution result,
Identify the errors and correct them. Then we store the repaired SQL in the
property `pred_sql`, which is the final result of the pipeline.

## CalcExecAcc

In this stage, we execute the final output of the pipeline, `pred_sql`, on its
corresponding database (`db_id`). We then execute the gold `SQL` which exists
In each entry and compare the results. If the result of `pred_sql` equals 
The result of `SQL`, we record an execution accuracy of 1 for the `pred_sql. Otherwise,
We record a score of zero.
For each entry, we record the execution accuracy in the property `eval.acc`, which 
is either 0 or 1.

## AddInferenceAttack
In this stage, we perform an inference attack on the `symbolic question` to evaluate
robustness of the masked question against inference attacks.
To do so, we create a prompt with `symbolic.question` and `symbolic.schema` and 
Ask LLM to infer the abstract symbols.
The output of LLM is a question where some of the tokens are re-identified.
We store this re-identified question in the `attack` property.

## Results
The final stage of the pipeline is for reporting. 
It prints the evaluation results of the pipeline. 
It does not modify the data entries and only calculates the accuracy, privacy, 
and efficiency metrics, and prints the results.
