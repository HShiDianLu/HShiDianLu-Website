# Server Maintenance main.py By HShiDianLu.
# Copyright © 2024-2025 HShiDianLu. All Rights Reserved.

import base64
import smtplib
import ssl
import string
from email.mime.text import MIMEText
import flask
import requests.cookies
from flask import *
from math import *
import requests
from datetime import *
import re
import time
import jieba
import logging
from logging.handlers import RotatingFileHandler
import uuid
import random
import hashlib
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymysql
from bs4 import BeautifulSoup
import os

# Basic Configs
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = ("xxx")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

limiter = Limiter(app=app, default_limits=["100/minute", "10000/day"], key_func=get_remote_address,
                  storage_uri="xxx")

databaseHost = "xxx"
databaseUser = "xxx"
databasePwd = "xxx"
database = "xxx"
databaseCharset = "utf8"

# colaUid = "xxx"
# colaAppKey = "xxx"

githubOAuthID = "xxx"
githubSecret = githubOAuthID + "xxx"
githubAuth = str(base64.b64encode(githubSecret.encode("utf-8")), "utf-8")
githubOAuthSecret = "xxx"
githubOAuthURL = "https://github.com/login/oauth/authorize?scope=read:user%20user:email&client_id=" + githubOAuthID + "&state="

recaptchaSecret = "xxx"

superUser = ["xxx", "xxx"]

# Log
logging.basicConfig(level=logging.DEBUG)
logHandler = RotatingFileHandler("logs/log_" + datetime.now().strftime('%Y-%m-%d %H.%M.%S') + ".log")
formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(filename)s:%(lineno)d %(message)s')
logHandler.setFormatter(formatter)
logging.getLogger().addHandler(logHandler)
app.logger.addHandler(logHandler)

# APIs & Modules Init

# colaKey = requests.post("https://luckycola.com.cn/ai/getColaKey", data={"uid": colaUid, "appKey": colaAppKey}).json()[
#    'data']
# logging.info("ColaKey: " + colaKey['cola_key'] + ", Exp: " + colaKey['end_time_str'] + " " + str(colaKey['end_time']))
# colaKey = colaKey['cola_key']

conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                       charset=databaseCharset)
cour = conn.cursor()
sql = 'select * from sensitiveWord'
cour.execute(sql)
result = cour.fetchall()
sensitiveWords = []
for i in result:
    sensitiveWords.append(i[1])
logging.info("Fetched sensitives.")

generalData = {}


def updateGeneral():
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from general'
    cour.execute(sql)
    result = cour.fetchall()
    for i in result:
        generalData[i[0]] = i[1]
    logging.debug(generalData)
    logging.info("Fetched general.")


updateGeneral()

jieba.lcut("预先初始化", cut_all=True)
logging.info("Loaded jieba model.")

# 致敬传奇服务器Github
repo = requests.get("https://api.github.com/users/HShiDianLu/repos",
                    headers={"Authorization": "Basic " + githubAuth}).json()
logging.info("Fetched repo.")
logging.debug(repo)


# Build Hash

def getHashofDirs(directory, blacklist):
    SHAhash = hashlib.md5()
    paths = os.walk(directory)
    for path, dirList, fileList in paths:
        flag = False
        for i in blacklist:
            if i in path:
                flag = True
                break
        if flag:
            continue
        for i in fileList:
            filename = os.path.join(path, i)
            try:
                f1 = open(filename, 'rb')
            except:
                logging.info("Hashing Failed " + i + ". Skip.")
                continue
            while 1:
                buf = f1.read(4096)
                if not buf:
                    break
                SHAhash.update(hashlib.md5(buf).hexdigest().encode())
    return SHAhash.hexdigest()[0:7]


buildHash = getHashofDirs("./", ["/others", "/logs", "/.idea", "/.github", "/WebsiteEnv", "/__pycache__"])
logging.info("Build Hash: " + buildHash)


# MD5处理
def md5(text):
    text = text.encode()
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()


# 主页
@app.route("/")
def index():
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from article order by date desc limit 3'
    cour.execute(sql)
    result = cour.fetchall()
    text = "false"
    try:
        text = requests.get(generalData['hitokoto_api'], timeout=1).text
        if not text:
            text = "false"
        logging.debug(text)
    except Exception as e:
        logging.error("Hitokoto connection error: " + str(e))
    descLens = []
    for i in result:
        descLens.append(len(i[2]))
    return render_template("index.html", articles=result, user=session.get('username'), repo=repo,
                           repoLen=len(repo), text=text, buildHash=buildHash, descLens=descLens,
                           articlesLen=len(result), info=generalData['homepage_info'])


# 文章页
@app.route("/article")
def article():
    page = request.args.get("page")
    if page == "1":
        return redirect("/article")
    if not page:
        page = "1"
    if not page.isdigit():
        return redirect("/article")
    page = int(page)
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from article order by date desc limit %s, 5'
    cour.execute(sql, [(page - 1) * 5])
    result = cour.fetchall()
    sql = 'select count(*) from article'
    cour.execute(sql)
    count = cour.fetchall()
    pages = [page - 2, page - 1, page, page + 1, page + 2]
    overall = ceil(count[0][0] / 5)
    flag = True
    if page > overall:
        return redirect("/article")
    if overall < 5:
        flag = False
        pages = []
        for i in range(overall):
            pages.append(i + 1)
    while flag:
        flag = False
        for i in pages:
            if i < 1:
                pages.remove(i)
                pages.append(pages[-1] + 1)
                flag = True
            if i > overall:
                pages.remove(i)
                pages.insert(0, pages[0] - 1)
                flag = True
    descLens = []
    for i in result:
        descLens.append(len(i[2]))
    return render_template("article.html", page=page, overallPage=overall, articles=result, pages=pages,
                           user=session.get('username'), buildHash=buildHash, descLens=descLens,
                           articlesLen=len(result))


# 文章详情
@app.route("/article/<pageId>")
def articlePage(pageId):
    if not pageId.isdigit():
        return render_template("alert.html", title="文章", alertTitle="发生错误", alertText="非法ID。",
                               alertIcon="error", href="/article")
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from article where id=%s limit 1'
    cour.execute(sql, [pageId])
    result = cour.fetchall()
    if len(result) == 0:
        return render_template("alert.html", title="文章", alertTitle="发生错误", alertText="找不到该文章。",
                               alertIcon="error", href="/article")
    cour.execute(sql, [str(int(pageId) - 1)])
    prev = cour.fetchall()
    cour.execute(sql, [str(int(pageId) + 1)])
    next = cour.fetchall()
    prevSplit = False
    if prev and len(prev[0][0]) > 12:
        prevSplit = True
    nextSplit = False
    if next and len(next[0][0]) > 12:
        nextSplit = True
    sql = 'select * from `comment` where article_id=%s order by date desc limit 10'
    cour.execute(sql, [pageId])
    comment = cour.fetchall()
    if session.get('username'):
        sql = 'select * from `like` where `user`=%s and article_id=%s limit 1'
        cour.execute(sql, [session.get('username'), pageId])
        like = cour.fetchall()
    else:
        like = []
    sql = 'update article set watch=watch+1 where id=%s'
    cour.execute(sql, [pageId])
    conn.commit()
    if len(like) == 0:
        like = False
    else:
        like = True
    if len(comment) < result[0][7]:
        moreContent = True
    else:
        moreContent = False
    return render_template("articlePage.html", article=result[0], user=session.get('username'), comment=comment,
                           like=like, moreContent=moreContent, buildHash=buildHash, prev=prev, next=next,
                           prevSplit=prevSplit, nextSplit=nextSplit)


# Bing 每日图片
@app.route("/getImg", methods=["POST"])
def getImg():
    result = requests.get("https://cn.bing.com/HPImageArchive.aspx?format=js&n=1")
    logging.debug(result)
    json = {'url': "https://cn.bing.com" + result.json()['images'][0]['url'],
            'copyright': result.json()['images'][0]['copyright']}
    return jsonify(json)


# 登录
@app.route("/login", methods=["POST"])
@limiter.limit("10/minute")
def login():
    username = request.form.get("username")
    pwd = request.form.get("password")
    token = request.form.get("token")
    pwd = md5(pwd)
    if (not username) or (not pwd) or (not token):
        return jsonify({'result': 'error', 'code': 1005})
    data = {
        "secret": recaptchaSecret,
        "response": token,
        "remoteip": request.remote_addr
    }
    try:
        verifyResult = requests.post("https://recaptcha.net/recaptcha/api/siteverify", data=data, timeout=5).json()
    except Exception as e:
        logging.error("Recaptcha connection error: " + str(e))
        return jsonify({'result': 'error', 'code': 1001})
    logging.debug(verifyResult)
    if verifyResult['score'] <= 0.5:
        return jsonify({'result': 'error', 'code': 1018})
    if verifyResult['action'] != 'login':
        return jsonify({'result': 'error', 'code': 1019})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from `user` where username=%s or email=%s limit 1'
    cour.execute(sql, [username, username])
    result = cour.fetchall()
    if len(result) == 0:
        return jsonify({'result': 'error', 'code': 1002})
    if result[0][2] == pwd:
        if result[0][4] == 1:
            return jsonify({'result': 'error', 'code': 1009})
        session['username'] = result[0][0]
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'error', 'code': 1002})


# 邮件发送
def sendMail(receiver, content, title):
    message = MIMEText(content, "html", "utf-8")
    message["From"] = f"HShiDianLu's Website<xxx>"
    message["To"] = receiver
    message["Subject"] = title
    logging.debug(content)
    try:
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT')
        logging.debug("Connect")
        smtpObj = smtplib.SMTP("xxx", 25, timeout=5)
        logging.debug("Login")
        smtpObj.login("xxx", "xxx")
        logging.debug("Send")
        smtpObj.sendmail("xxx", receiver, message.as_string())
    except Exception as e:
        logging.error("Email sending error: " + str(e))
        return -1
    return 0


# 注册
@app.route("/register", methods=["POST"])
@limiter.limit("10/minute")
def register():
    email = request.form.get("email")
    username = request.form.get("username")
    pwd = request.form.get("password")
    token = request.form.get("token")
    if (not username) or (not pwd) or (not email) or (not token):
        return jsonify({'result': 'error', 'code': 1005})
    if re.match("^(?![^a-zA-Z]+$)(?!\D+$)", pwd) == None:
        return jsonify({'result': 'error', 'code': 1005})
    if re.match("^[a-zA-Z0-9_]+$", username) == None:
        return jsonify({'result': 'error', 'code': 1005})
    if re.match("^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$", email) == None:
        return jsonify({'result': 'error', 'code': 1005})
    data = {
        "secret": recaptchaSecret,
        "response": token,
        "remoteip": request.remote_addr
    }
    try:
        verifyResult = requests.post("https://recaptcha.net/recaptcha/api/siteverify", data=data, timeout=5).json()
    except Exception as e:
        logging.error("Recaptcha connection error: " + str(e))
        return jsonify({'result': 'error', 'code': 1001})
    logging.debug(verifyResult)
    if verifyResult['score'] <= 0.5:
        return jsonify({'result': 'error', 'code': 1018})
    if verifyResult['action'] != 'register':
        return jsonify({'result': 'error', 'code': 1019})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from `user` where username=%s limit 1'
    cour.execute(sql, [username])
    validUsername = cour.fetchall()
    sql = 'select * from `user` where email=%s limit 1'
    cour.execute(sql, [email])
    validEmail = cour.fetchall()
    if len(validEmail) != 0:
        return jsonify({'result': 'error', 'code': 1007})
    if len(validUsername) != 0:
        return jsonify({'result': 'error', 'code': 1006})
    if sensitiveCheck(username, True):
        return jsonify({'result': 'error', 'code': 1003})
    token = str(uuid.uuid4()).replace("-", "")
    email_content = (
            "<h1>HShiDianLu's Website</h1><p>感谢您注册账户，请点击下方链接验证邮箱。</p><a href='https://" + generalData[
        'server_ip'] + "/verify?token=" + token + "'>https://" + generalData[
                'server_ip'] + "/verify?token=" + token + "</a>")
    email_title = "注册账号 | 验证您的电子邮件"
    respond = sendMail(email, email_content, email_title)
    if respond == -1:
        return jsonify({'result': 'error', 'code': 1004})
    if respond == 0:
        md5Pwd = md5(pwd)
        createUUID = str(uuid.uuid4()).replace("-", "")
        sql = 'insert into `user` (username, uuid, `password`, email, locked) values (%s, %s, %s, %s, 1)'
        cour.execute(sql, [username, createUUID, md5Pwd, email])
        sql = 'insert into verify (verifyUUID, token, expire) values (%s, %s, %s)'
        cour.execute(sql, [createUUID, token, round(time.time()) + 1200])
        conn.commit()
        logging.info(username + " registered.")
        return jsonify({'result': 'success'})
    return jsonify({'result': 'error', 'code': '1008'})


# 登出
@app.route("/logout")
def logout():
    to = request.args.get("to")
    if not to:
        to = ""
    try:
        session.pop("username")
    except:
        pass
    return redirect(to)


# 敏感词 type: True - 严格查询；False - 宽松查询
def sensitiveCheck(word, type):
    if type:
        for i in sensitiveWords:
            if i in word:
                return True
        return False
    else:
        words = jieba.lcut(word, cut_all=True)
        logging.debug(words)
        for i in words:
            if i in sensitiveWords:
                return True
        return False


# 邮箱验证
@app.route("/verify")
def verify():
    token = request.args.get("token")
    if not token:
        return render_template("alert.html", title="邮箱验证", alertTitle="验证失败",
                               alertText="缺少参数：Token。", alertIcon="error", noButton=True)
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from verify where token=%s limit 1'
    cour.execute(sql, [token])
    result = cour.fetchall()
    if len(result) == 0:
        return render_template("alert.html", title="邮箱验证", alertTitle="验证失败",
                               alertText="Token不正确或已失效。", alertIcon="error", noButton=True)
    sql = 'select * from `user` where uuid=%s limit 1'
    cour.execute(sql, [result[0][0]])
    userResult = cour.fetchall()
    if userResult[0][4] == 0:
        return render_template("alert.html", title="邮箱验证", alertTitle="验证失败",
                               alertText="您已通过验证，无需重复验证。", alertIcon="error", noButton=True)
    if result[0][2] < time.time():
        return render_template("verify.html",
                               script='swal({title: "验证失败",text: "Token已过期。",icon: "error",buttons: {resent:"向我重新发送邮件"},closeOnClickOutside: false,})',
                               token=token)
    sql = 'delete from verify where token=%s'
    cour.execute(sql, [token])
    sql = 'update `user` set locked=0 where uuid=%s'
    cour.execute(sql, [result[0][0]])
    conn.commit()
    logging.info(str(uuid) + " passed the verification.")
    return render_template("alert.html", title="邮箱验证", alertTitle="验证成功",
                           alertText="您已通过验证，请返回主页重新登录。您现在可以关闭此页面了。", alertIcon="success",
                           noButton=True)


# 重发邮件
@app.route("/emailResent", methods=["POST"])
@limiter.limit("5/minute")
def resent():
    token = request.form.get("token")
    recaptchaToken = request.form.get("recaptchaToken")
    if (not token) or (not recaptchaToken):
        return jsonify({'result': 'error', 'code': 1010})
    data = {
        "secret": recaptchaSecret,
        "response": recaptchaToken,
        "remoteip": request.remote_addr
    }
    try:
        verifyResult = requests.post("https://recaptcha.net/recaptcha/api/siteverify", data=data, timeout=5).json()
    except Exception as e:
        logging.error("Recaptcha connection error: " + str(e))
        return jsonify({'result': 'error', 'code': 1001})
    logging.debug(verifyResult)
    if verifyResult['score'] <= 0.5:
        return jsonify({'result': 'error', 'code': 1018})
    if verifyResult['action'] != 'emailResent':
        return jsonify({'result': 'error', 'code': 1019})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from verify where token=%s limit 1'
    cour.execute(sql, [token])
    result = cour.fetchall()
    if len(result) == 0:
        return jsonify({'result': 'error', 'code': 1011})
    sql = 'select * from `user` where uuid=%s limit 1'
    cour.execute(sql, [result[0][0]])
    userResult = cour.fetchall()
    if userResult[0][4] == 0:
        return jsonify({'result': 'error', 'code': 1012})
    newToken = str(uuid.uuid4()).replace("-", "")
    email_content = (
            "<h1>HShiDianLu's Website</h1><p>感谢您注册账户，请点击下方链接验证邮箱。</p><a href='https://" + generalData[
        'server_ip'] + "/verify?token=" + newToken + "'>https://" + generalData[
                'server_ip'] + "/verify?token=" + newToken + "</a>")
    email_title = "注册账号 | 验证您的电子邮件"
    respond = sendMail(userResult[0][3], email_content, email_title)
    if respond == -1:
        return jsonify({'result': 'error', 'code': 1004})
    if respond == 0:
        sql = 'delete from verify where token=%s'
        cour.execute(sql, [token])
        sql = 'insert into verify (verifyUUID, token, expire) values (%s, %s, %s)'
        cour.execute(sql, [result[0][0], newToken, round(time.time()) + 1200])
        conn.commit()
        return jsonify({'result': 'success'})
    return jsonify({'result': 'error', 'code': '1008'})


# 文章操作
@app.route("/articleOperate", methods=["POST"])
@limiter.limit("4/second")
@limiter.limit("20/minute")
def articleOperate():
    type = request.form.get("type")
    comment = request.form.get("comment")
    id = str(request.form.get("id"))
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    if type == "like":
        sql = 'select * from `like` where `user`=%s and article_id=%s limit 1'
        cour.execute(sql, [session.get('username'), id])
        like = cour.fetchall()
        if len(like) == 0:
            sql = 'insert into `like` (`user`, article_id) values (%s, %s)'
            cour.execute(sql, [session.get('username'), id])
            sql = 'update article set `like`=`like`+1 where id=%s'
        else:
            sql = 'delete from `like` where `user`=%s and article_id=%s'
            cour.execute(sql, [session.get('username'), id])
            sql = 'update article set `like`=`like`-1 where id=%s'
        cour.execute(sql, [id])
    elif type == "comment":
        if not comment:
            return jsonify({'result': 'error', 'code': 1005})
        if len(comment) > 200:
            return jsonify({'result': 'error', 'code': 1005})
        if sensitiveCheck(comment, False):
            return jsonify({'result': 'error', 'code': 1016})
        commentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = 'update article set `comment`=`comment`+1 where id=%s'
        cour.execute(sql, [id])
        sql = 'insert into `comment` (`user`, id, article_id, date, `comment`, `like`) values (%s, %s, %s, %s, %s, 0)'
        cour.execute(sql, [session.get('username'), str(uuid.uuid4()).replace("-", ""), id,
                           commentTime, comment])
        conn.commit()
        return jsonify({'result': 'success', 'data': commentTime})
    elif type == "share":
        sql = 'select * from `share` where `user`=%s and article_id=%s limit 1'
        cour.execute(sql, [session.get('username'), id])
        share = cour.fetchall()
        if len(share) == 0:
            sql = 'insert into `share` (`user`, article_id) values (%s, %s)'
            cour.execute(sql, [session.get('username'), id])
            sql = 'update article set `share`=`share`+1 where id=%s'
            cour.execute(sql, [id])
        else:
            return jsonify({'result': 'error', 'code': 1017})
    else:
        return jsonify({'result': 'error', 'code': 1013})
    conn.commit()
    return jsonify({'result': 'success'})


# 评论获取
@app.route("/commentFetch", methods=["POST"])
@limiter.limit("3/second")
def commentFetch():
    id = request.form.get("id")
    start = int(request.form.get("start"))
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from `comment` where article_id=%s order by date desc limit %s, 5'
    cour.execute(sql, [id, start])
    result = cour.fetchall()
    return jsonify({'result': 'success', 'data': result})


# 一言
@app.route("/hitokoto")
def hitokoto():
    id = request.args.get("uuid")
    if (not id) or id == "undefined":
        text = requests.get(generalData['hitokoto_api'])
        logging.debug(text.text)
        try:
            text = text.json()
        except Exception as e:
            logging.critical("Hitokoto connection error: " + str(e))
            return render_template("alert.html", title="出错啦 o_o ....", alertTitle="发生错误",
                                   alertText="发生错误，无法获取一言。请稍后再试。| " + str(e), alertIcon="error",
                                   reload=True)
        if not text['from_who']:
            text['from_who'] = ""
        textFrom = "—— " + text['from_who'] + "「" + text['from'] + "」"
        textContent = text['hitokoto']
    else:
        text = requests.get("https://hitokoto.cn/?uuid=" + id).text
        soup = BeautifulSoup(text, 'html.parser')
        textFrom = soup.find('div', id='hitokoto_author').get_text()
        textContent = soup.find('div', id='hitokoto_text').get_text()
    return render_template("hitokoto.html", user=session.get("username"), text=textContent, who=textFrom,
                           buildHash=buildHash)


# 一言获取
@app.route("/getHitokoto", methods=["POST"])
@limiter.limit("1/second")
@limiter.limit("15/minute")
def getHitokoto():
    text = requests.get(generalData['hitokoto_api'])
    logging.debug(text.text)
    try:
        text = text.json()
    except:
        logging.error("Hitokoto connection error:" + str(e))
        return jsonify({'result': 'error', 'code': 1021})
    if not text['from_who']:
        text['from_who'] = ""
    textFrom = "—— " + text['from_who'] + "「" + text['from'] + "」"
    textContent = text['hitokoto']
    return jsonify({'result': 'success', 'data': {'from': textFrom, 'content': textContent}})


# 编辑文章
@app.route("/editArticle/<id>")
def editArticle(id):
    if not session.get("username") in superUser:
        abort(403)
    if not id.isdigit():
        return render_template("alert.html", title="编辑文章", alertTitle="发生错误", alertText="非法ID。",
                               alertIcon="error", href="/article")
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from article where id=%s limit 1'
    cour.execute(sql, [id])
    result = cour.fetchall()
    if len(result) == 0:
        return render_template("alert.html", title="编辑文章", alertTitle="发生错误", alertText="找不到该文章。",
                               alertIcon="error", href="/article")
    return render_template("articleConfig.html", user=session.get("username"), operate="编辑", opBtn="保存修改",
                           opEnglish="Edit Article",
                           title=result[0][0], desc=result[0][2], content=result[0][4].split("\n"), id=result[0][1],
                           date=result[0][3], banner=result[0][9], type="edit", success="保存",
                           successText="成功保存了您所做的修改。", buildHash=buildHash)


# 发布文章
@app.route("/publishArticle")
def publishArticle():
    if not session.get("username") in superUser:
        abort(403)
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from article order by id desc limit 1'
    cour.execute(sql)
    result = cour.fetchall()
    return render_template("articleConfig.html", user=session.get("username"), operate="发布", opBtn="发布文章",
                           opEnglish="Publish Article", id=result[0][1] + 1, content=[],
                           date=datetime.now().strftime('%Y-%m-%d'), type="add", success="发布",
                           successText="您的文章已成功发布。将在3秒后跳转至文章。", buildHash=buildHash)

# 更新文章
@limiter.limit("1/second")
@limiter.limit("20/minute")
@app.route("/updateArticle", methods=["POST"])
def updateArticle():
    if not session.get("username") in superUser:
        abort(403)
    id = request.form.get("id")
    title = request.form.get("title")
    desc = request.form.get("desc")
    content = request.form.get("content")
    type = request.form.get("type")
    banner = request.form.get("banner")
    if (not id) or (not title) or (not desc) or (not content):
        return jsonify({'result': 'error', 'code': 1005})
    if not id.isdigit():
        return jsonify({'result': 'error', 'code': 1014})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    if type == "edit":
        sql = 'update article set title=%s, `desc`=%s, content=%s, banner=%s where id=%s'
        cour.execute(sql, [title, desc, content, banner, id])
    else:
        sql = 'insert into article (title, id, `desc`, date, content, watch, `like`, `comment`, `share`, banner) values (%s, %s, %s, %s, %s, 0, 0, 0, 0, %s)'
        cour.execute(sql, [title, id, desc, datetime.now().strftime('%Y-%m-%d'), content, banner])
    conn.commit()
    return jsonify({'result': 'success'})


# @app.route("/logPage")
# def getLogPage():
#     if session.get("username") != "HShiDianLu":
#         abort(403)
#     logHTML = open("nginx-log.html", encoding="utf-8").read()
#     return logHTML
#
#
# @app.route("/log")
# def getLog():
#     if session.get("username") != "HShiDianLu":
#         abort(403)
#     return render_template("iframe.html", title="日志", iframeLink="/logPage", user=session.get("username"),
#                            buildHash=buildHash, nowHref="/log",
#                            pre='Powered By <a class="simple-link" href="https://goaccess.io/" target="_blank">GoAccess</a>. | ')


@app.route("/status", methods=["GET", "POST"])
def status():
    logging.debug(generalData['status_text'])
    if request.method == "GET":
        return render_template("status.html", status=generalData['status_text'], time=generalData['status_change'],
                               user=session.get("username"), buildHash=buildHash)
    return jsonify(
        {'result': 'success', 'data': {'status': generalData['status_text'], 'time': generalData['status_change']}})


@app.route("/changeStatus", methods=["POST"])
def changeStatus():
    key = request.args.get("key")
    status = request.args.get("status")
    if md5(key) != generalData['status_key'] or not status:
        return jsonify({'result': 'error', 'code': 1005})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    changeTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = 'update general set `value`=%s where `key`="status_text"'
    cour.execute(sql, [status])
    sql = 'update general set `value`=%s where `key`="status_change"'
    cour.execute(sql, [changeTime])
    conn.commit()
    generalData['status_text'] = status
    generalData['status_change'] = changeTime
    # logging.info("Status change: " + status + " - " + changeTime)
    return jsonify({'result': 'success'})


@app.route("/homework")
def homeworkLatest():
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from homeworkList order by modify desc limit 1'
    cour.execute(sql)
    latestUUID = cour.fetchall()[0][1]
    return redirect("/homework/" + latestUUID)


@app.route("/homework/<uuid>")
def homework(uuid):
    text = "false"
    try:
        text = requests.get(generalData['hitokoto_api'], timeout=1).text
        if not text:
            text = "false"
        logging.debug(text)
    except Exception as e:
        logging.error("Hitokoto connection error: " + str(e))
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from homeworkList where uuid=%s limit 1'
    cour.execute(sql, [uuid])
    hwInfo = cour.fetchall()
    if len(hwInfo) == 0:
        return render_template("alert.html", title="作业", alertTitle="发生错误", alertText="找不到该作业。",
                               alertIcon="error", href="/homework")
    sql = 'select * from homework where belong=%s'
    cour.execute(sql, [uuid])
    hwList = cour.fetchall()
    hwFinal = [[], [], [], [], [], [], [], [], []]
    hwLen = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in hwList:
        hwFinal[i[0]].append([len(hwFinal[i[0]]), i[1], i[2], i[3]])
    logging.debug(hwFinal)
    for i in range(9):
        hwLen[i] = len(hwFinal[i])
    return render_template("homework.html", text=text, allLen=len(hwList), hwList=hwFinal, title=hwInfo[0][0],
                           hwMap=eval(generalData['hw_map']), hwLen=hwLen, changeTime=hwInfo[0][3], eta=hwInfo[0][2],
                           uuid=hwInfo[0][1], user=session.get("username"), buildHash=buildHash)


@app.route("/oauth/github")
def oauthGithubRedirect():
    to = request.args.get("to")
    if not to:
        to = "/"
    # if session.get("username"):
    #     return render_template("alert.html", title="OAuth 登录", alertTitle="登录失败",
    #                            alertText="您已登录，请先退出当前帐号后再进行登录。", alertIcon="error")
    session['oauth_to'] = to
    state = str(uuid.uuid4()).replace("-", "")
    session['state'] = state
    return redirect(githubOAuthURL + state)


@app.route("/oauth/github/login", methods=["POST"])
def oauthGithubLogin():
    code = request.form.get("code")
    if not code:
        return jsonify({'result': 'error', 'code': 1005})
    access = requests.post("https://github.com/login/oauth/access_token",
                           json={"client_id": githubOAuthID, "client_secret": githubOAuthSecret, "code": code},
                           headers={"Accept": "application/json"}).json()
    logging.debug(access)
    try:
        scope = access['scope'].split(",")
    except:
        return jsonify({'result': 'error', 'code': 1015, 'data': "OAuth 验证失败。| " + access['error_description']})
    if not ("read:user" in scope and "user:email" in scope):
        return jsonify({'result': 'error', 'code': 1005})
    user = requests.get("https://api.github.com/user",
                        headers={"Authorization": "Bearer " + access['access_token']}).json()
    email = requests.get("https://api.github.com/user/emails",
                         headers={"Authorization": "Bearer " + access['access_token']}).json()[0]['email']
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    uid = "Github_" + str(user['id'])
    sql = 'select * from `user` where email=%s or uuid=%s'
    cour.execute(sql, [email, uid])
    existAccount = cour.fetchall()
    if len(existAccount) != 0:
        logging.info("Github login: " + str(existAccount))
        session['username'] = existAccount[0][0]
        return jsonify({'result': 'success'})
    sql = 'select * from `user` where username=%s'
    cour.execute(sql, [user['login']])
    validUsername = cour.fetchall()
    if len(validUsername) != 0:
        return jsonify({'result': 'error', 'code': 1020})
    logging.info("Github register: " + uid)
    sql = 'insert into `user` (username, uuid, `password`, email, locked) values (%s, %s, -1, %s, 0)'
    cour.execute(sql, [user['login'], uid, email])
    conn.commit()
    session['username'] = user['login']
    return jsonify({'result': 'success'})


@app.route("/oauth/github/callback")
def oauthGithubCallback():
    code = request.args.get("code")
    error = request.args.get("error")
    errorDesc = request.args.get("error_description")
    state = request.args.get("state")
    if not session.get("oauth_to"):
        session['oauth_to'] = "/"
    if session.get("state") != state:
        return render_template("alert.html", title="OAuth 登录", alertTitle="登录失败",
                               alertText="数据校验异常。", alertIcon="error", href=session.get("oauth_to"))
    # if session.get("username"):
    #     return render_template("alert.html", title="OAuth 登录", alertTitle="登录失败",
    #                            alertText="您已登录，请先退出当前帐号后再进行登录。", alertIcon="error")
    if not state:
        return render_template("alert.html", title="OAuth 登录", alertTitle="登录失败",
                               alertText="数据校验异常。", alertIcon="error", href=session.get("oauth_to"))
    if error == "access_denied":
        return redirect(session.get("oauth_to"))
    elif error:
        return render_template("alert.html", title="OAuth 登录", alertTitle="登录失败",
                               alertText="OAuth 授权失败。| " + errorDesc, alertIcon="error",
                               href=session.get("oauth_to"))
    return render_template("oauthLoadPage.html", code=code, to=session.get("oauth_to"))
    # access = requests.post("https://github.com/login/oauth/access_token",
    #                        json={"client_id": githubOAuthID, "client_secret": githubOAuthSecret, "code": code},
    #                        headers={"Accept": "application/json"}).json()
    # try:
    #     scope = access['scope'].split(",")
    # except:
    #     return render_template("alert.html", title="OAuth 登录", alertTitle="登录失败",
    #                            alertText="OAuth 验证失败。| " + access['error_description'], alertIcon="error")
    # if not ("read:user" in scope and "user:email" in scope):
    #     return render_template("alert.html", title="OAuth 登录", alertTitle="登录失败",
    #                            alertText="？？？你在干嘛？| OAuth 权限验证失败。", alertIcon="error")
    # user = requests.get("https://api.github.com/user",
    #                     headers={"Authorization": "Bearer " + access['access_token']}).json()
    # email = requests.get("https://api.github.com/user/emails",
    #                      headers={"Authorization": "Bearer " + access['access_token']}).json()[0]['email']
    # conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
    #                        charset=databaseCharset)
    # cour = conn.cursor()
    # uid = "Github_" + str(user['id'])
    # sql = 'select * from `user` where email=%s or uuid=%s'
    # cour.execute(sql, [email, uid])
    # existAccount = cour.fetchall()
    # if len(existAccount) != 0:
    #     # if existAccount[0][4] == 1:
    #     #     return render_template("alert.html", title="OAuth 登录", alertTitle="登录失败",
    #     #                            alertText="您的 Github 邮箱曾在本站注册过，且您尚未通过邮箱验证，请验证邮箱后重试。",
    #     #                            alertIcon="error")
    #     logging.info("Github login: " + str(existAccount))
    #     session['username'] = existAccount[0][0]
    #     return redirect(state)
    # sql = 'select * from `user` where username=%s'
    # cour.execute(sql, [user['login']])
    # validUsername = cour.fetchall()
    # if len(validUsername) != 0:
    #     return render_template("alert.html", title="OAuth 登录", alertTitle="登录失败",
    #                            alertText="抱歉，您的 Github 用户名与本站现有用户名重复，故无法登录。请尝试更换您的 Github 用户名或在本站进行注册。若同名账号与您的账号为同一人所属，请联系管理员合并。",
    #                            alertIcon="error")
    # logging.info("Github register: " + uid)
    # sql = 'insert into `user` (username, uuid, `password`, email, locked) values (%s, %s, -1, %s, 0)'
    # cour.execute(sql, [user['login'], uid, email])
    # conn.commit()
    # session['username'] = user['login']
    # return redirect(state)


# Handlers

@app.errorhandler(404)
def handler404(error):
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1404})
    return render_template("alert.html", title="出错啦 (っ °Д °;)っ", alertTitle="找不到网页",
                           alertText="你是怎么过来的？| " + str(error), alertIcon="error"), 404


# Maybe this is useless
@app.errorhandler(500)
def handler500(error):
    logging.critical(str(error))
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1500})
    return render_template("alert.html", title="出错啦 （；´д｀）ゞ", alertTitle="发生错误",
                           alertText="服务器发生内部错误。请将此问题上报网站管理员。| " + str(error),
                           alertIcon="error", reload=True), 500


@app.errorhandler(Exception)
def handlerException(error):
    logging.critical(error)
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1500})
    return render_template("alert.html", title="出错啦 （；´д｀）ゞ", alertTitle="发生错误",
                           alertText="服务器发生内部错误。请将此问题上报网站管理员。| " + str(error),
                           alertIcon="error", reload=True), 500


@app.errorhandler(429)
def handler429(error):
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1429})
    return render_template("alert.html", title="出错啦 o((>ω< ))o", alertTitle="流量限制",
                           alertText="访问页面过于频繁。你在干什么？！| " + str(error), alertIcon="error",
                           reload=True), 429


@app.errorhandler(405)
def handler405(error):
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1405})
    return render_template("alert.html", title="出错啦 (；′⌒`)", alertTitle="发生错误",
                           alertText="请求方式不正确。不要再瞎输啦……| " + str(error), alertIcon="error"), 405


@app.errorhandler(403)
def handler405(error):
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1403})
    return render_template("alert.html", title="出错啦 (○´･д･)ﾉ", alertTitle="权限不足",
                           alertText="请求被拒绝。您可能没有适当的权限访问此页面。| " + str(error),
                           alertIcon="error"), 403


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True, debug=True)
