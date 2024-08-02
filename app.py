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


if __name__ == '__main__':
    app.run(debug=True)
