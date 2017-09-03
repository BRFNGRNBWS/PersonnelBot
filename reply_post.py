import praw
import pdb
import re
import os
from datetime import datetime
import sys

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

if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []
else:
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))

if not os.path.isfile("comments_replied_to.txt"):
	comments_replied_to = []
else:
	with open("comments_replied_to.txt", "r") as q:
		comments_replied_to = q.read()
		comments_replied_to = comments_replied_to.split("\n")
		comments_replied_to = list(filter(None, comments_replied_to))

log = open("BotLog.txt", "a")

subreddit = reddit.subreddit('hydeparkms')
for submission in subreddit.hot(limit=10):
	if re.search("Nothing personal, kid", submission.title, re.IGNORECASE) and submission not in posts_replied_to:
		try:
			postrep = "*personnel"
			submission.reply(postrep)

			logout = "\n\n" + color.BLUE + color.BOLD + str(datetime.now()) + color.END + color.END + " | " + color.GREEN + "successfully replied to post" + color.END + " \"" + submission.title + color.CYAN + "\", post id: " + color.END + submission.id + " with \"" + postrep + "\""
			log.write(logout)

			posts_replied_to.append(submission.id)
			with open("posts_replied_to.txt", "w") as f:
				for post_id in posts_replied_to:
					f.write(post_id + "\n\n")

		except:
			e = str(sys.exc_info())
			logout = "\n\n" + color.BLUE + color.BOLD + str(datetime.now()) + color.END + color.END + " | " + color.RED + e + color.END + " while trying to reply to post \"" + submission.title + color.CYAN + "\", post id: " + color.END + submission.id
			log.write(logout)

	comments = submission.comments

	for comment in comments:
		body = comment.body
		if (one in body or two in body or three in body or four in body) and (comment not in comments_replied_to):

			ancestor = comment
			refresh_count = 0
			while not ancestor.is_root:
				ancestor = ancestor.parent()
				if refresh_count % 9 == 0:
					ancestor.refresh()
					refresh_count += 1

			parent_post = ancestor.parent()

			try:
				comrep = "*personnel"
				comment.reply(comrep)

				logout = "\n\n" + color.BLUE + color.BOLD + str(datetime.now()) + color.END + color.END + " | " + color.GREEN + "successfully replied to comment" + color.END + " \"" + body + color.CYAN + "\", comment id: " + color.END + comment.id + ", post \"" + parent_post.title + color.CYAN + "\", post id: " + color.END + parent_post.id + "with \"" + comrep
				log.write(logout)

				comments_replied_to.append(comment.id)
				with open("comments_replied_to.txt", "w") as q:
			                q.write(comment_id + "\n\n")

			except:
				e = str(sys.exc_info())
				logout = "\n\n" + color.BLUE + color.BOLD + str(datetime.now()) + color.END + color.END + " | " + color.RED + e + color.END + " while trying to reply to comment \"" + body + color.CYAN + "\", comment id: " + color.END + comment.id + ", post \"" + parent_post.title + color.CYAN + "\", post id: " + color.END + parent_post.id
				log.write(logout)
