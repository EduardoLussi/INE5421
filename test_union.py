from AF import AF
from afd_operations import intersection, union
from pathlib import Path


def test_union():
    root = Path(__file__).parent
    af1 = AF(name="A1")
    af1.readData(root / "testes/afd1.txt")
    af2 = AF(name="A2")
    af2.readData(root / "testes/afd2.txt")
    union_af = union(af2, af1)
    print("AFD1:")
    af1.plot()
    print("AFD2:")
    af2.plot()
    print("Union:")
    union_af.plot()

def test_intersection():
    root = Path(__file__).parent
    af1 = AF(name="A1")
    af1.readData(root / "testes/afd1.txt")
    af2 = AF(name="A2")
    af2.readData(root / "testes/afd2.txt")
    inter_af = intersection(af2, af1)
    print("AFD1:")
    af1.plot()
    print("AFD2:")
    af2.plot()
    print("Intersection:")
    inter_af.plot()


test_union()