from fastapi import FastAPI,UploadFile,Form, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3

con = sqlite3.connect('dang.db', check_same_thread=False)
cur = con.cursor()

app = FastAPI()

SECRET ='super-coding'
manager = LoginManager(SECRET, '/login') #액세스 토큰을 만들어 주는 라이브러리 manager

#유저가 해당 db에 존재하는지 확인하는 함수
@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'''id="{data}"'''
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * from users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post("/login")
def login(id:Annotated[str, Form()],
           password:Annotated[str, Form(),]):
    user = query_user(id)
    print(user['password'])
    if not user:
        raise InvalidCredentialsException #서버에서 상태 코드를 내려줌 (401 자동 생성)
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data = {
        'sub' : {
        'id': user['id'],
        'name': user['name'],
        'email': user['email']
        }
    })
    return {'access_token': access_token}

@app.post("/signup")
def signup(id:Annotated[str, Form()],
           password:Annotated[str, Form(),],
           name: Annotated[str, Form(),],
           email: Annotated[str,Form()]
           ):
    cur.execute(f"""
                INSERT INTO users (id, name, email, password)
                VALUES ('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit()
    return '200'

@app.post("/items")
async def create_items(image:UploadFile,
                 title:Annotated[str,Form()], 
                 price:Annotated[int,Form()], 
                 description:Annotated[str,Form()], 
                 place:Annotated[str,Form()],
                 insertAt:Annotated[int,Form()],
                 ):
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items (title, image, price, description, place, insertAt)
                VALUES ('{title}', '{image_bytes.hex()}', {price}, '{description}', '{place}', '{insertAt}')
                """)
    con.commit()
    return '200'

@app.get("/items")
async def get_items(user=Depends(manager)): #인증된 회원일 경우에만
    con.row_factory = sqlite3.Row #특정 컬럼을 조회하기 위해 컬럼명도 같이 가져옴
    cur = con.cursor() #위치 업데이트
    rows = cur.execute(f"""
                       SELECT * FROM items
                       """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows)) #객체로 만들어 프론트엔드로 넘겨줌, 배열 형식

#이미지를 받아오기 위함
@app.get("/images/{item_id}")
async def get_image(item_id):
    cur = con.cursor()
    #16진법 hex
    image_bytes = cur.execute(f"""
                              SELECT image FROM items WHERE id = {item_id} 
                              """).fetchone()[0]
    #변환 필요
    return Response(content=bytes.fromhex(image_bytes))

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")