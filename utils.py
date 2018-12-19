import requests
import json
import string

GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = "EAAD9ZB7nRKsYBAKk76VZAZA0HcFdcqZA0Bj6a6CINV7twRHvUbhBN18cM4oBTnogtNDLa0vu6E8X916YzN8mXXphMA0JcfSS9cMNiOdNKPVUgG9wGRngvQ1ssDWRF1IOsIxbQFsoATgFQ73obvMSTQnpbbTdUvRmYgcjy9uKuwZDZD"
SPIDER_TOKEN = "EAAD9ZB7nRKsYBAPOYOZBocw0zfPU9Dx4kdu2CAgfn6UZBoGJY8lT8I70k55tLCbQA1ZAXPVmAKUB5Lcv4ZC6QAouU9sa2dZBOVsfvHxo6evdCdL4BI7eg4qfyoZAEJMJ2u2sRqATIxhg2GBw4uiYdIkRk8ZAvwSCnBnbyOOkYLVrZBqzZCOJyI86P2ZAGCAZCfbKcRwZD"

def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


def send_image_url(id, img_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment":{
                "type":"image",
                "payload":{
                    "url":img_url
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send img: " + response.text)

def send_button_message(id,text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":text,
                    "buttons":[
                      {
                        "type":"postback",
                        "title":"Yes",
                        "payload":"YES"
                      },
                      {
                        "type":"postback",
                        "title":"No",
                        "payload":"NO"
                      }
                    ]
                  }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def spider(id,upper_post,tag):
    url = "https://graph.facebook.com/v3.2/289195411286102?fields=posts.limit(100)&access_token={0}".format(SPIDER_TOKEN)
    response = requests.get(url)
    html = json.loads(response.text)
    count = 0
    text = ''
    upper = upper_post
    for i in range(len(html['posts']['data'])):
        message = html['posts']['data'][i]['message']
        if message.find(tag)>0:
            count = count+1
            send_text_message(id, message)
        if count==upper:
            break
    if count==0:
        send_text_message(id,"沒有人問過相關的問題，歡迎提問！")
    else:
        send_text_message(id,"搜尋完畢，請問需要什麼服務呢？")
            
def is_number(s):
    try:
        i = int(s)
        if i>0:
            return True
    except ValueError:
        pass
    return False