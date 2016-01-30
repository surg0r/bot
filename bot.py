__author__ = 'pete'

import quickstart
import time
import praw
import sys
import schedule
import os
import random

PASSWORD = 'password' #the password for the throwaway accounts..


accounts = ['random_throwaway1', 'random_throwaway2', 'etc' ]
downvoters = ['some','user','to','downvote']
upvoters = ['some','user','to','upvote']

n_upvotes = 0
n_downvotes = 0

already_comment_id = []

def r_login():
 while True:
    try:
        attempt = accounts[random.randint(0,len(accounts)-1)]
        print 'attempt login with account:', attempt
        r.login(attempt, PASSWORD, disable_warning=True)
        log(time.strftime("%Y-%m-%d %H:%M:%S")+' login success: '+attempt+'\n')
        return
    except praw.errors.InvalidUserPass as e:
        print 'login failed - praw.errors.InvalidUserPass', attempt
        log(time.strftime("%Y-%m-%d %H:%M:%S")+' '+str(type(e))+attempt+'\n')
        accounts.remove(attempt)
        time.sleep(15)
        continue
    except Exception as e:
        print 'login failed', type(e), e.args, e
        quickstart.ErrorSendEmail()
        exit()



def log_work():
    global n_upvotes, n_downvotes
    print "Emailing 24 hourly log file.."
    print 'Upvotes ',str(n_upvotes),' Downvotes ', str(n_downvotes)
    quickstart.CredsSendLog(n_upvotes, n_downvotes)
    os.rename('./log/log.txt','./log/log.old'+str(random.randint(0,6553500)))
    n_upvotes = 0
    n_downvotes = 0
    print "Saving old log file, creating new file.."
    log(time.strftime("%Y-%m-%d %H:%M:%S")+' New daily log begins.. \n')
    #sends the log.txt to my email address and moves the log to a new file..
    return

def log(string_data):
    with open("./log/log.txt", "a") as myfile:
        myfile.write(string_data)
    return



r = praw.Reddit(user_agent='Some unique text not containing bot')

r_login()

subreddit = r.get_subreddit('any subreddit you want')      #lazy so no need to error check..

print '>>>Reddit /r/bitcoin bot..<<<'

print 'Downvoting:', downvoters
print 'Upvoting:', upvoters

print '>>>active - logging to ./log/log.txt<<<'

schedule.every().day.at("07:00").do(log_work)
schedule.every().day.at("19:00").do(log_work)

while True:

 try:
        subreddit_comments = subreddit.get_comments()

        for comment in subreddit_comments:

            if comment.id in already_comment_id:
                pass

            else:
                already_comment_id.append(comment.id)

                if comment.author.name in downvoters:
                        #comment.reply('test')
                    print "downvoted: ", comment.author.name, comment.id
                    comment.downvote()
                    n_downvotes+=1
                    logstr = time.strftime("%Y-%m-%d %H:%M:%S")+' downvoted '+comment.author.name+' '+comment.id+'\n'
                    log(logstr)


                if comment.author.name in upvoters:
                    print 'match', comment.author.name, comment.id
                    logstr = time.strftime("%Y-%m-%d %H:%M:%S")+' upvoted '+comment.author.name+' '+comment.id+'\n'
                    log(logstr)
                    comment.upvote()
                    n_upvotes+=1


        sys.stdout.write('.')
        sys.stdout.flush()
        schedule.run_pending()
        time.sleep(random.randint(0,20))

 except praw.errors.InvalidUserPass as e:
        print 'login failed - praw.errors.InvalidUserPass'
        log(time.strftime("%Y-%m-%d %H:%M:%S")+' '+str(type(e))+'\n')
        time.sleep(15)
        r_login()
        continue
 except praw.errors.LoginRequired as e:
        print 'logged out - praw.errors.LoginRequired'
        log(time.strftime("%Y-%m-%d %H:%M:%S")+' '+str(type(e))+'\n')
        time.sleep(15)
        r_login()
        continue
 except Exception as e:
        print "Error", type(e), e.args, e
        log(time.strftime("%Y-%m-%d %H:%M:%S")+" Error"+str(e)+"\n")
        time.sleep(20)
        continue

 except KeyboardInterrupt:
        print 'Exiting..upvotes: '+str(n_upvotes), ' downvotes: '+str(n_downvotes)
        log(time.strftime("%Y-%m-%d %H:%M:%S")+' manual shutdown CTRL-C..\n')
        exit()
