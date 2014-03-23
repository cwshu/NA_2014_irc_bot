#!/usr/bin/env python3
import socket
import time
import re

import irc_commands as irc_cmd

# part2 calculator
def cal(exp):
    # print("cal recv:", exp)
    if re.findall(r"([0-9+\-*/.()\^]*)", exp)[0] != exp:
        # check no special characters
        return "special char"
    
    double_star_or_divide = re.findall(r"[*]{2}|[/]{2}", exp)
    if double_star_or_divide:
        return "double_star_or_divide"

    exp = exp.replace("^", "**")
    print(exp)
    try:
        val = eval(exp)
    except SyntaxError:
        return "syntax error"
    except ZeroDivisionError:
        return "overflow"
    else:
        return val

# part3 tinyurl
# part5 rup
# part6 log
def statistical(input_list, identity_func):
    # statistic times
    ret = dict()
    for item in input_list:
        item = identity_func(item)
        if ret.get(item):
            ret[item] += 1
        else:
            ret[item] = 1

    return ret

def log(mode, number):
    log_file = open("messages", "r")
    auth_error_list = []
    for line in log_file:
        idx = line.find("authentication error")
        if idx == -1:
            continue

        line = line[idx+len("authentication error"):]
        line_tuple = line.split()
        if len(line_tuple) == 4:
            (user, ip) = (line_tuple[1], line_tuple[3])
        elif len(line_tuple) == 6:
            (user, ip) = (line_tuple[3], line_tuple[5])
        else:
            continue
        auth_error_list.append((ip, user))

    auth_error_times = dict()
    if mode == "ip":
        auth_error_times = statistical(auth_error_list, lambda a: a[0])
    elif mode == "user":
        auth_error_times = statistical(auth_error_list, lambda a: a[1])

    auth_error_times = sorted(auth_error_times.items(), key=lambda a: a[1], reverse=True)
    return auth_error_times[:number]


class IrcBot():
    # an irc bot class
    def __init__(self):
        pass

    def connect(self, server_socket, username, realname):
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_socket.connect(server_socket)
        irc_cmd.send_command(self.irc_socket, "USER {} 1 unused {}\r\n".format(username, realname))
        irc_cmd.set_nick(self.irc_socket, username)

    def listen_and_response(self):
        msg = irc_cmd.recv_msg(self.irc_socket, 1)
        if not msg:
            return

        privmsg = irc_cmd.parsing_irc_privmsg(msg[0])
        if not privmsg:
            return
        (user, channel, dialog) = privmsg
        dialog = dialog.strip()
        # dialog only messages "@xxx xxx xxx" without endline
        print("\nprivmsg", privmsg)
        if dialog.startswith("@cal"):
            val = cal(dialog[len("@cal "):])

            if type(val) in (int, float, complex):
                msg = val
            elif val == "overflow":
                msg = "overflow"
            else:
                msg = "Usage: @cal <expression>"

            irc_cmd.send_msg_to(self.irc_socket, channel, "{}: {}".format(user, msg))
        elif dialog.startswith("@log"):
            parameters = dialog.split()

            try:
                number_idx = parameters.index("-n")
                number = int(parameters[number_idx+1])
            except:
                number = None

            try:
                parameters.index("-u")
                mode = "user"
            except:
                mode = "ip"
            
            num = number if number else 5
            auth_error_times = log(mode, num)
            for line in auth_error_times:
                print(line)
                ip = line[0] + (15 - len(line[0]))*" "
                times = line[1]
                irc_cmd.send_msg_to(self.irc_socket, channel, "{} {} times".format(ip, times))

        else:
            print(dialog, channel, user)
            self.keyword_match(dialog, channel, user)
            
    # part4 keyword
    def keyword_match(self, msg, channel, user):
        match = re.findall(r"(>[/]+<)", msg)
        for i in match:
            irc_cmd.send_msg_to(self.irc_socket, channel, i.replace("/", "\\"))

        match = re.findall(r"(>[\\]+<)", msg)
        for i in match:
            irc_cmd.send_msg_to(self.irc_socket, channel, i.replace("\\", "/"))
                    
        match = re.findall(r"惹$", msg)
        if match:
            irc_cmd.send_msg_to(self.irc_socket, channel, "{}: 你國文沒學好嗎？".format(user))
            
        match = re.findall(r"[ㄅㄎㄇㄉ]$", msg)
        if match:
            irc_cmd.send_msg_to(self.irc_socket, channel, "{}: 請重念小學吧！".format(user))

        match = re.findall(r"[Qq][Bb]", msg)
        if match:
            irc_cmd.send_msg_to(self.irc_socket, channel, "QB 必需死")

        match = re.findall(r"傲嬌", msg)
        if match:
            irc_cmd.send_msg_to(self.irc_socket, channel, "人... 人家才不是傲嬌呢 >////<")
            
#    def send_msg(self, msg):
#        self.irc_socket.sendall(msg.encode("UTF-8"))
#        print(msg.encode("UTF-8"))

if __name__ == "__main__":
    config_file = open("./config", "r")
    config = dict()
    for line in config_file:
        line = line.split("=")
        config[line[0]] = line[1].strip()[1:-1]
    # print(config)
    # input()

    bot1 = IrcBot()
    bot1.connect(("irc.freenode.net", 6667), "u0016002", "Hello")
    irc_cmd.join_channel(bot1.irc_socket, config["CHAN"][1:], config["CHAN_KEY"])
    irc_cmd.send_msg_to_channel(bot1.irc_socket, config["CHAN"][1:], "Hi I'm u0016002, I'm written in Python.")
    # irc_cmd.join_channel(bot1.irc_socket, "u0016002_test")
    # irc_cmd.send_msg_to_channel(bot1.irc_socket, "u0016002_test", "Hi I'm u0016002, I'm written in Python.")
    irc_cmd.send_msg_to_user(bot1.irc_socket, "susu", "test user function")

    while 1:
        bot1.listen_and_response()
