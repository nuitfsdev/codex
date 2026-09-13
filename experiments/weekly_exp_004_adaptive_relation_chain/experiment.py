import argparse, json, math, random, time
from pathlib import Path

RELATIONS = ("left", "right", "front", "behind", "near")

def dist(a,b):
    return math.hypot(a["x"]-b["x"], a["y"]-b["y"])

def holds(o,a,r):
    dx,dy=o["x"]-a["x"],o["y"]-a["y"]
    d=math.hypot(dx,dy)
    if r=="left": return dx < -0.35 and abs(dy) < 2.0
    if r=="right": return dx > 0.35 and abs(dy) < 2.0
    if r=="front": return dy > 0.35 and abs(dx) < 2.0
    if r=="behind": return dy < -0.35 and abs(dx) < 2.0
    return d < 1.7

def relation_score(o,a,r):
    dx,dy=o["x"]-a["x"],o["y"]-a["y"]
    d=math.hypot(dx,dy)
    if r=="left": s=max(0.0,-dx)/(1.0+abs(dy))
    elif r=="right": s=max(0.0,dx)/(1.0+abs(dy))
    elif r=="front": s=max(0.0,dy)/(1.0+abs(dx))
    elif r=="behind": s=max(0.0,-dy)/(1.0+abs(dx))
    else: s=1.0/(0.2+d)
    return 0.7*s + 0.3/(0.5+d)

def make_scene(rng,n=24):
    return [{"id":i,"x":rng.uniform(-5,5),"y":rng.uniform(-5,5)} for i in range(n)]

def ensure_candidates(rng,objs,a,r,exclude=None):
    exclude=exclude or set()
    cs=[o for o in objs if o["id"]!=a["id"] and o["id"] not in exclude and holds(o,a,r)]
    if cs: return cs
    o=rng.choice([x for x in objs if x["id"]!=a["id"] and x["id"] not in exclude])
    if r=="left": o["x"],o["y"]=a["x"]-rng.uniform(.5,1.5),a["y"]+rng.uniform(-.8,.8)
    elif r=="right": o["x"],o["y"]=a["x"]+rng.uniform(.5,1.5),a["y"]+rng.uniform(-.8,.8)
    elif r=="front": o["x"],o["y"]=a["x"]+rng.uniform(-.8,.8),a["y"]+rng.uniform(.5,1.5)
    elif r=="behind": o["x"],o["y"]=a["x"]+rng.uniform(-.8,.8),a["y"]-rng.uniform(.5,1.5)
    else:
        ang,rr=rng.uniform(0,2*math.pi),rng.uniform(.5,1.4)
        o["x"],o["y"]=a["x"]+rr*math.cos(ang),a["y"]+rr*math.sin(ang)
    return [o]

def make_query(rng,objs,two_hop_prob=.45):
    a=rng.choice(objs); r1=rng.choice(RELATIONS)
    c1=sorted(ensure_candidates(rng,objs,a,r1),key=lambda o:relation_score(o,a,r1),reverse=True)[:3]
    b=rng.choice(c1)
    if rng.random()<two_hop_prob:
        r2=rng.choice(RELATIONS)
        c2=sorted(ensure_candidates(rng,objs,b,r2,{a["id"]}),key=lambda o:relation_score(o,b,r2),reverse=True)[:3]
        t=rng.choice(c2)
        return {"seed":a["id"],"required":{a["id"],b["id"],t["id"]},"chain":[r1,r2],"type":"2hop"}
    return {"seed":a["id"],"required":{a["id"],b["id"]},"chain":[r1],"type":"1hop"}

def select_A_full(objs,q): return {o["id"] for o in objs}
def select_B_seed(objs,q): return {q["seed"]}
def select_C_knn(objs,q,k=4):
    a=next(o for o in objs if o["id"]==q["seed"])
    rs=sorted((o for o in objs if o["id"]!=a["id"]),key=lambda o:dist(o,a))
    return {a["id"], *[o["id"] for o in rs[:k]]}
def select_D_chain(objs,q,beam=3):
    selected={q["seed"]}; frontier=[next(o for o in objs if o["id"]==q["seed"])]
    for r in q["chain"]:
        nxt=[]
        for a in frontier:
            rs=sorted((o for o in objs if o["id"] not in selected),key=lambda o:relation_score(o,a,r),reverse=True)[:beam]
            for o in rs: selected.add(o["id"]); nxt.append(o)
        frontier=nxt
        if not frontier: break
    return selected
def select_E_oracle(objs,q): return set(q["required"])

def run(seed=42,scenes=20000,objects_per_scene=24,beam=3):
    rng=random.Random(seed)
    methods={"A_full":select_A_full,"B_seed":select_B_seed,"C_knn4":lambda o,q:select_C_knn(o,q,4),"D_adaptive_chain":lambda o,q:select_D_chain(o,q,beam),"E_oracle":select_E_oracle}
    agg={m:dict(sel=0,seed=0,srec=0,full=0,prec=0,one=0,two=0,oner=0,twor=0) for m in methods}
    t0=time.time()
    for _ in range(scenes):
        objs=make_scene(rng,objects_per_scene); q=make_query(rng,objs); req=q["required"]; sup=req-{q["seed"]}
        for name,fn in methods.items():
            s=fn(objs,q); a=agg[name]; ok=req.issubset(s)
            a["sel"]+=len(s); a["seed"]+=q["seed"] in s; a["srec"]+=len(s&sup)/len(sup); a["full"]+=ok; a["prec"]+=len(s&req)/len(s)
            if q["type"]=="1hop": a["one"]+=1; a["oner"]+=ok
            else: a["two"]+=1; a["twor"]+=ok
    out={}
    for name,a in agg.items():
        avg=a["sel"]/scenes
        out[name]={"avg_selected_objects":avg,"object_reduction_ratio":1-avg/objects_per_scene,"question_entity_coverage":a["seed"]/scenes,"supporting_context_recall":a["srec"]/scenes,"full_required_retention":a["full"]/scenes,"selector_precision_proxy":a["prec"]/scenes,"onehop_retention":a["oner"]/a["one"],"twohop_retention":a["twor"]/a["two"]}
    d,c=out["D_adaptive_chain"],out["C_knn4"]
    passed=d["object_reduction_ratio"]>=.5 and d["question_entity_coverage"]>=.999 and d["supporting_context_recall"]>=.9 and d["full_required_retention"]>=c["full_required_retention"]+.30
    return {"experiment_id":"weekly_exp_004_adaptive_relation_chain","seed":seed,"synthetic_scenes":scenes,"objects_per_scene":objects_per_scene,"two_hop_probability":.45,"beam":beam,"summaries":out,"sanity_acceptance":{"criterion":">=50% object reduction, >=99.9% seed coverage, >=90% support recall, >=30 pp full-retention gain over KNN","passed":passed},"runtime_seconds":time.time()-t0,"status":"SUPPORT_SANITY_ONLY" if passed else "INCONCLUSIVE","real_benchmark_status":"BLOCKED","scope_note":"Synthetic relation-chain retention test only; no ScanQA/SQA3D VLM QA score is claimed."}

def beam_ablation(seed=42,scenes=10000):
    return {str(b):run(seed=seed,scenes=scenes,beam=b)["summaries"]["D_adaptive_chain"] for b in (1,2,3,4)}

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--seed",type=int,default=42); p.add_argument("--scenes",type=int,default=20000); p.add_argument("--beam",type=int,default=3); p.add_argument("--output",default="results/result.json"); a=p.parse_args()
    r=run(a.seed,a.scenes,beam=a.beam); r["beam_ablation"]=beam_ablation(a.seed,10000); Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))
