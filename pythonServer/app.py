
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.listing import IncomingListing
from parsers.marketplace import MarketplaceParser

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
        # print(f"Title: {item.title}\nPrice: {item.price}\nLocation: {item.location}\nLink: {item.link}\nJust Listed: {item.is_just_listed}\n")
        parsed_listings_queue.append(item)
    return {"status": "received", "parsed_count": len(parsed)}
