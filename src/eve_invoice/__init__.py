from pathlib import Path
import platformdirs
from requests_cache import CachedSession, SQLiteCache


dirs = Path(platformdirs.user_data_dir(appname="eveinvoice", appauthor="Tusca", version='1.0'))
holoDirs = dirs/ "hololleak"

requestBackend = SQLiteCache(dirs / 'http_cache.sqlite')
requestSession = CachedSession(backend=requestBackend)
requestEsiHeaders=          {
            "X-Compatibility-Date": "2020-01-01",
            "X-Tenant": "",
            "X-User-Agent": "EveInvoice/1.2.3 (tuscaonine@gmail.com; +https://github.com/tuscaonline/EveInvoice)",
            "Accept": "application/json",
        }