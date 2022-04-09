# Copyright <koterin> 2022

#!/usr/local/bin/python3

# curl -i -H "Authorization: token
# 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" https://api.github.com/user/repos

import logging
import requests

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    ParseMode,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

TOKEN = '5203607992:AAFsailOGPmQUGdzL01eaJ2BvOcoVkHfUhk'
GITAPI_TOKEN = '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'
BASE_URL = 'https://api.github.com'
OWNER = 'drunkbatya'
REPO = 'purpledb'
PAGE_LIST = 100

logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    logger.info("User %s pressed start", user.username)

    reply_keyboard = [['Repo Info', 'Last 5 commits',
                       'ur mama', 'Top contributors', '/stop']]
    update.message.reply_text(
        fr'Yippee-ki-yay, {user.first_name}!',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
            input_field_placeholder='What would you like to see?'
        ),
    )


def get_commits_for_branch(urlRepo, branch) -> int:
    urlCom = urlRepo + '/commits' + '?per_page=' \
                + str(PAGE_LIST) + '&sha=' + branch
    headers = {'Authorization': 'token ' + GITAPI_TOKEN}
    r = requests.get(urlCom, headers=headers)
    commits = 0
    for dictComm in r.json():
        commits = commits + 1
    # TODO: check if there is only one page
    # TODO: diff function for last_page_commits

    last_url = r.headers.get('Link').split(";", 2)[1]
    last_url = last_url.split(",", 1)[1].split("<", 1)[1].split(">", 1)[0]
    pages = int(last_url[-1])
    comm = requests.get(last_url, headers=headers)
    commits = 0
    for dictCommLast in comm.json():
        commits = commits + 1
    commits = commits + PAGE_LIST * (pages - 1)
    return commits


def get_repo_branches(urlRepo) -> str:
    urlBr = urlRepo + '/branches'
    headers = {'Authorization': 'token ' + GITAPI_TOKEN}
    branches = requests.get(urlBr, headers=headers)
    repoBranches = '\n*Branches:*'
    for dictBr in branches.json():
        repoBranches += '\n' + '>> ' + dictBr["name"]
        repoBranches += '\n' + '      ' + "commits: " \
            + str(get_commits_for_branch(urlRepo, dictBr["name"]))
    return repoBranches


def repo_info(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    logger.info("User %s asked for repo_info", user.username)

    update.message.reply_text('Loading...')
    urlRepo = '{}/repos/{}/{}'.format(BASE_URL, OWNER, REPO)
    urlContr = urlRepo + '/collaborators'
    headers = {'Authorization': 'token ' + GITAPI_TOKEN}
    # TODO: diff funciton for get_collaborators
    r = requests.get(urlRepo, headers=headers)
    contr = requests.get(urlContr, headers=headers)
    dictRepos = r.json()
    repoContr = '\n*Contributors:*'
    for dictContr in contr.json():
        repoContr += '\n' + '>> ' + dictContr["login"]

    repoName = '*' + dictRepos["name"] + '*' + '\n' + dictRepos["html_url"]
    repoDesc = '\n' + '*' + dictRepos["description"] + '*'
    repoLang = '\n' + "*Language:* " + dictRepos["language"]
    repoBranches = get_repo_branches(urlRepo)

    strout = repoName + repoDesc + repoLang
    strout += repoContr + repoBranches
    #  context.bot.edit_message_text(chat_id=update.message.chat_id,
    #                              message_id=update.message.reply_to_message.message_id,
    #                              text="edited")
    update.message.reply_text(strout,
                              parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True)


def last_5_commits(update: Update, contect: CallbackContext) -> None:
    user = update.effective_user
    logger.info("User %s asked for last 5 commits", user.username)

    update.message.reply_text('there would be last 5 commits')


def ur_mama(update: Update, contect: CallbackContext) -> None:
    user = update.effective_user
    logger.info("User %s asked for ur mama", user.username)

    update.message.reply_text('there would be ur mama')


def top_contr(update: Update, contect: CallbackContext) -> None:
    user = update.effective_user
    logger.info("User %s asked for top contributors", user.username)

    update.message.reply_text('there would be top contr')


def stop_command(update: Update, contect: CallbackContext) -> None:
    user = update.effective_user
    logger.info("User %s stopped the bot", user.username)

    update.message.reply_text(
        r'Yippee-ki-yay!',
        reply_markup=ReplyKeyboardRemove()
    )


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text('Repo Info'), repo_info))
    dispatcher.add_handler(MessageHandler(
        Filters.text('Last 5 commits'), last_5_commits))
    dispatcher.add_handler(MessageHandler(
        Filters.text('ur mama'), ur_mama))
    dispatcher.add_handler(MessageHandler(
        Filters.text('Top contributors'), top_contr))
    dispatcher.add_handler(CommandHandler("stop", stop_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
