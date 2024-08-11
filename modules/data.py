import duckdb


def import_data():
    data = duckdb.sql(""" SELECT * FROM 'data/occurence-data.parquet' """)
    return data
