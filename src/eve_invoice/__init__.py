from pathlib import Path
import platformdirs
from requests_cache import CachedSession, SQLiteCache


dirs = Path(platformdirs.user_data_dir(appname="eveinvoice", appauthor="Tusca", version='1.0'))
holoDirs = dirs/ "hololleak"

requestBackend = SQLiteCache(dirs / 'http_cache.sqlite')
requestSession = CachedSession(backend=requestBackend)
