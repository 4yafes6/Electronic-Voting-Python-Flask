from smtplib import SMTP 
import random

class Mail():
    def __init__(self,gönderici, alıcı, kod):
        self.gönder = gönderici
        self.al = alıcı
        self.k = kod 
            
    def gönder(sendTo):
        randomCode = random.randint(100000,999999)
        try:
            # Mail Message Information
            subject = "E-Mail authentication system"
            message = ("Here is E-Mail authentication system"+ " :" +str(randomCode))
            contents = "Subject: {0}\n\n{1}".format(subject,message)

            # Account Information
            mailaddress = "example@gmail.com"
            password = "passwd"

            # To Whom To Send Information
            mail = SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login(mailaddress,password)
            mail.sendmail(mailaddress, sendTo, contents.encode("utf-8"))
            print("Your code has been sent successfully!")
        except Exception as e:
                print("Error!\n {0}".format(e))
                    
        return randomCode
    
# Mail.gönder("yusufbalik0046@gmail.com")