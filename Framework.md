[Go home](./Readme.md)

# Framework

MaskSQL is implemented on top of an LM-enabled pipeline framework which we explain here.

We start to dig into how the framework works, starting from the `main.py`.

Here, we construct a pipeline by specifying the steps of the pipeline.
Then, we can run the pipeline on a dataset by specifying the path of the input file.
At the first stage of the pipeline, the processing is done on the input file,
and output is saved into a file labeled with the name of the stage. 
For instance, if the first stage of the pipeline is `LimitJson`, then 
pipeline first reads the `1_input.json` (given as the argument of the `run` function call),
and write the result of the processing to the file `2_LimitJson.json`. 

> Note that each stage increases the prefix number of its input file.

Each subsequent stage then reads the file of the previous stage, and similarly 
saves the results into the output file.

## JsonListTransformer
This class is the parent of all classes that implement a pipeline stage.
The behavior of each pipeline stage is specified by implementing the abstract
 `_process_row` function.
This function receives a single dataset entry and returns the processed row.
For instance, the `SchemaLinking` stage adds a field `schema_links` to the row.
So, to put it simply, each pipeline stage reads a file that includes a list of 
entries (JSON objects), applies the `process_row` on each entry, and saves the 
return the result of this function to an output file.

## PromptProcessor
Prompt processor is a subclass of `JsonListTransformer` that sends a prompt 
to the language model as a part of processing a JSON object.
The behavior of a `PromptProcessor` is specified by implementing the `_get_prompt`
and `_process_output` functions.
`_get_prompt` receives a row and returns the prompt that should be sent to the
LM.
`_process_output` returns a processed version of the LM output and returns
the result.
The output of the `_process_output` is then set to the field `prop_name`.

So, in summary, a prompt processor first calls `_get_prompt(row)` to generate the prompt.
The prompt is sent to LM, and the output is processed by `_process_output`, which 
is then set to the field `prop_name`.

### Usage stats
The `PromptProcessor` keeps track of the `total_latency` and `total_toks` used.
So, in the input to the whole pipeline, we set `total_latency` and `total_toks`
fields to zero. 
Each `PromptProcessor` then adds the time and tokens spent to these total values.
