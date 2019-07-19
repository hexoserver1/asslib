def sendmail(to, subject, text, host='mailhost.nerc-liv.ac.uk', sender='do-not-reply@nerc-liv.ac.uk', sendname=None,
             send=True, sub=None):
    """
    email = sendmail(to,subject,text,[host],[sender],[sendname],[send],[sub],[conndb])

    where
        email is the formatted email content
        to is the recipient email address or list of email addresses
        subject is the email subject
        text is the email body text
        host is the SMTP server hostname or IP address, defaults to mailhost.nerc-liv.ac.uk
        sender is the sender email, defaults to do-not-reply@nerc-liv.ac.uk
        sendname is the name to give the sender, defaults to the local-part of sender
        send is a bool that decides whether or not to send the formatted email, defaults to True
        sub is a list of tuples defining email substitutions

    Formats an email message for sending via SMTP

    title - sendmail vr - 1.1 author - fakas date - 20170802

    mods  - 1.1 Corrections to better conform with Python conventions (20190708fakas)
    """
    from smtplib import SMTP

    if type(to) is str:
        to = [to]

    if sub is not None:
        for ii, vv in enumerate(to):
            for tup in sub:
                if tup[0] == vv:
                    to[ii] = tup[1]

    if sendname is None:
        sendname = sender.split('@')[0]

    for vv in [subject, host, sender]+to:
        if "\n" in vv:
            raise Exception("Newlines not allowed in fields other than text!")

    email = "From: "+sendname+" <"+sender+">\n"\
            + "To: "+to[0].split('@')[0]+" <"+to[0]+">\n"\
            + "Subject: "+subject+"\n\n"\
            + text+"\n"

    if send:
        sobj = SMTP(host)
        sobj.sendmail(sender, to, email)

    return email
