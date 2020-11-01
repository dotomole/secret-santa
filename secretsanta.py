import smtplib, ssl, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Pick(object):
    firstName = ""
    lastName = ""
    email = ""
    toBuyFirst = ""
    toBuyLast = ""

    #Constructor
    def __init__(self, firstName, lastName, email, toBuyFirst, toBuyLast):
        self.firstName = firstName
        self.email = email
        self.lastName = lastName
        self.toBuyFirst = toBuyFirst
        self.toBuyLast = toBuyLast

def getPeople(filename):
    people = []

    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            people.append(a_contact)
    return people
def sendMessage(receiver_first, receiver_last, receiver_email, toBuyFirst, toBuyLast):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"

    message = MIMEMultipart()
    message["Subject"] = "Secret Santa for {fname} {lname} - 2020".format(fname=receiver_first, lname=receiver_last)
    message["From"] = "Secret Santa"
    message["To"] = receiver_email

    html = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  
</head>

<body yahoo bgcolor="#ffebeb" style="margin: 0; padding: 0; min-width: 100%!important;">
<table width="100%" bgcolor="#ffebeb" border="0" cellpadding="0" cellspacing="0">
<tr>
  <td>
    <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
    <![endif]-->     
    <table bgcolor="#ffffff" class="content" align="center" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width: 600px;">
      <tr>
        <td bgcolor="#d96666" class="header" style="padding: 40px 30px 20px 30px;">
          <table width="70" align="left" border="0" cellpadding="0" cellspacing="0">  
            <tr>
              <td height="70" style="padding: 0 20px 20px 0;">
                <img style="height: auto;" class="fix" src="https://i.pinimg.com/originals/d7/5a/03/d75a03be8c8462a7f0abdea69c685e36.png" width="70" height="70" border="0" alt="" />
              </td>
            </tr>
          </table>
          <!--[if (gte mso 9)|(IE)]>
            <table width="425" align="left" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td>
          <![endif]-->
          <table class="col425" align="left" border="0" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 425px;">  
            <tr>
              <td height="70">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="subhead" style="padding: 0 0 0 3px;font-size: 15px; color: #ffffff; font-family: sans-serif; letter-spacing: 10px;">
                      WELCOME TO
                    </td>
                  </tr>
                  <tr>
                    <td class="h1" style="padding: 5px 0 0 0;color: #153643; font-family: sans-serif;font-size: 33px; line-height: 38px; font-weight: bold;">
                      Secret Santa - 2020
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <!--[if (gte mso 9)|(IE)]>
                </td>
              </tr>
          </table>
          <![endif]-->
        </td>
      </tr>
      <tr>
        <td class="innerpadding borderbottom" style="padding: 30px 30px 30px 30px;border-bottom: 1px solid #f2eeed;">
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>

            </tr>
            <tr>
              <td class="bodycopy" style="color: #153643; font-family: sans-serif;font-size: 16px; line-height: 22px;">
                Dear <b>{fname} {lname}</b>,
                <br>
                You have been invited to this year's Secret Santa. There will be a <b>$50</b> limit.
                <br><br>
                <text style="text-align:center">You must buy a present for:</text>
              </td>
            </tr>
            <td class="h2" style="text-align:center;color: #153643; font-family: sans-serif;padding: 0 0 15px 0; font-size: 24px; line-height: 28px; font-weight: bold;">
              <br>
              {fname2} {lname2}
            </td>
          </table>
        </td>
    </tr>
</table>
</body>
</html>
    """.format(fname=receiver_first, lname=receiver_last, fname2=toBuyFirst.upper(), lname2=toBuyLast.upper())

    textMsg = MIMEText(html, "html")
    message.attach(textMsg)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def main():
    picks = [] #obj arr
    i=0

    #All people from file
    people = getPeople("people.csv")

    #Initialized to enter the loop below
    theirPick = people[len(people)-1]

    #If the last person gets themselves then the whole process
    #must be restarted...
    while (theirPick == people[len(people)-1]):
        j=0

        #If it has ever been restarted, delete all picks and start again
        if (i >= 1):
            del picks
            picks = []

        #Copy all people into another 'choices' arr
        choices = people.copy()

        #people[j] = the person getting the email
        #theirPick = the person they buy for
        while (j < len(people)):

            #Pick random choice
            theirPick = random.choice(choices)

            #Cant choose yourself
            #Last person will get stuck in an inf loop if here.
            while ((theirPick == people[j]) and (len(choices) > 1)):
                theirPick = random.choice(choices)


            #Remove people that have already been chosen
            choices.remove(theirPick)

            #Variables for Picks object
            firstName = people[j].split(",")[0]
            lastName = people[j].split(",")[1]
            email = people[j].split(",")[2]
            toBuyFirst = theirPick.split(",")[0]
            toBuyLast = theirPick.split(",")[1]

            #Create object of who's buying for who, to later send emails
            picks.append(Pick(firstName, lastName, email, toBuyFirst, toBuyLast))
            j+=1
        i+=1

    k=0
    #Send all the emails
    for pick in picks:
        print("Sending Email "+str(k+1)+" ...")
        sendMessage(pick.firstName, pick.lastName, pick.email, pick.toBuyFirst, pick.toBuyLast)
        k+=1
    
if __name__ == '__main__':
    sender_email = input("Enter your Email Address: ")
    password = input("Enter your Email Password: ")
    main()
