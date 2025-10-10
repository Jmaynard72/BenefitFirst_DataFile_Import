import utils.log_tracking as log 

import paramiko

import os 


def main():
    #Configuration
    HOSTNAME = 'sftp.benefitfirst.com'
    PORT = 22
    USERNAME = 'RoodandRiddle'
    PASSWORD = 'FZAUWpB%2e'
    REMOTE_PATH = '/outbound'
    LOCAL_PATH = os.path.dirname(__file__) + '/ToProcess'

    try:
        #Create an SSH client
        transport = paramiko.Transport((HOSTNAME,PORT))
        transport.connect(username=USERNAME,password=PASSWORD)

        #Create and SFTP session
        sftp = paramiko.SFTPClient.from_transport(transport)

        #List all files in the remote directory
        files = sftp.listdir(REMOTE_PATH)

        #Filter for .csv files
        csv_files = [f for f in files if f.endswith('.csv')]

        if not csv_files:
            print("No csv files found in the remote directory")
        else:
            for file_name in csv_files:
                remote_file = os.path.join(REMOTE_PATH,file_name)
                local_file = os.path.join(LOCAL_PATH,file_name)
                log.write_log(f"Downloading {file_name}...",'info')
                sftp.get(remote_file,local_file)
            

        
        #Close the SFTP connection
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == '__main__':
    main()


