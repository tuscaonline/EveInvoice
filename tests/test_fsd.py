from eve_invoice import load
from eve_invoice.bom import Bom

def test_loadFsd():
    fsd = load.loadFsd()

    vulture =Bom("Ferox", 1 ,fsd)


    ...