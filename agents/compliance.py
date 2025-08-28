RISKY = ["guarantee","100%","unlimited","classified"]
def check(text):
    flags = [w for w in RISKY if w.lower() in text.lower()]
    return {"risky_terms": flags, "ok": len(flags)==0}
