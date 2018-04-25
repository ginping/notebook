import requests
import json

url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_551816010?csrf_token=19b24778fc96ded4f7ce7cf5f13f1536'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3327.2 Safari/537.36',
    'Referer': 'http://music.163.com/song?id=551816010',
    'Origin': 'http://music.163.com',
    'Host': 'music.163.com'
}

# 加密数据，直接拿过来用
user_data = {
    'params': 'je7XMs9voBmS2EOGiNcp+WG4CThil17JVfTFAugiMzWo+frb7wVB0Wm957/+UjU5YixNohJoIu1VB4vWNyVnO12NSnL+r6GI2M6/XI0+o2KCSVxi6tHUQuFqW6f6pntKDCVPQMwM9Pg8Vs8FaKYdxfKPPVzcVTgw+WFTpjnOeNasT9Igh3g5YfyK8Jk8Ck9DRZlZDs2SlOJhy8h8Gqu8ivMlLMWXs6+zUyvfU5RmOwc=',
    'encSecKey': 'e099485120b4aa56fe54533044bec850f2f6f2d9f15cfc77f2de7e88c73988b2853cc3180cb440ec79d404f46cc3bc93f1786cb09ddfe4a83318120baba775786859b7a3820fba080e2e97cdf9bfbc65b8149e0084103f43e74eef1d106471c5982ad2caeb6738b713d88cc837fc2a4cf8b9bd4631a1275decb0e53ec6bed6c2'
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


from pyecharts import Bar

bar = Bar("热评中点赞数示例图")
bar.add( "点赞数",nickname, liked_count, is_stack=True,mark_line=["min", "max"],mark_point=["average"])
bar.render()


from wordcloud import WordCloud
import matplotlib.pyplot as plt

content_text = " ".join(content_list)
wordcloud = WordCloud(font_path=r"C:\simhei.ttf",max_words=200).generate(content_text)
plt.figure()
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()
