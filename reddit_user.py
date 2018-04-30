import praw
import config
import json
import argparse
import datetime

reddit = praw.Reddit(client_id = config.client_id,
                    client_secret = config.client_secret,
                    username = config.username,
                    password = config.password,
                    user_agent = config.user_agent)

def get_parser():
    parser = argparse.ArgumentParser(description="Reddit Downloader")
    parser.add_argument("-u",
                        "--user",
                        dest="user",
                        help="User to retrieve data from",
                        default=None)

    parser.add_argument("-l",
                        "--limit",
                        dest="limit",
                        help="Pull N number of submissions",
                        default=None)

    parser.add_argument("-ul",
                        "--userlist",
                        dest="userlist",
                        help="List of users to pull information from",
                        default=None)

    parser.add_argument("-of",
                        "--outputfolder",
                        dest="outputfolder",
                        help="Name of the Folder to store user info in",
                        default="User_Hold")

    return parser

def prawAPI(user, lt, outputFolder):
    print("Collecting {} submissions".format(user))

    u = reddit.redditor(user)
    com = reddit.redditor(user).comments.new(limit=lt)
    sub = reddit.redditor(user).submissions.new(limit=lt)

    redditData = {}
    redditData[str(user)] = [{}]
    redditData[str(user)][0]['0_comments'] = [{}]
    redditData[str(user)][0]['1_submissions'] = [{}]
    comCount=0
    subCount=0
    try:
        for comment in com:
            comCount+=1
            print("Found: {} Comments".format(comCount))
            redditData[str(user)][0]['0_comments'][0][str(comment.id)] = [{}]
            redditData[str(user)][0]['0_comments'][0][str(comment.id)][0]['0_Comment Submission'] = comment.submission.title
            redditData[str(user)][0]['0_comments'][0][str(comment.id)][0]['1_Text'] = ''.join((comment.body)).encode('utf-8').strip()
            redditData[str(user)][0]['0_comments'][0][str(comment.id)][0]['2_Subreddit'] = comment.subreddit.display_name
        print("Found: {} Comments Total".format(comCount))
    except:
        pass
    try:
        for submission in sub:
            subCount+=1
            if subCount%10==0:
                print("Found: {} Submissions".format(subCount))
            redditData[str(user)][0]['1_submissions'][0][str(submission)] = [{}]
            redditData[str(user)][0]['1_submissions'][0][str(submission)][0]['0_Title'] = ''.join((submission.title)).encode('utf-8').strip()
            redditData[str(user)][0]['1_submissions'][0][str(submission)][0]['1_Text'] = ''.join((comment.body)).encode('utf-8').strip()
            redditData[str(user)][0]['1_submissions'][0][str(submission)][0]['2_Subreddit'] = submission.subreddit.display_name
    except:
        pass
    print("Found: {} Submissions".format(subCount))
    print
    print("Downloaded {} comments from user {}.".format(comCount, user))
    print("Downloaded {} submissions from user {}.".format(subCount, user))
    with open(outputFolder+'/reddit_'+user+'.json', 'w') as o:
        o.write(json.dumps(redditData, sort_keys=True))

if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    limit = args.limit
    if limit != None:
        limit = int(limit)
    if args.user == None:
        print("Error: You have not specified a user(s) to retrieve submissions from.")
    #users = args.user.split(',')
    if args.userlist != None:
        with open(args.userlist, "r") as inputF:
            userHold = []
            d = inputF.readlines()
            for line in d:
                if not line in userHold:
                    userHold.append(line)
            for user in userHold:
                prawAPI(user.strip(),limit,args.outputfolder)
    else:
        users = args.user.split(',')
        for s in users:
            prawAPI(s, limit, args.outputfolder)