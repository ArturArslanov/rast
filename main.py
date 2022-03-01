from datetime import datetime

from flask import Flask, render_template, redirect, jsonify

from add_team import add_team, add_work
from data import db_session, api_jobs
from config import secret_key, bd_path, params
from data.jobs import Jobs
from data.users import User
from form.register import RegisterForm
from flask import make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', **params, jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            address=form.address.data,
            speciality=form.speciality.data,
            position=form.position.data,
            age=form.age.data,
            surname=form.surname.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title1='Регистрация', form=form, **params)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init(bd_path)
    session = db_session.create_session()
    app.register_blueprint(api_jobs.blueprint)
    if not bool(session.query(User).all()):
        add_team(db_session)
    if not bool(session.query(Jobs).all()):
        add_work(db_session)
    app.run(port=8081, host='127.0.0.2')


if __name__ == '__main__':
    main()
