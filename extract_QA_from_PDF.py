"""Script to extract law questions and answers from pdf."""

import PyPDF2 as pyPDF
import re
from enchant.checker.CmdLineChecker import CmdLineChecker
import enchant
import enchant.checker
import json

FILE_QandQ_NAME = 'law-Q&A-005'

chkr = enchant.checker.SpellChecker("en_US")


def spell_check(text):
    """Spell checker."""
    chkr.set_text(text)
    cmdln = CmdLineChecker()
    cmdln.set_checker(chkr)
    cmdln.run()

    return chkr.get_text()


def generate_text_from_pdf_page(FILE_QandQ_NAME):
    """Generate text from pdf, one page at a time."""
    pdfFileObj = open(FILE_QandQ_NAME + '.pdf', 'rb')
    pdfReader = pyPDF.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages
    # print(pages)

    for page in range(pages):
        pageObj = pdfReader.getPage(page)
        pageContent = pageObj.extractText()

        yield pageContent


def route_pages(page):
    """Decide based on content if the pages contains answers."""
    answers = False
    if 'Item Answer Subject'.lower() in page.lower():
        pageAnswers = page[page.find('Item Answer Subject'):]
        page = page[:page.find('Item Answer Subject')]
        page = page[page.find('1.'):]
        answersPattern = re.compile('(\d{1,3}\.?\s+\w)')
        answers = answersPattern.findall(pageAnswers)
        answers = [tuple(i.split('. ')) if '.' in i else tuple(i.split(' ')) for i in answers]
        answers = dict(answers)
        print('{} answers found'.format(len(answers)))

    return page, answers


def get_questions_from_text(page):
    """Extract questions from a page."""
    questionsPattern = re.compile('^\d{1,3}\.\s|\w\.\s?\d{1,3}\.\s|-\s?\d{1,3}\.\s')
    find = questionsPattern.findall(page)
    for f in find:
        findPattern = re.compile('(.{}{}(.\s?){})'.format('{0,10}', str(f), '{10,100}'))
        print(f, findPattern.search(page).group().replace('\n', ' '))
        # print(len(find))
    questions = questionsPattern.split(page)
    questions = [q for q in questions if q]
    # print(questions)
    # print(len(questions))
    return questions


def replace_patterns(text, patterns):
    """Remove gibberish characters from text."""
    for pattern in patterns:
        # print(pattern)
        text = re.compile(pattern[0]).sub(pattern[1], text)
    return text


if __name__ == '__main__':
    text_generator = generate_text_from_pdf_page(FILE_QandQ_NAME)
    questions = []
    answers = {}
    for text in text_generator:
        page, tempAnswers = route_pages(text)
        if tempAnswers:
            for k, v in tempAnswers.items():
                answers[k] = v
        questions.extend(get_questions_from_text(page))
    print(len(questions))

    GibberishPatterns = [('™', "'"), ('ﬁ', '"'), ('ﬂ', '"'), ('(?<=\w)\s*-\s*(?=\w)', ''),
                         ('\s\d*.?MBE Sample Test Questions\s+(\|?\s?\d?)?', ''), ('\s+', ' '),
                         ('\n', ' '), ('\s?GO\sON\sTO\sTHE\sNEXT\sPAGE.\s?-?\d?\d?-?', '')]

    with open('law-words.txt', 'r') as r:
        WordsToReplace = r.read().split('\n')
        WordsToReplace = [tuple(w.split(', ')) for w in WordsToReplace if w]

    i = 1
    cleanQuestions = []
    for q in questions:
        # print(q)
        q = str(q)
        q = replace_patterns(q, GibberishPatterns)
        q = replace_patterns(q, WordsToReplace)
        q = q.strip()
        # q = spell_check(q)
        cleanQuestions.append(q)

    with open(FILE_QandQ_NAME + '.txt', 'w') as f:
        # f.write(docText)
        f.write(json.dumps(answers) + '\n')
        for QA in cleanQuestions:
            f.write(QA.strip()+'\n')

    print(len(questions), len(answers))
