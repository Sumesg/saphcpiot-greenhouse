#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This code will extract the ip address of your Pi and then send an email
containing the ip to the specified email address. This is inspired by
the need to access the Pi via SSH or other network protocols without a
monitor and moving from network to network. This uses a Gmail SMTP server,
and assumes you have a valid Gmail address. You may need to alter a bit
for other servers (beyond the scope of this article).

http://elinux.org/RPi_Email_IP_On_Boot_Debian
"""


import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime

if __name__ == "__main__":
    # Change to your own account information
    to = 'name@example.com'
    your_mail_user = 'name@example.com'
    your_mail_password = 'your_password'
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(your_mail_user, your_mail_password)
    today = datetime.date.today()

    # Very Linux Specific
    arg = 'ip route list'
    p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index('src') + 1]
    my_ip = 'Your ip is %s' % ipaddr
    msg = MIMEText(my_ip)
    msg['Subject'] = ' - IP For RaspberryPi on %s' % today.strftime('%b %d %Y')
    msg['From'] = your_mail_user
    msg['To'] = to
    smtpserver.sendmail(your_mail_user, [to], msg.as_string())
    smtpserver.quit()
