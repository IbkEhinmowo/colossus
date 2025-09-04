
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.listing import IncomingListing
from parsers.marketplace import MarketplaceParser
from database import engine, listings
import datetime

app = FastAPI()

parsed_listings_queue = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
parser = MarketplaceParser()

@app.post("/listings")
def upload(lists: IncomingListing):
    parsed = [parser.parse(html) for html in lists.listings]
    success_count = 0
    for item in parsed:
        try:
            with engine.connect() as conn:
                # Check for duplicate by link before inserting
                check_query = listings.select().where(listings.c.link == item.link)
                result = conn.execute(check_query).fetchone()
                if result:
                    print(f"Duplicate listing skipped: {item.title}")
                    continue
                if not item.is_just_listed :
                    continue  # Skip non-just-listed items
                DATABASE_INSERT = listings.insert().values(
                    title=item.title,
                    price=item.price,
                    location=item.location,
                    link=item.link,
                    is_just_listed=item.is_just_listed
                )
                conn.execute(DATABASE_INSERT)
                conn.commit()
                print(f"Inserted listing into database: {item.title}")
                parsed_listings_queue.append(item)
                success_count += 1
        except Exception as e:
            print(f"Error inserting into database: {str(e)}")
    return {"status": "received", "parsed_count": len(parsed), "inserted_count": success_count}




@app.delete("/PurgeDatabase")
def purge_database():
    try:
        with engine.connect() as conn:
            purge_query = listings.delete()
            result = conn.execute(purge_query)
            conn.commit()
            return {"status": "success"}
            
    except Exception as e:
            print(f"Error purging database: {str(e)}")
            return {"status": "error", "message": str(e)}