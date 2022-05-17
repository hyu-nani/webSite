
from flask import Blueprint, render_template, request, flash, redirect, url_for, request, jsonify
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, user_accessed
import json

auth = Blueprint('auth', __name__)

#로그인 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('로그인 되었습니다.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))#홈페이지 이동
            else:
                flash('비밀번호가 일치하지 않습니다.', category='error')
        else:
            flash('회원정보가 일치하지 않습니다.', category='error')

    return render_template("login.html", user=current_user)


#로그아웃
@auth.route('/logout')
def logout():
    logout_user()
    return render_template("home.html", user=current_user)

#이용약관
@auth.route('/termOfUse', methods=['GET', 'POST'])
def termOfUse():
    if request.method == 'POST':
        return redirect(url_for('auth.sign_up'))#홈페이지 이동
    return render_template("termOfUse.html", user=current_user)

#회원가입
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        advTerms = request.form.get('check')#마케팅 계약

        user = User.query.filter_by(email=email).first()
        if user:
            flash('이미 가입한 정보입니다.', category='error')
        elif len(email) == 0 or len(name) == 0 or len(password1) == 0:
            flash('필수입력란(*)을 기입해주세요.', category='error')
        elif len(email) < 4:
            flash('이메일은 4글자 이상 입력해주세요.', category='error')
        elif len(name) < 2:
            flash('이름은 한글자 이상 입력해주세요.', category='error')
        elif len(password1) < 8:
            flash('비밀번호는 8자리 이상 입력해주세요.', category='error')
        elif password1 != password2:
            flash('비밀번호와 비밀번호 확인이 일치하지 않습니다.', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('가입을 환영합니다.', category='success')
            return redirect(url_for('views.home'))#홈페이지 이동

    return render_template("sign_up.html", user=current_user)

@auth.route('/bulletinBoard', methods=['GET', 'POST'])
@login_required# 로그인 요청
def bulletinBoard():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('너무 짧습니다.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.email)
            db.session.add(new_note)
            db.session.commit()
            flash('성공.', category='success')
    return render_template("bulletinBoard.html", user=current_user)

@auth.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.email:
            db.session.delete(note)
            db.session.commit()
            flash('삭제완료.', category='success')
        else:
            flash('작성자가 아닙니다.', category='error')
    return jsonify({})

@auth.route('/information')
def information():
    return render_template("information.html", user=current_user)

@auth.route('/estimate')
@login_required# 로그인 요청
def estimate():
    return render_template("estimate.html", user=current_user)