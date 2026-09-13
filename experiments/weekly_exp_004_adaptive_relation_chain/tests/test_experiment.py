import importlib.util
from pathlib import Path

p=Path(__file__).parents[1]/"experiment.py"
spec=importlib.util.spec_from_file_location("exp",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_relation_holds():
    a={"id":0,"x":0.0,"y":0.0}
    assert m.holds({"id":1,"x":-1.0,"y":0.0},a,"left")
    assert m.holds({"id":1,"x":1.0,"y":0.0},a,"right")

def test_chain_keeps_seed():
    objs=[{"id":0,"x":0.0,"y":0.0},{"id":1,"x":1.0,"y":0.0},{"id":2,"x":2.0,"y":0.0}]
    q={"seed":0,"required":{0,1,2},"chain":["right","right"],"type":"2hop"}
    assert 0 in m.select_D_chain(objs,q,beam=1)

def test_determinism():
    a=m.run(seed=7,scenes=500,beam=3)
    b=m.run(seed=7,scenes=500,beam=3)
    assert a["summaries"]==b["summaries"]

if __name__=="__main__":
    test_relation_holds(); test_chain_keeps_seed(); test_determinism(); print("3 tests passed")
