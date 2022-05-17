#%%
import os

import logging
import tempfile

import pandas as pd
from dotenv import load_dotenv, find_dotenv

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

#load environment variables
load_dotenv(find_dotenv())    

#%%
class SharepointConnector:

    def __init__(self
                , url
                , file_url
                , user=os.environ['SP_CLIENT']
                , pswd=os.environ['SP_SECRET'] ):

        self.credentials = UserCredential(user,pswd)
        self.url = url
        self.file_url = file_url
        
            
        self.ctx = None
        self.file = None
        
    @property
    def connect(self):
        self.ctx = ClientContext(self.url).with_credentials(self.credentials)
        return self.ctx

    @property
    def file_url(self):
        return self._file_url
    
    @file_url.setter
    def file_url(self, value):
        self._file_url = value
        self.connect


#%%
class SharepointDownloader(SharepointConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.file_dir = os.path.join(os.getcwd(), "tmp/data/sharepoint_transfer/")
        self.file_path =  os.path.join(self.file_dir, os.path.basename(self.file_url))

        if not os.path.exists(self.file_dir):
            os.makedirs(self.file_dir)

    @property
    def f_extension (self):
        """Checks file extension"""
        excel_f = ['xls','xlsx','xlsm']
        texts_f = ['txt','csv']
        fileExtension = self.file_url.split('.')[-1]

        if  fileExtension in excel_f:
            return 'xls'
        elif fileExtension in texts_f:
            return 'csv'

    @property
    def download(self):
        self.connect
        try:
            with open(self.file_path, 'wb') as f:
                self.file = self.ctx.web.get_file_by_server_relative_path(self._file_url).download(f).execute_query()
            logging.info(f"File successfully downloaded at: {self.file_path}")

        except Exception as e:
            logging.error(f"Error downloading file: {e}")
        
    @property
    def df(self):
        # check if file exists
        self.download if not os.path.exists(self.file_path) else None

        info = pd.read_excel(self.file_path, sheet_name='auto_info')
        info.columns = info.columns.str.lower()
        insert_columns = info['columns']
        table = info['table'].iloc[0]

        csv_path = os.path.join( self.file_dir, table + ".csv")

        #Remove old csv file if exists 
        if os.path.exists(csv_path):
            os.remove(csv_path)

        args = { 
         'database' : info['database'].iloc[0]
        ,'schema' : info['schema'].iloc[0]
        ,'table' : info['table'].iloc[0]
        ,'method' : info['method'].iloc[0]
        ,'schedule' : info['schedule'].iloc[0]
        ,'owner' : info['owner'].iloc[0]
       # ,'id_columns' :  info['columns'].where(info['id'].notnull())
        }

        df =  pd.read_excel(self.file_path, sheet_name='data', usecols=insert_columns)
        df.to_csv(csv_path, sep = ',' , index=False)

        logging.info("Tempory file created: " + csv_path)      

        return args , df

    @property
    def cleanup(self):
        # Cleanup file if it exists
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
# %%
