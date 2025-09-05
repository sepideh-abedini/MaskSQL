[Go home](./Readme.md)

# Framework

MaskSQL is implemented on top of an LM-enabled pipeline framework which we explain here.

We start to dig into how the framework works, starting from the `main.py`.

To define a pipeline, first we create a list of pipeline stages:
```python
# Line 27
def create_pipeline_stages(conf: MaskSqlConfig):
    mask_pipe = [
        LimitJson(),
        AddResd(conf.resd_path),
        RankSchemaResd(conf.tables_path),
.
.
.
```
Then, we can run the pipeline on a dataset by specifying the path of the input file:
```python
# line 57
    conf = MaskSqlConfig(args.data)
    pipeline_stages = create_pipeline_stages(conf)
    pipeline = Pipeline(pipeline_stages)
    await pipeline.run(conf.input_path)
```

Each stage of the pipeline reads a json file which is a list of dataset entries, 
applies a processing, and then writes the result back into an json file.
The input to the pipe line is specified by the path of the input json file.
For instance, if the first stage of the pipeline is `LimitJson`, then 
pipeline first reads the `1_input.json` (given as the argument of the `run` function call),
and write the result of the processing to the file `2_LimitJson.json`. 
The subsequent steps, then read the output of the previous stage and write the result into a json
file for the next stage.

> Note that each stage increases the prefix number of its input file.

## JsonListTransformer
This class is the parent of all classes that implement a pipeline stage.
The behavior of each pipeline stage is specified by implementing the abstract
 `_process_row` function:
```python
    @abstractmethod
    async def _process_row(self, row: Dict) -> Dict:
        pass
```
This function receives a single dataset entry and returns the updated row.
For instance, the `SchemaLinking` stage processes the row and adds a field `schema_links` to the row.

So, to put it simply, each pipeline stage reads a file that includes a list of 
entries (JSON objects), applies the `process_row` on each entry, and saves the 
return the result of this function to an output file.

## PromptProcessor
Prompt processor is a subclass of `JsonListTransformer` that sends a prompt 
to the language model as a part of processing a JSON object.
The behavior of a `PromptProcessor` is specified by implementing the `_get_prompt`
and `_process_output` functions:
```python
 @abstractmethod
 def _process_output(self, row, output):
  pass

 @abstractmethod
 def _get_prompt(self, row):
  pass
```

`_get_prompt` receives a row and returns the prompt that should be sent to the
LM.
`_process_output` returns a processed version of the LM output and returns
the result.
Each `PromptProcessor` also has a property `prop_name` which is the key of the property 
where the result of this stage should be saved for each entry.

So, in summary, a prompt processor first calls `_get_prompt(row)` to generate the prompt.
The prompt is sent to LM, and the output is processed by `_process_output`, which 
is then set to the field `prop_name`.

### Usage stats
The `PromptProcessor` keeps track of the `total_latency` and `total_toks` used.
So, in the begining of the pipeline, we set `total_latency` and `total_toks`
fields to zero. 
Each `PromptProcessor` then adds the time and tokens spent to these total values.
