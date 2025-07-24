from eve_invoice.fsd import EveBillOfMaterialRow
from eve_invoice.sde import Sde, EveBDD

def test_fsd_download():
    test = EveBDD()
    assert test.fsdTypes['Ferox'].id == 16227
    assert test.fsdTypes['Ferox'].sdeMaterials is not None
    assert isinstance(test.fsdTypes['Ferox'].sdeMaterials[0], EveBillOfMaterialRow)

    ...