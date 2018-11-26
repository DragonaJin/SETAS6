import traceback
import pandas as pd
from datetime import datetime
import pymysql


def save_paper(row):
    # 存论文
    date_d = ''
    pid = row['id'][10:-1]
    title = row['title']
    abstract = ''
    if row['abstract'] and row['abstract'] == row['abstract']:    # nan float类型
        abstract = row['abstract']
    doi_num = ''
    if row['pubDate'] and row['pubDate'] == row['pubDate']:  # date缺失
        date_d = string_date(row['pubDate'])
    if row['DOInumber'] and row['DOInumber'] == row['DOInumber']:  # doi缺失
        doi_num = row['DOInumber']
    sql = """INSERT INTO webapp_paper(pid,paper_title, paper_abstract, paper_pubDate,doi_number)
            VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE
            pid = VALUES(pid),
            paper_title = VALUES(paper_title),
            paper_abstract = VALUES(paper_abstract),
            paper_pubDate = VALUES(paper_pubDate),
            doi_number = VALUES(doi_number)"""    # 防止重复

    try:
        cursor.execute(sql, (pid, title, abstract, date_d, doi_num))
        db.commit()
        return pid
    except Exception:
        print(row['id'])
        traceback.print_exc()
        db.rollback()     # 事务回滚


def string_date(date_s):
    #  21 Apr 2012 | Apr 2012 | March 1999 | March - April 1998 | Mar/Apr 1998 | Sept.-Oct.  1995 | Sept.  1994 |
    try:
        date_d = datetime.strptime(date_s.strip(), "%d %B %Y").strftime('%Y-%m-%d')
    except:
        try:
            date_d = datetime.strptime(date_s.strip(), "%b %Y").strftime('%Y-%m-%d')
        except:
            try:
                date_d = datetime.strptime(date_s.strip(), "%B %Y").strftime('%Y-%m-%d')
            except:
                try:
                    l = date_s.split()
                    date_s = l[0].strip('.')+' '+l[1]
                    date_d = datetime.strptime(date_s.strip(), "%b %Y").strftime('%Y-%m-%d')
                except:
                    date_d = datetime.strptime("1998-10-10", "%Y-%m-%d").strftime('%Y-%m-%d')

    return date_d


def save_author(row):
    # 存作者
    author_row = row['authors']    # a1,单位---简介***a2,单位---简介***a3,单位---简介***
    if author_row and author_row == author_row:
        if '，' in author_row:     # 中英文符号混杂
            author_row = author_row.replace("，", ",")
        author_list = [i.strip() for i in author_row.split('***')]
        for person in author_list:
            if person:    # a1,单位---简介
                person_list = person.split('---')
                name_from = person_list[0].split(',')
                name = name_from[0].strip()
                a_from = ''
                if name_from[1]:  # 作者单位缺失
                    a_from = name_from[1].strip()
                intro = ''
                if person_list[1]:  # 作者简介缺失
                    intro = person_list[1].strip()

                sql = """INSERT INTO webapp_author(author_introduction, author_name, author_from)
                            VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE 
                            author_introduction = VALUES(author_introduction),
                            author_name = VALUES(author_name),
                            author_from = VALUES(author_from)"""
                try:
                    cursor.execute(sql, (intro, name, a_from))
                    db.commit()
                    sql = """SELECT id FROM webapp_author WHERE author_name = %s"""
                    cursor.execute(sql, (name))
                    aid = cursor.fetchone()[0]
                    return aid
                except Exception:
                    print(row['id'])
                    traceback.print_exc()
                    db.rollback()


def save_key(row, pid):
    # 存关键词
    key_row = row['IEEEkeys']     # key1,key2....
    if key_row and key_row ==key_row:
        if '，' in key_row:
            key_row = key_row.replace("，", ",")
        key_list = [i.strip() for i in key_row.split(',')]
        for key in key_list:
            if key and key==key:
                sql = """SELECT id FROM webapp_ktop WHERE kTop_paper_id = %s AND kTop_keyword = %s"""
                cursor.execute(sql, (pid, key))
                if not cursor.fetchone():
                    sql = """INSERT INTO webapp_ktop(kTop_paper_id, kTop_keyword) VALUES (%s, %s) ON DUPLICATE KEY UPDATE 
                            kTop_paper_id = VALUES(kTop_paper_id),
                            kTop_keyword = VALUES(kTop_keyword)"""
                    try:
                        cursor.execute(sql, (pid, key))
                        db.commit()
                    except Exception:
                        print(row['id'])
                        traceback.print_exc()
                        db.rollback()

    key_row = row['authorkeys']
    if key_row and key_row ==key_row:
        if '，' in key_row:
            key_row = key_row.replace("，", ",")
        key_list = [i.strip() for i in key_row.split(',')]
        for key in key_list:
            if key and key==key:
                sql = """SELECT id FROM webapp_ktop WHERE kTop_paper_id = %s AND kTop_keyword = %s"""
                cursor.execute(sql, (pid, key))
                if not cursor.fetchone():
                    sql = """INSERT INTO webapp_ktop(kTop_paper_id, kTop_keyword) VALUES (%s, %s) ON DUPLICATE KEY UPDATE 
                            kTop_paper_id = VALUES(kTop_paper_id),
                            kTop_keyword = VALUES(kTop_keyword)"""
                    try:
                        cursor.execute(sql, (pid, key))
                        db.commit()
                    except Exception:
                        print(row['id'])
                        traceback.print_exc()
                        db.rollback()


def save_atop(aid, pid):
    sql = """SELECT id FROM webapp_atop WHERE aTop_author_id = %s AND aTop_paper_id = %s"""
    cursor.execute(sql, (aid, pid))    # 先查找防止重复
    if not cursor.fetchone():
        sql = """INSERT INTO webapp_atop(aTop_author_id, aTop_paper_id) VALUES (%s, %s)"""
        try:
            cursor.execute(sql, (aid, pid))
            db.commit()
        except Exception:
            print(row['id'])
            traceback.print_exc()
            db.rollback()


def save_ptop(row, pid):
    references = row['references']
    if references and references == references:
        references = references.strip().replace("，", ",")
        r_list = references.split(',')
        for rid in r_list:
            if rid:
                rid = rid[10:-1]
                sql = """SELECT id FROM webapp_ptop WHERE pTop_paper_id = %s AND pTop_reference_id = %s"""
                cursor.execute(sql, (pid, rid))    # 先查找防止重复
                if not cursor.fetchone():
                    sql = """INSERT INTO webapp_ptop(pTop_paper_id, pTop_reference_id) VALUES (%s, %s) 
                                ON DUPLICATE KEY UPDATE 
                                pTop_paper_id = VALUES(pTop_paper_id),
                                pTop_reference_id = VALUES(pTop_reference_id)"""
                    try:
                        cursor.execute(sql, (pid, rid))
                        db.commit()
                    except Exception:
                        print(row['id'])
                        traceback.print_exc()
                        db.rollback()

    citations = row['citations']
    if citations and citations == citations:
        citations = citations.strip().replace("，", ",")
        c_list = citations.split(',')
        for cid in c_list:
            if cid:
                cid = cid[10:-1]
                sql = """SELECT id FROM webapp_ptop WHERE pTop_paper_id = %s AND pTop_reference_id = %s"""
                cursor.execute(sql, (pid, cid))
                if not cursor.fetchone():
                    sql = """INSERT INTO webapp_ptop(pTop_paper_id, pTop_reference_id) VALUES (%s, %s) 
                                            ON DUPLICATE KEY UPDATE 
                                            pTop_paper_id = VALUES(pTop_paper_id),
                                            pTop_reference_id = VALUES(pTop_reference_id)"""
                    try:
                        cursor.execute(sql, (cid, pid))
                        db.commit()
                    except Exception:
                        print(row['id'])
                        traceback.print_exc()
                        db.rollback()


df = pd.DataFrame(pd.read_excel("/Volumes/pyy/研究生/软件工程/数据/dataSet2.0.xlsx"))

db = pymysql.connect("localhost", "root", "18911912812pyy", "sedb")

cursor = db.cursor()

for index, row in df.iterrows():
    try:
        pid = save_paper(row)
        if pid:
            save_key(row, pid)
            if row['authors'] and row['authors'] == row['authors']:
                aid = save_author(row)
                save_atop(aid, pid)
        else:
            print(row['id']+"pid有误")
        # pid = row['id'][10:-1]
        # save_ptop(row, pid)

    except Exception as e:
        print(row['id'])
        traceback.print_exc()
        db.rollback()

cursor.close()
db.close()
