#!/usr/local/bin/python3

TOKEN='5203607992:AAFsailOGPmQUGdzL01eaJ2BvOcoVkHfUhk'
GITAPI_TOKEN='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'
BASE_URL='https://api.github.com'
OWNER='drunkbatya'
REPO='purpledb'

# curl -i -H "Authorization: token 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" https://api.github.com/user/repos

import requests
import json

'''
def get_all_commits_count():
    first_commit = get_first_commit()
    compare_url = '{}/repos/{}/{}/compare/{}'.format(BASE_URL, OWNER, REPO, first_commit)

    commit_req = requests.get(compare_url)
    commit_count = commit_req.json()['total_commits'] + 1
    print(commit_count)
    return commit_count

def get_first_commit():
    urlCom = '{}/repos/{}/{}/commits'.format(BASE_URL, OWNER, REPO)
    rCom = requests.get(urlCom)
    json_data = rCom.json()

    if rCom.headers.get('Link'):
        page_url = rCom.headers.get('Link').split(',')[1].split(';')[0].split('<')[1].split('>')[0]
        req_last_commit = requests.get(page_url)
        first_commit = req_last_commit.json()
        first_commit_hash = first_commit[-1]['sha']
    else:
        first_commit_hash = json_data[-1]['sha']
    print("hash is " + first_commit_hash)
    return first_commit_hash
'''

def get_commits_count(urlRepo) -> int:
    urlCom = urlRepo + '/commits'
    headers = {'Authorization': 'token ' + GITAPI_TOKEN}
    r = requests.get(urlCom, headers=headers)
    commits = 0
    for dictComm in r.json():
        commits = commits + 1
    print("commits on 1st page: " + str(commits))

    last_url = r.headers.get('Link').split(";", 2)[1].split(",", 1)[1].split("<", 1)[1].split(">", 1)[0]
    pages = int(last_url[-1])
    print("num of pages: " + last_url[-1])

    headers = {'Authorization': 'token ' + GITAPI_TOKEN}
    comm = requests.get(last_url, headers=headers)
    commits = 0
    for dictCommLast in comm.json():
        commits = commits + 1
    print("commits on last page: " + str(commits))

    commits = commits + 30 * (pages - 1)
    return commits

def repo_info() -> None:
    urlRepo = '{}/repos/{}/{}'.format(BASE_URL, OWNER, REPO)
    urlContr = urlRepo + '/collaborators'
    headers = {'Authorization': 'token ' + GITAPI_TOKEN}
    r = requests.get(urlRepo, headers=headers)
    contr = requests.get(urlContr, headers=headers)
    dictRepos=r.json()
    repoContr = '\nContributors:'
    for dictContr in contr.json():
        repoContr += '\n' + '>> ' + dictContr["login"]

    repoName = '*' + dictRepos["name"] + '*' + '\n' + dictRepos["html_url"]
    repoDesc = '\n' + '*' + dictRepos["description"] + '*'
    repoLang = '\n' + "Language: " + dictRepos["language"]
    repoCommits = '\n' + "Total commits number: " + str(get_commits_count(urlRepo))

    strout = repoName + repoDesc + repoLang + repoContr + repoCommits
    print(strout)

# TODO: add logger for every intro

   # for dictRepos in r.json():
   #     print(dictRepos["name"], end=' ')
   #     print(dictRepos["id"])
   #     strout += dictRepos["name"] + '\n'
   # update.message.reply_text(strout)

def main() -> None:
  #  repo_info()
    urlRepo = '{}/repos/{}/{}'.format(BASE_URL, OWNER, REPO)
    print("total num of commits: ", get_commits_count(urlRepo))

if __name__ == '__main__':
    main()

