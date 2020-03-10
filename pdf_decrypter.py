import json
import os

import PyPDF2

PDF_PASSWORD = json.load(open('config.json'))['Paycheck_Password']  # The required password to open the PDF file


def decrypter(input_file):
    """
    A function that decrypts a PDF file and saves a new copy with pre-defined naming convention

    :param input_file: the name of the file that needs to be decrypted
    :return: The name of the file that needs to be uploaded to Google Drive after it was decrypted and re-saved
    """

    file_name, file_ext = os.path.splitext(input_file)
    f_id, f_year, f_month = file_name.split('_')
    output_file = f'{f_year}.{f_month}{file_ext}'

    with open(input_file, mode='rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_reader.decrypt(PDF_PASSWORD)

        for page in range(pdf_reader.getNumPages()):
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(page))
            with open(output_file, mode='wb') as output:
                pdf_writer.write(output)

    return output_file
