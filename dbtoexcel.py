import pandas as pd
import sqlite3
import os

def export_db():
    db_file = "database.db"
    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]

    try:
        os.mkdir("excel_files")
    except FileExistsError:
        print("")
    try :
        os.mkdir("excel_files\\history")
    except FileExistsError:
        print("")
    for table in tables:
        df = pd.read_sql_query(f"SELECT * from {table}", conn)
        excel_file = f"excel_files/{table}.xlsx"
        df.to_excel(excel_file, index=False)

    conn.close()

def hist_excel(hID):
    try:
        os.mkdir("excel_files")
    except FileExistsError:
        print("")
    try :
        os.mkdir("excel_files\\history")
    except FileExistsError:
        print("")
    conn = sqlite3.connect('database.db')

    query = f"SELECT * FROM history WHERE hID=?"
    df = pd.read_sql_query(query, conn, params=(hID,))
    a="excel_files\\history\\"+hID+".xlsx"
    df.to_excel(a, index=False)
    
    conn.close()