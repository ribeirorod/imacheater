#!/usr/bin/env python
#%%
import os
import shutil

import logging
from typing import Optional, Union
import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv

# load environment variables
load_dotenv(find_dotenv())

pswd = os.environ['SNOFLK_PASSWORD']
user = os.environ['SNOFLK_USER']
acct = os.environ['SNOFLK_ACCOUNT']
db = os.environ['SNOFLK_DATABASE']
wh = os.environ['SNOFLK_WAREHOUSE']
sh = 'PUBLIC'
#%%
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
        __password = password
        self.account = account
        self._db = db
        self._wh = wh
        self._sh = sh
        self.role = role

        self.url = URL(
            user=self.user,
            password=__password,
            account=self.account,
            database=self._db,
            warehouse=self._wh,
            role=self.role,
            schema=self._sh
        )

        self.engine = create_engine(self.url)
        self.con = self.connect


    @property
    def connect (self):
        con = self.engine.connect()
        con.execute('USE WAREHOUSE {}'.format(self._wh))
        con.execute('USE DATABASE {};'.format(self._db))
        con.execute('USE SCHEMA {};'.format(self._sh))
        return con

    @property
    def db(self):
        return self._db
    
    @db.setter
    def db(self, value):
        self._db = value
        self.connect

    @property
    def sh( self):
        return self._sh
    
    @sh.setter
    def sh(self, value):
        self._sh = value
        self.connect
        
    @property
    def wh (self):
        return self._wh
    
    @wh.setter
    def wh(self, value):
        self._wh=value
        self.connect
        
            
#%%
# Snowflake UPloader class
class SnowflakerUploader(SnowflakerConnector):

    """ 
    Uploads a Pandas dataframe or file into a new or existing Snowflake table.
    If Create is set to True, the table will be created if not exists and it will be replaced if it exists.
    If the table exists, and Truncate = True it will be truncated.
    Currently CSV, JSON formats are supported 
    """
    @property
    def read (self):
        return { 
            'csv': pd.read_csv ,
            'json': pd.read_json ,
            'xlsx': pd.read_excel ,
            }.get(self.format , pd.read_csv)

    def __init__(self,*
                ,input : Union[pd.DataFrame, str]
                ,table_name
                ,create=False
                ,truncate=False
                ,format='csv'
                ,sep=','
                , **kwargs):
        super().__init__(**kwargs)
        self.sep = sep
        self.format = format
        self.create = create
        self.truncate = truncate
        self.table_name = table_name
        self.path = os.path.join(os.path.dirname(__file__),"tmp","")

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            
        if isinstance(input, pd.DataFrame) and not input.empty:
            self.df = input
            self.file_name = f'{self.table_name}.{self.format}'
            self.file_path = os.path.join(self.path, self.file_name)
            self.df.to_csv(self.file_path, sep=self.sep, index=False)
            # self.df.reset_index().to_json(self.file_path,orient='records', lines=True, date_unit='s')

        elif isinstance(input, str):
            self.format = os.path.splitext(input)[1].split('.')[-1]
            self.file_path = input
            self.df = self.read(self.file_path) if create else None
        else:
            raise TypeError(f"input must be a pandas dataframe or a file path")

    @property
    def if_exists(self):
        self.con.execute('USE WAREHOUSE {}'.format(self._wh))
        return self.con.execute(f""" SELECT EXISTS (
                                SELECT * FROM information_schema.tables 
                                WHERE  table_schema = '{self._sh}' 
                                AND table_name = '{self.table_name}')
                                """
                        ).fetchone()[0]
                        
    def _load(self):
    
        # if not self.df.empty:
        #     if self.format == 'csv':
        #         self.df.to_csv(self.file_path, sep=self.sep, index=False)
        #     elif self.format in ('json'):
        #         self.df.to_json(self.file_path,orient='records', lines=True, date_unit='s')
           
        if self.create or not self.if_exists:
            logging.info(f"Creating table {self._sh}.{self.table_name}")
            self.con.execute(f"DROP TABLE IF EXISTS {self.table_name};")
            self.df.head(0).to_sql( self.table_name.lower() , self.con, schema=self._sh, if_exists='replace', index=False)
        else:
             self.df.head(0).to_sql( self.table_name.lower() , self.con, schema=self._sh, if_exists='replace', index=False)
        
        if self.truncate:
            logging.info(f"truncating {self.table_name}")
            self.con.execute(f'TRUNCATE TABLE {self.table_name}')       

    def _stage(self):
        self._load()
        # Create stage and format
        self.con.execute("alter session set timezone='UTC';")
        
        # Create file format for upload
        if self.format == 'csv':
            self.con.execute(f""" create or replace file format my{self.format}format
                            type = {self.format}
                            field_delimiter = '{self.sep}'
                            skip_header = 1; """)

        elif self.format in ('json'):
            self.con.execute(f""" create or replace file format my{self.format}format
                            type = {self.format}; """)

        # Create Snowflake stage
        self.con.execute(f"""create or replace stage my_{self.format}_stage 
                        file_format = my{self.format}format; """)
        
        # Stage file
        self.con.execute(f"put file://{self.path}{self.file_name} @my_{self.format}_stage overwrite=true;")
        self.con.execute(f"list @my_{self.format}_stage;")
        logging.info(f"staged to file://{self.file_path}.gz")

    @property
    def insert(self):

        self._stage()
        try:
            # Insert file into Snowflake destination table
            logging.info(f'Loading file into Snowflake...')

            self.con.execute(f""" COPY INTO {self.table_name}
                            FROM @my_{self.format}_stage/{self.file_name}.gz
                            file_format = ( format_name = my{self.format}format )
                            on_error = 'skip_file'; """)
        except Exception as e:
            self.con.execute('ROLLBACK')
            logging.error(e)
        finally:
            self.con.close()

    def upsert(self, id_columns=None):
        # Merge - UPSERT file into database
        insert_columns = ','.join(self.df.columns)
        # difference = set(self.df.columns) - set(id_columns)
        # insert_columns = ','.join(difference)
        update_columns = ','.join(self.df.columns.difference(['id']))

        self._stage()
        try:
            self.con.execute(f""" 
                MERGE INTO {self.table_name}
                USING (SELECT {','.join([f'$1:{col} as {col}' for col in insert_columns])}
                    FROM @my_{self.format}_stage/{self.file_name}.gz) t
                ON ({' and '.join([f't.{col} = {self.table_name}.{col}' for col in id_columns])})
                WHEN MATCHED THEN
                    UPDATE SET {','.join([f'{col}=t.{col}' for col in update_columns])}
                WHEN NOT MATCHED THEN INSERT ({','.join(insert_columns)})
                VALUES ({','.join([f't.{col}' for col in insert_columns])});""")
        except Exception as e:
            self.con.execute('ROLLBACK')
            logging.error(e)
        finally:
            self.con.close()

    @property
    def cleanup(self):
        # ClEAN UP - Drop stage, format and remove temp dir and files
        with self.connect() as con:
            con.execute(f"remove @my_{self.format}_stage/{self.file_name}.gz;")
            con.execute(f"drop stage my_{self.format}_stage")
        shutil.rmtree(self.path) 

#%%
# Snowflake Query class
class SnowflakerQuery(SnowflakerConnector):
    def __init__(self,*,output_path=None, **kwargs):
        super().__init__(**kwargs)
        self.output_path = output_path
    
    def query(self, query):
        try:
            self.df = pd.read_sql( query, self.con ) 
        except Exception as e:
            self.con.execute('ROLLBACK')
            logging.error(e)
        finally:
            self.con.close()

        if self.output_path:
            self.df.to_csv(self.output_path, index=False)
            return None
        else:
            return self.df
#%%
# Snowflake Main abstract class
class Snowflaker(SnowflakerUploader, SnowflakerQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

