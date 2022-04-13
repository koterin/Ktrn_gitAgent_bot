# Ktrn Telegram Bot
Nice tool to check the info about one particular GitHub Repo - just what our team needed for another project

## What it does
1. It greets you by your name with a simple keyboard menu
2. It tells you some common info about the current state of a Repo:
```
PurpleDB
https://github.com/drunkbatya/PurpleDB
SQL-compatible RAM-free micro database with pretty terminal output
Language: C
Contributors:
>> drunkbatya
>> Koterin
>> GrusnyDance
Branches:
>> develop
      commits: 122
>> master
      commits: 124
>> version2.0
      commits: 159
```
3. It gives you info about 5 last commits in a chosen branch
```
2022-03-29T11:30:31Z
       GrusnyDance: Debug delete for all tables
2022-03-28T21:28:09Z
       koterin: done delete for modules
2022-03-27T17:42:31Z
       GrusnyDance: improve codestyle
2022-03-27T17:30:23Z
       GrusnyDance: add delete test
2022-03-27T13:49:54Z
       koterin: done all for status
```
4. It tells you a nice Die-hard-style goodbye

## What is so nice about it
There is an unpleasant part about GitHub API - it doesn't give you the number of commits on a given branch directly, and, moreover, it paginates your info (which is good, okay).
The solution here was to:
1. Manually set the number of records on a page (for commits)
```
urlCom = urlRepo + '/commits' + '?per_page=' \
                + str(PAGE_LIST) + '&sha=' + branch
```
2. Check the link to the last page in the 'link' header of API response and chunk the URL part:
```
    last_url = r.headers.get('Link').split(";", 2)[1]
    last_url = last_url.split(",", 1)[1].split("<", 1)[1].split(">", 1)[0]
```
4. Count the number of records on the last page
5. Count the complete number of records like this:
```
commits = commits + PAGE_LIST * (pages - 1)
```
It's nice, it's pretty simple and it works. Yippee-ki-yay
