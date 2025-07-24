from dataclasses import dataclass, field
from typing import Any
from eve_invoice import requestSession, requestEsiHeaders, dirs
from .fsd import EveTypes, EveBillOfMaterialRow
from .hololeak import loadHololeakBleuprint
from collections import UserDict
import logging
import zipfile
from io import BytesIO
import yaml
import pickle

log = logging.getLogger(__name__)
fsdTypePickles = dirs / "fsdType.pickle"


class EveBDD:
    """Static Data Export FSD representation"""

    def __init__(self, forcedownload=False):
        if not dirs.exists():
            dirs.mkdir(parents=True)
        # self.fsdTypes:EveTypes = EveTypes()
        self.fsdTypes = self.downloadFsd(forcedownload)

        



    def downloadFsd(self, force=False):
        log.info("fsd.zip download from Eve SDE")
        r = requestSession.get(
            "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/fsd.zip",
            headers={
                "Accept": "application/zip",
            },
        )

        with zipfile.ZipFile(BytesIO(r.content)) as zip:
            # reading types.yaml
            fsdTypes = EveTypes(
                self.__updateFsdFile(zip, "types.yaml", force, r.from_cache)
            )
            # reading typeMaterials
            fsdTypes = self.__readFsdTypeMaterial(self.__updateFsdFile(
                zip, "typeMaterials.yaml", force, r.from_cache,
            ), fsdTypes)


        return fsdTypes


    def __updateFsdFile(self, zip: zipfile, name: str, force: bool, cache: bool) -> Any:
        pickleFile = dirs / (name + ".pickle")
        if force or not cache or not pickleFile.exists():
            log.warning(f"Reading Yaml file {name}")
            with zip.open(name, "r") as fd:
                _fsdType = yaml.safe_load(fd)
                # yaml loading is very long so i cached it in pickle File
                with pickleFile.open("wb") as fd:
                    pickle.dump(_fsdType, fd)
        else:
            with pickleFile.open("rb") as fd:
                _fsdType = pickle.load(fd)

        return _fsdType

    def __readFsdTypeMaterial(self, _typeMaterial: dict, fsdTypes: EveTypes):
        for keys, item in _typeMaterial.items():
            if keys in fsdTypes:
                if "materials" in item:
                    fsdTypes[keys].sdeMaterials = [
                        EveBillOfMaterialRow(**x) for x in item['materials']
                    ]
        return fsdTypes




class Sde:
    """Static Data Export representation"""
