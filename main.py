from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Item
import pandas as pd
from schemas import ItemCreate
import io

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/")
def get_all_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.id == item_id).first()

@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}

@app.post("/upload-items/")
async def upload_items(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        filename = file.filename.lower()

        # Detect file type
        if filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Only CSV or Excel files are supported.")

        # Validate required columns
        required_columns = {"name", "description"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail=f"Missing columns: {required_columns - set(df.columns)}")

        # Convert rows to SQLAlchemy objects
        items = [Item(name=row["name"], description=row["description"]) for _, row in df.iterrows()]
        db.bulk_save_objects(items)
        db.commit()

        return {"message": f"{len(items)} items inserted successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


