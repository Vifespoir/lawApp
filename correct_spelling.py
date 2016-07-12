"""Spell checker."""

from enchant.checker.CmdLineChecker import CmdLineChecker
import enchant
import enchant.checker

chkr = enchant.checker.SpellChecker("en_US", 'law-words.txt')

with open('law-Q&A-001.txt', 'r') as r, open('law-Q&A-001.txt.new', 'w') as w:
    QA = r.read()
    chkr.set_text(QA)
    cmdln = CmdLineChecker()
    cmdln.set_checker(chkr)
    cmdln.run()
    QA = chkr.get_text()
    w.write(QA)
