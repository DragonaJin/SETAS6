import pandas as pd
import pymysql

df= pd.DataFrame(pd.read_excel("/Volumes/pyy/研究生/软件工程/demo1.xls"))
for row in df.iterrows():
    print(row)


# 'id', 'title', 'abstract', 'pubDate', 'DOInumber', 'authors','IEEEkeys', 'authorkeys', 'references', 'citations'
# 数据库连接
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='799625048@qq.com', db='testdb', charset='utf8')
# 创建游标，通过连接与数据通信
cursor = conn.cursor()





# 执行SQL，并返回受影响行数
# effect_row = cursor.execute("update tb7 set pass = '123' where nid = %s", (11,))
# 提交，不然无法保存新建或者修改的数据
conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()