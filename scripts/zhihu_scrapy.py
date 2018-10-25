# -*- coding:utf-8 -*-  
# ====#====#====#====
# @CreateTime  : 2018/10/24 18:37
# @Author      : Jeanfo
# @FileName    : zhihu_scrapy.py
# @Software    : PyCharm
"""
 @Desc: 爬取知乎热门50条问题
"""
import requests
import json
import time
import random
from flask_script import Command
from bs4 import BeautifulSoup
from app import db
from models import (
    Question,
    User,
    Answer
)

scrapy_user_id = 11  # 站长养的爬虫
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/69.0.3497.92 Safari/537.36'
}
# limit=50 限定一次爬取50条
# start_urls = 'https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=50&desktop=true'
start_urls = 'https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=10&desktop=true'
# start_urls = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?limit=2&desktop=true'


class ZhihuScrapy(Command):
    def run(self):
        res = requests.get(start_urls, headers=headers)
        data = json.loads(res.text)['data']
        urls = []
        for item in data:
            urls.append(item['target']['link']['url'])

        question_user_scrapy = User.query.filter(User.id == scrapy_user_id).first()
        for url in urls:
            if '/p/' in url:
                print "Maybe it is an article: {}, so skip this item.".format(url)
                print '-' * 40
                continue

            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                print "Question url: {}".format(url)
                print "Question page get fail, status_code: {}".format(res.status_code)
                print '-' * 40
                continue

            soup = BeautifulSoup(res.text, 'lxml')
            try:
                question_title = soup.select('.QuestionHeader-title')[0].get_text()
                question_content = soup.select('.QuestionRichText.QuestionRichText--expandable > '
                                               'div > span')[0].get_text()
            except Exception as e:
                print "Parse question info error, url:{} err_msg:{}".format(url, e)
                print '-' * 40
                continue

            question_user_random = random.choice(User.query.filter(User.telephone.ilike("2%")).all())
            question_user = random.choice([question_user_scrapy, question_user_random, question_user_random])
            print "Question title:", question_title

            if not Question.query.filter(Question.title == question_title).first():
                print "Question not exists, creating ..."
                question = Question(title=question_title, content=question_content)
                question.author = question_user
                db.session.add(question)
                db.session.commit()
                print "done"
            else:
                print "Question already exists, skip this item."
                print '-' * 40
                continue

            usernames = soup.select('.UserLink.AuthorInfo-name > div > div > a')
            contents = soup.select('.RichText.ztext.CopyrightRichText-richText')
            print "To check answer list"
            for username, content in zip(usernames, contents):
                username = username.get_text().strip()
                content = content.get_text().strip()

                print "Author of this answer:", username
                user = User.query.filter(User.username == username).first()
                if not user:
                    print "Author not exists, creating ..."
                    password = ''.join(random.choice('abcdefg1234567890uvwxyz') for i in xrange(8))
                    telephone = '2' + str(int(time.time()))[-5:] + ''.join(
                        random.choice('0123456789') for i in range(5)
                    )
                    user = User(username=username, password=password, telephone=telephone)
                    db.session.add(user)
                    db.session.commit()
                    print "done"
                else:
                    print "Author already exists, go next"

                print "Creating answer ..."
                answer = Answer(content=content)
                answer.question = question
                answer.author = user
                db.session.add(answer)
                db.session.commit()
                print "done"

            print '-' * 40
            time.sleep(1)
