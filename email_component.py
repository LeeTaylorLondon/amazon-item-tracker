# email_component.py

import smtplib
from typing import List, Tuple

def send_email(email_addr_re, email_addr, email_pw, item_url) -> None:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # init. email login, create email
    try:
        print(email_addr, email_pw)
        server.login(email_addr, email_pw)
    except smtplib.SMTPAuthenticationError:
        print("<email-status: 'failed' invalid login!>")
        return

    subject = "Amazon-Item-Tracker Item-Price Reduced!"
    body    = f'An item has fallen down in price!\n {item_url}'
    msg     = f"Subject: {subject}\n\n{body}"
    # sends email and quits
    server.sendmail(email_addr, email_addr_re, msg)
    print("<email_status: sent>")
    server.quit()


def instructions():
    print("\n<REQUIRES: Google-mail>")
    print("1 - Navigate to myaccount.google.com")
    print("2 - Click on the 'security' tab")
    print("3 - Click on 'App passwords'")
    print("4 - Select app -> 'Mail', Select Device -> '(Windows) Computer'")
    print("5 - Generate password, and enter it in this program when prompted")


def set_interval() -> int:
    """ auto ping prices every INTERVAL (seconds)

        this function allows the user to set the INTERVAL (seconds)
    """

    try:
        rv = int(input("Enter in seconds how often would like this program to check the prices: "))
    except ValueError:
        print("Please enter an integer!")
        return
    return rv


def set_sender_email() -> Tuple[str, str]:
    """ user must define sender email address and password 

        this information is not stored, due to the sensitivity
        user is recommended to use a throwaway account or google
        option displayed in video
    """
    
    email = str(input("Enter sender email: "))
    if(email.find("@gmail.com") == -1 and email.find("@googlemail.com")):
            raise TypeError('<invalid email, sender email must be google mail>')
    else:
            return email


def set_sender_pw() -> str:
    return str(input("Enter 'app (email) password': "))


def set_receiver_email() -> str:
    """ user must define receiver email """

    print("Receiver email can be of any email server, i.e 'Yahoo', 'Hotmail', ...")
    re_email = str(input("Enter email to receive notification: "))
    if(re_email.find('@') == -1):
        raise TypeError('<invalid email address>')
        return
    else:
        return re_email
    return
