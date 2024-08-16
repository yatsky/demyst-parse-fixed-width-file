# Usage

Run the following command.
``` shell
docker build -t fixed-to-delimited .

docker run -v ./data:/app/data fixed-to-delimited data/fixed_width_dataset.txt
```

Complete example.

``` shell
docker run -v ./data:/app/data fixed-to-delimited data/other_fixed_dataset.txt data/custom_output_file_name.csv path/to/spec_file_path.json
```

Output parsed file can be found in `data/output.csv`.

# Test
Run
``` shell
python -m unittest
```

