from collections import UserDict
from dataclasses import dataclass
from .hololeak import HoloLeakBillOfMaterialRow, HoloBlueprint
import json
from .esi import EsiMarket
from dataclasses import dataclass

from collections import UserDict
import logging

log = logging.getLogger(__name__)


@dataclass
class EveTrade:
    de: str | None = None
    en: str | None = None
    es: str | None = None
    fr: str | None = None
    it: str | None = None
    ja: str | None = None
    ko: str | None = None
    ru: str | None = None
    zh: str | None = None


@dataclass(kw_only=True)
class EveName(EveTrade): ...


@dataclass(kw_only=True)
class EveDesc(EveTrade): ...


@dataclass
class EveBillOfMaterialRow:
    materialTypeID: int
    quantity: int


class EveBillOfMaterials(UserDict[int, list[EveBillOfMaterialRow]]):
    def __init__(self, obj: dict[int, dict[str, list[dict[str, int]]]]) -> None:
        self.data = {}

        for keys, item in obj.items():
            if "materials" in item:
                bill = []
                for row in item["materials"]:
                    bill.append(EveBillOfMaterialRow(**row))
                self.data[keys] = bill

    def __getitem__(self, key: int) -> list[EveBillOfMaterialRow]:
        if isinstance(key, int):
            if key in self.data:
                return self.data[key]

        raise KeyError(key)


@dataclass
class EveType:
    id: int
    groupID: int
    published: bool
    portionSize: int
    name: EveName
    description: EveDesc | None = None

    mass: float | None = None
    volume: float | None = None
    radius: float | None = None
    graphicID: int | None = None
    soundID: int | None = None
    iconID: int | None = None
    raceID: int | None = None
    basePrice: float | None = None
    marketGroupID: int | None = None
    capacity: float | None = None
    metaGroupID: int | None = None
    variationParentTypeID: int | None = None
    factionID: int | None = None
    sofMaterialSetID: int | None = None

    masteries: str | None = None
    traits: str | None = None
    sofFactionName: str | None = None
    sdeMaterials: list[EveBillOfMaterialRow] | None = None
    hololeakMaterials: list[HoloLeakBillOfMaterialRow] | None = None
    hololeakBluePrint: HoloBlueprint | None = None
    bluePrintId: int | None = None
    esiMarket: EsiMarket | None = None

    def __post_init__(self):
        if isinstance(self.name, str):
            self.name = EveName(json.loads(self.name))
        if isinstance(self.name, dict):
            self.name = EveName(**self.name)
        if isinstance(self.description, str):
            self.description = EveDesc(json.loads(self.description))
        if isinstance(self.description, dict):
            self.description = EveDesc(**self.description)

    def getDesc(self):
        if self.description:
            if self.description.fr:
                return self.description.fr
        return None

    def __rich_repr__(self):
        yield "name", self.name.en
        yield "desc", self.getDesc()
        yield "id", self.id
        yield "basePrice ", self.basePrice, True
        yield "Eiv ", self.esiMarket, True

    def _repr_html_(self) -> str:
        return f"""<h4>{self.name.en}</h4>
            <p>{self.getDesc()}</p>"""


class EveTypes(UserDict[int, EveType]):
    def __init__(self, obj: dict[int, dict]) -> None:
        self.data = {}
        self._frName = {}
        for keys, item in obj.items():
            self.data[keys] = EveType(keys, **item)
            self._frName[self.data[keys].name.en] = keys
        pass

    def __getitem__(self, key: int | str) -> EveType:
        if isinstance(key, int):
            if key in self.data:
                return self.data[key]
            ...
        if isinstance(key, str):
            if key in self._frName:
                return self.data[self._frName[key]]

        raise KeyError(key)
