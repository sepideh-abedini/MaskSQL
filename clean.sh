DATA_DIR=$1
find "$DATA_DIR" -maxdepth 1 -type f -name '[0-9]*_*' ! -name '1_*' -delete
