#I got started and used a bunch of code from this guide: http://pythonforengineers.com/build-a-reddit-bot-part-1/

import praw
import pdb
import re
import os
from datetime import datetime
import sys

#colors to make the log output somewhat more readable
class color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

reddit = praw.Reddit('bot1')
one = "Nothing personal kid"
two = "nothing personal kid"
three = "Nothing personal, kid"
four = "nothing personal, kid"

postrep = "[*personnel](http://i.imgur.com/xAEucNL.jpg)"
comrep = "[*personnel](http://i.imgur.com/xAEucNL.jpg)"

#opens posts_replied_to.txt and stuff
if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []
else:
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))

#opens comments_replied_to.txt and stuff
if not os.path.isfile("comments_replied_to.txt"):
	comments_replied_to = []
else:
	with open("comments_replied_to.txt", "r") as q:
		comments_replied_to = q.read()
		comments_replied_to = comments_replied_to.split("\n")
		comments_replied_to = list(filter(None, comments_replied_to))

#opens the log
log = open("BotLog.txt", "a")

subreddit = reddit.subreddit('hydeparkms')

#gets 10 submissions from hot
for submission in subreddit.hot(limit=10):
	
	#searches title of each post
	if re.search("Nothing personal, kid", submission.title, re.IGNORECASE) and submission not in posts_replied_to:
		try:
			#reply
			submission.reply(postrep)

			#log output
			logout = "\n\n" + color.BLUE + color.BOLD + str(datetime.now()) + color.END + color.END + " | " + color.GREEN + "successfully replied to post" + color.END + " \"" + submission.title + color.CYAN + "\", post id: " + color.END + submission.id + " with \"" + postrep + "\""
			log.write(logout)

			#posts_replied_to.txt output
			posts_replied_to.append(submission.id)
			with open("posts_replied_to.txt", "w") as f:
				for post_id in posts_replied_to:
					f.write(post_id + "\n\n")
		
		#in case of the time limit error, or any other exception
		except:
			e = str(sys.exc_info())
			
			#log output including exception details
			logout = "\n\n" + color.BLUE + color.BOLD + str(datetime.now()) + color.END + color.END + " | " + color.RED + e + color.END + " while trying to reply to post \"" + submission.title + color.CYAN + "\", post id: " + color.END + submission.id
			log.write(logout)
	
	#gets all the comments for the current post
	comments = submission.comments

	#for each comment in each post
	for comment in comments:
		body = comment.body
		
		#searches comments for personal
		if (re.search(one, body, re.IGNORECASE) or re.search(three, body, re.IGNORECASE)) and (comment not in comments_replied_to):
			
			try:
				#reply
				comment.reply(comrep)

				#log output, including parent post info
				logout = "\n\n" + color.BLUE + color.BOLD + str(datetime.now()) + color.END + color.END + " | " + color.GREEN + "successfully replied to comment" + color.END + " \"" + body + color.CYAN + "\", comment id: " + color.END + comment.id + ", post \"" + submission.title + color.CYAN + "\", post id: " + color.END + submission.id + " with \"" + comrep
				log.write(logout)

				#comments_replied_to.txt output
				comments_replied_to.append(comment.id)
				with open("comments_replied_to.txt", "a") as q:
					q.write(comment.id + "\n\n")
			
			#for time limit or other exceptions
			except:
				e = str(sys.exc_info())
				
				#log output with exception info and parent post info
				logout = "\n\n" + color.BLUE + color.BOLD + str(datetime.now()) + color.END + color.END + " | " + color.RED + e + color.END + " while trying to reply to comment \"" + body + color.CYAN + "\", comment id: " + color.END + comment.id + ", post \"" + submission.title + color.CYAN + "\", post id: " + color.END + submission.id
				log.write(logout)
