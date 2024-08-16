import unittest
import json
import os
import csv
from main import FileParser


class TestFixedLengthFileParser(unittest.TestCase):

    def test__parse_fixed_line(self):
        parser = FileParser()

        offsets = [1, 2, 3]
        line1 = "A12XYZ"

        expected1 = ["A", "12", "XYZ"]

        self.assertEqual(
            parser._parse_fixed_length_line(line=line1, offsets=offsets), expected1
        )

        offsets = [1]
        line2 = "A"

        expected2 = ["A"]

        self.assertEqual(
            parser._parse_fixed_length_line(line=line2, offsets=offsets), expected2
        )

        offsets = [0]
        line2 = "A"

        expected2 = ["A"]

        self.assertNotEqual(
            parser._parse_fixed_length_line(line=line2, offsets=offsets), expected2
        )

        offsets = [-1]
        line2 = "A"

        expected2 = ["A"]

        self.assertNotEqual(
            parser._parse_fixed_length_line(line=line2, offsets=offsets), expected2
        )

        # commas in column
        offsets = [3, 2]
        line2 = "1,122"

        expected2 = ["1,1", "22"]

        self.assertEqual(
            parser._parse_fixed_length_line(line=line2, offsets=offsets), expected2
        )

    def test_fixed_length_to_csv_with_header(self):
        spec = {
            "ColumnNames": [
                "f1",
                "f2",
                "f3",
                "f4",
                "f5",
                "f6",
                "f7",
                "f8",
                "f9",
                "f10",
            ],
            "Offsets": ["5", "12", "3", "2", "13", "7", "10", "13", "20", "13"],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "True",
            "DelimitedEncoding": "utf-8",
        }
        spec_file = "spec.json"
        with open(spec_file, "w") as f:
            f.write(json.dumps(spec))

        parser = FileParser(config_path=spec_file)

        input_lines = [
            "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10",
            "11111222222222222333445555555555555666666677777777778888888888888999999999999999999990000000000000",
        ]
        expected_csv = [
            ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10"],
            [
                "11111",
                "222222222222",
                "333",
                "44",
                "5555555555555",
                "6666666",
                "7777777777",
                "8888888888888",
                "99999999999999999999",
                "0000000000000",
            ],
        ]

        input_file = "test_input.txt"
        with open(input_file, 'w', encoding=parser.config.in_file_encoding) as f:
            f.write('\n'.join(input_lines))

        output_file = "test_output.txt"

        parser.fixed_length_to_csv(in_file=input_file, out_file=output_file)

        with open(output_file, 'r', encoding=parser.config.out_file_encoding) as f:
            reader = csv.reader(f)
            lines = list(reader)

        self.assertEqual(lines, expected_csv)

        os.remove(input_file)
        os.remove(output_file)
        os.remove(spec_file)

    def test_fixed_length_to_csv_no_header(self):
        spec = {
            "ColumnNames": [
                "f1",
                "f2",
                "f3",
                "f4",
                "f5",
                "f6",
                "f7",
                "f8",
                "f9",
                "f10",
            ],
            "Offsets": ["5", "12", "3", "2", "13", "7", "10", "13", "20", "13"],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "False",
            "DelimitedEncoding": "utf-8",
        }
        spec_file = "spec.json"
        with open(spec_file, "w") as f:
            f.write(json.dumps(spec))

        parser = FileParser(config_path=spec_file)

        input_lines = [
            "11111222222222222333445555555555555666666677777777778888888888888999999999999999999990000000000000",
        ]
        expected_csv = [
            [
                "11111",
                "222222222222",
                "333",
                "44",
                "5555555555555",
                "6666666",
                "7777777777",
                "8888888888888",
                "99999999999999999999",
                "0000000000000",
            ],
        ]

        input_file = "test_input_2.txt"
        with open(input_file, 'w', encoding=parser.config.in_file_encoding) as f:
            f.write('\n'.join(input_lines))

        output_file = "test_output_2.txt"

        parser.fixed_length_to_csv(in_file=input_file, out_file=output_file)

        with open(output_file, 'r', encoding=parser.config.out_file_encoding) as f:
            reader = csv.reader(f)
            lines = list(reader)

        self.assertEqual(lines, expected_csv)

        os.remove(input_file)
        os.remove(output_file)
        os.remove(spec_file)


if __name__ == "__main__":
    unittest.main()
