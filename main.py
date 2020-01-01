import re
import base64
import time
import configparser
import requests
import hashlib
import threading
from urllib.parse import urlencode
from io import BytesIO
from PIL import Image
from queue import Queue
import cqhttp_helper as cq
from config import bot_host, bot_port, bot_img_file_dir, APP_ID, APP_KEY, qq_group, rules, compress_kb

bot = cq.CQHttp(api_root='http://127.0.0.1:5700/')
q = Queue()


@bot.on_message('group')
def handle_group_msg(context):
    if context['sender']['role'] == 'member' and context['group_id'] in qq_group:
        has_img, files = parse(context['message'])
        if has_img:
            for file in files:
                if file.endswith('.gif'):
                    continue
                q.put({
                    'user_id': context['user_id'],
                    'message_id': context['message_id'],
                    'group_id': context['group_id'],
                    'file': file
                })


def parse(msg):
    """
    解析是否有图片存在
    :param msg: 回复
    :return: 是否有, 图片位置和图片url
    """
    reg = re.findall('\\[CQ:image,file=(.*?),url=.*?\\]', msg)
    return len(reg) > 0, reg


def compress(file):
    """
    判断图片大小是否大于1M, 否则压缩到700kb (base64会使数据变大)
    :param file: 文件路径
    :return: 是否为base64, (如果超, 则返回base64, 如何没有超, 返回url)
    """

    conf = configparser.ConfigParser()
    conf.read(f'{bot_img_file_dir}\\{file}.cqimg')
    o_size = int(conf.get('image', 'size')) / 1024
    md5 = conf.get('image', 'md5')
    img_url = conf.get('image', 'url')

    img_bin = requests.get(img_url).content
    im = Image.open(BytesIO(img_bin))
    while o_size > compress_kb:
        width, height = im.size
        im = im.resize((int(width * 0.5), int(height * 0.5)), Image.ANTIALIAS)
        im.save(f'./tmp/{md5}.{file.split(".")[-1]}')
        with open(f'./tmp/{md5}.{file.split(".")[-1]}', 'rb') as f:
            img_bin = f.read()
            o_size = len(img_bin) / 1024
            im = Image.open(BytesIO(img_bin))
    return base64.b64encode(img_bin).decode('utf-8'), md5


def sign(body: dict):
    """
    sign计算
    :param body:
    :return:
    """
    b = urlencode(sorted(body.items(), key=lambda value: value[0]))
    b += '&app_key=' + APP_KEY
    return str(hashlib.md5(b.encode()).hexdigest()).upper()


def distinguish(data: str, md5: str):
    while True:
        try:
            body = {
                'app_id': APP_ID,
                'time_stamp': int(time.time()),
                'nonce_str': md5,
                'image': data
            }
            body['sign'] = sign(body)
            rsp = requests.post(url='https://api.ai.qq.com/fcgi-bin/vision/vision_porn',
                                data=body,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()
            result = {}
            if rsp['ret'] == 0:
                for v in rsp['data']['tag_list']:
                    result[v['tag_name']] = v['tag_confidence']
            return result
        except Exception as e:
            print('鉴黄出错', e, "5秒后重试")
            time.sleep(5)


def main():
    while True:
        try:
            while not q.empty():
                time.sleep(3)
                task = q.get()
                result = distinguish(*compress(task['file']))
                print(f'识别结果 用户{task["user_id"]} 色情{result["porn"]}% 性感{result["hot"]}% 综合{result["normal_hot_porn"]}%')
                for rule in rules:
                    tag = rule['tag_name']
                    percent = result[tag]
                    if rule['tag_min'] <= percent <= rule['tag_max']:
                        message = "[CQ:at,qq={}]\n识别到本图片为违规的概率为{}%\n给予{}处分\n若有误报, 请联系管理"
                        punishment = ""
                        if rule['punishment']['p'] == 'kick':
                            punishment = '移出本群'
                            bot.set_group_kick(group_id=task['group_id'], user_id=task['user_id'],
                                               reject_add_request=rule['punishment']['reject'])
                        if rule['punishment']['p'] == 'ban':
                            punishment = '禁言' + str(rule['punishment']['times'] / 24 * 60 * 60)
                            bot.set_group_ban(group_id=task['group_id'], user_id=task['user_id'],
                                              duration=rule['punishment']['times'])
                        bot.send_group_msg(group_id=task['group_id'],
                                           message=message.format(task['user_id'], percent, punishment))
        except Exception as e:
            print(e)


threading.Thread(target=main).start()
bot.run(host=bot_host, port=bot_port)
