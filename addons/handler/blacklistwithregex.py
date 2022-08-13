from audiobot.audio import AudioItem
import audiobot.blacklist
from re import search

# The blacklist check functions in regular expression.
def _check_song_name(item: AudioItem, content, whole):
    title = item.source.getTitle()
    if whole:
        return content.lower() == title.lower()
    else:
        return bool(search(content, title))

def _check_username(item: AudioItem, content, whole):
    username = item.username.lower()
    if whole:
        return username == content.lower()
    else:
        return bool(search(content, username))


# Override the functions.
audiobot.blacklist.BlacklistItemType.SONG_NAME.check = _check_song_name
audiobot.blacklist._check_song_name = _check_song_name

audiobot.blacklist.BlacklistItemType.USERNAME.check = _check_username
audiobot.blacklist._check_username = _check_username


print("Replaced blacklist filter rule to regular expression")