from flask import Flask, jsonify, request
from sqlalchemy import select
from db import db
from orm.models import Quotes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/flask_bd'
app.json.ensure_ascii = False

db.init_app(app)


@app.get("/quotes")
def get_quotes():
    author = request.args.get("author")
    rating = request.args.get("rating")
    stmt = select(Quotes)
    if author:
        stmt = stmt.where(Quotes.author.ilike(f"%{author}%"))
    if rating:
        stmt = stmt.where(Quotes.rating == int(rating))
    quotes_list = db.session.execute(stmt).scalars().all()
    return jsonify([q.to_dict() for q in quotes_list])


@app.get("/quotes/<int:quote_id>")
def get_quote(quote_id):
    quote = db.session.get(Quotes, quote_id)
    if quote:
        return jsonify(quote.to_dict()), 200
    return jsonify(error=f"Quote with id={quote_id} not found"), 404


@app.post("/quotes")
def create_quote():
    data = request.json
    new_quote = Quotes(
        author=data.get("author"),
        text=data.get("text"),
        rating=data.get("rating", 1)
    )
    db.session.add(new_quote)
    db.session.commit()
    return jsonify(new_quote.to_dict()), 201


@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id):
    quote = db.session.get(Quotes, quote_id)
    if not quote:
        return jsonify(error="Not found"), 404

    data = request.json
    if "author" in data:
        quote.author = data["author"]
    if "text" in data:
        quote.text = data["text"]
    if "rating" in data:
        new_rating = data["rating"]
        if 1 <= new_rating <= 5:
            quote.rating = new_rating

    db.session.commit()
    return jsonify(quote.to_dict()), 200


@app.delete("/quotes/<int:quote_id>")
def delete_quote(quote_id):
    quote = db.session.get(Quotes, quote_id)
    if not quote:
        return jsonify(error="Not found"), 404

    db.session.delete(quote)
    db.session.commit()
    return jsonify(message=f"Quote with id {quote_id} is deleted."), 200


if __name__ == "__main__":
    app.run(debug=True)
