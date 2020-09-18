from flask import render_template, url_for, redirect, flash, request, abort
from Hackathon import app, db, bcrypt, contestData
from Hackathon.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from Hackathon.models import User, Post, Submission
from flask_login import login_user, current_user, logout_user, login_required
from time import time, ctime

convert_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
duration = contestData['duration'] * 60
nProblems = len(contestData['problem'])

@app.context_processor
def inject_contest_data():
    time_left = max(0, contestData['timestart'] + contestData['duration'] * 60 - int(time()))
    unix_time = time_left
    hour = time_left // 3600
    time_left %= 3600
    minute = time_left // 60
    time_left %= 60
    second = time_left
    return dict(time_left=unix_time, hour=hour, minute=minute, second=second, nProblems=nProblems, duration=duration)

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.filter().order_by('id desc')
    return render_template('home.html', posts=posts)

@app.route("/statement")
@login_required
def statement():
    user = User.query.filter_by(username=current_user.username).first()
    subs = Submission.query.filter_by(author=user)
    submissions = []
    score = []
    for p in contestData['problem']:
        nSubtask = p['nSubtasks']
        log = list(filter(lambda x: convert_char[x.problem_id - 1] == p['problem_id'], subs))
        if len(log) == 0:
            submissions.append('')
            score.append(0)
        else:
            submissions.append(log[0].log)
            score.append(log[0].score)
    problem_list = contestData['problem']
    return render_template('statement.html', title='Statement', submissions=submissions, problem_list=problem_list, scores=score)

@app.route("/submit", methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == 'POST' and request.form['problem_id']:
        problem = list(filter(lambda p: p['problem_id'] == request.form['problem_id'], contestData['problem']))[0]
        score, nSubtasks = 0, int(problem['nSubtasks'])
        user = User.query.filter_by(username=current_user.username).first()
        problem_id = ord(problem['problem_id']) - ord('A') + 1
        new_submission = Submission.query.filter_by(author=user, problem_id=problem_id).first()
        time_left = contestData['timestart'] + contestData['duration'] * 60 - int(time())

        if time_left <= 0:
            flash(f"Nộp bài không thành công, đã hết thời gian làm bài", "danger")
            return redirect(url_for('submit'))

        if new_submission is None:
            new_submission = Submission(problem_id=problem_id, max_score=0, score=0, time_penalty=0, subs_penalty=0, is_first_AC=False, author=current_user)
        sub_logs = ""

        print(new_submission.is_first_AC)

        if new_submission.max_score == 100:
            flash(f"AC rồi mà nộp làm gì vậy???", "success")
            return redirect(url_for('submit'))

        for i in range(1, nSubtasks + 1):
            contestant_answer = request.form[f'subtask_{i}']
            jury_answer = problem[f'subtask_{i}']
            if contestant_answer == jury_answer:
                score += 100 // nSubtasks
                if i == nSubtasks:
                    sub_logs += f"<strong>Subtask {i}: <x style='color: green'>AC</x></strong>"
                else:
                    sub_logs += f"<strong>Subtask {i}: <x style='color: green'>AC</x><br></strong>"
            else:
                if i == nSubtasks:
                    sub_logs += f"<strong>Subtask {i}: <x style='color: red'>WA</x></strong>"
                else:
                    sub_logs += f"<strong>Subtask {i}: <x style='color: red'>WA</x><br></strong>"

        if score <= new_submission.max_score:
            new_submission.subs_penalty += 5
        else:
            new_submission.max_score = score

        if new_submission.max_score == 100:
            sub_list = Submission.query.filter_by(problem_id=problem_id)
            candidate = list(filter(lambda p: p.max_score == 100, sub_list))
            if len(candidate) == 1:
                new_submission.is_first_AC = True

        new_submission.score = score
        new_submission.log = sub_logs
        new_submission.time_penalty = contestData['duration'] - time_left // 60
        db.session.add(new_submission)
        db.session.commit()
        flash(f"Nộp bài thành công, bạn nhận được: {score} điểm", "success")
        if new_submission.is_first_AC:
            flash(f"Chúc mừng bạn đã là người đầu tiên AC bài {problem['problem_id']}", "success")
        return redirect(url_for('submit'))
    else:
        user = User.query.filter_by(username=current_user.username).first()
        subs = Submission.query.filter_by(author=user)
        submissions = []
        score = []
        for p in contestData['problem']:
            nSubtask = p['nSubtasks']
            log = list(filter(lambda x: convert_char[x.problem_id - 1] == p['problem_id'], subs))
            if len(log) == 0:
                submissions.append('')
                score.append(0)
            else:
                submissions.append(log[0].log)
                score.append(log[0].score)
        problem_list = contestData['problem']
        return render_template('submit.html', title='Submit', submissions=submissions, problem_list=problem_list, scores=score)

@app.route("/standings")
def standings():
    users = User.query.all()
    scores = []
    for user in users:
        submissions = Submission.query.filter_by(author=user)
        score = {'username': user.username}
        score['total_score'] = 0
        score['total_penalty'] = 0
        for i in range(1, nProblems + 1):
            submission = list(filter(lambda x: x.problem_id == i, submissions))
            if len(submission) == 0:
                score[f"{convert_char[i - 1]}_score"] = 0
                score[f"{convert_char[i - 1]}_penalty"] = 0
                score[f"{convert_char[i - 1]}_submitted"] = False
                score[f"{convert_char[i - 1]}_is_first_AC"] = False
            else:
                score[f"{convert_char[i - 1]}_score"] = submission[0].max_score
                score[f"{convert_char[i - 1]}_penalty"] = submission[0].time_penalty + submission[0].subs_penalty
                score[f"{convert_char[i - 1]}_submitted"] = True
                score[f"{convert_char[i - 1]}_is_first_AC"] = submission[0].is_first_AC
            score['total_score'] += score[f"{convert_char[i - 1]}_score"]
            score['total_penalty'] += score[f"{convert_char[i - 1]}_penalty"]
        scores.append(score)
    scores = sorted(scores, key=lambda x: (x['total_score'], -x['total_penalty']), reverse=True)
    problem_list = contestData['problem']
    return render_template('standings.html', title='standings', problem_list=problem_list, scores=scores, nUsers=len(users))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Tài khoản {form.username.data} đã được tạo thành công!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Đăng nhập không thành công. Hãy kiểm tra lại tài khoản và mật khẩu của bạn', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        db.session.commit()
        flash('Mật khẩu đã được cập nhật thành công', 'success')
        return redirect(url_for('profile'))
    image_file = url_for('static', filename='profile_images/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.username != "TeamHackathon2020":
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Bài viết của bạn đã được đăng', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Bài viết của bạn đã được cập nhật', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Bài viết đã được xóa', 'success')
    return redirect(url_for('home'))

@app.errorhandler(500)
def page_not_found(e):
    print('nhu loz')
    # note that we set the 404 status explicitly
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    print('nhu loz')
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    print('nhu loz')
    # note that we set the 404 status explicitly
    return render_template('403.html'), 403