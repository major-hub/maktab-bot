import sqlite3
import datetime as dt


def connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('pupils.db') as conn:
            result = func(*args, conn=conn, **kwargs)
        return result
    return inner


@connection
def init_db_pupils(conn, force: bool = False):
    c = conn.cursor()  # zaproslar uchun
    # c.execute(....) bu yerda SQLite zaproslari
    if force:
        c.execute('drop table if exists users')
    c.execute('''
    create table if not exists users(
    id integer primary key autoincrement,
    sana date,
    user_id int not null ,
    klass varchar(5) not null ,
    last_name varchar(30) not null ,
    first_name varchar(30) not null ,
    nomer varchar(15) not null,
    Rus_tili integer,
    Matematika integer,
    Ona_tili integer,
    Ingliz_tili integer,
    Jismoniy_tarbiya integer,
    Tarix integer,
    Kimyo integer,
    Fizika integer,
    Biologiya integer,
    Informatika integer,
    Geografiya integer,
    Texnologiya integer,
    Milliy_istiqlol_goyasi integer
    )
    ''')
    conn.commit()   # O'zgartirishlarni saqlash uchun

    if force:
        c.execute('drop table if exists admins')
    c.execute('''
        create table if not exists admins(
        id integer primary key autoincrement,
        admin_id int not null,
        last_name varchar(30) not null ,
        first_name varchar(30) not null ,
        fan varchar(50) not null ,
        nomer varchar(15) not null,
        either varchar(10)
        )
        ''')
    conn.commit()


@connection
def add_admin(conn, admin_id: int, last_name, first_name, fan, nomer):
    c = conn.cursor()
    c.execute("insert into admins(admin_id, last_name, first_name, fan, nomer, either) "
              "values (?, ?, ?, ?, ?, 'false')", (admin_id, last_name, first_name, fan, nomer))
    conn.commit()


@connection   #admin bormi
def check_admin(conn, admin_id: int):
    c = conn.cursor()
    c.execute("select admin_id from admins")
    res = c.fetchall()
    return True if (admin_id,) in res else False


@connection
def get_admin_fan(conn, admin_id: int):
    c = conn.cursor()
    c.execute("select fan from admins where admin_id= ?", (admin_id,))
    (res, ) = c.fetchone()
    return res


@connection
def get_pupil_fan(conn, user_id: int):
    c = conn.cursor()
    c.execute("select fan from users where user_id= ?", (user_id,))
    (res, ) = c.fetchone()
    return res


@connection
def get_admin_ids(conn):
    c = conn.cursor()
    c.execute("select admin_id from admins")
    return c.fetchall()


# Message handler uchun
@connection
def get_either(conn, admin_id):
    c = conn.cursor()
    c.execute("select either from admins where admin_id=?", (admin_id,))
    (res, ) = c.fetchone()
    return res


@connection
def set_either(conn, admin_id, force: str = 'false'):
    c = conn.cursor()
    c.execute("update admins set either=? where admin_id=?", (force, admin_id))
    conn.commit()


# royhatdan otganmi ?
@connection
def check_person(conn, user_id: int):
    c = conn.cursor()
    c.execute("select user_id from users")
    res = c.fetchall()
    return True if (user_id,) in res else False


# test topshirganmi?
@connection
def check_submit_test(conn, user_id: int, fan):
    c = conn.cursor()
    c.execute(f"select user_id, {fan} from users where user_id=?", (user_id,))
    res1 = c.fetchall()
    return False if (user_id, None) in res1 else True


@connection
def get_klass(conn, user_id: int):
    c = conn.cursor()
    c.execute("select klass from users where user_id = ?", (user_id,))
    (res,) = c.fetchone()
    return res[:-1]


@connection
def add_pupil(conn, sana, user_id: int, klass: str, last_name: str, first_name: str, nomer):
    c = conn.cursor()
    c.execute("insert into users (sana, user_id, klass, last_name, first_name, nomer) "
              "values(?, ?, ?, ?, ?, ?)", (sana, user_id, klass, last_name, first_name, nomer))
    conn.commit()


@connection
def get_pupils(conn, klass):
    c = conn.cursor()
    c.execute("select last_name, first_name from users where klass = ?", (klass, ))
    return c.fetchall()


@connection
def get_ustozlar(conn):
    c = conn.cursor()
    c.execute("select last_name, first_name, fan from admins")
    return c.fetchall()



@connection
def get_pupil_number(conn, klass, last_name, first_name):
    try:
        c = conn.cursor()
        c.execute("select nomer from users where klass= ? and last_name= ? and first_name= ?", (klass, last_name, first_name))
        (res,) = c.fetchone()
        return res

    except Exception:
        res = "Bunday ism familyali o'quvchi yo'q"
        return res


@connection
def get_teacher_number(conn, last_name, first_name):
    try:
        c = conn.cursor()
        c.execute("select nomer from admins where last_name= ? and first_name= ?", (last_name, first_name))
        (res,) = c.fetchone()
        print(res)
        return res
    except Exception:
        res = "Bunday ism familyali ustoz yo'q"
        return res


@connection
def rating(conn, user_id: int, fan, ball: int):
    c = conn.cursor()
    c.execute(f"update users set {fan} = ? where user_id = ?", (int(ball), int(user_id)))
    conn.commit()


@connection
def get_date_ball(conn, fan, date):
    c = conn.cursor()
    c.execute(f"select klass, last_name, first_name, {fan} from users where {fan} not null and sana = ? order by klass desc", (date,))
    return c.fetchall()


@connection
def get_klass_ball(conn, fan, klass):
    c = conn.cursor()
    c.execute(f"select sana, last_name, first_name, {fan} from users where {fan} not null and klass = ?  order by last_name", (klass, ))
    return c.fetchall()


@connection
def get_all_pupil_ids(conn, klass):
    c = conn.cursor()
    c.execute("select user_id from users where klass = ?", (klass,))
    return c.fetchall()


@connection
def delete_user(conn, last_name, first_name):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM users where last_name=? and first_name=?", (last_name, first_name))
        conn.commit()
        return "Muvofaqqiyatli o'chirildi"
    except Exception:
        return "Bunday o'quvchi mavjud emas"


@connection
def delete_teacher(conn, last_name, first_name):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM admins where last_name=? and first_name=?", (last_name, first_name))
        conn.commit()
        return "Muvofaqqiyatli o'chirildi"
    except Exception:
        return "Bunday ustoz mavjud emas"


@connection
def clear_one(conn, fan, klass):
    try:
        c = conn.cursor()
        c.execute(f"update users set {fan} = NULL where klass=?", (klass,))
        conn.commit()
        return True
    except Exception:
        return False

@connection
def add_fan_column(conn):
    c = conn.cursor()
    c.execute("alter table users add Milliy_istiqlol_goyasi integer")
    conn.commit()



if __name__ == '__main__':
    init_db_pupils()

