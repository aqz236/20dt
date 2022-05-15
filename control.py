import requests
import cleanData
import time
from fuzzy_que import fuzz
import random
import json

version = 1.1
unfindNum = 0
sureNum = 0     # 答对的数量
failQuesInfo = []   # 答错的题信息

def logo():
    print('''  
      ______   _                   
     |  ____| | |                  
     | |__ ___| |__   _____      __
     |  __/ __| '_ \ / _ \ \ /\ / /
     | |  \__ \ | | | (_) \ V  V / 
     |_|  |___/_| |_|\___/ \_/\_/  
                                   ''')


def send(phone):
    data = {'phone': phone}
    try:
        response = requests.get('http://gxwljs.xyz:9009/', data=data).json()
        if response['code'] == 0:
            body = response['data']
            print(response['msg'])
        else:
            print(response['msg'])
    except:
        print("❌    接口出错，请等待修复")
    url = 'https://gw.hntv.tv/user/auth/sms/send'
    headers = {'Host': 'gw.hntv.tv', 'Connection': 'keep-alive', 'Content-Length': '239',
               'Accept': 'application/json, text/javascript, */*; q=0.01', 'Origin': 'https://gw.hntv.tv',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63060012)',
               'Content-Type': 'application/json', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Dest': 'empty', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
    res = requests.post(url, headers=headers, data=str(body)).json()
    if res['code'] == 0:
        print("✔    验证码发送成功")


def getIndexCookie():
    url = 'https://gw.hntv.tv/uaa/oauth/authorize?response_type=code&client_id=uc_web&login_type=uc_web&redirect_uri=https://uc.hntv.tv/login'
    headers = {'Host': 'gw.hntv.tv', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Sec-Fetch-User': '?1',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'navigate',
               'Referer': 'https://static.hntv.tv/total/tzdt/',
               'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    # 禁止重定向
    html = requests.get(url, headers=headers, allow_redirects=False)
    # print(html.headers['Set-Cookie'])
    # print(html.headers['Set-Cookie'].split("SESSION=")[1].split(";")[0])
    return html.headers['Set-Cookie'].split("SESSION=")[1].split(";")[0]


def registerCookie(cookie, phone, smsCode):
    # 注册cookie？？ 拿到了新cookie
    url = 'https://gw.hntv.tv/uaa/login.do'
    headers = {'Host': 'gw.hntv.tv', 'Connection': 'keep-alive', 'Content-Length': '382', 'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1', 'Origin': 'null', 'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Sec-Fetch-User': '?1',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {'SESSION': cookie}
    data = f"authenticationType=response_type%3Dcode%26client_id%3Dbd4859dcd7b141eeb297e2f6b6333cec%26login_type%3Dapplication%26state%3Dhttps%253A%252F%252Fstatic.hntv.tv%252Ftotal%252Ftzdt%252F%2523%252F%253Fjump%253D1&username=%7B%22authenticationType%22%3A%22sms%22%2C%22principal%22%3A%22%7B%5C%22mobile%5C%22%3A{phone}%2C%5C%22smsCode%5C%22%3A{smsCode}%7D%22%7D&password=1234&autoCreate=1"
    res = requests.post(url, headers=headers, cookies=cookies, data=data, allow_redirects=False)
    return res.headers['Set-Cookie'].split("SESSION=")[1].split(";")[0]


def getCode(newCookie):
    url = 'https://gw.hntv.tv/uaa/oauth/authorize?response_type=code&client_id=bd4859dcd7b141eeb297e2f6b6333cec&login_type=application&state=https%3A%2F%2Fstatic.hntv.tv%2Ftotal%2Ftzdt%2F%23%2F%3Fjump%3D1'
    headers = {'Host': 'gw.hntv.tv', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Sec-Fetch-User': '?1',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {'SESSION': newCookie}
    res = requests.get(url, headers=headers, cookies=cookies, allow_redirects=False)
    try:
        code = res.headers['Location'].split("code=")[1].split("&")[0]
        return code
    except:
        print("❌    请确认验证码输入正确，且手机号曾绑定过答题平台")


def getToken(code):
    url = 'https://gw.hntv.tv/uaa/oauth/token'
    headers = {'Host': 'gw.hntv.tv', 'Connection': 'keep-alive', 'Content-Length': '131',
               'Origin': 'https://static.hntv.tv',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'content-type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'Sec-Fetch-Site': 'same-site',
               'Sec-Fetch-Mode': 'cors', 'Referer': 'https://static.hntv.tv/total/tzdt/',
               'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {}
    data = {'code': code, 'grant_type': 'authorization_code', 'client_id': 'bd4859dcd7b141eeb297e2f6b6333cec',
            'client_secret': '26e8cb2fbd284f9daa47123d44e9aa70'}
    res = requests.post(url, headers=headers, cookies=cookies, data=data).json()
    return res['access_token']


def createPaper(token):
    url = 'https://nms-general.dianzhenkeji.com/api/mayday/tzbanswer.php?action=start_answer'
    headers = {'Host': 'nms-general.dianzhenkeji.com', 'Connection': 'keep-alive', 'Content-Length': '0',
               'Authorization': token,
               'Origin': 'https://static.hntv.tv',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'content-type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'Sec-Fetch-Site': 'cross-site',
               'Sec-Fetch-Mode': 'cors', 'Referer': 'https://static.hntv.tv/total/tzdt/',
               'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    res = requests.post(url, headers=headers).json()
    # {"code":0,"msg":"\u6210\u529f","data":{"paper_id":2071825}}
    if res['code'] == 0:
        return res['data']['paper_id']
    else:
        print(res)
        print("❌     无法通过认证，请尝试重新登录")


def getQues(paperId, token):
    url = 'https://nms-general.dianzhenkeji.com/api/mayday/tzbanswer.php?action=get_question'
    headers = {'Host': 'nms-general.dianzhenkeji.com', 'Connection': 'keep-alive', 'Content-Length': '16',
               'Authorization': token,
               'Origin': 'https://static.hntv.tv',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'content-type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'Sec-Fetch-Site': 'cross-site',
               'Sec-Fetch-Mode': 'cors', 'Referer': 'https://static.hntv.tv/total/tzdt/',
               'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {}
    data = {'paper_id': paperId}
    res = requests.post(url, headers=headers, cookies=cookies, data=data)
    # print("题元数据：", res.json())
    # {'code': 0, 'msg': '成功', 'data': {'question_id': '4213', 'qtype': '1',
    #  'title': '习近平2017年3月4日看望参加全国政协十二届五次会议的民进、农工、九三学社委员并参加联组会时强调，我国广大____以时不我待的紧迫感、舍我其谁的责任感，主动担当积极作为，刻苦钻研，勤奋工作，为全面建成小康社会、建设世界科技强国作出更大贡献。',
    #  'options': {'optiona': '工人群众', 'optionb': '民主党派成员', 'optionc': '知识分子'}}}
    return res.json()


def showQues(quesInfo):
    print("题目：", quesInfo['data']['title'])
    a = 0
    for a, i in enumerate(quesInfo['data']['options']):
        print(f"{a + 1}: {quesInfo['data']['options'][i]}")


def findAns(quesInfo):
    # 题目检索逻辑
    # 1. 先对题目进行精准匹配，匹配成功直接取对应的答案；
    # 2. 若不能精准匹配，将进行题目模糊匹配，相似度>89%计入相似对象列表，遍历完题库取max，如果列表数量为0则说明没这道题，默认选择b

    ans = cleanData.findAns(quesInfo['data']['title'])
    options = quesInfo['data']['options']
    print("【精准匹配】此题答案是: ", ans)
    if len(ans) == 0:
        # 精准匹配失败
        print("搜不到此题，正在进行模糊匹配")
        # print("题信息：", quesInfo)
        fuzz_ans = cleanData.findAnsFuzz(quesInfo['data']['title'])
        if len(fuzz_ans) == 0:
            print("模糊匹配失败，请联系管理员添加此题，本次默认选择a选项")
            print("该题信息：\n", quesInfo)
            return 'a'  # 匹配不到默认选择a
        else:
            # print("此题答案是(模糊匹配): ", fuzz_ans)
            return selectOption(options, fuzz_ans)
    else:
        # 精准匹配成功
        return selectOption(options, ans)


def selectOption(options, ans):
    # 答案检索逻辑
    # 1. 先对答案进行精准匹配，匹配成功直接取对应的选项；
    # 2. 若不能精准匹配，将进行答案模糊匹配，相似度>89%计入相似对象列表，遍历完题库取max，如果列表数量为0则说明没这道题，默认选择b

    # options: {'optiona': '工人群众', 'optionb': '民主党派成员', 'optionc': '知识分子'}
    # options: {'optiona': '工人群众   ', 'optionb': '民主党派成员', 'optionc': '知识分子'}

    sureAns = []
    f = {}
    # 遇到答案带有空格的，无法匹配，采用了两种解决方案
    # 1.去除空格重新匹配
    # 2.答案模糊匹配
    for i in options:
        option = i.replace('option', '')
        f[str(options[i]).replace(" ", '')] = option  # 答案去空格 {'工人群众': 'a', '民主党派成员': 'b'}
    # print("反转：", f)
    for o in ans:  # 与题库答案匹配
        try:
            sureAns.append(f[o])
        except:
            # print("触发答案模糊匹配")
            for p in f:
                like = fuzz.ratio(p, o)
                if like > 89:
                    sureAns.append(f[p])

    print("正确选项：", sureAns)
    sureAns = sorted(sureAns)
    # print(sorted(sureAns))
    print(','.join(sureAns))
    # print(len(','.join(sureAns)))
    return ''.join(sureAns)


def sendAns(token, paperId, quesInfo, reply):
    global failQuesInfo, sureNum
    finishTime = random.randrange(6000, 20000, 1)
    url = 'https://nms-general.dianzhenkeji.com/api/mayday/tzbanswer.php?action=each_answer'
    headers = {'Host': 'nms-general.dianzhenkeji.com', 'Connection': 'keep-alive', 'Content-Length': '60',
               'Authorization': token,
               'Origin': 'https://static.hntv.tv',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'content-type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'Sec-Fetch-Site': 'cross-site',
               'Sec-Fetch-Mode': 'cors', 'Referer': 'https://static.hntv.tv/total/tzdt/',
               'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {}
    data = {'paper_id': paperId, 'question_id': quesInfo['data']['question_id'], 'answer_time': str(finishTime),
            'reply': reply}
    res = requests.post(url, headers=headers, cookies=cookies, data=data)
    print("提交响应：", res.json())  # 提交响应
    # {'code': 0, 'msg': '成功',
    #  'data': {'have_chance': 1, 'answer': ['B、各级党委（党组）主要负责人  '], 'reply': ['B、各级党委（党组）主要负责人  '], 'result': 0,
    #           'is_continue': '0'}}
    if res.json()['code'] == 0:
        if res.json()['data']['result'] == 1:
            failQuesInfo.append(quesInfo)
            # 提交成功但答案错误
            print("===缺失答案矫正===")
            sureAns = res.json()['data']['answer']
            ans = ''
            for i in sureAns:
                ans += (str(i[0])).lower()
            return 1, ''.join(sorted(ans))
        elif res.json()['data']['result'] == 0:
            # 提交成功且答案正确
            sureNum += 1
            print("✔    提交成功! ")
            return 0, "success"
    else:
        # 提交失败
        return -1, "fail"


def main():
    global unfindNum
    logo()
    newsUrl = 'https://blog-static.cnblogs.com/files/FSHOU/20dt_news.js'
    news = json.loads(requests.get(newsUrl).text.replace("\'", "\""))
    print(f"{news['msg']}")
    print(f"当前版本：{version}    最新版本：{news['version']} ({news['updateTime']})\n")
    phoneNum = input("⚪   输入答题网站绑定的手机号 ：")
    cookie = getIndexCookie()  # 页面cookie
    send(phoneNum)  # 发送验证码
    newCookie = registerCookie(cookie, phoneNum, input("⚪   请输入验证码："))
    code = getCode(newCookie)
    token = getToken(code)

    paperId = createPaper(token)
    print("生成的paperid:  ", paperId)
    num = 0
    while num < 20:
        print("\n" * 2)
        time.sleep(0.5)
        print(f"[[   开始答题    ----    第 {num + 1} 题")
        quesInfo = getQues(paperId, token)
        if type(quesInfo['data']) != dict:  # 试题获取失败则重新获取
            print("❌    系统问题导致，没获取到新题，可能已经答完了20道题\n如果不是满分，可以将以上所有程序输出复制，发送给作者，完善题库~")
            unfindNum += 1
            num += 1
            continue
        showQues(quesInfo)
        reply = findAns(quesInfo)
        print(f"[[   开始提交第 {num + 1} 题答案 {reply}")
        res = sendAns(token, paperId, quesInfo, reply)
        if res[0] == -1:
            # 提交失败
            continue
        elif res[0] == 0:
            # 提交成功且答案正确
            pass
        elif res[0] == 1:
            # 提交成功但答案错误, 重新提交正确答案
            sendAns(token, paperId, quesInfo, res[1])
            continue  # 答案矫正后卡死
        num += 1


if __name__ == '__main__':
    main()
    if unfindNum >= 3:
        print(f"系统原因，有{unfindNum}道题没有生成，尝试重新做一次")
        unfindNum = 0
        print("^^^^^^^^^^^^^^^^^^^题库缺失内容^^^^^^^^^^^^^^^^^^^")
        print(failQuesInfo)
        print("^^^^^^^^^^^^可将上方区域提供给作者，完善题库^^^^^^^^^^^^")
        print("正确答对的题目数量：", sureNum)
        main()

    print("✔    答题结束，来点个小星星吧~\n项目地址：https://github.com/aqz236/20dt")
    text = input("")
