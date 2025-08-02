
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
    for p in parsed:
        # print(f"Title: {p.title}\nPrice: {p.price}\nLocation: {p.location}\nLink: {p.link}\nJust Listed: {p.is_just_listed}\n")
        parsed_listings_queue.append(p)
    return {"status": "received", "parsed_count": len(parsed)}








# app = Flask(__name__)
# @app.route('/', methods=['GET', 'POST'])

# def index():
#     return "Welcome to the Flask server!"


# @app.route('/listings', methods=['GET','POST'])
# def receive():
#     data = request.get_json()
#     print("Headers received:", dict(request.headers))

#     if not data or 'listings' not in data:
#         return jsonify({'error': 'No listings provided'}), 400

#     listings = data['listings']
#     # Here you can process the listings as needed
#     print("Received listings:", listings)

#     return jsonify({'status': 'success', 'message': 'Listings received successfully'}), 200




# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, port=5001)
