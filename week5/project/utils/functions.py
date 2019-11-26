def val_pass(password):
    for char in password:
        if char.isdigit():
            return True
    return False