from datetime import datetime, timezone


# Note: datetime.utcnow() returns a datetime object with tzinfo set to None
# Which is not the same as datetime.now(timezone.utc)
# See: https://medium.com/@life-is-short-so-enjoy-it/python-datetime-utcnow-maybe-no-more-for-me-221795e8ddbf
def utcnow():
    return datetime.now(timezone.utc)
