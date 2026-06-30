import bcrypt
import sqlite3  
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
        conn, cursor = self.connect_database()
        hashed = self.hash_password(password)

        try: 
            cursor.execute("SELECT Username, FirstName FROM Users WHERE Email = ?", (email,)) 
            record = cursor.fetchone()
            
            if not record:
                print(f"[!] Access Denied: {email} not in Registry.")
                return False

            # FIX 1: Move the unpacking inside the try block and AFTER the 'None' check
            existing_username, first_name = record

            if existing_username is None or existing_username in ["", "PENDING"]:
                query = "UPDATE Users SET Username = ?, HashedPassword = ? WHERE Email = ?"
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
        
        except sqlite3.Error as e:
            print(f"Database Error during sign-up: {e}")
            return False
        finally:
            if conn:
                conn.close()
        
    def authenticate_user(self, username, password):
        conn, cursor = self.connect_database()
        if not conn: return None, None
        
        try:
            cursor.execute("SELECT HashedPassword, FirstName, UserType FROM Users WHERE Username = ?", (username,))
            result = cursor.fetchone()
            
            if result and result[0] is not None: 
                if self.check_password(password, result[0]):
                    return result[2], result[1] 
                else:
                    print("[!] Invalid Password.")
            else:
                print("[!] User not found or account not fully registered.")
                
        except sqlite3.Error as e:
            print(f"Database Error during auth: {e}")
        finally:
            if conn:
                conn.close()
            
        return None, None
        
    def plant_seeds(self): 
       self.success = self.sign_up()
       if self.success:
        print(f"[*] Seed planted: {self.first_name} is now registered.")
        return self.success