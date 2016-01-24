__author__ = 'pete'

import quickstart
import time
import praw
import sys
import schedule
import os
import random

USERNAME = ''       #add in login details for bot..
PASSWORD = ''

downvoters = []     #usernames to downvote and upvote..
upvoters = []

n_upvotes = 0
n_downvotes = 0

already_comment_id = []

def log_work():
    global n_upvotes, n_downvotes
    print "Emailing 24 hourly log file.."
    print 'Upvotes ',str(n_upvotes),' Downvotes ', str(n_downvotes)
    quickstart.CredsSendLog(n_upvotes, n_downvotes)
    os.rename('log.txt','log.old'+str(random.randint(0,65535)))
    n_upvotes = 0
    n_downvotes = 0
    print "Saving old log file, creating new file.."
    log(time.strftime("%Y-%m-%d %H:%M:%S")+' New daily log begins.. \n')
    #sends the log.txt to my email address and moves the log to a new file..
    return

def log(string_data):
    with open("log.txt", "a") as myfile:
        myfile.write(string_data)
    return



r = praw.Reddit(user_agent='Something random')          #change this to a unique string..
r.login(USERNAME, PASSWORD, disable_warning=True)
#r.login(USERNAME, PASSWORD)
subreddit = r.get_subreddit('test')                     #a subreddit to monitor..
#subreddit_comments = subreddit.get_comments()

print '>>>Reddit /r/bitcoin bot..<<<'

print 'Downvoting:', downvoters
print 'Upvoting:', upvoters

print '>>>active - logging to /log.txt<<<'

schedule.every().day.at("07:00").do(log_work)           #scheduled log maintenance and emailing..
schedule.every().day.at("19:00").do(log_work)

while True:


    subreddit_comments = subreddit.get_comments()       #get the new comments..


    for comment in subreddit_comments:                  #make sure they havent been seen already..
        
        if comment.id in already_comment_id:
         pass
       
        else:
            already_comment_id.append(comment.id)
            
            chance = random.randint(1,4)                #only vote manipulate 75% of time..
            if chance == 4:
                pass
            
            elif comment.author.name in downvoters:
               print "downvoted: ", comment.author.name, comment.id
               comment.downvote()
               n_downvotes+=1
               logstr = time.strftime("%Y-%m-%d %H:%M:%S")+' downvoted '+comment.author.name+' '+comment.id+'\n'
               log(logstr)
               
            elif comment.author.name in upvoters:
                print 'match', comment.author.name, comment.id
                logstr = time.strftime("%Y-%m-%d %H:%M:%S")+' upvoted '+comment.author.name+' '+comment.id+'\n'
                log(logstr)
                comment.upvote()
                n_upvotes+=1

    sys.stdout.write('.')
    sys.stdout.flush()
    schedule.run_pending()
    time.sleep(random.randint(0,20))            #randomly wait before scanning subreddit again..
