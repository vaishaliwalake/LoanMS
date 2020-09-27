import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector import pooling

db1 = mysql.connector.connect(pool_name="LoanDBConnPool",
                                                                  pool_size=3,
                                                                  pool_reset_session=True,
                                                                  host='127.0.0.1',
                                                                  database='loan',
                                                                  user='root',
                                                                  password='123456',
                                                                  port='3306')



print("Connection db1:", db1.connection_id)


