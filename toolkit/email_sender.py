import smtplib

class SendMail:
    """CLASS Specifically designed to send emails
    """
    def __init__(self, SMTP, EMAIL, PW, EMAIL_TO, MESSAGE, SUBJECT) -> None:
        self.server = SMTP
        self.message = MESSAGE
        self.subject = SUBJECT
        self.email= EMAIL
        self.pw = PW
        self.email_to = EMAIL_TO
        #now we connect to the smtp lib
        connection = smtplib.SMTP(self.server)
        connection.starttls()
        connection.login(user=self.email,password=self.pw)
        connection.sendmail(
            from_addr=self.email, 
            to_addrs=self.email_to, 
            msg=f"{self.subject}\n\n{self.message}")
        connection.close()

