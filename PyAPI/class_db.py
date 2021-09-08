import pymysql.cursors
class DB:

    connection = False

    @staticmethod
    def connect(host:str='', database:str='', user:str='', password:str=''):
        '''Connect to the database'''
        try:
            connection = pymysql.connect(
                host        = host or '127.0.0.1',
                user        = user or 'tester',
                password    = password or 'tester',
                database    = database or 'test',
                cursorclass=pymysql.cursors.DictCursor
            )
            DB.connection = connection
            return {'status': 200, 'msg': 'connected to db'}
        except Exception as e:
            print(e)
            return {'status': 403, 'msg': 'error, possibly creds are incorrent, or server / db not found!'}

    @staticmethod
    def insert(query:str=''):
        '''Insert rows into the database'''
        try:
            with DB.connection:
                with DB.connection.cursor() as cursor:
                    cursor.execute(query)
                    DB.connection.commit()
            return {'status': 200, 'row_id': cursor.lastrowid, 'msg': 'success'}
        except Exception as e:
            print(e)
            return {'status': 500, 'msg': 'failed to insert data'}

    @staticmethod
    def get(query:str=''):
        '''Get one or more rows from the database'''
        try:
            with DB.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return {'status': 200, 'msg': 'success', 'data': result} if result.__len__() > 0 else {'status': 500, 'msg': 'nothing was found in db'}
                    
        except Exception as e:
            print(e)
            return {'status': 500, 'msg': 'failed to fetch data'}

    @staticmethod
    def update(query:str=''):
        '''Update one or more rows in the database'''
        try:
            with DB.connection.cursor() as cursor:
                cursor.execute(query)
                DB.connection.commit()
                return {'status': 200, 'msg': 'success'}
        except Exception as e:
            print(e)
            return {'status': 500, 'msg': 'failed to update data'}

    @staticmethod
    def delete(query:str=''):
        '''Delete one or more rows in the database'''
        try:
            with DB.connection.cursor() as cursor:
                cursor.execute(query)
                DB.connection.commit()
                return {'status': 200, 'msg': 'success'}
        except Exception as e:
            print(e)
            return {'status': 500, 'msg': 'failed to delete data'}