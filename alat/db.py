import pandas as pd
import streamlit as st
class Database:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)

    def create_record(self, data):
        new_record = pd.DataFrame([data])
        self.df = pd.concat([self.df, new_record], ignore_index=True)
        self.df.to_csv(self.csv_file, index=False)

    def read_records(self):
        return self.df

    def update_record(self, index, data):
        # Use .loc with the specific index and column names for updating
        self.df.loc[index, :] = data
        self.df.to_csv(self.csv_file, index=False)

    def delete_record(self, index):
        self.df = self.df.drop(index)
        self.df.to_csv(self.csv_file, index=False)

    def find_index_by_nik(self, nik):
        try:
            index = self.df[self.df['nik'] == int(nik)].index.to_frame().to_string(index=False).split()
            return index[1]
        except IndexError:
            print(f"No record found with 'nik' {nik}")
            return None