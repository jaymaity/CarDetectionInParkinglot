import ftplib
import socket
import urllib
import os
from os import listdir
from os.path import isfile, join
import time

INPUT_FILE_PATH = "C:\\BigData\\images\\"
FTP_HOST = 'ftp.******.***'
FTP_USERNAME = '***@****.***'
FTP_PASSWORD = '*****'
FTP_FOLDER = 'parkinglot'


def upload_folder_content(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, upload_folder, is_delete_local):
    """
    Upload file from a folder in local
    :param FTP_HOST:
    :param FTP_USERNAME:
    :param FTP_PASSWORD:
    :param FTP_FOLDER:
    :param upload_folder:
    :return:
    """
    all_files = [f for f in listdir(upload_folder) if isfile(join(upload_folder, f))]

    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USERNAME, FTP_PASSWORD)
    ftp.cwd(FTP_FOLDER)

    for filename in all_files:
        filetocopy = open(upload_folder + filename, 'rb')
        ftp.storbinary('STOR ' + filename, filetocopy)
        filetocopy.close()
        if is_delete_local:
            os.remove(upload_folder + filename)
    ftp.quit()


def monitor_upload_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, upload_folder):
    """
    Monitor folder for any file content to put in ftp
    :param FTP_HOST:
    :param FTP_USERNAME:
    :param FTP_PASSWORD:
    :param FTP_FOLDER:
    :param upload_folder:
    :return:
    """
    while True:
        upload_folder_content(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, upload_folder, is_delete_local=True)
        print("File uploaded..")
        time.sleep(10)

def download_ftp_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, download_folder, is_delete_download):
    """
    Download all files in a ftp
    :param FTP_HOST:
    :param FTP_USERNAME:
    :param FTP_PASSWORD:
    :param FTP_FOLDER:
    :param download_folder:
    :return:
    """
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USERNAME, FTP_PASSWORD)
    ftp.cwd(FTP_FOLDER)
    filenames = ftp.nlst() # get filenames within the directory
    print(filenames)

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for filename in filenames:
        if filename != "." and filename != "..":
            urllib.urlcleanup()
            urllib.urlretrieve(
                'ftp://' + FTP_USERNAME + ':' + FTP_PASSWORD + '@' + FTP_HOST + '/' + FTP_FOLDER + '/' + filename,
                download_folder + filename)
            if is_delete_download:
                ftp.delete(filename)

    ftp.quit()

def delete_ftp_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER):
    """
    Delete all content within a folder in FTP
    :param FTP_HOST:
    :param FTP_USERNAME:
    :param FTP_PASSWORD:
    :param FTP_FOLDER:
    :return:
    """
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USERNAME, FTP_PASSWORD)
    ftp.cwd(FTP_FOLDER)
    filenames = ftp.nlst()  # get filenames within the directory

    for filename in filenames:
        if filename != "." and filename != "..":
            ftp.delete(filename)

    ftp.quit()




# Test Download
# download_ftp_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, "C:\\BigData\\images\\test1\\",
#                    is_delete_download=True)

# Test Upload
# upload_folder_content(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, "C:\\BigData\\images\\rawsfu\\",
#                      is_delete_local=True)

# Test Delete Ftp
# delete_ftp_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER)

monitor_upload_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, "C:\\BigData\\images\\rawsfu\\")
