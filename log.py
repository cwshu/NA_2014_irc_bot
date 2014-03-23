
"Feb 20 20:19:49 bsd5 sshd[24159]: error: PAM: authentication error for root from 162.221.12.179"
"Feb 13 12:12:03 bsd5 sshd[22168]: error: PAM: authentication error for chiachunt from 140.113.235.115"
"Feb  5 15:41:40 bsd5 sshd[64811]: error: PAM: authentication error for illegal user lei from 42.70.140.144"
def statistical(input_list, identity_func):
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
        
print(log("ip", 5))
print(log("ip", 1))
print(log("user", 1))
