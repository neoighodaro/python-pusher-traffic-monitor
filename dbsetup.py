
import sqlite3
from sqlite3 import Error
 
def create_connection(database):
    try:
        conn = sqlite3.connect(database, isolation_level=None, check_same_thread = False)
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        
        return conn
    except Error as e:
        print(e)
        
def create_table(c,sql):
    c.execute(sql)
    
def update_or_create_page(c,data):
    sql = "SELECT * FROM pages where name=? and session=?"
    c.execute(sql,data[:-1])
    result = c.fetchone()
    if result == None:
        create_pages(c,data)
    else:
        print(result)
        update_pages(c, result['id'])
 
def create_pages(c, data):
    print(data)
    sql = ''' INSERT INTO pages(name,session,first_visited)
              VALUES (?,?,?) '''
    c.execute(sql, data)
    
def update_pages(c, pageId):
    print(pageId)
    sql = ''' UPDATE pages
              SET visits = visits+1 
              WHERE id = ?'''
    c.execute(sql, [pageId])
    
def create_session(c, data):
    sql = ''' INSERT INTO sessions(ip, continent, country, city, os, browser, session, created_at)
              VALUES (?,?,?,?,?,?,?,?) '''
    c.execute(sql, data)
    
def select_all_sessions(c):
    sql = "SELECT * FROM sessions"
    c.execute(sql)
    rows = c.fetchall()
    return rows
    
def select_all_pages(c):
    sql = "SELECT * FROM pages"
    c.execute(sql)
    rows = c.fetchall()
    return rows
    
def select_all_user_visits(c, session_id):
    sql = "SELECT * FROM pages where session =?"
    c.execute(sql,[session_id])
    rows = c.fetchall()
    return rows
 
def main():
    database = "./pythonsqlite.db"
    sql_create_pages = """ 
        CREATE TABLE IF NOT EXISTS pages (
            id integer PRIMARY KEY,
            name varchar(225) NOT NULL,
            session varchar(255) NOT NULL,
            first_visited datetime NOT NULL,
            visits integer NOT NULL Default 1
        ); 
    """
    sql_create_session = """ 
        CREATE TABLE IF NOT EXISTS sessions (
            id integer PRIMARY KEY,
            ip varchar(225) NOT NULL,
            continent varchar(225) NOT NULL, 
            country varchar(225) NOT NULL,
            city varchar(225) NOT NULL, 
            os varchar(225) NOT NULL, 
            browser varchar(225) NOT NULL, 
            session varchar(225) NOT NULL,
            created_at datetime NOT NULL
        ); 
    """
    
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create tables
        create_table(conn, sql_create_pages)
        create_table(conn, sql_create_session)
        print("Connection established!")
    else:
        print("Could not establish connection")
        
if __name__ == '__main__':
    main()