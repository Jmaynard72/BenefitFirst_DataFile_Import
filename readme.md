# BenefitFirst Incoming Change File

# To Run
Execute python main.py '7000,7001,7002,7020'

## Scope
Looks on BenefitFirst SFTP server and download any CSV files and import the information into Millennium

## Requirements
* Parminko

### To Do List
* Keep time stamped log daily for downloads (done)
* Send email notification reporting success or failure with log (done)
* Look on SFTP server for csv file and download it to local directory for  processing (done)

## Scripts
### connectionHandler.py
    Creates connection to SQL database and query/insert/update/delete data
    * fetch_data (query) - Execute query to pull data into a pandas data frame
    * insert_data (data frame,table name) - Insert data into a database table
    * execute_query (query) - Update/Delete data in database

### log_tracking.py
    Creates a log file and saves information to the log file during the application process
    * create_log - Initiates the creation of the log file
    * write_log (message,level) - add line to log file, available levels are info, warning, error, critical
        levels are case sensitive
    * read_log - reads the contents of the log file and returns is as a strings

### send_mail.py
    Sends email message
    * send_message (sendTo,subject,bodyText) - Takes the three parameters and sends out email

### sftp.py
    Connects to SFTP server and looks for CSV files and downloads them to a local directory




### Change Log
