# RESDSQL Instructions

TrsutSQL relies on output from the RESDSQL.
So, before running the MaskSQL, you should run the
RESDSQL to generate the required file needed by TrsutSQL.

Since RESDSQL is a legacy code, we will use a separate
virtual environment to run it.

### Requirements

RESDSQL requires python3.8, GCC and CUDA.

On the alliance servers you can use the following command
to load the dependencies:

```shell
module load StdEnv/2020 python/3.8.10
module load gcc cuda
```

### Installation

Run the following command to setup and install the required
python libraries for RESDSQL:

```shell
./install_resd.sh
```

Next, we need to download the

### Run RESDSQL

Use the following command to run the RESDSQL:

```shell
./run_resd.sh
```

This command generates the file `data/resd_output.json`
which is used inside the MaskSQL pipeline.

After successful execution of this script, we can run the
MaskSQL pipeline.
