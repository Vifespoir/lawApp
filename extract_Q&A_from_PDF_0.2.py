"""Script to extract law questions and answers from pdf."""

import PyPDF2 as pyPDF
import re


pdfFileObj = open('law-Q&A-001.pdf', 'rb')
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
docContent = docContent[docContent.find('1.')-1:]
answersPattern = re.compile('(\d\d?\.\s\w)')
answers = answersPattern.findall(answers)
answers = [tuple(i.split('. ')) for i in answers]
answers = dict(answers)
print(answers)

questionsPattern = re.compile('(?<!\d)(\n?\d{1,2}\.\s)')
questions = questionsPattern.sub('CUT-HERE', docContent)
questions = questions.split('CUT-HERE')

GibberishPatterns = [('™', "'"), ('ﬁ', '"'), ('ﬂ', '"'), ('(?<=\w)\s*-\s*(?=\w)', ''),
                     ('\s\d*.?MBE Sample Test Questions\s+(\|?\s?\d?)?', ''), ('\s+', ' '),
                     ('\n', ' ')]

with open('law-words.txt', 'r') as r:
    WordsToReplace = r.read().split('\n')
    WordsToReplace = [tuple(w.split(', ')) for w in WordsToReplace if w]


def replace_patterns(text, patterns):
    """Remove gibberish characters from text."""
    for pattern in patterns:
        text = re.compile(pattern[0]).sub(pattern[1], text)
    return text

cleanQuestions = []
for q in questions:
    q = replace_patterns(q, GibberishPatterns)
    for w in WordsToReplace:
        print(str(w[0]), str(w[1]))
        q = q.replace(str(w[0]), str(w[1]))
    q = q.strip()
    cleanQuestions.append(q)
i = 1
print(len(questions), len(answers))

with open('law-Q&A-001.txt', 'w') as f:
    # f.write(docText)
    for QA in cleanQuestions:
        f.write(QA.strip()+'\n')
