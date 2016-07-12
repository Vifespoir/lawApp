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

with open('law-words.txt', 'r') as r:
    WordsToReplace = r.read().split('\n')
    WordsToReplace = [tuple(w.split(', ')) for w in WordsToReplace if w]
    print(WordsToReplace)
    for w in WordsToReplace:
        docContent = docContent.replace(w[0], w[1])

answers = docContent[docContent.find('Answer Key'):]
docContent = docContent[:docContent.find('Answer Key')]
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


def replace_patterns(text, patterns):
    """Remove gibberish characters from text."""
    for pattern in GibberishPatterns:
        text = re.compile(pattern[0]).sub(pattern[1], text)
    return text

cleanQuestions = []
for q in questions:
    q = replace_patterns(q, GibberishPatterns)
    q = q.strip()
    cleanQuestions.append(q)
# print(docContent)
# print(docContent)

if cleanQuestions[0][:3] == '1. ':
    # print(questions[0][:3])
    cleanQuestions[0] = cleanQuestions[0][3:]
    # print(questions[0])
# print(questions)
i = 1
print(len(questions), len(answers))

with open('law-Q&A-001.txt', 'w') as f:
    # f.write(docText)
    for QA in cleanQuestions:
        f.write(QA.strip()+'\n')
