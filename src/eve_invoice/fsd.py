from collections import UserDict
from dataclasses import dataclass, field
from typing import Self
from .hololeak import HoloLeakBillOfMaterialRow, HoloBlueprint
import json
import pandas as pd
from .esi import EsiMarket

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
    hololeakBluePrint : HoloBlueprint| None = None
    bluePrintId : int | None = None
    esiMarket: EsiMarket|None= None


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


class Bom:
    def __init__(self, name: str|int, qty:int, fsd: EveTypes ):
  
        eqt = fsd[name]
        self.materialId = eqt.id
        self.name = eqt.name.en
        self.qty = qty
        self.bom : list[Self] =[]

        if eqt.hololeakBluePrint:
             if eqt.hololeakBluePrint.activities :
                if eqt.hololeakBluePrint.activities.manufacturing :
                    if eqt.hololeakBluePrint.activities.manufacturing.materials:
                        for row in eqt.hololeakBluePrint.activities.manufacturing.materials:
                            self.bom.append(
                                Bom(row.materialTypeID, row.quantity * self.qty, fsd)
                            )
                 
    def __rich_repr__(self):
        yield "name", self.name
        yield "qty", self.qty
        yield "bom", self.bom

    def __repr__(self):
        return f"{self.name}, qty: {self.qty}, {self.bom}"
    
    def to_json(self):
        _bom = {
            'product': self.name,
            'qty': self.qty,
            
        }
        _bom['bom']=[]
        for row in self.bom:
            _bom["bom"].append(
                {
                    "product": row.name,
                    "qty": row.qty
                }
            )
        return _bom
    
    def toDataframe(self):
        if len(self.bom) <1:
            return None

        index = pd.MultiIndex.from_tuples([('material', x.name )for x in self.bom], names=["Type", "Product"])
        _df =pd.DataFrame(
            columns=index,
            index=[self.name],
            data=[ [x.qty for x in self.bom]]

        )
        _df.insert(0, ("output","qte"), self.qty)
        _dfArray =[]
        _dfArray.append(_df)
        for bom in self.bom:
            _dfArray.append(bom.toDataframe())
        _df=pd.concat(_dfArray)
        _df = _df.drop(columns=[col for col in _df.columns if col[1] in _df.index] )
        return _df

  