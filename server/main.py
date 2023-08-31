from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#requirement
from schemas.index import Users, Auth
from config.db import conn
from models.index import users

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:3306",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def getPassword(username:str):
    data = conn.execute(users.select().where(users.c.username == username)).fetchall()
    password = data[0]['password']
    return password

@app.get("/users")
async def index():
    data = conn.execute(users.select().order_by('id')).fetchall()
    return {
        "status": "OKE!",
        "data": data
    }
    
@app.post("/users/{id}")
async def search(id:int):
    data = conn.execute(users.select().where(users.c.id == id)).fetchall()
    return {
        "status": "OKE!",
        "data": data
    }
    
@app.post("/findusers/{name}")
async def findName(name:str):
    data = conn.execute(users.select().where(users.c.username == name)).fetchall()
    if len(data) == 0:
        return {
            "status": "error",
            "msg": "Data not found"
        }
    else:
        return {
            "status": "OKE!",
            "data": data
        }
    
@app.post("/createusers")
async def create(user: Users):
    data = conn.execute(users.insert().values(
        username = user.username,
        email = user.email,
        password = user.password
    ))
    if data.is_insert:
        return {
            "status": "OKE!",
            "msg": "success insert record",
            "data": user.dict()
        }
    else:
        return {
            "status": "error",
            "msg": "Something went wrong",
        }

@app.post("/auth/login")
async def authLogin(auth: Auth):
    data = conn.execute(users.select().where(users.c.username == auth.username)).fetchall()
    if len(data) != 0:
        password = await getPassword(auth.username)
        if auth.password == password:
            return {
                "status": "success",
                "msg": "Access Granted",
            }
        else:
            return {
                "status": "error",
                "msg": "Password is incorrect",
            }
    else:
        return {
            "status": "error",
            "msg": "Access Denied",
        }