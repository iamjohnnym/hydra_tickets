from smtplib import SMTP, SMTPException


class SendMail():
    def __init__(self, recipient, ddi, ticket, name, phone, platform, details, id, status, updated=None, user_name=None, private=None):
        self.smtpObj = SMTP('localhost')
        self.recipient = recipient
        self.platform = platform
        self.details = details
        self.updated = updated
        self.private = private
        self.user_name = user_name
        self.status = status
        self.id = id
        self.ticket = ticket
        self.phone = phone
        self.name = name
        self.ddi = ddi

    def mail(self):
        message = """From: CallBack <test@ohaiworld.com>
To: {0}
Subject: {6} Ticket {4}
Account: {1}
Name: {2}
Phone Number: {3}
Ticket: https://customer-tickets/tickets/{4}

Call Details:
{5}
        """.format(self.recipient,
                   self.ddi,
                   self.name,
                   self.phone,
                   self.ticket,
                   self.details[0]['details'],
                   self.platform
                   )
        print message
        return message

    def run(self):
        message = """From: CallBack <postmaster@cb.ohaiworld.com>
To: {0}
Subject: {7}: {6} Call Back - Ticket {4}
In-Reply-To: {8}
Message-ID: {8}
References: {8}
Thread-Topic: {6} Call Back - Ticket {4}
Thread-Index: {8}

DDI: {1}
Name: {2}
Phone Number: {3}
Callback: http://10.14.209.209/callbacks/{8}

Call Details:
{5}
        """.format(self.recipient,
                   self.ddi,
                   self.name,
                   self.phone,
                   self.ticket,
                   self.details[0]['details'],
                   self.platform,
                   self.status,
                   self.id
                   )
        try:
            self.smtpObj.sendmail('test@cb.ohaiworld.com', self.recipient, message)
            return message
        except SMTPException,e:
            print e
            return "Error: Unable to send email"
