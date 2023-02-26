from pydantic import BaseModel
import random
import string

class PasswordGeneratorRequest(BaseModel):
    length: int
    
def generate_password(request: PasswordGeneratorRequest):
    letters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(letters) for i in range(request.length))
    return {"password": password}