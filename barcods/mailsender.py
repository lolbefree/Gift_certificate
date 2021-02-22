import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart  # New line
from email.mime.base import MIMEBase  # New line
from email import encoders  # New line
from PIL import Image
import os
import time 


def sender(receiver_emails, receiver_names, name_file):
    print(receiver_emails, receiver_names, name_file)


    # User configuration
    sender_email = "Gift_certificates@avtosojuz.ua"
    sender_name = "Gift_certificates"

    receiver_emails = [receiver_emails]
    receiver_names = [receiver_names]
    filename2 = name_file
    # Email body
    email_body = """<h1><img src="{}"></h1>""".format(filename2)
    print(receiver_emails, receiver_names, name_file)


    for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
            # Configurating user's info
            msg = MIMEMultipart()
            msg['To'] = formataddr((receiver_name, receiver_email))
            msg['From'] = formataddr((sender_name, sender_email))
            msg['Subject'] = 'Подарунковий сертифікат для вас, ' + receiver_name

            msg.attach(MIMEText(email_body, 'html'))

            try:
                # Open PDF file in binary mode
                with open(filename2, "rb") as attachment:
                                part = MIMEBase("application", "octet-stream")
                                part.set_payload(attachment.read())

                # Encode file in ASCII characters to send by email
                encoders.encode_base64(part)

                # Add header as key/value pair to attachment part
                part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename2}",
                )
                print(filename2)
                msg.attach(part)
            except Exception as e:
                    break

            try:
                    # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
                    server = smtplib.SMTP('10.10.10.47', 25)
                    # Encrypts the email
                    # We log in into our Google account
                    # Sending email from sender, to receiver with the email body
                    server.sendmail(sender_email, receiver_email, msg.as_string())
            except Exception as e:
                    break
            #finally:
                    #server.quit()
                   # time.sleep(20)

def five_100(mail, name, name_file):
    print(name_file)
    img1 = Image.open('C:\\AM\\BAT\\Gift_certificate\\barcods\\500.jpg')                        # main image
    barcd = Image.open("C:\\AM\\BAT\\Gift_certificate\\barcods\\{}".format(name_file))                   # save new size
    img1.paste(barcd, (0, 850))                         # paste barcode to main image
    img1.save("C:\\AM\\BAT\\Gift_certificate\\barcods\\img_with_barcode.png")                         # save with barcode
    
    sender(mail, name, "C:\\AM\\BAT\\Gift_certificate\\barcods\\img_with_barcode.png")


def One_1000(mail, name, name_file):
    print(name_file)
    img1 = Image.open('C:\\AM\\BAT\\Gift_certificate\\barcods\\1000.jpg',)                        # main image
    barcd = Image.open("C:\\AM\\BAT\\Gift_certificate\\barcods\\{}".format(name_file))  

    img1.paste(barcd, (0, 850))                         # paste barcode to main image
    img1.save("C:\\AM\\BAT\\Gift_certificate\\barcods\\img_with_barcode.png")                            # save with barcode
    sender(mail, name, "C:\\AM\\BAT\\Gift_certificate\\barcods\\img_with_barcode.png")