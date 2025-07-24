from dataclasses import dataclass, field
from eve_invoice import requestSession

from collections import UserDict


@dataclass
class EsiMarketPrice:
    type_id: int| None = None
    adjusted_price: float | None = None
    average_price: float | None = None

class EsiMarket(UserDict[int, EsiMarketPrice]):
    def __init__(self):
        super().__init__()

        url = "https://esi.evetech.net/markets/prices"

        headers = {
            "Accept-Language": "",
            "If-None-Match": "",
            "X-Compatibility-Date": "2020-01-01",
            "X-Tenant": "",
            "Accept": "application/json",
        }
        r = requestSession.get(url, headers=headers)

        _prices = r.json()
        for row in _prices:

            self.data[int(row["type_id"])] = EsiMarketPrice(**row)
        pass
