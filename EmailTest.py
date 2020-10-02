import smtplib, random, sys

students ={}

def load_scores(file_name):
  with open (file_name) as student_scores:
    line=student_scores.readline()
    while line:
      grade_rec=line.split(',')
      students[grade_rec[0]]=grade_rec[1:]
      line=student_scores.readline()

def send_email(user,passwd):
    #get presenting student
    rand_student=random.randrange(1,len(students))
    stu_count=1
    for student in students.keys():
        #compose the message
        scores=students[student]
        message="Dear "+ scores[0] +", Your score for the book assignment is broken down below by question number.\n"
        for question in range(2,5):
            message+=str(question-1) + ". " + scores[question]+"\n"
        
        if (stu_count==rand_student): #Add stuff for the chosen one
            message+="You've been randomly chosen to present a summary of the book in the next class. Looking forward to it!"
        stu_count+=1
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(user, passwd)
        server.sendmail(user,student,message)
    server.quit()

def main():
    load_scores(sys.argv[1])
    send_email(sys.argv[2],sys.argv[3])

if __name__ == "__main__":
    main()

