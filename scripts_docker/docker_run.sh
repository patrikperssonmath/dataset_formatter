docker run -u $(id -u):$(id -g) --rm -it \
 -v $1:/database:rw \
 -v $(pwd):/workspace:rw \
 -w /workspace \
  dataset_formatter
