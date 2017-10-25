import json
import re

f = open('posts.txt', 'r')
s = f.read()
f.close()

posts = json.loads(s)

def clean_html(text):
    bad_patterns = ['\r', '\n', '\t', '<!--.*-->', 
                    '<div.*>', '</div>', '<br>', '<a .*</a>',
                    '<img.*>', '<b>', '</b>', '<i>',
                    '</i>', '<font.*>', '</font>', '<u>',
                    '</u>', '<acronym.*>', '</acronym>', '<p.*>',
                    '</p>', '<span.*>', '</span>', '<li.*>',
                    '</li>', '<ul.*>', '</ul>', '<ol.*>',
                    '</ol>', '<em>', '</em>', '<strong>',
                    '</strong>', '<iframe.*>', '</iframe>', '</pre>',
                    '<h.*>', '</h.*>', '<blockquote.*>', '</blockquote>']
    exclude = '|'.join(bad_patterns)
    text = re.sub(exclude, '', text)    
    text = re.sub('<td.*</td>|<table.*</table>|<img.*>|<a.*>|<br.*>|</a>|<d.*>|</d.*>|<em.*>|<pre.*>|</sup>', '', text)
    text = re.sub('\xa0|\&lt;|\&gt;', ' ', text)
    text = re.sub('\&amp;', ' and ', text)
    return bytes(text, 'utf-8').decode('utf-8','ignore')

for post in posts:
    post['text'] = clean_html(post['text'])

f = open('clean_posts.txt', 'w')
s = json.dumps(posts)
f.write(s)
f.close()
