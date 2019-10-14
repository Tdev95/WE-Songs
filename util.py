from contextlib import contextmanager


@contextmanager
def execute_query(db, query):
    '''query context manager'''
    cursor = db.connection.cursor()
    cursor.execute(query)
    db.connection.commit()
    yield cursor.fetchall()
    cursor.close()
