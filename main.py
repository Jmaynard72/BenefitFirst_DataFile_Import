
from utils import get_files_to_process as get
import utils.sftp as sftp
from utils import log_tracking as log 

import pandas as pd
from sqlalchemy import create_engine, update, Table, MetaData, text
import argparse

import os 

#Config
SERVER = 'PSI-SQL'
DATABASE = 'Millennium'
DRIVER = 'ODBC Driver 17 for SQL Server'
key_columns = ['co','id','dcode']

#Send email notifications to
sent_to = 'jmaynard@payrollsolutions.cc'

#Determines if the application was successful for email notification
state = True 

def main():
    parser = argparse.ArgumentParser()

    #Required arguments
    parser.add_argument("company", type=str, help="Millennium company number. (required)")

    args = parser.parse_args()
    company = args.company
    
    # Step 1: Create log
    log.create_log()

    # Step 2: Look for files on the SFTP server
    #sftp.main()

    # Step 3: Determine if files where downloaded
    fileList = get.find_csv_files()
    fileCount = len(fileList)

    if fileCount > 0:
        for f in fileList:
            log.write_log(f'Processing...{f}','info')
            process_changes(f,company)
    else:
        log.write_log('No file found to process.','info')

def format_ssn(ssn):
    # add dashes back to ssn number
    ssn = str(ssn)
    return f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"           

def process_changes(file,company):
    # Connect to database
    connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?trusted_connection=yes&driver={DRIVER}"
    engine = create_engine(connection_string, fast_executemany=True)

    conn = engine.connect()

    # Load CSV data
    filePath = os.path.dirname(__file__) + '/ToProcess/' + file 
    df_csv = pd.read_csv(filePath)

    # Format SSN to include dashes
    if 'ssn' in df_csv.columns:
        df_csv['ssn'] = df_csv['ssn'].apply(format_ssn)

    
    #Query new list from SQL of company and ID numbers
    QUERY = f"SELECT co,id,ssn FROM einfo WHERE co = '{company}' AND empstatus='A'"
    df_sql = pd.read_sql(QUERY,conn)
    
    # Insert co and id columns where SSN matches between data frames
    df_csv = df_csv.merge(df_sql, on='ssn',how='left')

    df_csv['endDate'] = '2100-12-31'

    # Remove rows with no co or id column data
    df_csv = df_csv.dropna(subset=['co','id'])
  
    # Execute updates and inserts into SQL database
    for _, row in df_csv.iterrows():
        merge_sql = text(f"""
        MERGE INTO eded AS target
        USING (SELECT :co AS co, :id AS id, :dcode AS dcode, :rate AS rate, :startDate AS startDate, :endDate AS endDate) AS source
        ON target.id = source.id AND target.co = source.co AND target.dcode = source.dcode
        WHEN MATCHED THEN
            UPDATE SET rate = source.rate
        WHEN NOT MATCHED THEN
            INSERT (co,id,dcode,rate,startDate,endDate) VALUES (source.co,source.id,source.dcode,source.rate,source.startDate,source.endDate);
        """)
        
        conn.execute(merge_sql,dict(row))
        conn.commit()
        
    conn.close()

  
if __name__ == '__main__':
    main()


