"""Script to extract law questions and answers from pdf."""

import PyPDF2 as pyPDF
import re
from enchant.checker.CmdLineChecker import CmdLineChecker
import enchant
import enchant.checker
import json

FILE_QandQ_NAME = 'law-Q&A-003'

chkr = enchant.checker.SpellChecker("en_US", 'law-words.txt')


def spell_check(text):
    """Spell checker."""
    chkr.set_text(text)
    cmdln = CmdLineChecker()
    cmdln.set_checker(chkr)
    cmdln.run()

    return chkr.get_text()


def replace_patterns(text, patterns):
    """Remove gibberish characters from text."""
    for pattern in patterns:
        text = re.compile(pattern[0]).sub(pattern[1], text)
    return text

pdfFileObj = open(FILE_QandQ_NAME + '.pdf', 'rb')
pdfReader = pyPDF.PdfFileReader(pdfFileObj)
pages = pdfReader.numPages

docContent = []
for page in range(pages):
    pageObj = pdfReader.getPage(page)
    pageContent = pageObj.extractText()
    docContent.append(pageContent)

docContent = ''.join(docContent)

answers = docContent[docContent.find('Answer Key'):]
docContent = docContent[:docContent.find('Answer Key')]
docContent = docContent[docContent.find('1.'):]
answersPattern = re.compile('(\d\d?\.\s\w)')
answers = answersPattern.findall(answers)
answers = [tuple(i.split('. ')) for i in answers]
answers = dict(answers)
# print(answers)

questionsPattern = re.compile('(?<!\d)(\n?\d{1,2}\.\s)')
questions = questionsPattern.sub('CUT-HERE', docContent)
questions = questions.split('CUT-HERE')
questions = [q for q in questions if q]

GibberishPatterns = [('™', "'"), ('ﬁ', '"'), ('ﬂ', '"'), ('(?<=\w)\s*-\s*(?=\w)', ''),
                     ('\s\d*.?MBE Sample Test Questions\s+(\|?\s?\d?)?', ''), ('\s+', ' '),
                     ('\n', ' ')]

with open('law-words.txt', 'r') as r:
    WordsToReplace = r.read().split('\n')
    WordsToReplace = [tuple(w.split(', ')) for w in WordsToReplace if w]


i = 1
cleanQuestions = []
for q in questions:
    q = replace_patterns(q, GibberishPatterns)
    for w in WordsToReplace:
        q = q.replace(str(w[0]), str(w[1]))
    q = q.strip()
    q = spell_check(q)
    cleanQuestions.append(q)

with open(FILE_QandQ_NAME + '.txt', 'w') as f:
    # f.write(docText)
    f.write(json.dumps(answers) + '\n')
    for QA in cleanQuestions:
        f.write(QA.strip()+'\n')

print(len(questions), len(answers))
