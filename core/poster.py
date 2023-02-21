import newspaper
import requests

import os
import sys
import json

with open("./site_list.json", "r") as list_file:
    sites = json.loads(list_file.read())

BOT_TOKEN = os.getenv("NEWS_BOT_TOKEN", None)

if not BOT_TOKEN:
    print("Please set the bot token as an enviroment variable.")
    sys.exit(1)


def get_articles(url, site_name):
    paper = newspaper.build(url, memoize_articles=True)
    content = []
    for article in paper.articles[:5]:
        article.download()
        article.parse()
        article.nlp()
        content.append({'image': article.top_image, 'title': f"{article.title} | {site_name}",
                       'text': article.summary.replace('\n', ' ')[:250]+"[...]", 'link': article.url})
    return content


def post_to_telegram(url, site_name, token, ch_uname):
    articles = get_articles(url, site_name)
    params = {'chat_id': ch_uname,
              'parse_mode': 'html',
              "reply_markup": {
                  "inline_keyboard": [
                      [{"text": "Read Full Article", "url": ""}, ]
                  ]
              }
              }
    bot_url = f'https://api.telegram.org/bot{token}/sendphoto'
    for a in articles:
        caption = '\n\n'.join([f"<b>{a.get('title')}</b>", a.get('text')])
        params.update({'caption': caption, 'photo': a.get('image')})
        params['reply_markup']['inline_keyboard'][0][0]['url'] = a.get('link')
        rsp = requests.post(url=bot_url, json=params)
        # print(rsp.content)
        print(f"Posted: {a.get('title')}")


def main_task():
    for s in sites:
        post_to_telegram(s[0], s[1], BOT_TOKEN, '@swenezt_test')
