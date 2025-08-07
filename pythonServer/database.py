
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, UniqueConstraint
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

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
