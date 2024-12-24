import re

def is_valid_email(email):
    # Define the regex pattern for a valid email address
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Use re.match() to check if the email matches the pattern
    if re.match(email_regex, email):
        return True
    else:
        return False

# Example usage
email = "example@example.com"
if is_valid_email(email):
    print(f"{email} is valid.")
else:
    print(f"{email} is invalid.")
