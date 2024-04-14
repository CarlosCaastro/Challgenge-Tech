import pandas as pd
import json

class Extract:
    def __init__(self, file_path):
        self.file_path = file_path

    def to_dataframe(self):
        if self.file_path.endswith('.json'):
            return self._read_json()
        elif self.file_path.endswith('.csv'):
            return self._read_csv()
        else:
            raise ValueError("Extração apenas de JSON e CSVs.")

    def _read_json(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return pd.DataFrame(data)

    def _read_csv(self):
        return pd.read_csv(self.file_path)