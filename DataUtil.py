# -*- coding: utf-8 -*-
# @Time    : 2019/10/10 11:28
# @Author  : bjsasc
import os
import subprocess
import time
from urllib import parse, request
from DBClient import DBClient


def save_data(m: dict):
    """
    保存数据到数据库，
    """
    sql = "INSERT INTO `g_divcoverdata` (`type`, `name`, `suffix`, `sourcepath`, `checknum`, `status`, `dtime`)\
            VALUES ( {type}, {name}, {suffix}, {sourcepath},  {checknum}, {status}, {datetime}"\
        .format(m['type'], m[''], m['suffix'], m['sourcepath'], m['checknum'], m['status'],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    with DBClient() as db:
        db.execute(sql)


def update_data():
    """
    更新数据库文件，估计要传个id值过来，
    """
    sql = "select 1"
    with DBClient() as db:
        db.execute(sql)


def get_data():
    sql = "select * from g_divcoverdata"
    with DBClient() as db:
        db.execute(sql)
        return db.fetchall()


def parse_name(filepath: str):
    """
    根据文件路径，返回文件有效信息，
    :rtype: list，文件相关信息
    """
    filename = filepath.rsplit("/", 1)[1]
    name_info = filename.split("_")
    return name_info


def check_file(file_path):
    """
    用来检查文件
    :rtype: int
    """
    try:
        # print(filePath)
        f = open(file_path, 'r')
        result = list()
        for line in open(file_path):
            line = f.readline()
            # print(line)
            result.append(line)
            # print(result)
    except Exception as e:
        print("文件打开失败", file_path, e)
        return 1
    finally:
        f.close()
    return 0


def copy_file(from_path, to_path):
    """
     远程用scp复制文件，还未测试
    :param from_path:
    :param to_path:
    """
    user = "",
    ip = ""
    password = ""
    port = 22
    SCP_CMD_BASE = r"""
          expect -c "
          set timeout 300 ;
          spawn scp -P {port} -r {from_path} {username}@{host}:{to_path} ;
          expect *assword* {{{{ send {password}\r }}}} ;
          expect *\r ;
          expect \r ;
          expect eof
          "
        """.format(username=user, password=password, host=ip, remotedest=to_path, port=port)
    SCP_CMD = SCP_CMD_BASE.format(localsource=from_path)
    print("execute SCP_CMD: ", SCP_CMD)
    p = subprocess.Popen(SCP_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()
    os.system(SCP_CMD)


def notice(filename):
    """
        远程调用接口，暂时支持传入文件名称作为参数
    :param url:
    :param filename:
    """
    url = "http:/111.com"
    data = {'filename': filename}
    post_data = parse.urlencode(data).encode()
    rest = request.Request(url, data=post_data)
    resp = request.urlopen(rest)
