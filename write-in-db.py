import re
import sqlite3
import json
from extract_Q&A_from_PDF import FILE_QandQ_NAME

questionPattern = re.compile("(.+?)\(A\)(.+?)\(B\)(.+?)\(C\)(.+?)\(D\)(.+)")

with open(FILE_QandQ_NAME + '.txt', 'r') as f:
    # f.write(docText)
    i = 1
    questionsList = []
    answers = dict(json.loads(f.readline()))
    print(answers)
    for q in f:
        print(q)
        q = questionPattern.search(q).groups()
        q = [i.strip() for i in q]
        questionsList.append((q[0], q[1], q[2], q[3], q[4], answers[str(i)]))
        i += 1

test_number = '001'
conn = sqlite3.connect('ncbexQandA.db')
c = conn.cursor()
# Create table
tableName = '`NBE SAMPLE TEST ' + test_number + '`'
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
