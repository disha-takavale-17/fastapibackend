
import json
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Reads the JSON file and gives you back the list of users.
def get_users_json():
    users_data=[]    #default empty users_data list incase the file is missing
    with open("app/fixtures/user_list.json") as f:
        users_data = json.load(f)["user_list"]
    return users_data
         

# Purpose: Writes changes back into the JSON file.         
def save_users_json(users):
    if not users:
        print("Warning: Attempted to save empty user list. Skipping save.")
        return
    
    with open("app/fixtures/user_list.json", "w") as f:
        json.dump({"user_list": users}, f)

def is_username_taken(users, username: str):
    """Return True if username already exists in user_list."""
    for u in users:
        if u["username"] == username:
            return True
    return False




# If multiple routes need to read/write users, 
# you don’t want to duplicate open("app/fixtures/user_list.json") everywhere.

# Instead, you call get_users_json()         