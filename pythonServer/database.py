
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, UniqueConstraint
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
connection = engine.connect()
metadata = MetaData()

listings = Table(
    "listings", 
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("price", String),
    Column("location", String),
    Column("link", String ),
    Column("is_just_listed", Boolean),
    UniqueConstraint("title", "price", name="uix_title_price")

)

metadata.create_all(engine)
