import sqlite3
from fastmcp import FastMCP
import os

mcp=FastMCP("expences tracker")

# database connection

db_path=os.path.join(os.path.dirname(__file__),"expenses.db")
categores_path=os.path.join(os.path.dirname(__file__),"categories.json")


def init_db():
    with sqlite3.connect(db_path) as connection:
        cursor=connection.cursor()

        cursor.execute("""
        create table if not exists expenses(
        
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        sub_category TEXT DEFAULT '' ,
        note TEXT DEFAULT ''
    )
        """)

init_db()



# creating mcp tool

@mcp.tool()
def add_expenses(date:str,amount:float,category:str,sub_category:str="",note:str=""):
    with sqlite3.connect(db_path) as connection:
        cursor=connection.cursor()

        cursor.execute("""
        INSERT INTO expenses(
        date,
        amount,
        category,
        sub_category,
        note
        )
        VALUES(?,?,?,?,?)
        """,
        (date,amount,category,sub_category,note)) 

        expenses_id=cursor.lastrowid
    return{
     "status":"ok",
     "expenses_id":expenses_id

    }    

@mcp.tool()
def list_expenses(start_date:str,end_date:str):
    with sqlite3.connect(db_path) as connection:
        cursor=connection.cursor()
        cursor.execute(
            """ SELECT 
            id,
            date,
            amount,
            category,
            sub_category,
            note

            FROM expenses WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date,end_date)

        )
        row=cursor.fetchall()
        column=[description[0] for description in cursor.description ]

    return  [dict(zip(column,row)) for row in row]
     


@mcp.resource("categories://data",mime_type="application/json")
def show_resource():
    with open(r"D:\mymcp\categories.json",'r',encoding='utf-8') as f:
        return f.read()




if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )