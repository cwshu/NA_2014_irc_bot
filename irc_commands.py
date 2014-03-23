#!/usr/bin/python3
import re
# irc_commands
def send_command(irc_socket, cmd):
    # send irc command from client socket to server
    # cmd should be 'str' type
    byte_msg = cmd.encode("UTF-8")
    irc_socket.sendall(byte_msg)
    print(byte_msg)

def recv_msg(irc_socket, times):
    messages = []
    for i in range(times):
        msg = irc_socket.recv(4096)
        if msg:
            print(msg.decode("UTF-8"), end="")
            messages.append(msg.decode("UTF-8"))
    return messages

def set_nick(irc_socket, nickname):
    # set your nick name
    send_command(irc_socket, "NICK {}\r\n".format(nickname))

def join_channel(irc_socket, channel, key=""):
    # join the channel
    send_command(irc_socket, "JOIN #{} {}\r\n".format(channel, key))

def leave_channel(irc_socket, channel):
    pass

def send_msg_to_channel(irc_socket, channel, msg):
    send_command(irc_socket, "PRIVMSG #{} :{}\r\n".format(channel, msg))

def send_msg_to_user(irc_socket, username, msg):
    send_command(irc_socket, "PRIVMSG {} :{}\r\n".format(username, msg))

send_msg_to = send_msg_to_user

def quit(irc_socket):
    # quit irc
    send_command(irc_socket, "QUIT\r\n")

# parsing recieve message
":susu!~cwshu@140.113.27.39 PRIVMSG #u0016002_test :@cal\r\n"
":susu!~cwshu@140.113.27.39 PRIVMSG u0016002 :hello"
def parsing_irc_privmsg(msg):
    user = re.match(r":(.+)!", msg)
    if user:
        user = user.group(0)[1:-1]

    idx = msg.find(" PRIVMSG ")
    if idx == -1:
        return

    usage_msg = msg[idx+len(" PRIVMSG "):]
    idx = usage_msg.find(" :")
    channel = usage_msg[:idx]
    dialog = usage_msg[idx+len(" :"):]
    return (user, channel, dialog)

if __name__ == "__main__":
    cal("1+2")
