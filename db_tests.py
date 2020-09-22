import sqlite3
import datetime as dt

TABLES = ['five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven']


def connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect("tests.db") as conn:
            result = func(*args, conn=conn, **kwargs)
        return result
    return inner


@connection
def init_db_tests(conn, force: bool = False):

    c = conn.cursor()  # zaproslar uchun
    # c.execute(....) bu yerda SQLite zaproslari
    for table in TABLES:
        if force:
            c.execute(f'drop table if exists {table}')
        c.execute(f'''
        create table if not exists {table}(
            id integer primary key autoincrement,
            test text,
            answers text,
            fan varchar(20)
            )
        ''')
        conn.commit()   # O'zgartirishlarni saqlash uchun


@connection
def add_test(conn, sinf, test, answer, fan):  # table=[sinf, test, answer, fan]
    c = conn.cursor()
    c.execute(f"insert into {sinf} (test, answers, fan) values(?, ?, ?)", (test, answer, fan))
    conn.commit()


@connection
def get_tests(conn, klass, fan):
    c = conn.cursor()
    c.execute(f"select test, answers from {klass} where fan=?", (fan,))
    return c.fetchall()


if __name__ == '__main__':
    init_db_tests(force=True)