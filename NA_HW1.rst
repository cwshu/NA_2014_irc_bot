***************
NA HW1: IRC bot
***************

Ref: https://tools.ietf.org/html/rfc2812

requirement
===========

- Use Python 3+ or Perl 5.14+.
- You should upload a .tar.gz file, which structure is::

    <your_student_id>
    |- main
    |- config
    |- <other files/directories if you need>

- TAs will execute your program by: ``./main``
    - You need make sure your program is executable.
    - TA will check your shebang is python or perl, you cannot use other lang.
    
- ``config`` should contain the following setting and your bot should
  automatically connect to CHAN with CHAN_KEY::

    CHAN='#channal_name'
    CHAN_KEY='channal_key'
    
- You should make sure your program is portable on bsd[1-6].cs.nctu.edu.tw
  and linux[1-6].cs.nctu.edu.tw. Your program will be executed on one of them.

- Feel free to use PyPI/CPAN. If the packages you use are not installed
  on CS workstations, please mail TAs before the due day.

- Due day: 3/24 (Mon)


overview
========

0. basic (10%)
1. @weather (10%)
2. @cal (20%)
3. tinyurl (10%)
4. keyword matching (10%)
5. @rup (20%)
6. @log (20%)


0. basic (10%)
==============

- connect to specify channel (5%)
    - helo message: ``Hi, I'm {id}, I'm written in (Perl|Python).``
- change nick name to 'u' + student_id (5%)


1. @weather (10%)
=================

Get data from http://www.cwb.gov.tw/pda/observe/real/46757.htm

Example::

    me > @weather
    bot> 天氣現象: X    溫度: 13.8 ℃


2. @cal <expression> (20%)
==========================

- correctness (10%)
- syntax check (10%)
- allowed character: ``[0-9+\-*/.()]``
- allowed operator: ``+``, ``-``, ``*``, ``/``, ``^``
  
Example::

    me > @cal 1+2*3
    bot> me: 7

    me > @cal (1+2) * (3+4) /2
    bot> me: 10.5

    me > @cal 0^0
    bot> me: 1

    me > @cal
    bot> me: Usage: @cal <expression>

    me > @cal haha
    bot> me: Usage: @cal <expression>

    me > @cal 1 +
    bot> me: Usage: @cal <expression>


3. tinyurl (10%)
================

If the message contains URL, you should make a short URL for him.

`URL format and allowed characters
<http://en.wikipedia.org/wiki/Uniform_resource_locator>`_

http://tinyurl.com/

Example::

    me > http://www.google.com
    bot> me: http://tinyurl.com/1c2

    me > 這個太有趣了http://imgur.com/jfKKV8r哈哈
    bot> me: http://tinyurl.com/mbtaovt


4. keyword matching (10%)
=========================

- >///< (2%)
- 惹$ (2%)
- [ㄅㄎㄇㄉ]$ (2%)
- [Qq][Bb] (2%)
- 傲嬌 (2%)

Example::

    me > >///<
    bot> >\\\<

    me > >//////<
    bot> >\\\\\\<

    me > 我懂惹
    bot> me: 你國文沒學好嗎？

    me > 說中文好ㄇ
    bot> me: 請重念小學吧！

    me > QB
    bot> QB 必需死

    me > 傲嬌bot
    bot> 人... 人家才不是傲嬌呢 >////<

    
5. @rup host [host ...] (20%)
=============================

- data currectness, format (10%)
- injection (10%)
  
- Time should be in 24hr format.
- ``[machine name]`` is 10-char in width. (Not include the space between time.)

Example::

    me > @rup bsd1
    bot> [bsd1]     time: 00:40  uptime: 19d 08:18  load: 0.00 0.02 0.00

    me > @rup bsd1 linux3
    bot> [bsd1]     time: 00:42  uptime: 19d 08:20  load: 0.00 0.02 0.00
    bot> [linux3]   time: 00:42  uptime: 71d 13:59  load: 0.01 0.02 0.05

    me > @rup
    bot> Usage: @rup host [host ...]

    me > @rup bsd1;ls
    bot> unknown host "bsd1;ls"


6. @log [-n num] [-u] (20%)
===========================

- parse the log in /tmp/messages

========== ===================================
-n num     number of output. default = 5
-u         sort by user instead of ip address.
========== ===================================
authentication error

- sort with ip (8%)
- sort with user (8%)
- -n option (2% for each)

Example::

    me > @log
    bot> 1.93.29.180     73 times
    bot> 1.93.24.74      61 times
    bot> 1.93.26.70      55 times
    bot> 217.217.134.249 44 times
    bot> 61.160.212.43   10 times

    me > @log -n 1
    bot> 1.93.29.180     73 times

    me > @log -n 1 -u
    bot> root            500 times


