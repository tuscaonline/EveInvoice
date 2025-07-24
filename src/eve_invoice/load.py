import yaml
from pathlib import Path
from eve_invoice import fsd, holoDirs
from .hololeak import HoloBlueprints, HoloLeakBillOfMaterials
import functools
import platformdirs
import pickle
import json
from more_itertools import first
from eve_invoice.esi import EsiMarket
import logging

log = logging.getLogger(__name__)

dirs = Path(
    platformdirs.user_data_dir(appname="eveinvoice", appauthor="Tusca", version="1.0")
)
pickleFsd = dirs / "fsd.pickle"


def fsdLoadType(update=False):
    pickleEveTypes = dirs / "fsdtypes.pickle"
    if pickleEveTypes.exists() and not update:
        with pickleEveTypes.open("rb") as fd:
            _type = pickle.load(fd)
    else:
        _type = yaml.full_load(Path("fsd/types.yaml").open("r", encoding="UTF-8"))
        with pickleEveTypes.open("wb") as fd:
            pickle.dump(_type, fd)
    return fsd.EveTypes(_type)


def fsdLoadTypeMaterials(update=False):
    pickleEvMaterials = dirs / "fsdtypeMaterials.pickle"
    if pickleEvMaterials.exists() and not update:
        with pickleEvMaterials.open("rb") as fd:
            _type = pickle.load(fd)
    else:
        _type = yaml.full_load(
            Path("fsd/typeMaterials.yaml").open("r", encoding="UTF-8")
        )
        with pickleEvMaterials.open("wb") as fd:
            pickle.dump(_type, fd)

    return fsd.EveBillOfMaterials(_type)


def loadFsdFromFiles(update=False):
    if not dirs.exists():
        dirs.mkdir(parents=True)
    log.warning("loadFsd")
    fsdTypes = fsdLoadType(update)
    # import le materiel de la SDE
    log.warning("fsdTypeMaterials")

    fsdTypeMaterials = fsdLoadTypeMaterials(update)
    for keys, item in fsdTypeMaterials.items():
        if keys in fsdTypes:
            fsdTypes[keys].sdeMaterials = item

    holoLeakMaterial = HoloLeakBillOfMaterials()
    for keys, item in holoLeakMaterial.items():
        if keys in fsdTypes:
            fsdTypes[keys].hololeakMaterials = item

    # lecture des blueprint hololeak
    holoLeakBP = HoloBlueprints()
    for keys, item in holoLeakBP.items():
        if keys in fsdTypes:
            fsdTypes[keys].hololeakBluePrint = item

    # association des BP au produit d'origine
    log.warning("AsssoBP")

    bps = filter(lambda y: y.hololeakBluePrint, fsdTypes.values())
    for eveType in bps:
        if eveType.hololeakBluePrint:
            if eveType.hololeakBluePrint.activities:
                if eveType.hololeakBluePrint.activities.manufacturing:
                    if eveType.hololeakBluePrint.activities.manufacturing.products:
                        product = first(
                            eveType.hololeakBluePrint.activities.manufacturing.products,
                            None,
                        )
                        if product:
                            if product.typeID in fsdTypes:
                                fsdTypes[product.typeID].bluePrintId = (
                                    eveType.hololeakBluePrint.blueprintTypeID
                                )
                                fsdTypes[product.typeID].hololeakBluePrint = (
                                    eveType.hololeakBluePrint
                                )

    marketPrice = EsiMarket()
    for keys, item in marketPrice.items():
        if keys in fsdTypes:
            fsdTypes[keys].esiMarket = item

    return fsdTypes


def loadFsd(renew: bool = False) -> fsd.EveTypes:

    return loadFsdFromFiles(renew)
