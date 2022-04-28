import flask
from flask import jsonify
from sqlalchemy import orm
from werkzeug.exceptions import abort

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'api_user',
    __name__,
    template_folder='../templates'
)


@blueprint.route('/api/delete_user/<int:id>', methods=['POST', 'DELETE'])
def delete_user(id):
    print(id)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    print(user)
    if not user:
        abort(404)
    session.delete(user)
    session.commit()

    return jsonify(f'successfully deleted user with id {id}')
