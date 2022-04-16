
import os
import io
import re
import pandas as pd
from dotenv import load_dotenv, find_dotenv

from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext


#load environment variables
load_dotenv(find_dotenv())    

FILEPATH = os.path.abspath(os.path.dirname(__file__))

class SharepointConnector:

    def __init__(self, user, pswd, file_url):
        self.url = 'https://sellerx.sharepoint.com'
        self.file_url = file_url

        if user:
            self.client_credentials = ClientCredential(user,pswd)
        else:
            user = os.environ['SP_CLIENT']
            pswd = os.environ['SP_SECRET']
            self.client_credentials = ClientCredential(user,pswd)
            
        self.ctx = None
        self.file = None
        

    def connect(self):

        if not self.credentials:
            self.credentials = ClientCredential(os.environ['SP_CLIENT'], os.environ['SP_SECRET'])

        self.ctx = ClientContext(self.url).with_credentials(self.credentials)
        return self.ctx


class SharepointDownloader(SharepointConnector):

    def __init__(self,*, output_dir:str, to_pd=False, **kwargs):
        super().__init__(**kwargs)
        self.output_dir = output_dir
        self.to_pd = to_pd
        self.download_path = os.path.join(self.output_dir, os.path.basename(self.file_url))

    #check file extension
    def check_extension(file_name):
        """Checks file extension"""
        excel_f = ['xls','xlsx','xlsm']
        texts_f = ['txt','csv']
        fileExtension = file_name.split('.')[-1]

        if  fileExtension in excel_f:
            return 'xls'
        elif fileExtension in texts_f:
            return 'csv'
    def to_path(self) -> None:
        self.connect()
        try:
            self.file = self.ctx.web.get_file_by_server_relative_path(self.file_url).download(self.download_path).execute_query()
            logging.info(f"File successfully downloaded at: {self.download_path}")

        except Exception as e:
            logging.error(f"Error downloading file: {e}")
    
    def to_df(self) -> pd.DataFrame:
        self.connect()
        bytes_file_obj = io.BytesIO()
        self.file = self.ctx.web.get_file_by_server_relative_path(self.file_url).download(bytes_file_obj).execute_query()
        return pd.read_excel(bytes_file_obj, sheet_name=None)



url = 'https://sellerx.sharepoint.com'
file_url = '/sites/sx-dep-tech/cogs_appended.xlsx?web=1'

clientid = os.environ['SP_CLIENT']
secret = os.environ['SP_SECRET']


client_credentials = ClientCredential(clientid, secret)
ctx = ClientContext(url).with_credentials(client_credentials)

excelFile = io.BytesIO()
ctx.web.get_file_by_server_relative_path(file_url).download(excelFile).execute_query()

df = pd.read_excel(excelFile, sheet_name=None)

#save data to BytesIO stream
bytes_file_obj = io.BytesIO()
bytes_file_obj.write(response.content)
bytes_file_obj.seek(0) #set file object to start

#read excel file and each sheet into pandas dataframe 
df = pd.read_excel(bytes_file_obj, sheetname = None)




#ctx.web.get_file_by_server_relative_url(url).download(os.path.join(os.getcwd(), 'COGS_202111_SHARED.xlsx'))


#self.ctx.web.lists.get_by_title('EOM Data Entry').items.get().select(self.select_fields).expand(self.expand_fields).execute_query()




# abs_file_url = "{site_url}sites/team/Shared Documents/big_buck_bunny.mp4".format(site_url=test_site_url)

# with tempfile.TemporaryDirectory() as local_path:
#     file_name = os.path.basename(abs_file_url)
#     with open(os.path.join(local_path, file_name), 'wb') as local_file:
#         file = File.from_url(abs_file_url).with_credentials(test_client_credentials).download(local_file).execute_query()
#     print("'{0}' file has been downloaded into {1}".format(file.serverRelativeUrl, local_file.name))



# From Pandas to Snowflake 
import re
import pandas as pd
import logging




PATH = '/mnt/c/Users/rodolfo.ribeiro/Documents/SellerX/Profit&loss'
FILE = 'COGS_202111_SHARED.xlsx'
NAMES = ['channel', 'marketplace','seller','asin', 'sku','currency', 'cogs', 'effective date']

FILEPATH = os.path.join(PATH, FILE)
xlsFile = pd.read_excel(FILEPATH, sheet_name=None)
# del xlsFile['Methodology']

def validate_columns(df, names=NAMES):
    """Select rearrange and rename columns to be used"""
    selected = []
    for col in df.columns:
        for name in names:
            if re.search(name, col, re.IGNORECASE) is not None:
                df.rename(columns={col:name}, inplace=True, index=str)
                selected.append(name)
    return df[selected]
    
    
def append_sheets(dfs):
    """Append sheets to a single dataframe"""
    df = pd.DataFrame()
    for name, sheet in dfs.items():
        print('processing sheet:'+ name, type(sheet))
        sheet = validate_columns(sheet)
        sheet['source'] = name
        df = df.append(sheet, ignore_index=True)
    return df


    
all=append_sheets(xlsFile)


'/sites/sx-dep-tech/cogs_appended.xlsx?web=1'