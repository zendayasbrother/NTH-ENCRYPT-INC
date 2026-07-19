from unittest import result
import bcrypt
import psycopg2  
from database import DataManager

class AuthSystem(DataManager): 
    def __init__(self, db_path):
        super().__init__(db_path)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password, hashed):
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def sign_up(self, email, username, password):
        conn, cursor = self.connect_database() #[cite: 4]
        if not conn: return False
        
        hashed = self.hash_password(password) #[cite: 4]

        try: 
            # 1. Fixed casing using double quotes, and added the trailing tuple comma
            cursor.execute('SELECT "Username", "FirstName" FROM "Users" WHERE "Email" = %s', (email,)) 
            record = cursor.fetchone()
            
            if not record: 
                print(f"[!] Access Denied: {email} not in Registry.") 
                return False 

            existing_username, first_name = record 

            if existing_username is None or existing_username in ["", "PENDING"]:
                query = 'UPDATE "Users" SET "Username" = %s, "HashedPassword" = %s WHERE "Email" = %s'
                cursor.execute(query, (username, hashed, email)) 
                
                if cursor.rowcount == 0: 
                    print("[!] Error: No rows updated. Check if Email matches exactly.") 
                    return False
                    
                conn.commit() 
                print(f"[*] Identity Verified for {first_name}. Credentials attached.")
                return True 
            else: 
                print(f"[!] Error: {email} already has username '{existing_username}'.") 
                return False
        
        except psycopg2.Error as e:
            print(f"Database Error during sign-up: {e}") 
            return False 
        finally: 
            if conn: 
                conn.close()
        
    def login(self, username, password):
        conn, cursor = self.connect_database()
        if not conn: return None, None
        
        try:
            cursor.execute("SELECT HashedPassword, FirstName, UserType FROM Users WHERE Username = %s", (username,))
            result = cursor.fetchone()
            
            if result and result[0] is not None: 
                if self.check_password(password, result[0]):
                    user_type = result[2]
                    first_name = result[1]

                    return user_type, first_name
                else:
                    print("[!] Invalid Password.")
            else:
                print("[!] User not found or account not fully registered.")
                
        except psycopg2.Error as e:
            print(f"Database Error during auth: {e}")
        finally:
            if conn:
                conn.close()
            
        return None, None