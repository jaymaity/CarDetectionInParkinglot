import ftplib
import socket
import urllib
import os
from os import listdir
from os.path import isfile, join
import time
import sys

INPUT_FILE_PATH = "C:\\BigData\\images\\"
FTP_HOST = 'ftp.******.****'
FTP_USERNAME = '******'
FTP_PASSWORD = '******'
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

monitor_upload_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, sys.argv[1])
