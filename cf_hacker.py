from bs4 import BeautifulSoup as bs
import requests
import os

base_url = 'http://codeforces.com/'

def html(url):
    return requests.get(url).content


def find_solutions_links(url, problem_ID, contest_ID):
    page = bs(html(url), 'html.parser')
    res = []
    for el in page.select(".standings tr td"):
        tp = str(type(el.attrs.get('problemid')))
        if 'str' in tp:
            if el.has_attr('problemid') and str(problem_ID) in el.attrs.get('problemid'):
                if el.has_attr('title') and 'C++' in el.attrs.get('title'):
                    if el.has_attr('acceptedsubmissionid'):
                        res.append(base_url + 'contest/' + str(contest_ID) + '/submission/' + el.attrs.get('acceptedsubmissionid'))
    return res


def find_pages(url):
    res = [url]
    page = bs(html(url), 'html.parser')
    for x in page.select('.custom-links-pagination a'):
        global base_url
        res.append(base_url[:-1] + x.attrs.get('href'))
    return res



def download_solution(url):
    page = bs(html(url), 'html.parser')
    cpp = open("sol.cpp", "w")
    cpp.write(page.select('#program-source-text')[0].text)
    cpp.close()



def check():
    import glob
    inps = glob.glob("*.in")
    x = 0
    for case in range(0, len(inps)):
        os.system("./sol < " + str(case) + ".in > temp.out")
        temp_out = open("temp.out", "r")
        out = open(str(x) + ".out", "r")
        if temp_out.read().strip() != out.read().strip():
            print("Test:")
            inp = open(str(case) + '.in', "r")
            print(inp.read())   
            inp.close()
            print("True answer:")
            print(out.read())
            print("Participant's answer:")
            print(temp_out.read())
            return False
        out.close()
        temp_out.close()
        x += 1
    return True



def start():
    contest_ID = input("Contest ID: ")
    global base_url
    pages = find_pages(base_url + 'contest/' + str(contest_ID) + '/standings')
    problem_ID = input("Problem ID: ")
    solutions = []
    page_num = 1
    for page in pages:
        solutions += find_solutions_links(page, problem_ID, contest_ID)
        print('Page ' + str(page_num) + ' of ' + str(len(pages)))
        page_num += 1
    xxx = 1
    for link in solutions:
        download_solution(link)
        os.system("g++ -std=c++17 -o sol sol.cpp ")
        if check() == False:
            print(link + ' HACK IT!')
        print('Problem #' + str(xxx) + "of " + str(len(solutions))) 
        xxx += 1

if __name__ == '__main__':
    start()
