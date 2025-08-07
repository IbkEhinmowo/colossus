
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.listing import IncomingListing
from parsers.marketplace import MarketplaceParser
from database import engine, listings

app = FastAPI()

parsed_listings_queue = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://jlhkcmiblgookadimdmdbihbkbgeokbi"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
parser = MarketplaceParser()

@app.post("/listings")
def upload(lists: IncomingListing):
    parsed = [parser.parse(html) for html in lists.listings]
    for item in parsed:
        # print(f"Processing: Title: {item.title}\nPrice: {item.price}\nLocation: {item.location}\nLink: {item.link}\nJust Listed: {item.is_just_listed}\n")
        try:
            with engine.connect() as conn:
                trans = conn.begin()
                DATABASE_INSERT = listings.insert().values(
                    title=item.title,
                    price=item.price,
                    location=item.location,
                    link=item.link,
                    is_just_listed=item.is_just_listed
                )
                conn.execute(DATABASE_INSERT)
                trans.commit()
                print(f"Inserted listing into database: {item.title}")
                parsed_listings_queue.append(item)  # Only add to queue if DB insert succeeds
        except Exception as e:
            print(f"Error inserting into database: {str(e)}")
    return {"status": "received", "parsed_count": len(parsed)}