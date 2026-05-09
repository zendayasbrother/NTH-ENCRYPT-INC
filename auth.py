import bcrypt
import sqlite3  
from database import DataManager

class AuthSystem(DataManager): 
    def __init__(self, db_path):
        super().__init__(db_path)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password, hashed):
        # Convert stored TEXT back to bytes for comparison
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def sign_up(self, email, username, password):
        
        conn, cursor = self.connect_database()
        hashed = self.hash_password(password)

        try:
            # Check if email exists and if it already has a username
            cursor.execute("SELECT Username, FirstName FROM Users WHERE Email = ?", (email,))
            record = cursor.fetchone()

            if record:
                existing_username, first_name = record

                
                if existing_username is None or existing_username == "" or existing_username == "PENDING":
                    query = "UPDATE Users SET Username = ?, HashedPassword = ? WHERE Email = ?"
                    cursor.execute(query, (username, hashed, email))
                    conn.commit()
                    print(f"[*] Identity Verified for {first_name}. Credentials attached to {email}")
                    return True
                else:
                    print(f"[!] Error: Account for {email} is already registered.")
                    return False
            else:
                print("[!] Access Denied: Email not recognized in Encrypt Inc Registry.")
                return False

        except sqlite3.Error as e:
            print(f"Auth Error: {e}")
            return False
        finally:
            conn.close()

    def authenticate_user(self, username, password):
        conn, cursor = self.connect_database()
        if not conn: return None, None
        
        try:
            cursor.execute("SELECT HashedPassword, FirstName, UserType FROM Users WHERE Username = ?", (username,))
            result = cursor.fetchone()
            
            # CHECK: Does the user exist AND do they have a hashed password stored?
            if result and result[0] is not None: 
                if self.check_password(password, result[0]):
                    return result[2], result[1] # UserType, FirstName
                else:
                    print("[!] Invalid Password.")
            else:
                print("[!] User not found or account not fully registered.")
                
        except sqlite3.Error as e:
            print(f"Database Error during auth: {e}")
        finally:
            conn.close()
            
        return None, None
        
    def plant_seeds(self): 
       pass