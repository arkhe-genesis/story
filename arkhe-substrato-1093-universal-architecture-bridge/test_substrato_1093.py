import pytest
from substrato_1093 import CathedralArchitectureCatalog, ArchitectureParadigm, MaturityLevel, Deity

def test_catalog_initialization():
    catalog = CathedralArchitectureCatalog()
    assert len(catalog.substrates) == 20

def test_get_substrate():
    catalog = CathedralArchitectureCatalog()
    sub = catalog.get("1093.1")
    assert sub is not None
    assert sub.name == "MONOLITHIC_MODULAR"

def test_by_paradigm():
    catalog = CathedralArchitectureCatalog()
    subs = catalog.by_paradigm(ArchitectureParadigm.MICROSERVICES)
    assert len(subs) == 1
    assert subs[0].id == "1093.2"

def test_by_maturity():
    catalog = CathedralArchitectureCatalog()
    subs = catalog.by_maturity(MaturityLevel.CANONIZED)
    assert len(subs) == 11

def test_by_deity():
    catalog = CathedralArchitectureCatalog()
    subs = catalog.by_deity(Deity.HEFESTO)
    assert len(subs) == 7

def test_get_telemetry():
    catalog = CathedralArchitectureCatalog()
    telem = catalog.get_telemetry()
    assert telem["total_architectures"] == 20
    assert telem["module"] == "CathedralArchitectureCatalog"
