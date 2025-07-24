from collections import UserDict
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

# from .fsd import EveBillOfMaterialRow
from eve_invoice import requestSession

@dataclass
class HoloLeakBillOfMaterialRow:
    materialTypeID: int
    quantity: int


class HoloLeakBillOfMaterials(UserDict[int, list[HoloLeakBillOfMaterialRow]]):
    def __init__(self, obj: dict[str, dict[str, list[dict[str, int]]]]| None=None) -> None:
        self.data = {}
        if obj:
            for keys, item in obj.items():
                if "materials" in item:
                    bill = []
                    for row in item["materials"]:
                        bill.append(HoloLeakBillOfMaterialRow(**row))
                    self.data[int(keys)] = bill
        else:
            r = requestSession.get("https://sde.hoboleaks.space/tq/typematerials.json")
            _bp = r.json()
            if isinstance(_bp, dict):
                for keys, item in _bp.items():
                    if "materials" in item:
                        bill = []
                        for row in item["materials"]:
                            bill.append(HoloLeakBillOfMaterialRow(**row))
                        self.data[int(keys)] = bill


    def __getitem__(self, key: int) -> list[HoloLeakBillOfMaterialRow]:
        if isinstance(key, int):
            if key in self.data:
                return self.data[key]

        raise KeyError(key)


@dataclass
class HoloProduct:
    typeID: int
    quantity: int
    probability: float | None = None


@dataclass
class HoloSkill:
    typeID: int
    level: int


@dataclass
class HoloBP_activites:
    time: timedelta | None = None
    materials: list[HoloLeakBillOfMaterialRow] | None = None

    products: list[HoloProduct] | None = None
    skills: list[HoloSkill] | None = None

    def __post_init__(self):
        if isinstance(self.time, int):
            self.time = timedelta(seconds=self.time)

        if isinstance(self.skills, list):
            _skill = []
            for row in self.skills:
                if isinstance(row, dict):
                    _skill.append(
                        HoloSkill(row["typeID"], row["level"])
                    )
                else:
                    raise TypeError()
            self.skills = _skill

        if isinstance(self.materials, list):
            _matos = []
            for row in self.materials:
                if isinstance(row, dict):
                    _matos.append(
                        HoloLeakBillOfMaterialRow(row["typeID"], row["quantity"])
                    )
                else:
                    raise TypeError()
            self.materials = _matos

        if isinstance(self.products, list):
            _product = []
            for row in self.products:
                _product.append(HoloProduct(**row))  # type: ignore
            self.products = _product


@dataclass
class HoloBP_activities:

    manufacturing: HoloBP_activites | None = None

    invention: HoloBP_activites | None = None
    reaction: HoloBP_activites | None = None
    research_material: HoloBP_activites | None = None
    research_time: HoloBP_activites | None = None
    copying: HoloBP_activites | None = None

    def __post_init__(self):
        if isinstance(self.research_material, dict):
            self.research_material = HoloBP_activites(**self.research_material)
        if isinstance(self.research_time, dict):
            self.research_time = HoloBP_activites(**self.research_time)
        if isinstance(self.copying, dict):
            self.copying = HoloBP_activites(**self.copying)
        if isinstance(self.invention, dict):
            self.invention = HoloBP_activites(**self.invention)
        if isinstance(self.manufacturing, dict):
            self.manufacturing = HoloBP_activites(**self.manufacturing)


@dataclass
class HoloBlueprint:
    activities: HoloBP_activities
    blueprintTypeID: int
    maxProductionLimit: int

    def __post_init__(self):
        if isinstance(self.activities, dict):
            self.activities = HoloBP_activities(**self.activities)


class HoloBlueprints(UserDict[int, HoloBlueprint]):

    def __init__(self, obj: dict[str, Any] | None = None) -> None:
        self.data = {}
        if obj:
            for keys, item in obj.items():
                self.data[int(keys)] = HoloBlueprint(**item)
        else:
            r = requestSession.get("https://sde.hoboleaks.space/tq/blueprints.json")
            _bp = r.json()
            for keys, item in _bp.items():
                self.data[int(keys)] = HoloBlueprint(**item)


    def __getitem__(self, key: int) -> HoloBlueprint:
        if isinstance(key, int):
            if key in self.data:
                return self.data[key]

        raise KeyError(key)
 
