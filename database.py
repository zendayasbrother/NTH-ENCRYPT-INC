import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect_database(self):
        if not self.db_path or not os.path.exists(self.db_path):
            print(f"Error: Database file not found at {self.db_path}")
            return None, None
            
        try:
            # Added timeout to handle the OneDrive/Locked file issue
            con = psycopg2.connect(self.db_path, timeout=20)
            cursor = con.cursor()
            
            cursor.execute("PRAGMA integrity_check;")
            if cursor.fetchone()[0] == "ok":
                return con, cursor
        except psycopg2.Error as error:
            print(f"Database error: {error}")
            return None, None

    def display_table(self, table_name):
        conn, _ = self.connect_database()
        if conn:
            try:
                # pandas makes SQL results look like a clean spreadsheet
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                
                if df.empty:
                    print(f"\n[!] The {table_name} table is currently empty.")
                else:
                    if table_name.lower() == "users" and 'HashedPassword' in df.columns:
                        df = df.drop(columns=['HashedPassword']) # drops the HashedPassword column for security reasons
                    print(f"\n--- {table_name} Table ---")
                    print(df.to_string(index=False)) 
            except Exception as e:
                print(f"Error reading table: {e}")
            finally:
                conn.close() # edit database accordingly (createdAt timestamps for Proposals and Projects alike)