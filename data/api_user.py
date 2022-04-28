import flask
from flask import jsonify, request
from werkzeug.exceptions import abort

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'api_users',
    __name__,
    template_folder='../templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_all_users():
    session = db_session.create_session()
    users = session.query(User).all()
    if not users:
        return jsonify('пока что нет пользователей')
    return jsonify(
        {
            'users': [item.to_dict(only=(
                'id', 'name', 'surname', 'age', 'position', 'email',
                'speciality', 'address', 'modified_date')) for item in users]
        }
    )


@blueprint.route('/api/users/<int:id>', methods=['GET'])
def concretable_user(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if not user:
        return jsonify({f'users': [f'not user with id {id}']})
    return jsonify(
        {'users': [user.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'email',
                                      'speciality', 'address', 'modified_date'))]})


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['name', 'surname', 'age', 'position', 'email',
                                                 'speciality', 'address', 'password']):
        return jsonify({'error': 'Bad request'})
    elif request.json['id'] and session.query(User).filter(User.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    res = request.json
    if not isinstance(res['age'], int):
        return jsonify({'error': 'age must be integers'})
    user = User()
    user.surname = res["surname"]
    user.name = res["name"]
    user.age = res["age"]
    user.position = res["position"]
    user.speciality = res["speciality"]
    user.address = res["address"]
    user.email = res['email']
    user.set_password(res['password'])
    session.add(user)
    session.commit()


@blueprint.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if not user:
        abort(404)
    session.delete(user)
    session.commit()
    return jsonify(f'successfully deleted user with id {id}')


@blueprint.route('/api/users/<int:id>', methods=['PUT'])
def change_user(id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    res = request.json
    session = db_session.create_session()
    job = session.query(User).filter(User.id == id).first()
    if not job:
        abort(404)
    if 'surname' in res.keys():
        job.surname = res['surname']
    if 'name' in res.keys():
        job.name = res['name']
    if 'age' in res.keys():
        if not isinstance(res['age'], int):
            return jsonify({'error': 'age must be integers'})
        job.age = res['age']
    if 'position' in res.keys():
        job.position = res['position']
    if 'speciality' in res.keys():
        job.speciality = res['speciality']
    if 'address' in res.keys():
        job.address = res['address']
    if 'email' in res.keys():
        job.email = res['email']
    session.commit()
    return jsonify('successfully changed job')
