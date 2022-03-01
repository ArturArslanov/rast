import flask
from flask import jsonify

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'api_jobs',
    __name__,
    template_folder='../templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict(only=(
                'id', 'team_leader', 'job', 'work_size', 'start_date', 'end_date',
                'collaborators', 'is_finished')) for item in jobs]
        }
    )
