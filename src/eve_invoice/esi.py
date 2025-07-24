from dataclasses import dataclass, field
from eve_invoice import requestSession, requestEsiHeaders

from collections import UserDict
import logging
log  = logging.getLogger(__name__)

@dataclass
class EsiMarketPrice:
    type_id: int| None = None
    adjusted_price: float | None = None
    average_price: float | None = None

class EsiMarket(UserDict[int, EsiMarketPrice]):
    def __init__(self):
        super().__init__()

        url = "https://esi.evetech.net/markets/prices"
        log.info(f'downloading market')


        r = requestSession.get(url, headers=requestEsiHeaders)
        if r.from_cache:        
            log.info(f'using market data from cache')

        _prices = r.json()
        
        for row in _prices:

            self.data[int(row["type_id"])] = EsiMarketPrice(**row)
        pass
