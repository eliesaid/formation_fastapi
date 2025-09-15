from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

# Conversion automatique : Pydantic convertit "42" (str) en 42 (int)
user = User(id="42", name="Alice")

print(user)       # User(id=42, name='Alice')
print(user.id)    # 42
print(type(user.id))  # <class 'int'>

