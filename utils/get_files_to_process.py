import os 

def find_csv_files():
    directory = os.getcwd() + '/ToProcess'
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    return csv_files
