# coding: utf-8

import config
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from exts import db
from decorators import login_required
from models import (
    User,
    Question,
    Answer
)

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    page = request.args.get('page', app.config['INIT_PAGE_NUM'], type=int)
    pagination = Question.query.order_by('-create_time').paginate(page, app.config['INIT_PAGE_LEN'], False)
    context = {
        'questions': pagination.items,
        'pagination': pagination
    }
    return render_template('index.html', **context)


@app.route('/questions/page/<int:page>')
def questions_page(page=None):
    if page is None:
        page = 1
    qstring = request.args.get('qstring')
    if qstring is not None:
        questions = Question.query.filter(Question.title.ilike(u"%{}%".format(qstring)))
    else:
        questions = Question.query
    pagination = questions.order_by('-create_time').paginate(page, app.config['INIT_PAGE_LEN'], False)
    context = {
        'questions': pagination.items,
        'pagination': pagination,
        'qstring': qstring
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 31天保存session信息
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'用户名或密码错误，请确认后登录！'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        passwd1 = request.form.get('password1')
        passwd2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号已被注册'

        if passwd1 != passwd2:
            return u'两次输入密码不相等'

        user = User(telephone=telephone, username=username, password=passwd1)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id')
    # del session['user_id']
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user = User.query.filter(User.id == session.get('user_id')).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    qst = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=qst)


@app.route('/add_answer', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    qstion = Question.query.filter(Question.id == question_id).first()
    answer.question = qstion
    db.session.add(answer)
    db.session.commit()

    return redirect(url_for('detail', question_id=question_id))


@app.route('/search', methods=['POST'])
def search():
    qstring = request.form.get('qstring')
    return redirect(url_for('questions_page', page=1, qstring=qstring))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return dict(user=user)

    return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
