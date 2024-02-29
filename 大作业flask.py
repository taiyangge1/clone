from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, IntegerField, FloatField,DateField, SelectField,SelectMultipleField,PasswordField
from wtforms.validators import DataRequired,EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,current_user, login_user, logout_user, login_required, LoginManager
from functools import wraps

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'test_secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:206607860@localhost:3306/StudentData'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)


# -------------------------------------------------------------------
#创建登录实例
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_view = 'teacher_login'

# -------------------------------------------------------------------
#用户模型
class User(UserMixin,db.Model):
    __tablename__='user'
    id = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(256))
    role = db.Column(db.String(256),unique=True, nullable=False)
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

#用户加载函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.login_view = "login"
login_manager.login_view = "teacher_login"


# -------------------------------------------------------------------
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'student':
            return f(*args, **kwargs)
        else:
            flash('这个页面只有学生才能访问。')
            return redirect(url_for('login'))  # 或重定向到其他合适的页面
    return decorated_function

# -------------------------------------------------------------------
# 学生登录表单
class LoginForm(FlaskForm):
    id = StringField('账号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

# 登录路由
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student_id = form.id.data
        student = User.query.filter_by(id=student_id).first()
        if student and check_password_hash(student.password, str(form.password.data)):
            login_user(student)
            return redirect(url_for('select_lesson'))
        else:
            flash('学号不存在或密码错误，请重新输入！', 'danger')
    return render_template('login.html', form=form)


# -------------------------------------------------------------------
# 学生更改密码表单
class Stud_RegisterForm(FlaskForm):
    student_id = IntegerField('学号', validators=[DataRequired()])
    student_password = PasswordField('密码', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='密码必须匹配。')  # 确保两次密码输入相同
    ])
    confirm_password = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField("更改密码")
# -------------------------------------------------------------------
# 设置密码路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Stud_RegisterForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        # 现在查询的是 studentinfo 表
        existing_student_info = StudentInfo.query.filter_by(id=student_id).first()
        if existing_student_info:
            # 学号存在，现在检查密码是否已设置
            existing_student_password = User.query.filter_by(id=student_id).first()
            if existing_student_password:
                flash('这个学号的密码已经存在了。', 'warning')
            else:
                hashed_password = generate_password_hash(form.student_password.data)
                new_student = User(id=student_id, password=hashed_password,role='student')
                db.session.add(new_student)
                db.session.commit()
                session['student_id'] = student_id
                return redirect(url_for('login'))
        else:
            flash('这个学号不存在，请联系管理员。', 'danger')

    return render_template('register.html', form=form)

# -------------------------------------------------------------------
#选课表
class SelectlessonForm(FlaskForm):
    course = SelectField('Course', coerce=int, validators=[DataRequired()])
    submit = SubmitField('选课')
#选课模型
class StudentLesson(db.Model):
    __tablename__ = 'student_lesson'
    student_id = db.Column(db.Integer, db.ForeignKey('studentinfo.id', ondelete='CASCADE'), primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessoninfo.id', ondelete='CASCADE'), primary_key=True)
    #与LessonInfo模型的关系
    lesson_info = db.relationship('LessonInfo', back_populates='student_lessons')

# -------------------------------------------------------------------
#选课路由
@app.route('/select_lesson', methods=['GET', 'POST'])
@student_required
@login_required
def select_lesson():
    student_id = current_user.id
    student = StudentInfo.query.get(student_id)

    lessons = LessonInfo.query.all()
    form = SelectlessonForm()
    form.course.choices = [(lesson.id, lesson.name) for lesson in lessons]

    selected_lessons = StudentLesson.query.filter_by(student_id=student_id).all()

    # 计算总学分
    total_credits = sum(lesson.lesson_info.grade for lesson in selected_lessons)

    if form.validate_on_submit():
        selected_lessons_ids = request.form.getlist('course')
        existing_lessons_ids = [lesson.lesson_id for lesson in selected_lessons]

        for lesson_id in selected_lessons_ids:
            if int(lesson_id) not in existing_lessons_ids:  # 只添加尚未选择的课程
                new_entry = StudentLesson(student_id=student_id, lesson_id=lesson_id)
                db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('select_lesson'))

    return render_template('select_lesson.html', form=form, student=student, selected_lessons=selected_lessons,
                           total_credits=total_credits)

#删课路由
@app.route('/delete_SelectLesson/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
@student_required
def delete_SelectLesson(lesson_id):
    student_id = current_user.id
    # 找到对应的学生选课记录并删除
    StudentLesson.query.filter_by(student_id=student_id, lesson_id=lesson_id).delete()
    db.session.commit()
    return redirect(url_for('select_lesson'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
# -------------------------------------------------------------------
#管理员权限
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            return f(*args, **kwargs)
        else:
            flash('这个页面只有管理员才能访问。')
            return redirect(url_for('login'))
    return decorated_function

# -------------------------------------------------------------------

# 登录路由
@app.route('/admin', methods=['GET', 'POST'])
def teacher_login():
    form = LoginForm()
    if form.validate_on_submit():
        teacher_id = form.id.data
        teacher = User.query.filter_by(id=teacher_id).first()
        if teacher and check_password_hash(teacher.password, str(form.password.data)):
            login_user(teacher)
            return redirect(url_for('index'))
        else:
            flash('账号不存在或密码错误，请重新输入！', 'danger')
    return render_template('teacher_login.html', form=form)



# -------------------------------------------------------------------
# 管理员注册表单
class Teacher_RegisterForm(FlaskForm):
    teacher_id = IntegerField('管理员账号', validators=[DataRequired()])
    teacher_password = PasswordField('密码', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='密码必须匹配。')  # 确保两次密码输入相同
    ])
    confirm_password = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField("注册")
# -------------------------------------------------------------------
# 注册路由
@app.route('/teacher_register', methods=['GET', 'POST'])
def teacher_register():
    form = Teacher_RegisterForm()
    if form.validate_on_submit():
        teacher_id = form.teacher_id.data
        existing_teacher = User.query.filter_by(id=teacher_id).first()
        if existing_teacher:
            flash('这个账号已经被注册了。', 'warning')
            return redirect(url_for('teacher_register'))

        # 不需要在会话中存储密码，只需在数据库中存储哈希过的密码
        hashed_password = generate_password_hash(form.teacher_password.data)
        new_teacher = User(id=teacher_id, password=hashed_password,role='admin')
        db.session.add(new_teacher)
        db.session.commit()

        # 存储学生ID到会话中作为登录状态的标记
        session['teacher_id'] = teacher_id
        flash('注册成功，请登录。', 'success')
        return redirect(url_for('teacher_login'))

    return render_template('teacher_register.html', form=form)

# -------------------------------------------------------------------
#管理员主界面
@app.route('/admin/index', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    form = LoginForm()
    studs = StudentInfo.query.all()
    lessons = LessonInfo.query.all()
    select_lesson=StudentLesson.query.all()

    return render_template('index.html', form=form,studs=studs, lessons=lessons,select_lesson=select_lesson)

# -------------------------------------------------------------------
#学生表
class StudentForm(FlaskForm):
    id = IntegerField('学号')
    name = StringField('姓名')
    birthday = DateField('出生日期', format='%Y-%m-%d')
    placeofbirth = StringField('籍贯')
    gender=SelectField("性别",choices=[("M","男"),('F',"女")])
    college = StringField('学院')
    major = StringField('专业')
    submit = SubmitField('提交')

#学生信息模型
class StudentInfo(db.Model):
    __tablename__ = 'studentinfo'
    id = db.Column(db.Integer, primary_key=True,autoincrement=False)
    name = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    placeofbirth = db.Column(db.String(255), nullable=False)
    college = db.Column(db.String(255), nullable=False)
    major = db.Column(db.String(255), nullable=False)


# -------------------------------------------------------------------
#学生信息视图
@app.route('/admin/studentinfo')
@login_required
@admin_required
def studentinfo():
    students=StudentInfo.query.all()
    return render_template("studentinfo.html",students=students)

# -------------------------------------------------------------------
#新增学生
@app.route('/admin/new_stud', methods=['GET', 'POST'])
@login_required
@admin_required
def new_stud():
    form = StudentForm()
    if form.validate_on_submit():
        student_id = form.id.data
        # 检查ID是否已存在
        existing_student = StudentInfo.query.get(student_id)
        if existing_student:
            flash('该学号已存在，请输入一个新的学号。')
            return render_template('new_student.html', form=form)

        # 如果学号不存在，创建新的学生记录
        newstud = StudentInfo(
            id=student_id,
            name=form.name.data,
            birthday=form.birthday.data,
            placeofbirth=form.placeofbirth.data,
            gender=form.gender.data,
            college=form.college.data,
            major=form.major.data,
        )
        db.session.add(newstud)
        db.session.commit()
        flash("新增了一位学生！")
        return redirect(url_for('studentinfo'))
    return render_template('new_student.html', form=form)


# -------------------------------------------------------------------
#编辑学生
class EditForm_1(StudentForm):
    submit = SubmitField('编辑')
@app.route('/admin/edit_stud/<int:stu_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_stud(stu_id):
    form = EditForm_1()
    stud = StudentInfo.query.get_or_404(stu_id)  # 获取学生信息或返回404

    if form.validate_on_submit():
        # 检查用户是否尝试修改了id字段
        if form.id.data != stud.id:
            flash("学生ID为无法修改的字段，请直接删除后重新添加记录。", "error")  # 向用户显示错误消息
            return redirect(url_for('edit_stud', stu_id=stu_id))  # 重定向回编辑页面

        # 更新其他字段
        stud.name = form.name.data
        stud.birthday = form.birthday.data
        stud.placeofbirth = form.placeofbirth.data
        stud.college = form.college.data
        stud.major = form.major.data
        db.session.commit()
        flash("修改了一条信息", "success")
        return redirect(url_for('studentinfo'))

    # 预填充表单
    form.id.data=stud.id
    form.name.data = stud.name
    form.birthday.data = stud.birthday
    form.placeofbirth.data = stud.placeofbirth
    form.college.data = stud.college
    form.major.data = stud.major

    return render_template('edit_student.html', form=form, stu_id=stu_id)

#删除学生
@app.route('/admin/delete_stud/<int:stu_id>',methods=['GET','POST'])
@login_required
@admin_required
def delete_stud(stu_id):
    stud = StudentInfo.query.get(stu_id)
    student_lessons = StudentLesson.query.filter_by(student_id=stu_id).first()
    db.session.delete(stud)
    db.session.commit()
    flash("删除了一条学生信息")
    return redirect(url_for('studentinfo'))

@app.route('/admin/delete_multiple_students', methods=['POST'])
@login_required
@admin_required
def delete_multiple_students():
    selected_students = request.form.getlist('selected_students')
    for student_id in selected_students:
        student = StudentInfo.query.get(student_id)
        if student:
            db.session.delete(student)
    db.session.commit()
    return redirect(url_for('studentinfo'))

# -------------------------------------------------------------------
#课程表
class LessonForm(FlaskForm):
    id = IntegerField('课程号')
    name = StringField('课程名称')
    teacher = StringField('开课教师')
    major = StringField('开课专业')
    grade = FloatField('学分')
    submit = SubmitField('提交')

#课程信息模型
class LessonInfo(db.Model):
    __tablename__='lessoninfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    teacher = db.Column(db.String(255), nullable=False)
    grade = db.Column( db.Integer,nullable=False)
    major = db.Column(db.String(255), nullable=False)
    #与StudentLesson模型的关系
    student_lessons = db.relationship('StudentLesson', back_populates='lesson_info')

# -------------------------------------------------------------------
#课程信息视图
@app.route('/admin/lessoninfo')
@login_required
@admin_required
def lessoninfo():
    lessons=LessonInfo.query.all()
    return render_template("lessoninfo.html",lessons=lessons)

# -------------------------------------------------------------------
#新增课程
@app.route('/admin/new_lesson', methods=['GET', 'POST'])
@login_required
@admin_required
def new_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        newlesson = LessonInfo(
            id=form.id.data,
            name=form.name.data,
            teacher=form.teacher.data,
            major=form.major.data,
            grade=form.grade.data
        )
        db.session.add(newlesson)
        db.session.commit()
        flash("新增了一门课程！")
        return redirect(url_for('lessoninfo'))
    return render_template('new_lesson.html', form=form)

#编辑课程类
class EditForm_2(LessonForm):
    submit = SubmitField('编辑')
@app.route('/admin/edit_lesson/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_lesson(lesson_id):
    form = EditForm_2()
    lesson = LessonInfo.query.get_or_404(lesson_id)  # 获取课程信息或返回404

    if form.validate_on_submit():
        # 检查用户是否尝试修改了id字段
        if form.id.data != lesson.id:
            flash("ID为无法修改的字段，请直接删除后重新添加记录。", "error")  # 向用户显示错误消息
            return redirect(url_for('edit_lesson', lesson_id=lesson_id))  # 重定向回编辑页面

        # 更新其他字段
        lesson.name = form.name.data
        lesson.teacher = form.teacher.data
        lesson.major = form.major.data
        lesson.grade = form.grade.data
        db.session.commit()
        flash("修改了一条信息", "success")
        return redirect(url_for('lessoninfo'))

    # 预填充表单
    form.id.data=lesson.id
    form.name.data = lesson.name
    form.teacher.data = lesson.teacher
    form.major.data = lesson.major
    form.grade.data = lesson.grade

    return render_template('edit_lesson.html', form=form, lesson_id=lesson_id)


# -------------------------------------------------------------------

#删除课程
@app.route('/admin/delete_lesson/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_lesson(lesson_id):
    # 先尝试删除所有相关联的student_lesson记录
    StudentLesson.query.filter_by(lesson_id=lesson_id).delete()

    # 然后删除lessoninfo记录
    lesson = LessonInfo.query.get(lesson_id)
    if lesson:
        db.session.delete(lesson)
        db.session.commit()
        flash("删除了一条课程信息")
    else:
        flash("课程信息未找到")

    return redirect(url_for('lessoninfo'))

@app.route('/admin/delete_multiple_lessons', methods=['POST'])
@login_required
@admin_required
def delete_multiple_lessons():
    selected_lessons = request.form.getlist('selected_lessons')
    for lesson_id in selected_lessons:
        lesson = LessonInfo.query.get(lesson_id)
        if lesson:
            db.session.delete(lesson)
    db.session.commit()
    return redirect(url_for('lessoninfo'))

# -------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True,port=8080)