from bs4 import BeautifulSoup
from requests import get
import sys
import os
from pathlib import Path

def html(url):
    return get(url).content

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Codeforces:

    siteUrl = "http://codeforces.com/"

    def __init__(self):
        pass

class Contest(Codeforces):

    contestId = None
    
    problems_name = []
    problems_link = []

    def __init__(self):
        self.contestId = input("Contest ID: ")
        page = BeautifulSoup(html(self.siteUrl + "contest/" + self.contestId), "html.parser")
        for problem in page.select("table.problems tr td.id a"):
            self.problems_name.append(problem.text.strip().lower())
            self.problems_link.append(problem.attrs.get("href"))
        self.makeFolders()
        self.makeCppFiles()
        self.makeInputFiles()
        os.chdir(self.contestId)
        os.system("bash")

    def makeFolders(self):
        if not os.path.exists(self.contestId):
            os.makedirs(self.contestId)
        for name in self.problems_name:
            if not os.path.exists(self.contestId + "/" + name):
                os.makedirs(self.contestId + "/" + name)

    def makeCppFiles(self):
        templateF = open(str(Path.home()) + "/cpp/template.cpp", "r")
        tpl = templateF.read()
        templateF.close()
        for name in self.problems_name:
            if not os.path.exists(self.contestId + "/" + name + "/" + name + ".cpp"):
                cpp = open(self.contestId + "/" + name + "/" + name + ".cpp", "w")
                cpp.write(tpl)
                cpp.close()
    
    def makeInputFiles(self):
        for i in range(len(self.problems_link)):
            page = BeautifulSoup(html(self.siteUrl + self.problems_link[i]), "html.parser")
            number = 0
            for test in page.select(".sample-test .input pre"):
                txt = open(str(self.contestId) + "/" + self.problems_name[i] + "/in" + str(number), "w")
                txt.write(test.text)
                txt.close()
                number += 1
            i += 1

def main():
    cf = Contest()

if __name__ == '__main__':
    main()
