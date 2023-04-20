from flask import request
from flask_restful import Resource, fields, marshal_with
from database.models import db
from database.models import Book
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.schemas import review_schema 
from database.models import Review

book_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "author": fields.String,
    "isbn": fields.String,
}

class BookResource(Resource):
    @marshal_with(book_fields)
    def get(self, book_id=None):
        if book_id:
            book = Book.query.filter_by(id=book_id).first()
            if not book:
                return {"message": "Book not found"}, 404
            return book
        else:
            books = Book.query.all()
            return books

    @marshal_with(book_fields)
    def post(self):
        data = request.get_json()
        book = Book(title=data["title"], author=data["author"], isbn=data["isbn"])
        db.session.add(book)
        db.session.commit()
        return book, 201

    def delete(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return {"message": "Book not found"}, 404
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted"}, 204

class ReviewResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        form_data = request.get_json()
        new_review = review_schema.load(form_data)
        new_review.user_id = user_id
        db.session.add(new_review)
        db.session.commit()
        return review_schema.dump(new_review), 201