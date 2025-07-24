from eve_invoice.hololeak import HoloBlueprint
from datetime import timedelta

 

def test_holobp():
    bp = {
        "activities": {
            "research_material": {"time": 5250},
            "research_time": {"time": 5250},
            "reaction": {
                "skills": [{"typeID": 45746, "level": 1}],
                "materials": [
                    {"typeID": 4246, "quantity": 5},
                    {"typeID": 16633, "quantity": 100},
                    {"typeID": 16635, "quantity": 100},
                ],
            },
            "manufacturing": {
                "skills": [{"typeID": 3380, "level": 1}],
                "materials": [
                    {"typeID": 34, "quantity": 2800000},
                    {"typeID": 35, "quantity": 1000000},
                    {"typeID": 36, "quantity": 180000},
                    {"typeID": 37, "quantity": 20000},
                    {"typeID": 38, "quantity": 8000},
                    {"typeID": 39, "quantity": 2000},
                    {"typeID": 40, "quantity": 400},
                ],
                "products": [{"typeID": 16227, "quantity": 1}],
                "time": 15000,
            },
            "invention": {
                "skills": [
                    {"typeID": 11452, "level": 1},
                    {"typeID": 11454, "level": 1},
                    {"typeID": 21790, "level": 1},
                ],
                "materials": [
                    {"typeID": 20424, "quantity": 16},
                    {"typeID": 25887, "quantity": 16},
                ],
                "products": [{"typeID": 22447, "probability": 0.26, "quantity": 1}],
                "time": 160200,
            },
            "copying": {"time": 12000},
        },
        "blueprintTypeID": 16228,
        "maxProductionLimit": 10,
    }

    test = HoloBlueprint(**bp)
    assert test.activities.copying.time == timedelta(seconds=12000)
    assert test.activities.research_material.time == timedelta(seconds=5250)
    assert test.activities.research_time.time == timedelta(seconds=5250)
    assert test.activities.invention
    assert test.activities.invention.time == timedelta(seconds=160200)
    assert test.activities.invention.materials

    assert test.activities.invention.materials[0].materialTypeID == 20424
    assert test.activities.invention.materials[0].quantity == 16
    assert test.activities.invention.products

    assert test.activities.invention.products[0].typeID == 22447
    assert test.activities.invention.products[0].probability == 0.26
    assert test.activities.invention.products[0].quantity == 1
    assert test.activities.reaction

    assert test.activities.manufacturing
    assert test.activities.manufacturing.materials
    assert test.activities.manufacturing.materials[0].materialTypeID == 34
    assert test.activities.manufacturing.materials[0].quantity == 2800000
    assert test.activities.manufacturing.products

    assert test.activities.manufacturing.products[0].typeID == 16227
    assert test.activities.manufacturing.products[0].probability == None
    assert test.activities.manufacturing.products[0].quantity == 1

    ...
