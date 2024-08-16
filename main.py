import csv
import json
import click
from attrs import define


@define
class Config:
    field_names: list[str]
    offsets: list[int]
    in_file_encoding: str
    out_file_encoding: str
    include_header: bool


@define
class FileParser:
    config_path: str | click.Path
    _config: Config | None = None

    @property
    def config(
        self,
    ) -> Config:
        if not self._config:
            # avoids `eval`
            map = {"False": False, "True": True}
            with open(self.config_path) as f:
                spec = json.load(f)

            self._config = Config(
                field_names=spec['ColumnNames'],
                offsets=[int(i) for i in spec['Offsets']],
                in_file_encoding=spec['FixedWidthEncoding'],
                out_file_encoding=spec['DelimitedEncoding'],
                include_header=map[spec['IncludeHeader']],
            )

        return self._config

    def _parse_fixed_length_line(self, line: str, offsets: list[int]) -> list[str]:
        parsed_data = []
        cur_pos = 0

        for length in offsets:
            field_data = line[cur_pos : cur_pos + length].strip()
            parsed_data.append(field_data)

            cur_pos += length

        return parsed_data

    def fixed_length_to_csv(
        self, in_file: str | click.Path, out_file: str | click.Path
    ) -> None:
        with open(in_file, encoding=self.config.in_file_encoding) as infile, open(
            out_file, "w", newline='', encoding=self.config.out_file_encoding
        ) as outfile:
            writer = csv.writer(outfile)

            if self.config.include_header:
                writer.writerow(self.config.field_names)
                next(infile)

            for line in infile:
                parsed_line = self._parse_fixed_length_line(line, self.config.offsets)
                writer.writerow(parsed_line)


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', default="data/output.csv", type=click.Path())
@click.argument(
    'config_path', default="./code-kata/spec.json", type=click.Path(exists=True)
)
def main(config_path: click.Path, input_file: click.Path, output_file: click.Path):
    parser = FileParser(config_path=config_path)
    parser.fixed_length_to_csv(input_file, output_file)


if __name__ == "__main__":
    main()
