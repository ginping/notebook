import requests
import json

url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_3986017?csrf_token=96590d3aba1d4404f016c8629ff27204'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3327.2 Safari/537.36',
    'Referer': 'http://music.163.com/song?id=3986017',
    'Origin': 'http://music.163.com',
    'Host': 'music.163.com'
}

# 加密数据，直接拿过来用
user_data = {
    'params': '8tKOK9wKMA3v2equwLgV1FdvFAYzHDChzCsapgInzdMD+ctBnS6s5w1FOsYBjveV4Gz/sYD/ibeiZrekkrKPkfr98GUukcNTL9keZQC9vBkec3v1bGnXsmqOl9E6/rOz7O7NPVRoPkKr7UPym82hNz0E5h7YWOTYKlWo0XmMozoB77iW4MeK1cqOUxER5Gc8jq4Zj+3qKf10Az8K9qP1Gs1RtFa2rptrBrZ6kznnzak=',
    'encSecKey': '6ffe19635b11e9ea21c268689aca795a9e9066edb75e60f5c39313f7d2aec6ac71262764a9917af1dba2be07535fce7e9839adedb6ce9febb8ad3b65ab51a7ed5021b36d2c5dd0fd2c03cb6ac989eed7433283fc6578165f9dcbbbcc8350ca84a0a32b9d277986df3b6350cccd3bef3f25566c62fbd49ccc2a8a8e799bd356fd'
}

response = requests.post(url, headers=headers, data=user_data)

data = json.loads(response.text)
hotcomments = []
for hotcomment in data['hotComments']:
    item = {
        'nickname':hotcomment['user']['nickname'],
        'content':hotcomment['content'],
        'likedCount':hotcomment['likedCount']
    }
    hotcomments.append(item)

#获取评论用户名,内容,以及对应的获赞数
content_list = [content['content'] for content in hotcomments]
nickname = [content['nickname'] for content in hotcomments]
liked_count = [content['likedCount'] for content in hotcomments]


from wordcloud import WordCloud
import matplotlib.pyplot as plt

content_text = " ".join(content_list)
wordcloud = WordCloud(font_path=r"C:\simhei.ttf",max_words=200).generate(content_text)
plt.figure()
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()
