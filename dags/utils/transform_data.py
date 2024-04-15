import json
import csv


def txt_to_json(txt_file, json_file):
    with open(txt_file, "r") as file:
        lines = file.readlines()
        json_data = []

        for line in lines:
            line = line.strip()
            json_data.append({"item": line})

    with open(json_file, "w") as file:
        json.dump(json_data, file, indent=4)


def csv_to_json(csv_file, json_file):
    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]

    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)


def split_file(input_file, num_parts):
    with open(input_file, "r") as f:
        lines = f.readlines()

    total_lines = len(lines)
    lines_per_part = total_lines // num_parts

    for i in range(num_parts):
        start_index = i * lines_per_part
        end_index = (i + 1) * lines_per_part if i < num_parts - 1 else total_lines
        part_lines = lines[start_index:end_index]

        output_file = f"{input_file}_part{i + 1}.txt"
        with open(output_file, "w") as f_out:
            f_out.writelines(part_lines)

    print(f"Arquivo dividido em {num_parts} partes.")
