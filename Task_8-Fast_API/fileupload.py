import os
import cv2
import shutil
import numpy as np
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    Depends,
    Form,
    Query,
    Request,
    Response,
)
from sqlmodel import Field, Session, SQLModel, create_engine, select


# model for database
class imageupload(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str


sqlite_file_name = "filedata.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def creat_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    creat_db()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ROTATED_DIR = "rotated"
os.makedirs(ROTATED_DIR, exist_ok=True)

app.mount("/rotated", StaticFiles(directory=ROTATED_DIR), name="rotated")

def save_to_db(data: imageupload, session: SessionDep) -> imageupload:
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


@app.post("/upload/")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    try:
        image = file.filename
        file_loc = os.path.join(UPLOAD_DIR, image)

        with open(file_loc, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        imgdata = imageupload(filename=image)
        db_entry = save_to_db(data=imgdata, session=session)

        print(f"image >> {image}")

        img = cv2.imread(file_loc)
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        rotate = cv2.rotate(img, cv2.ROTATE_180)
        rotated_filename = f"rotated_{image}"
        rotate_loc = os.path.join(ROTATED_DIR, rotated_filename)
        cv2.imwrite(rotate_loc, rotate)

        base_url = str(request.base_url)
        image_url = f"{base_url}rotated/{rotated_filename}"

        return {
            "message": f"Successfully uploaded {image}",
            "db": db_entry,
            "image_url": image_url,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occured in file uplaod!{e}")
    finally:
        await file.close()