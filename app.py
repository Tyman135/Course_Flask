import random
from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False


quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
   },
   {
       "id": 6,
       "author": "Mosher's Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так."
   },

]

about_me = {
    "name": "Иван",
    "surname": "Дудыкин",
    "email": "dudykin@list.ru"
}


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.get("/quotes")
def get_quotes():
    return jsonify(quotes)


@app.route("/about")
def about():
    return about_me


@app.get("/quotes/<int:quote_id>")
def quot_id(quote_id: int):
    for quote in quotes:
        if quote["id"] == quote_id:
            return jsonify(quote), 200
    return jsonify(error=f"Quote with id={quote_id} not found"), 404


@app.get("/quotes/count")
def get_count():
    return {"count": len(quotes)}


@app.get("/quotes/random")
def get_random_quote():
    if not quotes:
        return jsonify(error="No quotes available"), 404
    return jsonify(random.choice(quotes))


def get_next_id() -> int:
    if not quotes:
        return 1
    return quotes[-1]["id"] + 1


def validate_rating(rating):
    if 1 <= rating <= 5:
        return rating
    return 1 # Значение по умолчанию


@app.get("/quotes/<int:quote_id>")
def get_quote(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return jsonify(quote), 200
    return jsonify(error=f"Quote with id={quote_id} not found"), 404


@app.post("/quotes")
def create_quote():
    data = request.json
    client_rating = data.get("rating", 1)

    new_quote = {
        "id": get_next_id(),
        "author": data.get("author"),
        "text": data.get("text"),
        "rating": validate_rating(client_rating)
    }
    quotes.append(new_quote)
    return jsonify(new_quote), 201


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    new_data = request.json
    for quote in quotes:
        if quote["id"] == quote_id:
            if "author" in new_data:
                quote["author"] = new_data["author"]
            if "text" in new_data:
                quote["text"] = new_data["text"]
            if "rating" in new_data:
                new_rating = new_data["rating"]
                if 1 <= new_rating <= 5:
                    quote["rating"] = new_rating
            return jsonify(quote), 200
    return jsonify(error="Not found"), 404


@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote(quote_id):
    for i in range(len(quotes)):
        if quotes[i]["id"] == quote_id:
            quotes.pop(i)
            return jsonify({"message": f"Quote with id {quote_id} is deleted."}), 200
    return jsonify({"error": "Quote not found"}), 404


@app.route("/quotes/filter", methods=['GET'])
def filter_quotes():
    author = request.args.get("author")
    rating = request.args.get("rating")

    result = []
    for quote in quotes:
        match_author = (author is None or quote["author"].lower() == author.lower())
        match_rating = (rating is None or quote.get("rating", 0) == int(rating))

        if match_author and match_rating:
            result.append(quote)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)