import PyPDF2 as pyPDF
import re
import enchant
import enchant.checker
from enchant.checker.CmdLineChecker import CmdLineChecker
chkr = enchant.checker.SpellChecker("en_US")

pdfFileObj = open('law-Q&A-001.pdf', 'rb')
pdfReader = pyPDF.PdfFileReader(pdfFileObj)
pages = pdfReader.numPages

docContent = []
for page in range(pages):
    pageObj = pdfReader.getPage(page)
    pageContent = pageObj.extractText()
    docContent.append(pageContent)

docContent = ''.join(docContent)
removeGibberishPattern = re.compile('™')
docContent = removeGibberishPattern.sub("'", docContent)
removeDashPattern = re.compile('(?<=\w)(\s?-\s?)(?=\w)')
docContent = removeDashPattern.sub('', docContent)

docText = docContent.replace('\n', ' ')
QandAnswPattern = re.compile('(?<=\d\.\s)(.+?)(?=\d\d?\.\s)')
QandAnswers = QandAnswPattern.findall(docText)

i = 1
print(len(QandAnswers))
for QA in QandAnswers:
    # print(i)
    print(QA)
    i += 1

with open('law-Q&A-001.txt', 'w') as f:
    # f.write(docText)
    for QA in QandAnswers:
        f.write(QA.strip()+'\n')
