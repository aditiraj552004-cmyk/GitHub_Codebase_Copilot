def login(username, password):
    if username == "admin" and password == "1234":
        print("Login successful")
        return True

    print("Invalid credentials")
    return False