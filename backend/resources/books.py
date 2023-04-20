from flask import request
from flask_restful import Resource, fields, marshal_with
from sqlalchemy import func
from database.schemas import ReviewSchema
from database.models import db, Book, Review, Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.schemas import review_schema 
from database.schemas import  favorite_schema, Favorite
from database.schemas import book_schema, review_schema


book_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "author": fields.String,
    "isbn": fields.String,
}
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

class UserFavorites(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        return favorite_schema.dump(favorites), 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        form_data = request.get_json()
        new_favorite = favorite_schema.load(form_data)
        new_favorite.user_id = user_id
        db.session.add(new_favorite)
        db.session.commit()
        return favorite_schema.dump(new_favorite), 201
    
class GetBookInformation(Resource):
     @jwt_required()
     def get(self, book_id):
         user_id = get_jwt_identity()
         book = Book.query.get(book_id)
         if not book:
             return {"message": "Book not found"}, 404
         review = Review.query.filter_by(book_id=book_id).all()
         avg_rating = db.session.query(func.avg(Review.rating)).filter_by(book_id=book_id).scalar()
         user_favorited_book = Favorite.query.filter_by(user_id=user_id, book_id=book_id).first()

        # Create the response dictionary
         response = {
            "book": book_schema.dump(book),
            "reviews": review_schema.dump(ReviewSchema, many=True),
            "avg_rating": avg_rating,
            "user_favorited_book": bool(user_favorited_book)
        }

         return response, 200