import requests as req
import json
import telebot
import time
import _thread
from telegram.ext import Updater, CommandHandler

TOKEN = '{your token}'
bot = telebot.TeleBot(TOKEN)
updater = Updater(TOKEN)

url = 'https://querycourse.ntust.edu.tw/querycourse/api/courses'
semestersinfoUrl = 'https://querycourse.ntust.edu.tw/querycourse/api/semestersinfo'
courseNumber = ['TCG065301', 'GE3729301']
data = {"CourseName":"","CourseTeacher":"","Dimension":"","CourseNotes":"","ForeignLanguage":0,"OnlyGeneral":0,"OnleyNTUST":0,"OnlyMaster":0,"OnlyUnderGraduate":0,"OnlyNode":0,"Language":"zh"}
users = ['344370253']

data['Semester'] = req.get(semestersinfoUrl, cookies = {'a':'b'}).json()[0]['Semester']

def add(bot, update):
    number = update.message.text[5:].replace('\n', ' ')
    courseNumber.append(number)
    update.message.reply_text('已加入：' + number)

def hi(bot, update):
    update.message.reply_text('Im here')

def listCourse(bot, update):
    update.message.reply_text(courseNumber)

def handle():
    for course in courseNumber:
        data['CourseNo'] = course
        res = req.post(url, data, cookies = {'ouo':'owo'}).json()
        if (res):
            res = res[0]
            if (int(res['Restrict2']) - res['ChooseStudent'] > 0):
                msg = str(course) + ' ' + res['CourseTeacher'] + ' ' + res['CourseName'] + '\n' + str(res['ChooseStudent']) + ' / ' + str(res['Restrict2']) + ' 人' + '\n僅供參考，實際以課程查詢系統為主 https://querycourse.ntust.edu.tw/querycourse'
                for user in users:
                    req.get('https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + user + '&text=' + msg)

def main():
    while 1:
        handle()
        time.sleep(10)

_thread.start_new_thread(main, ())
updater.dispatcher.add_handler(CommandHandler('add', add))
updater.dispatcher.add_handler(CommandHandler('hi', hi))
updater.dispatcher.add_handler(CommandHandler('list', listCourse))
updater.start_polling()
updater.idle()
