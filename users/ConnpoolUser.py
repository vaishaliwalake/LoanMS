from users import Connpool
import mysql.connector

db3 = mysql.connector.connect(pool_name='LoanDBConnPool')
db3curr = db3.cursor()
print("Connection db3:", db3.connection_id)
#db4= mysql.connector.connect(pool_name='LoanDBConnPool')





def GetConn():
    for i in range(3):
        if i==2:
            db3curr.close()

            try:
                db4=mysql.connector.connect(pool_name='LoanDBConnPool')
            except mysql.connector.errors.PoolError as e:
                print(e)




