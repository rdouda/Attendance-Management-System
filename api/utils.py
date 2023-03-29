from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password):
    return password_context.hash(password)

def compare(password, hashed_password):
    return password_context.verify(password, hashed_password)