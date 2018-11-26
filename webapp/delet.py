import pymysql

db = pymysql.connect("localhost", "root", "18911912812pyy", "sedb")

cursor = db.cursor()

sql_delete = 'DELETE FROM webapp_atop'
cursor.execute(sql_delete)
sql_delete = 'DELETE FROM webapp_author'
cursor.execute(sql_delete)
sql_delete = 'DELETE FROM webapp_ktop'
cursor.execute(sql_delete)
sql_delete = 'DELETE FROM webapp_paper'
cursor.execute(sql_delete)

db.commit()
db.close()