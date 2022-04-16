#!/usr/bin/env python

import os
import logging
import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv

# load environment variables
load_dotenv(find_dotenv())

pswd = os.environ['SNOFLK_PASSWORD']
user = os.environ['SNOFLK_USER']
acct = os.environ['SNOFLK_ACCOUNT']

db = 'RAW_MERGE_DEV'
wh = 'DATON_WAREHOUSE'
sh = 'PUBLIC'

# Snowflake connector class
class SnowflakerConnector:
    def __init__(self
                 , user=user 
                 , password=pswd
                 , account=acct
                 , db=db
                 , wh=wh
                 , sh=sh
                 , role='sysadmin'):
                 
        self.user = user
        self.password = pswd
        self.account = account
        self.db = db
        self.wh = wh
        self.sh = sh
        self.role = role

        self.url = URL(
            user=self.user,
            password=self.pswd,
            account=self.account,
            database=self.db,
            warehouse=self.wh,
            role=self.role,
            schema=self.sh
        )

        self.engine = create_engine(self.url)

    @property
    def connect(self):
        return self.engine.connect()


# Snowflake UPloader class
class SnowflakerUploader(SnowflakerConnector):
    def __init__(self,*
                ,df
                ,table_name
                ,create=False
                ,truncate=True
                ,format='csv'
                ,sep=','
                , **kwargs):
        super().__init__(**kwargs)
        self.df = df
        self.table_name = table_name
        self.create = create
        self.truncate = truncate
        self.format = format
        self.sep = sep
    
    def upload(self):

        self.file_name = f'{self.table_name}.{self.format}'
        self.file_path = os.path.join(os.path.dirname(__file__),'data', self.file_name)
        self.df.to_csv(self.file_path, sep=self.sep, index=False)

        with self.connect as con:
            try:
                if self.create:
                    self.df.head(0).to_sql(self.table_name, con, if_exists='replace', index=False)
                
                if self.truncate:
                    con.execute(f'TRUNCATE TABLE {self.table_name}')
                
                # Create file format for upload
                con.execute(f""" create or replace file format my{self.format}format
                                type = {self.format}
                                field_delimiter = {self.sep}
                                skip_header = 1; """)
                # Create Snowflake stage
                con.execute(f"""create or replace stage my_{self.format}_stage 
                                file_format = my{self.format}format; """)
                
                # Stage file
                con.execute(f"put file://{self.file_path} @my_{self.format}_stage")

                # Load file into Snowflake
                logging.info(f'Loading file into Snowflake...')
                con.execute(f""" copy into {self.table_name}
                                from @my_{self.format}_stage
                                file_format = ( format_name = my{self.format}format )
                                on_error = 'skip_file; """)

                # ClEAN UP - Drop stage, format and remove file
                con.execute(f"drop stage my_{self.format}_stage")
                con.execute(f"drop file format my{self.format}format")
                os.remove(self.file_path)

            except Exception as e:
                con.execute('ROLLBACK')
                logging.error(e)
            finally:
                con.close()

# Snowflake Query class
class SnowflakerQuery(SnowflakerConnector):
    def __init__(self,*,query,output_path, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        self.output_path = output_path
    
    def query(self):
        with self.connect as con:
            try:
                self.df = pd.read_sql(self.query, con)
            except Exception as e:
                con.execute('ROLLBACK')
                logging.error(e)
            finally:
                con.close()

        if self.output_dir:
            self.df.to_csv(self.output_path, index=False)
            return None
        else:
            return self.df

# Snowflake Main abstract class
class Snowflaker(SnowflakerUploader, SnowflakerQuery):
    def __init__(self,*,**kwargs):
        super().__init__(**kwargs)
