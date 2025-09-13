
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.listing import IncomingListing
from parsers.marketplace import MarketplaceParser
from database import engine, listings
from models.llm_sort import get_llm_response
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
    queued_count = 0
    for item in parsed:
        try:
            with engine.connect() as conn:
                # First, check if the listing already exists in the database.
                check_query = listings.select().where(
                    listings.c.title == item.title,
                    listings.c.price == item.price,
                    listings.c.link == item.link
                )
                result = conn.execute(check_query).fetchone()

                # If it exists, we've already processed it. Skip.
                if result:
                    continue

                # If it's a new listing, insert it into the database first.
                # This prevents re-running the LLM on subsequent runs.
                if not item.is_just_listed:
                    continue  # Optional: still skip if not a fresh listing

                DATABASE_INSERT = listings.insert().values(
                    title=item.title,
                    price=item.price,
                    location=item.location,
                    link=item.link,
                    is_just_listed=item.is_just_listed
                )
                conn.execute(DATABASE_INSERT)
                conn.commit()

                # Now, for this new item, check if it's relevant for a notification.
                if get_llm_response(f"Is the following listing a tech item? '{item.title}'"):
                    print(f"Listing accepted by LLM: {item.title} at {item.price}")
                    parsed_listings_queue.append(item)
                    queued_count += 1
                else:
                    print(f"Listing filtered out by LLM: {item.title} at {item.price}")

        except Exception as e:
            print(f"Error processing listing: {str(e)}")
    return {"status": "received", "parsed_count": len(parsed), "queued_for_discord": queued_count}




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