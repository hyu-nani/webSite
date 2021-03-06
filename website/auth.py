
from flask import Blueprint, render_template, request, flash, redirect, url_for, request, jsonify
from .models import User, Note, Order
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
        return redirect(url_for('auth.sign_up'))
    return render_template("termOfUse.html", user=current_user)

#회원가입
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone = request.form.get('phone')

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
            new_user = User( email = email,  name = name, password = generate_password_hash(password1, method='sha256'), phone = phone)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('가입을 환영합니다.', category='success')
            return redirect(url_for('views.home'))#홈페이지 이동

    return render_template("sign_up.html", user=current_user)

#게시판
@auth.route('/bulletinBoard', methods=['GET', 'POST'])
@login_required# 로그인 요청
def bulletinBoard():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('너무 짧습니다.', category='error')
        else:
            new_note = Note(note_data=note, user_id=current_user.email)
            db.session.add(new_note)
            db.session.commit()
            flash('완료', category='success')
    list = Note.query.all()
    return render_template("bulletinBoard.html", user=current_user, Notes=list)

#노트 삭제
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

#견적 삭제
@auth.route('/delete-order', methods=['POST'])
def delete_order():
    order = json.loads(request.data)
    orderId = order['orderId']
    order = Order.query.get(orderId)
    if order:
        if order.order_id == current_user.email:
            db.session.delete(order)
            db.session.commit()
            flash('삭제완료.', category='success')
        else:
            flash('작성자가 아닙니다.', category='error')
    return jsonify({})

#회사소개
@auth.route('/information')
def information():
    return render_template("information.html", user=current_user)

#견적 시안 새글 작성칸
@auth.route('/estimateSheet', methods=['GET', 'POST'])
@login_required# 로그인 요청
def estimateSheet():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('pwd')
        note = request.form.get('note')
        phone = request.form.get('phone')
        title = request.form.get('title')
        if len(phone) == 0:
            flash('전화 적어 주세요', category='error')
        if len(name) == 0:
            flash('이름을 적어 주세요', category='error')
        elif len(password) == 0:
            flash('비밀번호를 적어 주세요', category='error')
        elif len(note) == 0:
            flash('내용을 적어 주세요', category='error')
        else:
            new_order = Order(order_id=current_user.email, order_title=title, order_name=name, order_password=password, order_data=note, order_number = phone)
            db.session.add(new_order)
            db.session.commit()
            flash('완료', category='success')
            return redirect(url_for('auth.estimate'))
    return render_template("estimateSheet.html", user=current_user)

#견적 시안 창
@auth.route('/estimate', methods=['GET', 'POST'])
@login_required# 로그인 요청
def estimate():
    if request.method == 'POST':
        return redirect(url_for('auth.estimateSheet'))
    list = Order.query.all()
    return render_template("estimate.html", user=current_user, Order=list)

#내정보
@auth.route('/myPage')
def myPage():
    return render_template("myPage.html", user=current_user)

######################################################################################
# 샘플 리스트
######################################################################################

@auth.route('/sample/purpleStick')
def purpleStick():
   return render_template("sample/purpleStick.html", user=current_user)
