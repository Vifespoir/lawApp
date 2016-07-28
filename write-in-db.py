import re
import sqlite3
import json

FILE_QandQ_NAME = 'law-Q&A-001'

questionPattern = re.compile("(.+?)\(A\)(.+?)\(B\)(.+?)\(C\)(.+?)\(D\)(.+)")

with open(FILE_QandQ_NAME + '.txt', 'r') as f:
    # f.write(docText)
    i = 1
    questionsList = []
    answers = dict(json.loads(f.readline()))
    answers = {str(int(k)): v for k, v in answers.items()}
    answers[200] = 'A'
    print(answers)
    for q in f:
        # print(q)
        q = questionPattern.search(q).groups()
        q = [i.strip() for i in q]
        # print(len(q))
        questionsList.append((q[0], q[1], q[2], q[3], q[4], answers[str(i)]))
        i += 1

conn = sqlite3.connect('ncbexQandA.db')
c = conn.cursor()
# Create table
tableName = '`NBE SAMPLE TEST ' + FILE_QandQ_NAME + '`'
createColumns = 'id integer primary key, question text, propA text, propB text, propC text, propD text, answer text'
insertColumns = 'question, propA, propB, propC, propD, answer'
command = 'CREATE TABLE {} ({})'.format(tableName, createColumns)
c.execute('DROP TABLE IF EXISTS {}'.format(tableName))
c.execute(command)
# Insert a row of data
c.executemany("INSERT INTO {} ({}) VALUES (?,?,?,?,?,?)".format(tableName, insertColumns), questionsList)
# Save (commit) the changes
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
