import pymysql

db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '206607860',  # Change 'your_password' to the actual password
    'db': 'studentdata',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def create_tables():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 创建管理员密码表
            create_teacher_password_sql = """
            CREATE TABLE IF NOT EXISTS teacher_password (
                id INT PRIMARY KEY,
                password VARCHAR(255) NOT NULL
            );
            """
            cursor.execute(create_teacher_password_sql)

            # 创建学生信息表
            create_studentinfo_sql = """
            CREATE TABLE IF NOT EXISTS studentinfo (
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                birthday DATE NOT NULL,
                placeofbirth VARCHAR(255) NOT NULL,
                gender CHAR(1),
                college VARCHAR(255) NOT NULL,
                major VARCHAR(255) NOT NULL
            );
            """
            cursor.execute(create_studentinfo_sql)

            # 创建学生密码表
            create_student_password_sql = """
            CREATE TABLE IF NOT EXISTS student_password (
                id INT,
                password VARCHAR(255) NOT NULL,
                FOREIGN KEY (id) REFERENCES studentinfo(id) ON DELETE CASCADE
            );
            """
            cursor.execute(create_student_password_sql)

            # 创建课程信息表
            create_lessoninfo_sql = """
            CREATE TABLE IF NOT EXISTS lessoninfo (
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                teacher VARCHAR(255) NOT NULL,
                major VARCHAR(255) NOT NULL,
                grade FLOAT NOT NULL
            );
            """
            cursor.execute(create_lessoninfo_sql)

            # 创建学生选课表
            create_student_lesson_sql = """
            CREATE TABLE IF NOT EXISTS student_lesson (
                student_id INT,
                lesson_id INT,
                FOREIGN KEY (student_id) REFERENCES studentinfo(id) ON DELETE CASCADE,
                FOREIGN KEY (lesson_id) REFERENCES lessoninfo(id) ON DELETE CASCADE,
                PRIMARY KEY (student_id, lesson_id)
            );
            """
            cursor.execute(create_student_lesson_sql)

        connection.commit()
    finally:
        connection.close()

# 调用函数创建表
create_tables()
