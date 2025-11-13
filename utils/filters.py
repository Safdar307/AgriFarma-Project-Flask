import humanize
from datetime import datetime
from markupsafe import escape, Markup

def timesince(dt):
    """Convert datetime to human readable time difference"""
    if not dt:
        return ''
    now = datetime.utcnow()
    diff = now - dt
    return humanize.naturaltime(diff)

def nl2br(value):
    """Convert newlines to <br> tags"""
    if not value:
        return ''
    return Markup(escape(value).replace('\n', Markup('<br>')))