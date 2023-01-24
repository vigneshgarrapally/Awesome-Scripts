#PyDrive2 is a active fork of pydrive that supports extra features 
# like downloading from shared drives
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import requests
import os
import sys
import urllib.parse as urlparse
import re
from urllib.parse import parse_qs
import logging
#helper functions for downloading public gdrive files
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)



class gdrive():
    def __init__(self):
        self.drive=None

    def authenticate(self):
        
        """
        Authenticates Drive
        """

        try:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(gauth)
        except:
            logging.warning("Authentication to Drive Failed.Exiting")
            sys.exit(0)
        msg="Successfully Authenticated to Drive"
        logging.info(msg)

    @staticmethod
    def getIdFromUrl(link: str):
        if "folders" in link or "file" in link:
            regex = r"https://drive\.google\.com/(drive)?/?u?/?\d?/?(mobile)?/?(file)?(folders)?/?d?/([-\w]+)[?+]?/?(w+)?"
            res = re.search(regex,link)
            if res is None:
                raise IndexError("GDrive ID not found.")
            return res.group(5)
        parsed = urlparse.urlparse(link)
        return parse_qs(parsed.query)['id'][0]
    
    def filedownload(self,link:str,dest=None,overwrite=False):
        """Download's a File from Google Drive Given file ID
        Args:
            link ([String]): Google Drive Link
            dir_path ([os.path object], optional): Downloads file to the given Directory.
                                                    If None, download to current Directory
            overwrite([bool]): Overwrites the file if already exists. If overwrite=False 
            and file already exists, raises FileAlreadyExists Error                                
        """
        try:
            id = self.getIdFromUrl(link)
        except(IndexError):
            msg = "Google drive ID could not be found in the provided link.Exiting"
            logging.warning(msg)
            sys.exit(0)
        msg = ""
        #authenticate the drive
        if self.drive is None:
            self.authenticate()
        filetodownload = self.drive.CreateFile({'id':id})
        #check if file exists
        if dest is None:
            dest=os.getcwd()
        status=os.path.exists(os.path.join(dest,filetodownload['title']))
        exp=(status and overwrite) or (not status)
        if exp:
            save_path=os.path.join(dest,filetodownload['title'])
            os.makedirs(os.path.dirname(save_path),exist_ok=True)
            filetodownload.GetContentFile(save_path)
            msg=" Succesfully Downloaded to Destination"
        else:
            logging.info("File Already Exists. Add overwrite=True to overwrite existing files")
            msg="Skipping Downloads as overwrite=Flase"
        logging.info(msg)

    def create_folder(self,subfolder_name:str,link=None):
        """Creates a folder in google drive

        Args:
            link ([str]): [Parent Drive Link in which folder has to be created]
            subfolder_name ([str]): [Name of folder to bre created]

        Returns:
            [pydrive2.files.GoogleDriveFile]: [pydrive File Instance]
        """
        config={'title': subfolder_name,"mimeType": "application/vnd.google-apps.folder"}
        if link is not None:     
            try:
                parent_folder_id = self.getIdFromUrl(link)
                config['parents']=[{'kind': 'drive#fileLink', 'id': parent_folder_id}]
            except(IndexError):
                logging.warning("Google drive ID could not be found in the provided link")
                return None
        newFolder = self.drive.CreateFile(config)
        newFolder.Upload()
        logging.info("Folder Created Sucessfully")
        return newFolder

    def folderdownload(self,link:str,dest=None,overwrite=False):
        """Downloads folder to destination path

        Args:
            link (str):  Google Drive Link
            dest ([Path], optional): [Destination path]. Defaults to None.
            overwrite (bool, optional): [Overwrite Flag]. Defaults to False.

        """
        try:
            id = self.getIdFromUrl(link)
        except(IndexError):
            msg = "Google drive ID could not be found in the provided link"
            logging.warning(msg)
            sys.exit(0)
        if self.drive is None:
            self.authenticate()
        if dest is None:
            dest=self.drive.CreateFile({'id':id})['title']
        file_list = self.drive.ListFile({'supportsAllDrives':True,'q': "'{}' in parents and trashed=false".format(id)}).GetList()
        for i, file1 in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
            print('Downloading {} from GDrive ({}/{})'.format(file1['title'], i, len(file_list)))
            status=os.path.exists(os.path.join(dest,file1['title']))
            if (status and overwrite) or (not status):
                save_path=os.path.join(dest,file1['title'])
                os.makedirs(os.path.dirname(save_path),exist_ok=True)
                file1.GetContentFile(save_path)
            else:
                logging.info("skipping {} as file already exists in destination. set overwrite=True to force download".format(file1['title']))
        logging.info("Folder Download Complete")
    
    #gdown is an simple alternative to download public files
    def publicfiledownload(self,link:str,dest=None):
        """Given link, downloads for public folders

        Args:
            link (str): Google Drive Link
            dest ([Path], optional): Destination path. Defaults to None.

        """
        try:
            id = self.getIdFromUrl(link)
        except(IndexError):
            msg = "Google drive ID could not be found in the provided link"
            logging.warning(msg)
            sys.exit(0)
        if dest is None:
            dest=os.getcwd()   
        URL = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(URL, params = { 'id' : id }, stream = True)
        token = get_confirm_token(response)
        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)
        save_response_content(response,dest) 
        msg="Downloaded Successfully"
        logging.info(msg)

    def fileupload(self,file_path,link=None):
        """Uploads file to destination google drive link

        Args:
            file_path ([Path]): Path of file to upload
            link ([type]): Destination Drive Folder Link to which file has to be uploaded
        """
        config={}
        if link is not None:
            try:
                id = self.getIdFromUrl(link)
                config['parents']=[{'kind': 'drive#fileLink', 'id':id}]
            except(IndexError):
                msg = "Google drive ID could not be found in the provided link"
                logging.warning(msg)
                sys.exit(0)
        try:
            if os.path.isfile(file_path):
                config['title']=os.path.basename(file_path)
                file = self.drive.CreateFile(config)
                file.SetContentFile(file_path)
                file.Upload()
                logging.info("File Uploaded Successfully")
            else:
                raise FileNotFoundError()
        except (FileNotFoundError):
            logging.info("File Not found in given path")
            sys.exit(0)
    
    def folderupload(self,folder_path,link=None):
        """Uploads file to destination google drive link

        Args:
            folder_path ([Path]): Path of folder to upload
            link ([type]): Destination Drive Folder Link to which file has to be uploaded
        """
        try:
            if os.path.isdir(folder_path):
                root_folder=self.create_folder(os.path.basename(folder_path),link)
                for i in os.listdir(folder_path):
                    path=os.path.join(folder_path,i)
                    # print(os.path.isfile(path))
                    # print(os.path.isdir(path))
                    if os.path.isfile(path):
                        #print("file")
                        self.fileupload(path,root_folder['alternateLink'])
                    elif os.path.isdir(path):
                        #print("folder")
                        self.folderupload(path,root_folder['alternateLink'])
            else:
                raise OSError()
        except OSError:
            logging.warning("Given path is not a directory")
            sys.exit(0)


    def trash(self,id:str):
        """Moves file to trash given file id

        Args:
            id (str): [File/Folder ID]
        """
        if self.drive is None:
            self.authenticate()
        to_trash=self.drive.CreateFile({'id':id})
        to_trash.Trash()

    def untrash(self,id:str):
        """Moves file out of trash given fileid"""
        if self.drive is None:
            self.authenticate()
        to_trash=self.drive.CreateFile({'id':id})
        to_trash.UnTrash()

    def delete(self,id:str):
        """Permanently deletes the file"""
        if self.drive is None:
            self.authenticate()
        to_trash=self.drive.CreateFile({'id':id})
        to_trash.Delete()

    def search(self,title:str):
        pass



    def folder_trash(self,id:str):
        """Moves a folder to trash"""
        if self.drive is None:
            self.authenticate()
        file_list = self.drive.ListFile({'supportsAllDrives':True,'q': "'{}' in parents and trashed=false".format(id)}).GetList()
        for to_trash in file_list:
            to_trash.Trash()
        self.drive.CreateFile({'id':id}).Trash()

    def list(self,id,maxresults=None):
        if self.drive is None:
            self.authenticate()
        file_list=self.drive.ListFile({'supportsAllDrives':True,'q': "'{}' in parents and trashed=false".format(id)}).GetList()
        for file1 in file_list:
            print(file1["title"])





