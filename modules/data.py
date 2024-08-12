import duckdb


def import_data():
    data = duckdb.sql(""" SELECT * FROM 'data/occurence-data.parquet' """)
    return data


def import_image():
    data = duckdb.sql(""" SELECT * FROM 'data/multimedea.parquet' """)
    return data
