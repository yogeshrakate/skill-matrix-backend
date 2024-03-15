import smtplib
def send_mail(reciver,data):
    try:
        
        mail=smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        sender='golubajpai302@gmail.com'
        mail.login('mvl@gmail.com','9893116200')
        header='To:'+reciver+'\n'+'From:' \
        +sender+'\n'+'subject:testmail\n'
        data=header+data
        mail.sendmail(sender, recipient, data)
        mail.close()
        return True

    except Exception as e:
        print(e)
        raise e