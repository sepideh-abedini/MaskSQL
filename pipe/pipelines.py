
unmask_pipe_llm = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddSchema(tables_path),
    GenSql("pred_sql", model="openai/gpt-4.1"),
    ExecAccCalc(database_path)
]

unmask_pipe_slm = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddSchema(tables_path),
    GenSql("pred_sql", model=PRIVATE_MODEL),
    ExecAccCalc(database_path),
    PrintResults()
]

value_link_eval = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    DetectValues("values", model=SLM_MODEL),
    LinkValues("value_links", model=SLM_MODEL),
    CopyTransformer("value_links", "filtered_value_links"),
    ValueLinkEval()
]

schema_link_eval = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    CopyTransformer("gold_value_links", "filtered_value_links"),
    AddGoldValues(),
    LinkSchema("schema_links", model=SLM_MODEL),
    CopyTransformer("schema_links", "filtered_schema_links"),
    SchemaLinkEval()
]

gen_sql_eval = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    CopyTransformer("gold_value_links", "value_links"),
    CopyTransformer("gold_value_links", "filtered_value_links"),
    AddGoldValues(),
    CopyTransformer("gold_schema_links", "schema_links"),
    CopyTransformer("gold_schema_links", "filtered_schema_links"),
    AddSymbolicSchema("symbolic", tables_path),
    AddSymbolicQuestion(),
    GenerateSymbolicSql("symbolic", model=LLM_MODEL),
    RepairSymbolicSQL('symbolic', model=LLM_MODEL),
    AddConcreteSql(),
    WrongExecAccOutput(database_path),
    GenSqlEval()
]

full_gold = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    CopyTransformer("gold_value_links", "value_links"),
    CopyTransformer("gold_value_links", "filtered_value_links"),
    AddGoldValues(),
    CopyTransformer("gold_schema_links", "schema_links"),
    CopyTransformer("gold_schema_links", "filtered_schema_links"),
    AddSymbolicSchema("symbolic", tables_path),
    AddSymbolicQuestion(),
    GenerateSymbolicSql("symbolic", model=LLM_MODEL),
    RepairSymbolicSQL('symbolic', model=LLM_MODEL),
    AddConcreteSql(),
    WrongExecAccOutput(database_path),
    RepairSQL('pred_sql', model=SLM_MODEL),
    ExecAccCalc(database_path),
    PrintResults()
]

