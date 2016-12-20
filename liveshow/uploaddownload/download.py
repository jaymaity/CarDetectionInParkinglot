import ftplib
import socket
import urllib
import os
from os import listdir
from os.path import isfile, join
import time

LIVE_DATA_PATH = "/home/jay/BigData/MLProj732/dl/static/datalive/"

FTP_HOST = 'ftp.****.***'
FTP_USERNAME = '******'
FTP_PASSWORD = '*****'
FTP_FOLDER = 'parkinglot'


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

            urllib.urlretrieve(
                'ftp://' + FTP_USERNAME + ':' + FTP_PASSWORD + '@' + FTP_HOST + '/' + FTP_FOLDER + '/' + filename,
                download_folder + filename)
            urllib.urlcleanup()

            if is_delete_download:
                ftp.delete(filename)

    ftp.quit()

def monitor_download_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, download_folder):
    """
    Monitor folder for any file content to download from FTP
    :param FTP_HOST:
    :param FTP_USERNAME:
    :param FTP_PASSWORD:
    :param FTP_FOLDER:
    :param download_folder:
    :return:
    """
    while True:
        download_ftp_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, download_folder, is_delete_download=True)
        print("File downloaded..")
        time.sleep(10)

monitor_download_folder(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, FTP_FOLDER, LIVE_DATA_PATH)

