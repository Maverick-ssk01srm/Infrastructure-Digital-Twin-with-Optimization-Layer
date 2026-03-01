import pandas as pd

class TimetableParser:
    @staticmethod
    def parse(file):
        df = pd.read_csv(file)
        required = ['room','students','capacity']
        for col in required:
            if col not in df.columns:
                df[col] = "Unknown"
        if 'occupancy' not in df.columns:
            df['occupancy'] = df['students'] / df['capacity']
        if 'hour' not in df.columns:
            df['hour'] = 10
        return df
