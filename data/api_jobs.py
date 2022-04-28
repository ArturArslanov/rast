from datetime import datetime
from json import loads

import flask
from flask import jsonify, request
from sqlalchemy import orm
from werkzeug.exceptions import abort

from . import db_session
from .jobs import Jobs
from .users import User

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


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=(
                'id', 'team_leader', 'job', 'work_size', 'start_date', 'end_date',
                'collaborators', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['job', 'work_size', 'collaborators',
                                                 'is_finished', 'user_id']):
        return jsonify({'error': 'Bad request'})
    elif request.json['id'] and session.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    res = request.json
    user = session.query(User).filter(User.id == res['user_id']).first()
    job = Jobs()
    job.job = res['job']
    job.work_size = res['work_size']
    job.collaborators = res['collaborators']
    job.is_finished = res['is_finished']
    if res['is_finished']:
        if not res['datetime']:
            job.end_date = datetime.today()
        else:
            job.end_date = res['datetime']
    if res['id']:
        job.id = res['id']
    user.jobs.append(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == id).first()
    if not job:
        abort(404)
    session.delete(job)
    session.commit()
    return jsonify(f'successfully deleted job with id {id}')


@blueprint.route('/api/jobs/<int:id>', methods=['PUT'])
def change_job(id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    res = request.json
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == id).first()
    if not job:
        abort(404)
    if 'team_leader' in res.keys():
        job.team_leader = res['team_leader']
    if 'job' in res.keys():
        job.job = res['job']
    if 'work_size' in res.keys():
        job.work_size = res['work_size']
    if 'start_date' in res.keys():
        job.start_date = res['start_date']
    if 'end_date' in res.keys():
        job.end_date = res['end_date']
    if 'collaborators' in res.keys():
        job.collaborators = res['collaborators']
    if 'is_finished' in res.keys():
        job.is_finished = res['is_finished']
    session.commit()
    return jsonify('successfully changed job')
