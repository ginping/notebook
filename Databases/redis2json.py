import redis
import json
import codecs

r = redis.Redis(host='localhost', port=6379)
results = r.lrange('disk:qyxx:primaryinfoapp', 0, 1)
with codecs.open('primaryinfoapp.json', 'w', 'utf-8') as f:
    for result in results:
        di = json.loads(result)
        data = json.dumps(di, ensure_ascii=False) + '\n'
        f.write(data)
