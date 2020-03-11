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
ID = json.load(open('config.json'))['ID']  # The ID to search for

authIns = api_authentication.Auth(SCOPES, CLIENT_SECRET_FILE)
credentials = authIns.get_credentials()
drive_service = build('drive', 'v3', credentials=credentials)


def search_file():
    """
    This function searches in Google Drive for the last file that was uploaded that follows the convention of '{ID}_'.
    After the file is found, the different elements from the file metadata are extracted and are passed on to the download_file function.
    """

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
            download_file(file_id, file_name, file_parents)
    else:
        print('File not found, terminating program')


def download_file(file_id, file_name, file_parents):
    """
    Downloads the file from Google Drive, calls the pdf_decrypter function and eventually calls the upload_file function.

    :param file_id: the file id that was extracted from the metadata
    :param file_name: the file name
    :param file_parents: the id of the folder that the file is located in
    """

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.close()
    file_to_upload = pdf_decrypter.decrypter(file_name)
    upload_file(file_to_upload, file_id, file_parents)


def upload_file(name, file_id, parents):
    """
    Uploads the new decrypted PDF file to the original file's folder in Google Drive.
    Calls the delete_file function

    :param name: the name of the new PDF file after decryption
    :param file_id: the id of the original file
    :param parents: the id of the folder that the original file is located in
    """

    file_metadata = {'name': name, 'mimeType': 'application/pdf',
                     'parents': parents}
    media = MediaFileUpload(name, mimetype='application/pdf')
    drive_service.files().create(body=file_metadata,
                                 media_body=media,
                                 fields='id').execute()
    media.__del__()
    delete_file(file_id)


def delete_file(file_id):
    """
    Deletes the original encrypted file from Google Drive, the local original copy and local decrypted file

    :param file_id: the id of the original file
    """

    file_metadata = {'trashed': True}
    drive_service.files().update(fileId=file_id, body=file_metadata).execute()
    for f in glob.glob('*.pdf'):
        os.remove(f)


def main():
    search_file()


if __name__ == '__main__':
    main()
