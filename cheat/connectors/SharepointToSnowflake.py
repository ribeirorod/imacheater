
from sharepoint import SharepointDownloader
from snowflake import SnowflakerUploader


def main(**kwargs):

    url = kwargs.get('url')
    file_url = kwargs.get('file_url')

    #Sharepoint Downloader
    sp = SharepointDownloader(url=url, file_url=file_url)
    sp.download
    args , df = sp.df

    table = args.get('table')
    schema = args.get('schema')
    database = args.get('database')
    id_cols = args.get('id_columns', None)

    #Snowflake Uploader
    sf = SnowflakerUploader(input = df, db=database, sh=schema, table_name=table)

    if not id_cols:
        sf.insert
    else:
        sf.upsert(id_columns=id_cols)
    
    sf.cleanup()

