# bot
As an exercise into the world of the blackhat hacker I created this simple bot as a proof of concept.
It is python based and uses the PRAW reddit api to monitor a subreddit for new comments, before upvoting and downvoting those people contained in the upvote or downvote lists.
A list of those redditors who have been up or downvoted is logged to log.txt.

Using the python google-api-client the bot emails from your gmail address with the log at scheduled checkpoints. Should reddit ban any throwaway accounts they are dropped and another is randomly tried. Basic exceptions are dealt with and logged to keep the bot running.



