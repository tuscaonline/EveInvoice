from eve_invoice import load
from eve_invoice.fsd import Bom

def test_loadFsd():
    fsd = load.loadFsd()

    vulture =Bom("Ferox", 1 ,fsd)


    ...