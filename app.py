from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from histo_diff_ui import db_utils


from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

app = Flask(__name__)
db = db_utils.get_db(app)
# app.config['SECRET_KEY'] = 'your_secret_key'
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

@app.route('/')
def index():
    return render_template('Homepage.html')

@app.route('/36-ComparisonORG')
def dashboard():
    return render_template('36-ComparisonORG.htm')

@app.route('/submit', methods=['POST'])
def submit_form():
    setID = request.form.get('setId')
    imageID = request.form.get('imageId')
    comment = request.form.get('comment')
    score = request.form.get('score')
    ranking = request.form.get('ranking')
    
    db_utils.insert_feedback(db,{"setID": setID, "imageID": imageID, "comment": comment, "score": score, "ranking": ranking})

    return redirect(url_for('index'))

@app.route('/api')
def api_form():
    return render_template('API_query_form.html')
@app.route('/api/get-all', methods=['GET'])
def get_all_feedback():
    data_list = db_utils.get_feedback_all(db)
    return jsonify(data_list)

@app.route('/api/display-all', methods=['GET'])
def display_all_feedback():
    data_list = db_utils.get_feedback_all(db)
    return render_template('API_result.html', data=data_list)

@app.route('/api/get-feedback', methods=['GET'])
def get_feedback():
    key = request.args.get('key')
    value = request.args.get('value')
    query = {key: value}

    if not key or not value:
        return render_template('API_error.html', error_message = "Key or value missing")

    data_list = db_utils.get_feedback_by_query(db,query)
    return jsonify(data_list)

@app.route('/api/display-feedback', methods=['GET'])
def display_feedback():
    key = request.args.get('key')
    value = request.args.get('value')
    query = {key: value}

    if not key or not value:
        return render_template('API_error.html', error_message="Key or value missing")

    data_list = db_utils.get_feedback_by_query(db, query)
    return render_template('API_result.html', data=data_list, key=key, value=value)

"""
retrieve data of one certain field (eg. scores) with filters(eg.image_ID=1)
eg. retrieve all comments of image 1
"""
@app.route('/api/filter-feedback', methods=['GET'])
def filter_feedback():
    field = request.args.get('field')
    filter_key = request.args.get('filter_key')
    filter_value = request.args.get('filter_value')

    if not filter_key or not filter_value:
        return render_template('API_error.html', error_message = "Filter key or value missing")

    # construct the query
    query_filter = {filter_key: filter_value}
    projection = {field: 1, "_id": 0}

    # perform the query
    feedback = db_utils.get_feedback_by_field(db, query_filter, projection)
    return jsonify(feedback)

@app.route('/api/display-filter-feedback', methods=['GET'])
def display_filter_feedback():
    field = request.args.get('field')
    filter_key = request.args.get('filter_key')
    filter_value = request.args.get('filter_value')

    if not filter_key or not filter_value:
        return render_template('API_error.html', error_message="Filter key or value missing")

    # construct the query
    query_filter = {filter_key: filter_value}
    projection = {field: 1, "_id": 0}

    # perform the query
    feedback = db_utils.get_feedback_by_field(db, query_filter, projection)
    return render_template('filter_result.html',data = feedback, field = field, filter_key = filter_key, filter_value = filter_value)
# @app.route('/clam',methods=['GET'])
# def clam_view():
#     return render_template('Homepage.html')

if __name__ == '__main__':
    app.run(debug=True)

