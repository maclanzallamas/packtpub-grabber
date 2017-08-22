
import requests
import smtplib
import config
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml.html import fromstring
from bs4 import BeautifulSoup


def readURL(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')

    tagImage=soup.find(class_='dotd-main-book-image float-left')
    tagTitle=soup.find(class_='dotd-title')
    tagDecription=soup.find(class_='dotd-main-book-summary float-left')

    title = tagTitle.h2.string.strip()
    imageURL = 'https:' + tagImage.a.img['src']
    description = tagDecription.contents[7].text.strip().replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u2013","-")
    return [title, imageURL, description]


def sendMail(title, imageURL, description):
    today = datetime.date.today()

    msg = MIMEMultipart()
    msg['From'] = config.emailSender['senderUsername']
    msg['To'] = ", ".join(config.emailReceiver['receivers'])
    msg['Subject'] = "Free e-book from Packtpub on " + str(today)

    body = """\
    <html>
      <head></head>
      <body>
        <div><h2>{title}</h2>
        <br>
        </div>
        <div><img src="{imageURL}">
        <br>
        </div>
        <div><br>{description}
        <br>
        </div>
        <div><a href="https://www.packtpub.com/packt/offers/free-learning">Download this e-book here</a></div>
      </body>
    </html>
    """.format(title=title,imageURL=imageURL,description=description)
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config.emailSender['senderUsername'], config.emailSender['senderPassword'])
    text = msg.as_string()
    server.sendmail(config.emailSender['senderUsername'], config.emailReceiver['receivers'], text)
    server.quit()

def main():
    url = 'https://www.packtpub.com/packt/offers/free-learning'
    bookInfo = readURL(url)
    sendMail(bookInfo[0], bookInfo[1], bookInfo[2])


main()
