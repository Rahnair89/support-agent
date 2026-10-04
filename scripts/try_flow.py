from app.graph import flow

for q in open("evals/questions.txt"):
    q = q.strip()
    if not q:
        continue
    s = flow.invoke({"message": q})
    print(f"\n### {q}\ncategory={s.get('category')} escalate={s.get('escalate')}")
    print(s.get("answer", "(routed straight to a human)"))
    print("sources:", [d["source"] for d in s.get("docs", [])])
