from flask import Flask, request, make_response, jsonify
from database import db
from models.meal import Meal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)


@app.route('/meal', methods=['POST'])
def create_meal():
    """
    This function creates a new meal.
    Returns:
        Response: Message with the created meal.
    """

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    datetime = data.get('date_hour')
    is_in_diet = data.get('is_in_diet')

    if name and description and datetime:
        meal = Meal(name=name, description=description, datetime=datetime, is_in_diet=is_in_diet)
        db.session.add(meal)
        db.session.commit()
        return make_response(jsonify({'message': 'Meal created successfully'}))
    return make_response(jsonify({'message': 'Missing parameters'}), 400)


@app.route('/meal', methods=['GET'])
def get_meals():
    """
    This function gets all meals.
    Returns:
        Response: List of meals.
    """

    meals = Meal.query.all()
    meals_list = []
    for meal in meals:
        meals_list.append({
            'id': meal.id,
            'name': meal.name,
            'description': meal.description,
            'datetime': meal.datetime,
            'is_in_diet': meal.is_in_diet
        })
    return make_response(jsonify(meals_list))

@app.route('/meal/<int:meal_id>', methods=['GET'])
def get_meal_by_id(meal_id):
    """
    This function gets a meal by id.
    Args:
        meal_id (int): The meal id.
    Returns:
        Response: The meal.
    """

    meal = Meal.query.get(meal_id)
    if meal:
        return make_response(jsonify({
            'id': meal.id,
            'name': meal.name,
            'description': meal.description,
            'datetime': meal.datetime,
            'is_in_diet': meal.is_in_diet
        }))
    return make_response(jsonify({'message': 'Meal not found'}), 404)


@app.route('/meal/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    """
    This function updates a meal.
    Args:
        meal_id (int): The meal id.
    Returns:
        Response: Message with the updated meal.
    """

    meal = Meal.query.get(meal_id)
    if meal:
        data = request.get_json()
        meal.name = data.get('name', meal.name)
        meal.description = data.get('description', meal.description)
        meal.datetime = data.get('date_hour', meal.datetime)
        meal.is_in_diet = data.get('is_in_diet', meal.is_in_diet)
        db.session.commit()
        return make_response(jsonify({'message': 'Meal updated successfully'}))
    return make_response(jsonify({'message': 'Meal not found'}), 404)
        

@app.route('/meal/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    """
    This function deletes a meal.
    Args:
        meal_id (int): The meal id.
    Returns:
        Response: Message with the deleted meal.
    """

    meal = Meal.query.get(meal_id)
    if meal:
        db.session.delete(meal)
        db.session.commit()
        return make_response(jsonify({'message': 'Meal deleted successfully'}))
    return make_response(jsonify({'message': 'Meal not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
