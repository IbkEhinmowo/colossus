from flask import Flask, request, jsonify


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def index():
    return "Welcome to the Flask server!"


@app.route('/listings', methods=['GET','POST'])
def receive():
    data = request.get_json()
    print("Headers received:", dict(request.headers))

    if not data or 'listings' not in data:
        return jsonify({'error': 'No listings provided'}), 400

    listings = data['listings']
    # Here you can process the listings as needed
    print("Received listings:", listings)

    return jsonify({'status': 'success', 'message': 'Listings received successfully'}), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
