# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def get():
#     return 'Hello World'

from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# from . import model, schema, crud
import memo_load.model as model
import memo_load.schema as schema
import memo_load.crud as crud
from memo_load.database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# メモ参照
@app.get("/memos", response_model=List[schema.MemoSchema])
async def read_memos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    memos = crud.get_memos(db, skip=skip, limit=limit)
    return memos

#メモ登録
@app.post("/memos", response_model=schema.MemoSchema)
async def create_memo(memo: schema.MemoCreatingSchema, db: Session = Depends(get_db)):
    return crud.create_memo(db=db, memo=memo)

