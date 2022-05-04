#%%
import os
import io

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

        self.url = url
        self._file_url = file_url
        self.credentials = UserCredential(user,pswd)
            
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

    def __init__(self,*, output_dir:str=None, to_pd=False, **kwargs):
        super().__init__(**kwargs)
        self.output_dir = output_dir if output_dir else tempfile.gettempdir()
        self.to_pd = to_pd
        self.download_path =  os.path.join(self.output_dir, os.path.basename(self.file_url))

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
        self.connect()
        try:
            with open(self.download_path, 'wb') as f:
                self.file = self.ctx.web.get_file_by_server_relative_path(self._file_url).download(f).execute_query()
            logging.info(f"File successfully downloaded at: {self.download_path}")

        except Exception as e:
            logging.error(f"Error downloading file: {e}")
    
    def to_df(self, sheet='data'):

        self.connect()
        self.download if not os.path.exists(self.download_path) else None
        if self.f_extension == 'xls':
            return pd.read_excel(self.download_path, sheet_name=sheet)
            # bytes_file_obj = io.BytesIO()
            # self.file = self.ctx.web.get_file_by_server_relative_path(self.file_url).download(bytes_file_obj).execute_query()
        else:
            return pd.read_csv(self.download_path)
    
    def cleanup(self):
        # Cleanup file if it exists
        if os.path.exists(self.download_path):
            os.remove(self.download_path)


#%%

site_url = "https://sellerx.sharepoint.com/sites/Operations/"
file_url = "/sites/Operations/Shared Documents/General/Sellerboard-Profitloss/landedcogs.xlsx"

sp= SharepointDownloader(url= site_url, file_url=file_url)
output_file = sp.download
df = sp.to_df()
#sp.cleanup()

#%%



# FILEPATH = os.path.join(PATH, FILE)
# xlsFile = pd.read_excel(FILEPATH, sheet_name=None)
# del xlsFile['Methodology']

# def validate_columns(df, names=NAMES):
#     """Select rearrange and rename columns to be used"""
#     selected = []
#     for col in df.columns:
#         for name in names:
#             if re.search(name, col, re.IGNORECASE) is not None:
#                 df.rename(columns={col:name}, inplace=True, index=str)
#                 selected.append(name)
#     return df[selected]
    
    
# def append_sheets(dfs):
#     """Append sheets to a single dataframe"""
#     df = pd.DataFrame()
#     for name, sheet in dfs.items():
#         print('processing sheet:'+ name, type(sheet))
#         sheet = validate_columns(sheet)
#         sheet['source'] = name
#         df = df.append(sheet, ignore_index=True)
#     return df


    
# all=append_sheets(xlsFile)
