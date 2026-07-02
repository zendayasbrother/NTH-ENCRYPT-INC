import os
import pwinput
from engine import ManagementSystem
from auth import AuthSystem
from dotenv import load_dotenv

def run_app(auth, engine):
    print("--- Encrypt Inc. OS ---")
    auth_choice = input("Do you have an account? (yes/no): ").strip().lower()

    if auth_choice == "no":
        email = input("Enter your email for verification: ")
        username = input("Choose a username: ")
        password = pwinput.pwinput(prompt="Password: ", mask="*")
        corpcode = input("Enter your corporate code: ")
        success = auth.sign_up(email, username, password)
        if success:
            print("[*] Sign-up successful. You can now log in.")
        else:
            print("[!] Sign-up failed. Please try again.")
            return

    if auth_choice == "yes":
        username = input("Username: ")
        password = pwinput.pwinput(prompt="Password: ", mask="*")
        login_result = auth.login(username, password)
        if login_result:
            user_type, first_name = login_result
            print("[*] Login successful. You can now log in.")
            if user_type:
                print(f"[*] Login successful. Welcome {first_name}.")
                engine.current_user = username
                engine.current_user_type = user_type
                engine.current_user_first_name = first_name

                if user_type == "Admin":
                    engine.admin_interface()
                else:
                    engine.talent_interface()
        else:
            print("[!] Login failed. Please check your credentials.")
    else:
        print("[!] Authentication failed. Please enter 'yes' or 'no' to proceed.")
        return



if __name__ == "__main__":
    load_dotenv()
    db_path = os.getenv("DB_PATH")

    if db_path and os.path.exists(db_path):
        auth = AuthSystem(db_path)
        engine = ManagementSystem(db_path)
        run_app(auth, engine)
    else:
        print(f"Error: Database path is invalid or missing.")