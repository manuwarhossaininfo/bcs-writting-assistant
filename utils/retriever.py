import json, re

def load_institutions(path="data/institutions.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def tokenize(text):
    return set(re.findall(r"[a-zA-Z\u0980-\u09FF]+", text.lower()))

def retrieve_relevant(text, institutions, top_k=8):
    q = tokenize(text)
    scored = []
    for inst in institutions:
        pool = " ".join([inst.get("name_bn",""), inst.get("name_en",""),
                          " ".join(inst.get("keywords", [])), inst.get("role","")])
        score = len(q & tokenize(pool))
        if score > 0:
            scored.append((score, inst))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [i for _, i in scored[:top_k]]