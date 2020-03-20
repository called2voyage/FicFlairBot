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
from datetime import datetime, timezone

reddit = praw.Reddit('bot2')
print(reddit.user.me())
subreddit = reddit.subreddit("IAmAFiction")
print(subreddit)

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
