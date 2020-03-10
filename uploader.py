import glob
import io
import json
import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

import api_authentication
import pdf_decrypter

SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'google_drive_api_credentials.json'  # Google Drive API credentials
PARENT_FOLDER = json.load(open('config.json'))['Parent_Folder']  # The ID of the folder to which the file will be uploaded
ID = json.load(open('config.json'))['ID']  # The ID to search for

authIns = api_authentication.Auth(SCOPES, CLIENT_SECRET_FILE)
credentials = authIns.get_credentials()
drive_service = build('drive', 'v3', credentials=credentials)


def search_file():
    results = drive_service.files().list(
        q=f"name contains '{ID}_.' and mimeType='application/pdf' and trashed=False", pageSize=1,
        orderBy='createdTime desc',
        fields=" files(name,id,mimeType,parents,createdTime)").execute()
    items = results.get('files', [])

    if items:
        for item in items:
            file_id = item['id']
            file_name = item['name']
            file_parents = item['parents']
            download_file(file_id, file_name)
    else:
        print('File not found, terminating program')


def download_file(file_id, file_name):
    """:arg file_id """
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    file_to_upload = pdf_decrypter.decrypter(file_name)
    upload_file(file_to_upload, file_id, PARENT_FOLDER)


def upload_file(name, file_id, parents):
    file_metadata = {'name': name, 'mimeType': 'application/pdf',
                     'parents': PARENT_FOLDER}
    media = MediaFileUpload(name, mimetype='application/pdf')
    drive_service.files().create(body=file_metadata,
                                 media_body=media,
                                 fields='id').execute()

    delete_file(file_id)


def delete_file(file_id):
    file_metadata = {'trashed': True}
    drive_service.files().update(fileId=file_id, body=file_metadata).execute()
    for f in glob.glob('*.pdf'):
        os.remove(f)


def main():
    search_file()


if __name__ == '__main__':
    main()
