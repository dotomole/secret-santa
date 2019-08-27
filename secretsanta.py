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
    message["Subject"] = "Secret Santa for {fname} {lname}".format(fname=receiver_first, lname=receiver_last)
    message["From"] = "Secret Santa"
    message["To"] = receiver_email

    html = """\
    <html>
      <body>
        <p>Dear {fname} {lname},<br><br>
        You have been invited to this year's <b>Secret Santa!</b><br><br>

        You have been given <u><b>{fname2} {lname2}</b></u> to buy a gift for.<br><br> 

        Merry Christmas!<br><br>

        Love, <br>
        Secret Santa.
        </p>
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

    #Send all the emails
    for pick in picks:
        print("sending email "+str(i+1)+" ...")
        sendMessage(pick.firstName, pick.lastName, pick.email, pick.toBuyFirst, pick.toBuyLast)
        i+=1
    
if __name__ == '__main__':
    sender_email = input("Enter your email address: ")
    password = input("Enter your email password: ")
    main()