from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


# model for database
class healthdata(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    app_name: str
    steps: int | None = Field(default=None, index=True)
    oxygen: str
    calories: str
    distance: str


# creating SQL engine
sqllite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqllite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.post("/healthdata/")
def add_data(data: healthdata, session: SessionDep) -> healthdata:
    # print(data)
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


@app.get("/healthdata/")
def get_data(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[healthdata]:
    dataitems = session.exec(select(healthdata).offset(offset).limit(limit)).all()
    return dataitems


# fetch by id
@app.get("/data/{data_id}")
def read_data(data_id: int, session: SessionDep) -> healthdata:
    data = session.get(healthdata, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data


# delete data
@app.delete("/data/{data_id}")
def delete_data(data_id: int, session: SessionDep):
    data = session.get(healthdata, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="data not found!")
    session.delete(data)
    session.commit()
    return {"ok": True}
