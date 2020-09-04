# Copyright 2020 called2voyage
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import praw
from prawutils.submissions import loop_submissions
from datetime import datetime, timezone

reddit = praw.Reddit('bot2')
print(reddit.user.me())
subreddit = reddit.subreddit("IAmAFiction")
print(subreddit)

def get_num_comments_per_commenter(submission, *args):
    commenters = args[0]
    most_recent_comment = args[1]
    submission_author = submission.author.name if submission.author is not None else ''
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        if comment.author is not None and comment.author.name != 'FicQuestionBot' and comment.author.name != 'FicFlairBot':
            if comment.author.name != submission_author:
                if comment.author.name not in commenters:
                    commenters[comment.author.name] = 0
                    most_recent_comment[comment.author.name] = comment
                commenters[comment.author.name] = commenters[comment.author.name] + 1

avid_commenters = []

limit = 10
limit_found = False
current_month = datetime.now(tz=timezone.utc).month

while not limit_found:
    n = 0
    for submission in subreddit.new(limit=limit):
        n = n + 1
        if datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).month != current_month:
            limit = n - 1
            limit_found = True
            break
    if not limit_found:
        limit = limit + 10

commenters = {}
most_recent_comment = {}
loop_submissions(subreddit, get_num_comments_per_commenter, limit, commenters, most_recent_comment)

for commenter, num_comments in commenters.items():
    if num_comments >= 10:
        avid_commenters.append(commenter)

template = '20492542-6ace-11ea-abe8-0eb5501e2a6b' # Avid Commenter template
for commenter in avid_commenters:
    flair = next(subreddit.flair(commenter))
    if flair['flair_css_class'] != 'avid-commenter':
        if flair['flair_text'] != '' and flair['flair_text'] is not None:
            flair_text = '%s, %s' % (flair['flair_text'], 'Avid Commenter')
            subreddit.flair.set(commenter, text=flair_text, flair_template_id=template)
        else:
            subreddit.flair.set(commenter, text='Avid Commenter', flair_template_id=template)
        most_recent_comment[commenter].reply('*Congratulations! You\'ve earned the "Avid Commenter" flair!*')

for flair in subreddit.flair(limit=None):
    if flair['flair_css_class'] == 'avid-commenter':
        if flair['user'] not in avid_commenters:
            if ',' in flair['flair_text']:
                subreddit.flair.set(flair['user'], text=flair['flair_text'].replace(', Avid Commenter', ''), css_class='')
            else:
                subreddit.flair.delete(flair['user'])
