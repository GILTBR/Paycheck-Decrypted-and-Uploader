## Paycheck Decrypted and Uploader
Every month i get my paycheck in an encrypted PDF file with the following format: '{ID}_YYYY_MM'.
In order to make my life a bit easier and to follow the paychecks naming convention that I am used to, i created this program.

This program downloads the encrypted PDF from my Google Drive, decrypts the file, creates a new decrypted PDF file with my naming convention 'YYYY.MM', uploads the new 
PDF to my Google Drive and deletes all the redundant files.

###Prerequisites
In order to run this program there are 2 prerequisites:
1. A JSON file named 'config.JSON' needs to be created in the project directory with these keys:
            `{
              "Paycheck_Password": "PDF PASSWORD",
              "ID": "ID NUMBER"
            }`
2. A Google Drive API key is required to run the program. After downloading the JSON file with your 
credentials, rename it to: 'google_drive_api_credentials.JSON' and place it in the project directory.

###Installation
1. Navigate to project's folder within Terminal/Command Prompt
2. Create a virtual environment (env) folder
       Windows - 'python/python3 -m venv env'
       macOS/Linux - 'python/python3 -m venv env'
3. Activate the virtual environment
    Windows - '.\env\Scripts\activate'
    macOS/Linux - 'source env/bin/activate'
4. Install requirements (3rd party libraries) from requirements.txt file
    'pip3 install -r requirements.txt'


Once the prerequisites are satisfied and the installation is done, simply run main.py from you console.
#####ENJOY!


