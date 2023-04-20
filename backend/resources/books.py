from flask import request
from flask_restful import Resource, fields, marshal_with
from database.models import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.schemas import review_schema 
from database.schemas import  favorite_schema, Favorite


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