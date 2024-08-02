"""
This module contains the Meal table model.
"""
from database import db


class Meal(db.Model):
    """
    This class represents the meal table in the database.
    """
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.String(255), nullable=False)
    datetime: str = db.Column(db.String(80), nullable=False)
    is_in_diet: bool = db.Column(db.Boolean, nullable=False)
