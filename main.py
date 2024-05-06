import requests
import pyperclip
import json
import ddddocr

mode = 1
_uid = 0
__client_id = ''
cookie = ''

dcr = ddddocr.DdddOcr(beta=True)

def init():
    global _uid, __client_id, cookie, mode
    try:
        with open('./setting.json', 'r') as f:
            js = json.load(f)
        _uid = js['_uid']
        __client_id = js['__client_id']
        cookie = f'__client_id={__client_id}; _uid={_uid};'
        try:
            mode = js['mode']
        except:
            pass
        return True
    except:
        return False


def getCsrfToken(url='https://www.luogu.com.cn'):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        'x-luogu-type': 'content-only',
        'cookie': cookie,
        'x-requested-with': 'XMLHttpRequest',
    }
    res2 = requests.get(url, headers=headers)
    res2 = res2.text
    csrftoken = res2.split("<meta name=\"csrf-token\" content=\"")[-1].split("\">")[0]
    return csrftoken


def getHeaders(url='https://www.luogu.com.cn'):
    headers = {
        'referer': url,
        'cookie': cookie,
        'x-csrf-token': getCsrfToken(url),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    }
    return headers


def getHeadersGet(url='https://www.luogu.com.cn'):
    headers = {
        'referer': url,
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    }
    return headers


def ocr(img: list):
    return dcr.classification(img)


def getCaptcha():
    print('开始获取验证码')
    url = 'https://www.luogu.com.cn/api/verify/captcha'
    response = requests.get(
        url=url, headers=getHeadersGet('https://www.luogu.com.cn/image')
    )
    print('开始解析验证码')
    return ocr(response.content)


def getUploadArgs():
    print('开始获取上传参数')
    c= getCaptcha();
    print(f'验证码解析完成，为 {c}')
    url = f'https://www.luogu.com.cn/api/image/generateUploadLink?watermarkType={mode}&captcha={c}&type=image_hosting'
    print('开始获取上传参数')
    res = requests.get(url=url, headers=getHeadersGet('https://www.luogu.com.cn/image'))
    if res.status_code == 200:
        print('获取上传参数成功')
        return json.loads(res.text)['uploadLink']
    else:
        print('验证码解析有误，正在重新开始')
        return getUploadArgs()


def uploadImage(filename):
    data = getUploadArgs()
    print('开始构造请求')
    files = {
        'signature': (None, data['signature'], None),
        'callback': (None, data['callback'], None),
        'success_action_status': (None, '200', None),
        'OSSAccessKeyID': (None, data['accessKeyID'], None),
        'policy': (None, data['policy'], None),
        'key': (None, f'{data['dir']}image.png', None),
        'name': (None, f'image.png', None),
        'x-oss-meta-luogu-uid': (None, data['_extra']['x-oss-meta-luogu-uid'], None),
        'x-oss-object-acl': ('None', data['_extra']['x-oss-object-acl'], None),
        'file': ('image.png', open(filename, 'rb'), 'image/png'),
    }
    print('开始上传图片')
    res = requests.post(data['host'], files=files)
    js = json.loads(res.text)
    if js['success']:
        print('上传成功')
        return [True, js['image']['url']]
    else:
        print('上传失败')
        return [False, None]

if __name__ == '__main__':
    init()
    while True:
        filename = input('filename: ')
        if filename[0] == '"':
            filename = filename[1:]
        if filename[-1] == '"':
            filename = filename[:-1]
        res = uploadImage(filename)
        if res[0]:
            pyperclip.copy(res[1])
            print(f'图片链接已复制到剪贴板，链接为 {res[1]}')
        else:
            print('未知错误')
        input('按回车继续')
        print('\033c', end='')
