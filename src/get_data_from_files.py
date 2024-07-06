import pandas as pd

def get_data_from_files(*files):
    for file in files:
        data = pd.read_csv(file)
        
    res = []
