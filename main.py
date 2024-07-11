# Server Maintenance main.py By HShiDianLu.
# Copyright © 2024 HShiDianLu. All Rights Reserved.

import base64
import string
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

app = flask.Flask(__name__)
app.config[
    'SECRET_KEY'] = ("P<IJL_[/c@@Y#'*A&A{:6:Y7Ur])+,v}>l*kSAOOK3z9L_,U-Hh!SJhw<{"
                     "9lWW}Ad+nlNj@8F9;2h|flmott8%12g*1:a}Cp!;.X")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

serverIp = "hshidianlu.site"
hitokotoURL = "https://v1.hitokoto.cn/?c=d&c=i&max_length=15"

databaseHost = "156.238.234.128"
databaseUser = "hshidianlu"
databasePwd = "100722Ss"
database = "website"
databaseCharset = "utf8"

logging.basicConfig(level=logging.DEBUG)
logHandler = RotatingFileHandler("logs/log_" + datetime.now().strftime('%Y-%m-%d %H.%M.%S') + ".log")
formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(filename)s:%(lineno)d %(message)s')
logHandler.setFormatter(formatter)
logging.getLogger().addHandler(logHandler)
app.logger.addHandler(logHandler)

limiter = Limiter(app=app, default_limits=["100/minute", "10000/day"], key_func=get_remote_address,
                  storage_uri="redis://default:100722Ss@156.238.234.128:6379/0")

colaUid = "JtUTQG170763402537197LigDjg96"
colaAppKey = "65c86d6940b584094f62a8a8"
colaKey = requests.post("https://luckycola.com.cn/ai/getColaKey", data={"uid": colaUid, "appKey": colaAppKey}).json()[
    'data']
logging.debug(colaKey)
logging.info("Exp: " + colaKey['end_time_str'] + " " + str(colaKey['end_time']))
colaKey = colaKey['cola_key']
logging.info("ColaKey: " + colaKey)

logging.info("Fetching sensitives...")
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

logging.info("Fetching info...")
cour = conn.cursor()
sql = 'select * from general where `key`="homePageInfo"'
cour.execute(sql)
result = cour.fetchall()
homePageInfo = result[0][1]
logging.info("Fetched info...")

logging.info("Loading jieba model...")
jieba.lcut("预先初始化", cut_all=True)
logging.info("Loaded jieba model.")

serect = "a7748306f43170da2651:b23eb9a8c74e4be38e08da0666579010c0e477f3"
auth = str(base64.b64encode(serect.encode("utf-8")), "utf-8")

# Github的破逼服务器
logging.info("Fetching repo...")
try:
    repo = requests.get("https://api.github.com/users/HShiDianLu/repos", headers={"Authorization": "Basic " + auth},
                        timeout=5).json()
    logging.info("Fetched repo.")
    logging.debug(repo)
except Exception as e:
    logging.error(str(e))
    logging.info("Using default repo.")
    repo = [
        {'id': 701256006, 'node_id': 'R_kgDOKcxRRg', 'name': 'DouyinCatcher', 'full_name': 'HShiDianLu/DouyinCatcher',
         'private': False, 'owner': {'login': 'HShiDianLu', 'id': 110763230, 'node_id': 'U_kgDOBpoc3g',
                                     'avatar_url': 'https://avatars.githubusercontent.com/u/110763230?v=4',
                                     'gravatar_id': '', 'url': 'https://api.github.com/users/HShiDianLu',
                                     'html_url': 'https://github.com/HShiDianLu',
                                     'followers_url': 'https://api.github.com/users/HShiDianLu/followers',
                                     'following_url': 'https://api.github.com/users/HShiDianLu/following{/other_user}',
                                     'gists_url': 'https://api.github.com/users/HShiDianLu/gists{/gist_id}',
                                     'starred_url': 'https://api.github.com/users/HShiDianLu/starred{/owner}{/repo}',
                                     'subscriptions_url': 'https://api.github.com/users/HShiDianLu/subscriptions',
                                     'organizations_url': 'https://api.github.com/users/HShiDianLu/orgs',
                                     'repos_url': 'https://api.github.com/users/HShiDianLu/repos',
                                     'events_url': 'https://api.github.com/users/HShiDianLu/events{/privacy}',
                                     'received_events_url': 'https://api.github.com/users/HShiDianLu/received_events',
                                     'type': 'User', 'site_admin': False},
         'html_url': 'https://github.com/HShiDianLu/DouyinCatcher',
         'description': 'A  tool that can download videos/pictures on Douyin without watermarks to the local.',
         'fork': False, 'url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher',
         'forks_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/forks',
         'keys_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/keys{/key_id}',
         'collaborators_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/collaborators{/collaborator}',
         'teams_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/teams',
         'hooks_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/hooks',
         'issue_events_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/issues/events{/number}',
         'events_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/events',
         'assignees_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/assignees{/user}',
         'branches_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/branches{/branch}',
         'tags_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/tags',
         'blobs_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/git/blobs{/sha}',
         'git_tags_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/git/tags{/sha}',
         'git_refs_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/git/refs{/sha}',
         'trees_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/git/trees{/sha}',
         'statuses_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/statuses/{sha}',
         'languages_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/languages',
         'stargazers_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/stargazers',
         'contributors_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/contributors',
         'subscribers_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/subscribers',
         'subscription_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/subscription',
         'commits_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/commits{/sha}',
         'git_commits_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/git/commits{/sha}',
         'comments_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/comments{/number}',
         'issue_comment_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/issues/comments{/number}',
         'contents_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/contents/{+path}',
         'compare_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/compare/{base}...{head}',
         'merges_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/merges',
         'archive_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/{archive_format}{/ref}',
         'downloads_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/downloads',
         'issues_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/issues{/number}',
         'pulls_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/pulls{/number}',
         'milestones_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/milestones{/number}',
         'notifications_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/notifications{?since,all,participating}',
         'labels_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/labels{/name}',
         'releases_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/releases{/id}',
         'deployments_url': 'https://api.github.com/repos/HShiDianLu/DouyinCatcher/deployments',
         'created_at': '2023-10-06T09:00:44Z', 'updated_at': '2023-10-17T13:42:47Z',
         'pushed_at': '2024-01-11T11:21:59Z', 'git_url': 'git://github.com/HShiDianLu/DouyinCatcher.git',
         'ssh_url': 'git@github.com:HShiDianLu/DouyinCatcher.git',
         'clone_url': 'https://github.com/HShiDianLu/DouyinCatcher.git',
         'svn_url': 'https://github.com/HShiDianLu/DouyinCatcher', 'homepage': '', 'size': 98, 'stargazers_count': 2,
         'watchers_count': 2, 'language': 'Python', 'has_issues': True, 'has_projects': True, 'has_downloads': True,
         'has_wiki': False, 'has_pages': False, 'has_discussions': False, 'forks_count': 0, 'mirror_url': None,
         'archived': False, 'disabled': False, 'open_issues_count': 0,
         'license': {'key': 'mit', 'name': 'MIT License', 'spdx_id': 'MIT',
                     'url': 'https://api.github.com/licenses/mit', 'node_id': 'MDc6TGljZW5zZTEz'},
         'allow_forking': True, 'is_template': False, 'web_commit_signoff_required': False,
         'topics': ['application', 'fluent-ui', 'pyqt5-desktop-application', 'python', 'ui'], 'visibility': 'public',
         'forks': 0, 'open_issues': 0, 'watchers': 2, 'default_branch': 'main'},
        {'id': 724125209, 'node_id': 'R_kgDOKylGGQ', 'name': 'HShiDianLu', 'full_name': 'HShiDianLu/HShiDianLu',
         'private': False, 'owner': {'login': 'HShiDianLu', 'id': 110763230, 'node_id': 'U_kgDOBpoc3g',
                                     'avatar_url': 'https://avatars.githubusercontent.com/u/110763230?v=4',
                                     'gravatar_id': '', 'url': 'https://api.github.com/users/HShiDianLu',
                                     'html_url': 'https://github.com/HShiDianLu',
                                     'followers_url': 'https://api.github.com/users/HShiDianLu/followers',
                                     'following_url': 'https://api.github.com/users/HShiDianLu/following{/other_user}',
                                     'gists_url': 'https://api.github.com/users/HShiDianLu/gists{/gist_id}',
                                     'starred_url': 'https://api.github.com/users/HShiDianLu/starred{/owner}{/repo}',
                                     'subscriptions_url': 'https://api.github.com/users/HShiDianLu/subscriptions',
                                     'organizations_url': 'https://api.github.com/users/HShiDianLu/orgs',
                                     'repos_url': 'https://api.github.com/users/HShiDianLu/repos',
                                     'events_url': 'https://api.github.com/users/HShiDianLu/events{/privacy}',
                                     'received_events_url': 'https://api.github.com/users/HShiDianLu/received_events',
                                     'type': 'User', 'site_admin': False},
         'html_url': 'https://github.com/HShiDianLu/HShiDianLu', 'description': 'Readme.', 'fork': False,
         'url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu',
         'forks_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/forks',
         'keys_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/keys{/key_id}',
         'collaborators_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/collaborators{/collaborator}',
         'teams_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/teams',
         'hooks_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/hooks',
         'issue_events_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/issues/events{/number}',
         'events_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/events',
         'assignees_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/assignees{/user}',
         'branches_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/branches{/branch}',
         'tags_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/tags',
         'blobs_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/git/blobs{/sha}',
         'git_tags_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/git/tags{/sha}',
         'git_refs_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/git/refs{/sha}',
         'trees_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/git/trees{/sha}',
         'statuses_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/statuses/{sha}',
         'languages_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/languages',
         'stargazers_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/stargazers',
         'contributors_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/contributors',
         'subscribers_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/subscribers',
         'subscription_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/subscription',
         'commits_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/commits{/sha}',
         'git_commits_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/git/commits{/sha}',
         'comments_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/comments{/number}',
         'issue_comment_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/issues/comments{/number}',
         'contents_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/contents/{+path}',
         'compare_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/compare/{base}...{head}',
         'merges_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/merges',
         'archive_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/{archive_format}{/ref}',
         'downloads_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/downloads',
         'issues_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/issues{/number}',
         'pulls_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/pulls{/number}',
         'milestones_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/milestones{/number}',
         'notifications_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/notifications{?since,all,participating}',
         'labels_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/labels{/name}',
         'releases_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/releases{/id}',
         'deployments_url': 'https://api.github.com/repos/HShiDianLu/HShiDianLu/deployments',
         'created_at': '2023-11-27T12:57:55Z', 'updated_at': '2023-11-28T13:55:03Z',
         'pushed_at': '2024-01-11T12:10:20Z', 'git_url': 'git://github.com/HShiDianLu/HShiDianLu.git',
         'ssh_url': 'git@github.com:HShiDianLu/HShiDianLu.git',
         'clone_url': 'https://github.com/HShiDianLu/HShiDianLu.git',
         'svn_url': 'https://github.com/HShiDianLu/HShiDianLu', 'homepage': '', 'size': 15, 'stargazers_count': 1,
         'watchers_count': 1, 'language': None, 'has_issues': False, 'has_projects': False, 'has_downloads': True,
         'has_wiki': False, 'has_pages': False, 'has_discussions': False, 'forks_count': 0, 'mirror_url': None,
         'archived': False, 'disabled': False, 'open_issues_count': 0, 'license': None, 'allow_forking': True,
         'is_template': False, 'web_commit_signoff_required': False, 'topics': [], 'visibility': 'public', 'forks': 0,
         'open_issues': 0, 'watchers': 1, 'default_branch': 'main'},
        {'id': 719061265, 'node_id': 'R_kgDOKtwBEQ', 'name': 'LunarBypasser', 'full_name': 'HShiDianLu/LunarBypasser',
         'private': False, 'owner': {'login': 'HShiDianLu', 'id': 110763230, 'node_id': 'U_kgDOBpoc3g',
                                     'avatar_url': 'https://avatars.githubusercontent.com/u/110763230?v=4',
                                     'gravatar_id': '', 'url': 'https://api.github.com/users/HShiDianLu',
                                     'html_url': 'https://github.com/HShiDianLu',
                                     'followers_url': 'https://api.github.com/users/HShiDianLu/followers',
                                     'following_url': 'https://api.github.com/users/HShiDianLu/following{/other_user}',
                                     'gists_url': 'https://api.github.com/users/HShiDianLu/gists{/gist_id}',
                                     'starred_url': 'https://api.github.com/users/HShiDianLu/starred{/owner}{/repo}',
                                     'subscriptions_url': 'https://api.github.com/users/HShiDianLu/subscriptions',
                                     'organizations_url': 'https://api.github.com/users/HShiDianLu/orgs',
                                     'repos_url': 'https://api.github.com/users/HShiDianLu/repos',
                                     'events_url': 'https://api.github.com/users/HShiDianLu/events{/privacy}',
                                     'received_events_url': 'https://api.github.com/users/HShiDianLu/received_events',
                                     'type': 'User', 'site_admin': False},
         'html_url': 'https://github.com/HShiDianLu/LunarBypasser',
         'description': 'A program that can bypass Freelook, Auto Text Hot Key, and other mods disabled by Lunar Client, as well as game advertising.',
         'fork': False, 'url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser',
         'forks_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/forks',
         'keys_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/keys{/key_id}',
         'collaborators_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/collaborators{/collaborator}',
         'teams_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/teams',
         'hooks_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/hooks',
         'issue_events_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/issues/events{/number}',
         'events_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/events',
         'assignees_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/assignees{/user}',
         'branches_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/branches{/branch}',
         'tags_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/tags',
         'blobs_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/git/blobs{/sha}',
         'git_tags_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/git/tags{/sha}',
         'git_refs_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/git/refs{/sha}',
         'trees_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/git/trees{/sha}',
         'statuses_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/statuses/{sha}',
         'languages_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/languages',
         'stargazers_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/stargazers',
         'contributors_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/contributors',
         'subscribers_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/subscribers',
         'subscription_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/subscription',
         'commits_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/commits{/sha}',
         'git_commits_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/git/commits{/sha}',
         'comments_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/comments{/number}',
         'issue_comment_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/issues/comments{/number}',
         'contents_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/contents/{+path}',
         'compare_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/compare/{base}...{head}',
         'merges_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/merges',
         'archive_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/{archive_format}{/ref}',
         'downloads_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/downloads',
         'issues_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/issues{/number}',
         'pulls_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/pulls{/number}',
         'milestones_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/milestones{/number}',
         'notifications_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/notifications{?since,all,participating}',
         'labels_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/labels{/name}',
         'releases_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/releases{/id}',
         'deployments_url': 'https://api.github.com/repos/HShiDianLu/LunarBypasser/deployments',
         'created_at': '2023-11-15T11:17:09Z', 'updated_at': '2023-11-26T04:22:50Z',
         'pushed_at': '2024-01-11T11:23:39Z', 'git_url': 'git://github.com/HShiDianLu/LunarBypasser.git',
         'ssh_url': 'git@github.com:HShiDianLu/LunarBypasser.git',
         'clone_url': 'https://github.com/HShiDianLu/LunarBypasser.git',
         'svn_url': 'https://github.com/HShiDianLu/LunarBypasser', 'homepage': '', 'size': 35, 'stargazers_count': 4,
         'watchers_count': 4, 'language': 'Python', 'has_issues': True, 'has_projects': True, 'has_downloads': True,
         'has_wiki': True, 'has_pages': False, 'has_discussions': False, 'forks_count': 0, 'mirror_url': None,
         'archived': False, 'disabled': False, 'open_issues_count': 1,
         'license': {'key': 'mit', 'name': 'MIT License', 'spdx_id': 'MIT',
                     'url': 'https://api.github.com/licenses/mit', 'node_id': 'MDc6TGljZW5zZTEz'},
         'allow_forking': True, 'is_template': False, 'web_commit_signoff_required': False,
         'topics': ['bypass', 'lunar-client', 'minecraft', 'python'], 'visibility': 'public', 'forks': 0,
         'open_issues': 1, 'watchers': 4, 'default_branch': 'main'},
        {'id': 741910888, 'node_id': 'R_kgDOLDipaA', 'name': 'Text2Block', 'full_name': 'HShiDianLu/Text2Block',
         'private': False, 'owner': {'login': 'HShiDianLu', 'id': 110763230, 'node_id': 'U_kgDOBpoc3g',
                                     'avatar_url': 'https://avatars.githubusercontent.com/u/110763230?v=4',
                                     'gravatar_id': '', 'url': 'https://api.github.com/users/HShiDianLu',
                                     'html_url': 'https://github.com/HShiDianLu',
                                     'followers_url': 'https://api.github.com/users/HShiDianLu/followers',
                                     'following_url': 'https://api.github.com/users/HShiDianLu/following{/other_user}',
                                     'gists_url': 'https://api.github.com/users/HShiDianLu/gists{/gist_id}',
                                     'starred_url': 'https://api.github.com/users/HShiDianLu/starred{/owner}{/repo}',
                                     'subscriptions_url': 'https://api.github.com/users/HShiDianLu/subscriptions',
                                     'organizations_url': 'https://api.github.com/users/HShiDianLu/orgs',
                                     'repos_url': 'https://api.github.com/users/HShiDianLu/repos',
                                     'events_url': 'https://api.github.com/users/HShiDianLu/events{/privacy}',
                                     'received_events_url': 'https://api.github.com/users/HShiDianLu/received_events',
                                     'type': 'User', 'site_admin': False},
         'html_url': 'https://github.com/HShiDianLu/Text2Block',
         'description': 'A tool for generating text images into buildings in Minecraft.', 'fork': False,
         'url': 'https://api.github.com/repos/HShiDianLu/Text2Block',
         'forks_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/forks',
         'keys_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/keys{/key_id}',
         'collaborators_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/collaborators{/collaborator}',
         'teams_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/teams',
         'hooks_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/hooks',
         'issue_events_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/issues/events{/number}',
         'events_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/events',
         'assignees_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/assignees{/user}',
         'branches_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/branches{/branch}',
         'tags_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/tags',
         'blobs_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/git/blobs{/sha}',
         'git_tags_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/git/tags{/sha}',
         'git_refs_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/git/refs{/sha}',
         'trees_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/git/trees{/sha}',
         'statuses_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/statuses/{sha}',
         'languages_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/languages',
         'stargazers_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/stargazers',
         'contributors_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/contributors',
         'subscribers_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/subscribers',
         'subscription_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/subscription',
         'commits_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/commits{/sha}',
         'git_commits_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/git/commits{/sha}',
         'comments_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/comments{/number}',
         'issue_comment_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/issues/comments{/number}',
         'contents_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/contents/{+path}',
         'compare_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/compare/{base}...{head}',
         'merges_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/merges',
         'archive_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/{archive_format}{/ref}',
         'downloads_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/downloads',
         'issues_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/issues{/number}',
         'pulls_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/pulls{/number}',
         'milestones_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/milestones{/number}',
         'notifications_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/notifications{?since,all,participating}',
         'labels_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/labels{/name}',
         'releases_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/releases{/id}',
         'deployments_url': 'https://api.github.com/repos/HShiDianLu/Text2Block/deployments',
         'created_at': '2024-01-11T11:15:23Z', 'updated_at': '2024-01-11T11:18:10Z',
         'pushed_at': '2024-01-11T23:43:18Z', 'git_url': 'git://github.com/HShiDianLu/Text2Block.git',
         'ssh_url': 'git@github.com:HShiDianLu/Text2Block.git',
         'clone_url': 'https://github.com/HShiDianLu/Text2Block.git',
         'svn_url': 'https://github.com/HShiDianLu/Text2Block', 'homepage': '', 'size': 6, 'stargazers_count': 1,
         'watchers_count': 1, 'language': 'Python', 'has_issues': True, 'has_projects': True, 'has_downloads': True,
         'has_wiki': True, 'has_pages': False, 'has_discussions': False, 'forks_count': 0, 'mirror_url': None,
         'archived': False, 'disabled': False, 'open_issues_count': 1,
         'license': {'key': 'mit', 'name': 'MIT License', 'spdx_id': 'MIT',
                     'url': 'https://api.github.com/licenses/mit', 'node_id': 'MDc6TGljZW5zZTEz'},
         'allow_forking': True, 'is_template': False, 'web_commit_signoff_required': False,
         'topics': ['image', 'minecraft', 'python', 'text', 'tool'], 'visibility': 'public', 'forks': 0,
         'open_issues': 1, 'watchers': 1, 'default_branch': 'main'}]


# Build Hash

def GetHashofDirs(directory, blacklist):
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
        logging.debug("Hashing path " + path)
        for i in fileList:
            logging.debug("Hashing file " + i)
            filename = os.path.join(path, i)
            try:
                f1 = open(filename, 'rb')
            except:
                logging.warning("Hashing Failed " + i + ". Skip.")
                continue
            while 1:
                buf = f1.read(4096)
                if not buf:
                    break
                SHAhash.update(hashlib.md5(buf).hexdigest().encode())
    return SHAhash.hexdigest()[0:7]


logging.info("Hashing Build...")
buildHash = GetHashofDirs("./", ["/others", "/logs", "/.idea", "/.github", "/WebsiteEnv", "/__pycache__"])
logging.info("Build Hash: " + buildHash)

logging.info("Generating GoAccess HTML...")
goaccess = os.popen(
    "sudo goaccess -a -d -m -f /var/log/nginx/access.log -o /home/hshidianlu/Website/nginx-log.html").read()
logging.info("Generated.")


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
        text = requests.get(hitokotoURL, timeout=1).text
        if not text:
            text = "false"
        logging.debug(text)
    except Exception as e:
        logging.error(str(e))
    descLens = []
    for i in result:
        descLens.append(len(i[2]))
    return render_template("index.html", articles=result, user=session.get('username'), repo=repo,
                           repoLen=len(repo), text=text, buildHash=buildHash, descLens=descLens,
                           articlesLen=len(result), info=homePageInfo)


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
@app.route("/article/<id>")
def articlePage(id):
    if not id.isdigit():
        return render_template("alert.html", title="文章", alertTitle="发生错误", alertText="非法ID。",
                               alertIcon="error")
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from article where id=%s'
    cour.execute(sql, [id])
    result = cour.fetchall()
    if len(result) == 0:
        return render_template("alert.html", title="文章", alertTitle="发生错误", alertText="找不到该文章。",
                               alertIcon="error")
    cour.execute(sql, [str(int(id) - 1)])
    prev = cour.fetchall()
    logging.debug("Prev: " + str(prev))
    cour.execute(sql, [str(int(id) + 1)])
    next = cour.fetchall()
    prevSplit = False
    if prev and len(prev[0][0]) > 12:
        prevSplit = True
    nextSplit = False
    if next and len(next[0][0]) > 12:
        nextSplit = True
    logging.debug("Next: " + str(next))
    sql = 'select * from `comment` where article_id=%s order by date desc limit 10'
    cour.execute(sql, [id])
    comment = cour.fetchall()
    if session.get('username'):
        sql = 'select * from `like` where `user`=%s and article_id=%s'
        cour.execute(sql, [session.get('username'), id])
        like = cour.fetchall()
    else:
        like = []
    sql = 'update article set watch=watch+1 where id=%s'
    cour.execute(sql, [id])
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
    if (not username) or (not pwd):
        return jsonify({'result': 'error', 'code': 1005})
    data = {
        "secret": "6LfgeG8pAAAAAD3v1-KecnL_vNPmWmWGNue-GtUA",
        "response": token,
        "remoteip": request.remote_addr
    }
    try:
        verifyResult = requests.post("https://recaptcha.net/recaptcha/api/siteverify", data=data, timeout=5).json()
    except Exception as e:
        logging.error(e)
        return jsonify({'result': 'error', 'code': 1001})
    logging.debug(verifyResult)
    if verifyResult['score'] <= 0.5:
        return jsonify({'result': 'error', 'code': 1018})
    if verifyResult['action'] != 'login':
        return jsonify({'result': 'error', 'code': 1019})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from `user` where username=%s or email=%s'
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
    # 小可爱服务器用不了smtp接口
    # message = MIMEText(content, "html", "utf-8")
    # message["From"] = mailSender
    # message["To"] = ",".join(receiver)
    # message["Subject"] = title
    # try:
    #     context = ssl.create_default_context()
    #     context.set_ciphers('DEFAULT')
    #     print("Connecting")
    #     smtpObj = smtplib.SMTP_SSL(mailHost, mailPort, context=context, timeout=5)
    #     print("Login")
    #     smtpObj.login(mailUser, mailPwd)
    #     print("Sending")
    #     smtpObj.sendmail(mailUser, receiver, message.as_string())
    #     return "ok"
    # except Exception as e:
    #     return e
    emailData = {
        "ColaKey": colaKey,
        "tomail": receiver,
        "fromTitle": "HShiDianLu's Website",
        "subject": title,
        "smtpCode": "REWTURECTFYRIBXP",
        "smtpEmail": "hshidianlu@163.com",
        "smtpCodeType": "163",
        "content": content
    }
    logging.debug(emailData)
    email = requests.post("https://luckycola.com.cn/tools/customMail",
                          data=emailData).json()
    logging.debug(email)
    logging.info("Email sent.")
    return email['code']


# Token生成
def create_string_number(n):
    m = random.randint(1, n)
    a = "".join([str(random.randint(0, 9)) for _ in range(m)])
    b = "".join([random.choice(string.ascii_letters) for _ in range(n - m)])
    return ''.join(random.sample(list(a + b), n))


# 注册
@app.route("/register", methods=["POST"])
@limiter.limit("10/minute")
def register():
    email = request.form.get("email")
    username = request.form.get("username")
    pwd = request.form.get("password")
    token = request.form.get("token")
    if (not username) or (not pwd) or (not email):
        return jsonify({'result': 'error', 'code': 1005})
    if re.match("^(?![^a-zA-Z]+$)(?!\D+$)", pwd) == None:
        return jsonify({'result': 'error', 'code': 1005})
    if re.match("^[a-zA-Z0-9_]+$", username) == None:
        return jsonify({'result': 'error', 'code': 1005})
    if re.match("^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$", email) == None:
        return jsonify({'result': 'error', 'code': 1005})
    data = {
        "secret": "6LfgeG8pAAAAAD3v1-KecnL_vNPmWmWGNue-GtUA",
        "response": token,
        "remoteip": request.remote_addr
    }
    try:
        verifyResult = requests.post("https://recaptcha.net/recaptcha/api/siteverify", data=data, timeout=5).json()
    except Exception as e:
        return jsonify({'result': 'error', 'code': 1001})
    logging.debug(verifyResult)
    if verifyResult['score'] <= 0.5:
        return jsonify({'result': 'error', 'code': 1018})
    if verifyResult['action'] != 'register':
        return jsonify({'result': 'error', 'code': 1019})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from `user` where username=%s'
    cour.execute(sql, [username])
    validUsername = cour.fetchall()
    sql = 'select * from `user` where email=%s'
    cour.execute(sql, [email])
    validEmail = cour.fetchall()
    if len(validEmail) != 0:
        return jsonify({'result': 'error', 'code': 1007})
    if len(validUsername) != 0:
        return jsonify({'result': 'error', 'code': 1006})
    if sensitiveCheck(username, True):
        return jsonify({'result': 'error', 'code': 1003})
    token = create_string_number(50)
    email_content = (
            "<h1>HShiDianLu's Website</h1><p>感谢您注册账户，请点击下方链接验证邮箱。</p><a href='https://" + serverIp + "/verify?token=" + token + "'>https://" + serverIp + "/verify?token=" + token + "</a>")
    email_title = "注册账号 | 验证您的电子邮件"
    respond = sendMail(email, email_content, email_title)
    if respond == 0:
        md5Pwd = md5(pwd)
        createUUID = str(uuid.uuid4()).replace("-", "")
        sql = 'insert into `user` (username, uuid, `password`, email,  locked) values (%s, %s, %s, %s, 1)'
        cour.execute(sql, [username, createUUID, md5Pwd, email])
        sql = 'insert into verify (verifyUUID, token, expire) values (%s, %s, %s)'
        cour.execute(sql, [createUUID, token, round(time.time()) + 1200])
        conn.commit()
        logging.info(username + " registered.")
        return jsonify({'result': 'success'})
    return jsonify({'result': 'error', 'code': '1008' + str(respond)})


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
                               alertText="缺少参数：Token。", alertIcon="error")
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from verify where token=%s'
    cour.execute(sql, [token])
    result = cour.fetchall()
    if len(result) == 0:
        return render_template("alert.html", title="邮箱验证", alertTitle="验证失败",
                               alertText="Token不正确或已失效。", alertIcon="error")
    sql = 'select * from `user` where uuid=%s'
    cour.execute(sql, [result[0][0]])
    userResult = cour.fetchall()
    if userResult[0][4] == 0:
        return render_template("alert.html", title="邮箱验证", alertTitle="验证失败",
                               alertText="您已通过验证，无需重复验证。", alertIcon="error")
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
                           alertText="您已通过验证，请返回主页重新登录。您现在可以关闭此页面了。", alertIcon="success")


# 重发邮件
@app.route("/emailResent", methods=["POST"])
@limiter.limit("5/minute")
def resent():
    token = request.form.get("token")
    if not token:
        return jsonify({'result': 'error', 'code': 1010})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from verify where token=%s'
    cour.execute(sql, [token])
    result = cour.fetchall()
    if len(result) == 0:
        return jsonify({'result': 'error', 'code': 1011})
    sql = 'select * from `user` where uuid=%s'
    cour.execute(sql, [result[0][0]])
    userResult = cour.fetchall()
    if userResult[0][4] == 0:
        return jsonify({'result': 'error', 'code': 1012})
    newToken = create_string_number(50)
    email_content = (
            "<h1>HShiDianLu's Website</h1><p>感谢您注册账户，请点击下方链接验证邮箱。</p><a href='https://" + serverIp + "/verify?token=" + newToken + "'>https://" + serverIp + "/verify?token=" + newToken + "</a>")
    email_title = "注册账号 | 验证您的电子邮件"
    respond = sendMail(userResult[0][3], email_content, email_title)
    if respond == 0:
        sql = 'delete from verify where token=%s'
        cour.execute(sql, [token])
        sql = 'insert into verify (verifyUUID, token, expire) values (%s, %s, %s)'
        cour.execute(sql, [result[0][0], newToken, round(time.time()) + 1200])
        conn.commit()
        return jsonify({'result': 'success'})
    return jsonify({'result': 'error', 'code': '1008-' + str(respond)})


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
        sql = 'select * from `like` where `user`=%s and article_id=%s'
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
        sql = 'update article set `comment`=`comment`+1 where id=%s'
        cour.execute(sql, [id])
        sql = 'insert into `comment` (`user`, id, article_id, date, `comment`, `like`) values (%s, %s, %s, %s, %s, 0)'
        cour.execute(sql, [session.get('username'), str(uuid.uuid4()).replace("-", ""), id,
                           datetime.now().strftime('%Y-%m-%d %H:%M:%S'), comment])
    elif type == "share":
        sql = 'select * from `share` where `user`=%s and article_id=%s'
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


# 刷新缓存
@app.route("/refresh")
@limiter.limit("5/hour")
def refresh():
    if session.get("username") != "HShiDianLu":
        abort(403)
    global repo
    global sensitiveWords
    global colaKey
    logging.info("Refreshing data...")
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from sensitiveWord'
    cour.execute(sql)
    result = cour.fetchall()
    sensitiveWords = []
    for i in result:
        sensitiveWords.append(i[1])
    colaKey = \
        requests.post("https://luckycola.com.cn/ai/getColaKey", data={"uid": colaUid, "appKey": colaAppKey}).json()[
            'data']
    logging.debug(colaKey)
    logging.info("Exp: " + colaKey['end_time_str'] + " " + str(colaKey['end_time']))
    colaKey = colaKey['cola_key']
    logging.info("ColaKey: " + colaKey)
    repo = requests.get("https://api.github.com/users/HShiDianLu/repos",
                        headers={"Authorization": "Basic " + auth}).json()
    logging.debug(repo)
    buildHash = GetHashofDirs("./", ["/others", "/logs", "/.idea", "/.github"])
    logging.info("Build Hash: " + buildHash)
    logging.warning("Refreshed data.")
    return jsonify({'result': 'success'})


# 一言
@app.route("/hitokoto")
def hitokoto():
    id = request.args.get("uuid")
    if (not id) or id == "undefined":
        text = requests.get(hitokotoURL)
        logging.debug(text.text)
        try:
            text = text.json()
        except:
            return render_template("alert.html", title="出错啦 o_o ....", alertTitle="发生错误",
                                   alertText="发生错误，无法获取一言。请稍后再试。", alertIcon="error")
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
    text = requests.get(hitokotoURL)
    logging.debug(text.text)
    try:
        text = text.json()
    except:
        return jsonify({'result': 'error', 'code': 1021})
    if not text['from_who']:
        text['from_who'] = ""
    textFrom = "—— " + text['from_who'] + "「" + text['from'] + "」"
    textContent = text['hitokoto']
    return jsonify({'result': 'success', 'data': {'from': textFrom, 'content': textContent}})


# 编辑文章
@app.route("/editArticle/<id>")
def editArticle(id):
    if session.get("username") != "HShiDianLu":
        abort(403)
    if not id.isdigit():
        return render_template("alert.html", title="编辑文章", alertTitle="发生错误", alertText="非法ID。",
                               alertIcon="error")
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from article where id=%s'
    cour.execute(sql, [id])
    result = cour.fetchall()
    if len(result) == 0:
        return render_template("alert.html", title="编辑文章", alertTitle="发生错误", alertText="找不到该文章。",
                               alertIcon="error")
    return render_template("articleConfig.html", user=session.get("username"), operate="编辑", opBtn="保存修改",
                           opEnglish="Edit Article",
                           title=result[0][0], desc=result[0][2], content=result[0][4].split("\n"), id=result[0][1],
                           date=result[0][3], type="edit", success="保存", successText="成功保存了您所做的修改。",
                           buildHash=buildHash)


# 发布文章
@app.route("/publishArticle")
def publishArticle():
    if session.get("username") != "HShiDianLu":
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


# Vditor Files
@app.route("/static/js/vditor/dist/js/<anything>/<filename>")
def returnVditorFile(anything, filename):
    return send_file("static/js/vditor-" + filename)


# 更新文章
@limiter.limit("1/second")
@limiter.limit("20/minute")
@app.route("/updateArticle", methods=["POST"])
def updateArticle():
    if session.get("username") != "HShiDianLu":
        abort(403)
    id = request.form.get("id")
    title = request.form.get("title")
    desc = request.form.get("desc")
    content = request.form.get("content")
    type = request.form.get("type")
    if (not id) or (not title) or (not desc) or (not content):
        return jsonify({'result': 'error', 'code': 1005})
    if not id.isdigit():
        return jsonify({'result': 'error', 'code': 1014})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    if type == "edit":
        sql = 'update article set title=%s, `desc`=%s, content=%s where id=' + id
        cour.execute(sql, [title, desc, content])
    else:
        sql = 'insert into article (title, id, `desc`, date, content, watch, `like`, `comment`, `share`) values (%s, %s, %s, %s, %s, 0, 0, 0, 0)'
        cour.execute(sql, [title, id, desc, datetime.now().strftime('%Y-%m-%d'), content])
    conn.commit()
    return jsonify({'result': 'success'})


@app.route("/logPage")
def getLogPage():
    if session.get("username") != "HShiDianLu":
        abort(403)
    logHTML = open("nginx-log.html", encoding="utf-8").read()
    return logHTML


@app.route("/log")
def getLog():
    if session.get("username") != "HShiDianLu":
        abort(403)
    return render_template("iframe.html", title="日志", iframeLink="/logPage", user=session.get("username"),
                           buildHash=buildHash, nowHref="/log",
                           pre='Powered By <a class="simple-link" href="https://goaccess.io/" target="_blank">GoAccess</a>. | ')


@app.route("/status", methods=["GET", "POST"])
def status():
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'select * from general where `key`="status"'
    cour.execute(sql)
    status = cour.fetchall()
    sql = 'select * from general where `key`="statusChangeTime"'
    cour.execute(sql)
    statusChangeTime = cour.fetchall()
    if request.method == "GET":
        return render_template("status.html", status=status[0][1], time=statusChangeTime[0][1],
                               user=session.get("username"),
                               buildHash=buildHash)
    return jsonify({'result': 'success', 'data': {'status': status[0][1], 'time': statusChangeTime[0][1]}})


@app.route("/changeStatus", methods=["POST"])
def changeStatus():
    key = request.args.get("key")
    status = request.args.get("status")
    print(key, status)
    if key != "3Pn_TlXID0mG9M7Dbq[=" or not status:
        return jsonify({'result': 'error', 'code': 1005})
    conn = pymysql.connect(host=databaseHost, user=databaseUser, password=databasePwd, database=database,
                           charset=databaseCharset)
    cour = conn.cursor()
    sql = 'update general set `value`=%s where `key`="status"'
    cour.execute(sql, [status])
    sql = 'update general set `value`=%s where `key`="statusChangeTime"'
    cour.execute(sql, [datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    conn.commit()
    return jsonify({'result': 'success'})


# Handlers

@app.errorhandler(404)
def handler404(error):
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1404})
    return render_template("alert.html", title="出错啦 (っ °Д °;)っ", alertTitle="找不到网页",
                           alertText="你是怎么过来的？| " + str(error), alertIcon="error")


# Maybe this is useless
@app.errorhandler(500)
def handler500(error):
    logging.error(str(error))
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1500})
    return render_template("alert.html", title="出错啦 （；´д｀）ゞ", alertTitle="发生错误",
                           alertText="服务器发生内部错误。请将此问题上报网站管理员。| " + str(error), alertIcon="error")


@app.errorhandler(Exception)
def handlerException(error):
    logging.error(error)
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1500})
    return render_template("alert.html", title="出错啦 （；´д｀）ゞ", alertTitle="发生错误",
                           alertText="服务器发生内部错误。请将此问题上报网站管理员。| " + str(error), alertIcon="error")


@app.errorhandler(429)
def handler429(error):
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1429})
    return render_template("alert.html", title="出错啦 o((>ω< ))o", alertTitle="发生错误",
                           alertText="访问页面过于频繁。你在干什么？！| " + str(error), alertIcon="error")


@app.errorhandler(405)
def handler405(error):
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1405})
    return render_template("alert.html", title="出错啦 (；′⌒`)", alertTitle="发生错误",
                           alertText="请求方式不正确。不要再瞎输啦……| " + str(error), alertIcon="error")


@app.errorhandler(403)
def handler405(error):
    if request.method == "POST":
        return jsonify({'result': 'error', 'code': 1403})
    return render_template("alert.html", title="出错啦 (○´･д･)ﾉ", alertTitle="发生错误",
                           alertText="请求被拒绝。您可能没有适当的权限访问此页面。| " + str(error), alertIcon="error")


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True, debug=True)
