# coding=utf-8
# import matplotlib.pylab as plt
import os
import threading

from core import log_handler
from core.Automator import *

# TODO 改LOG
log = log_handler.LOG()  # 初始化日志文件


# 测试程序

def runmain(address, account, password):
    # 主功能体函数
    # 请在本函数中自定义需要的功能

    a = Automator(address, account)
    a.start()

    # #opencv识别可视化无法在多线程中使用
    # plt.ion()
    # fig, ax = plt.subplots(1)
    # plt.show()

    print('>>>>>>>即将登陆的账号为：', account, '密码：', password, '<<<<<<<')
    a.login_auth(account, password)  # 注意！请把账号密码写在zhanghao2.txt内
    log.Account_Login(account)
    a.init_home()  # 初始化，确保进入首页

    # a.tansuo()  # 探索
    # a.dixiachengDuanya()  # 地下城，请把队伍列表里1队设置为打boss队，2队设置为aoe队
    # a.shouqurenwu()  # 收取任务
    # a.shouqu()  # 收取所有礼物

    # print(a.baidu_ocr(394,502,442,666))
    a.change_acc()  # 退出当前账号，切换下一个
    log.Account_Logout(account)


def connect():  # 连接adb与uiautomator
    try:
        os.system('cd adb & adb connect 127.0.0.1:5554')  # 雷电模拟器
        # os.system('adb connect 127.0.0.1:7555') #mumu模拟器
        os.system('python -m uiautomator2 init')
    except:
        print('连接失败')

    result = os.popen('cd adb & adb devices')  # 返回adb devices列表
    res = result.read()
    lines = res.splitlines()[1:]

    for i in range(len(lines)):
        lines[i] = lines[i].split('\t')[0]
    lines = lines[:-1]
    print(lines)
    emulatornum = len(lines)
    return (lines, emulatornum)


def read():  # 读取账号
    account_dic = {}
    with open('../zhanghao2.txt', 'r') as f:  # 注意！请把账号密码写在zhanghao2.txt内,不是zhanghao.txt!!!!!
        for line in f:
            account, password = line.split('\t')[:2]
            account_dic[account] = password.strip()
    account_list = list(account_dic.keys())
    accountnum = len(account_list)
    return (account_list, account_dic, accountnum)


# 主程序
if __name__ == '__main__':

    # 连接adb与uiautomator
    lines, emulatornum = connect()
    # 读取账号
    account_list, account_dic, accountnum = read()

    # 多线程执行
    count = 0  # 完成账号数
    thread_list = []
    # 完整循环 join()方法确保完成后再进行下一次循环
    for i in range(int(accountnum / emulatornum)):  # 完整循环 join()方法确保完成后再进行下一次循环
        for j in range(emulatornum):
            t = threading.Thread(target=runmain, args=(
                lines[j], account_list[i * emulatornum + j], account_dic[account_list[i * emulatornum + j]]))
            thread_list.append(t)
            count += 1
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        thread_list = []
    # 剩余账号
    i = 0
    while count != accountnum:
        t = threading.Thread(target=runmain,
                             args=(lines[i], account_list[count], account_dic[account_list[count]]))
        thread_list.append(t)
        i += 1
        count += 1
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

    # 退出adb
    os.system('cd adb & adb kill-server')
