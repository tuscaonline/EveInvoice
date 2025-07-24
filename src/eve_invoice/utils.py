import requests
import datetime
from dateutil.parser import parse as parsedate
 

def downloadIfNewer(url: str|bytes):
    r = requests.head(url)
    etag = r.headers.get("ETag")

    dt = parsedate(r.headers["last-modified"])

    return (etag, dt)

