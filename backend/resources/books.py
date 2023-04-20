import dbm
from flask import request
from flask_restful import Resource, fields, marshal_with
from database.models import db
from database.models import Book


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
