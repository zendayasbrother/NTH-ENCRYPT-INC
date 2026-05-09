from auth import AuthSystem

class ManagementSystem(AuthSystem):
    def __init__(self, db_path):
        AuthSystem.__init__(self, db_path)
        
    def run_app(self):
        print("--- Encrypt Inc. OS ---")
        user = input("Username: ")
        pw = input("Password: ")
        
        # This calls the standard auth check
        user_type, first_name = self.authenticate_user(user, pw)
        
        if user_type:
            print(f"\nLogin Successful! Welcome: {first_name} // ({user_type.upper()})")
            if user_type == "Admin":
                self.admin_interface() 
            else:
                self.talent_interface()
        else:
            print("\nAccess Denied.")

    def admin_interface(self):
        # Continue the admin interface here, allowing admins to view any table and manage records.
        name = input("Enter the table name to display: ")
        self.display_table(name)
        
    def talent_interface(self):
        # Continue the talent interface here, allowing talents to view only their own records.
        print(f"Accessing your records...") 

        
        