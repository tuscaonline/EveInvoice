
from typing import Self

import pandas as pd
from eve_invoice.fsd import EveTypes


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
