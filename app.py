from flask import Flask, jsonify, request, redirect
from tinydb import TinyDB, Query
from flask_cors import CORS
from datetime import date,timedelta,datetime



app = Flask(__name__)
CORS(app)

db = TinyDB('db.json')
items_table = db.table('items')
userstore_table = db.table('userstore')

@app.route('/', methods=['GET'])
def redirect_to_login():
    return redirect("https://karmugil.netlify.app/", code=302)

@app.route('/items', methods=['GET'])
def get_items():
    items = items_table.all()
    return jsonify(items)



@app.route('/items', methods=['POST'])
def add_item():
    item = request.get_json()
    items_table.insert(item)
    return '', 201


@app.route('/user', methods=['POST'])
def add_user():
    item = request.get_json()
    username = request.headers.get('username')
    password = request.headers.get('password')
    if username and password:
        item['username'] = username
        item['password'] = password
    userstore_table.insert(item)
    return '', 201


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    User = Query()
    user = userstore_table.get(User.username == username)
    if user:
        return jsonify({'username': user['username'], 'password': user['password']}), 200
    else:
        return jsonify({'success': False, 'message': 'User not found'}), 404


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = items_table.get(doc_id=item_id)
    if item:
        return jsonify(item)
    else:
        return '', 404


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = request.get_json()
    items_table.update(item, doc_ids=[item_id])
    return ''


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items_table.remove(doc_ids=[item_id])
    return ''

@app.route('/items/user/<username>', methods=['GET'])
def get_items_by_user_and_date(username):
    User = Query()
    user = userstore_table.get(User.username == username)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    today = date.today().strftime('%Y-%m-%d')
    items = items_table.search((Query().USERNAME == username) & (Query().DATE == today))
    count = len(items)
    percentage= int((count/80)*100)
    return jsonify({'username': username, 'date': today, 'count': count, 'percentage':percentage}), 200


@app.route('/items/date', methods=['GET'])
def get_items_by_date():
    today = date.today().strftime('%Y-%m-%d')
    items = items_table.search(Query().DATE == today)
    return jsonify(items), 200


@app.route('/items/week', methods=['GET'])
def get_items_by_date_week():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)
    
    items = items_table.search((Query().DATE >= start_date.strftime('%Y-%m-%d')) & (Query().DATE <= end_date.strftime('%Y-%m-%d')))
    return jsonify(items), 200

@app.route('/items/month', methods=['GET'])
def get_items_by_date_month():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)
    
    items = items_table.search((Query().DATE >= start_date.strftime('%Y-%m-%d')) & (Query().DATE <= end_date.strftime('%Y-%m-%d')))
    return jsonify(items), 200


@app.route('/items/users', methods=['GET'])
def get_user_per():
    today = date.today().strftime('%Y-%m-%d')
    users = userstore_table.all()
    performance_data = []
    for user in users:
        username = user['username']
        items = items_table.search((Query().USERNAME == username) & (Query().DATE == today))
        count = len(items)
        percentage = int((count / 80) * 100)  # Target count is 80 in this example
        performance_data.append({'username': username, 'date': today, 'count': count, 'percentage': percentage})
    return jsonify(performance_data), 200



if __name__ == '__main__':
    app.run(debug=True, port=5000)
