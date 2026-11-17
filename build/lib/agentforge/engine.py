import ast
import csv
import io
import json
import math
import re
import statistics
import tomllib
from datetime import date,timedelta
from .registry import TOOLS
def _text(p):
    return str(p.get("text",p.get("content",p.get("source",p.get("notes","")))))
def _lines(s):
    return [x.strip() for x in s.splitlines() if x.strip()]
def _csv(p):
    return list(csv.DictReader(io.StringIO(str(p.get("csv",p.get("text",""))))))
def _result(name,output,**extra):
    return {"tool":name,"result":output,**extra}
def _number(p,key,default=0):
    try: return float(p.get(key,default))
    except (TypeError,ValueError): raise ValueError(f"{key} must be numeric")
def _template(spec,p):
    source=_text(p)
    audience=p.get("audience","the intended audience")
    goal=p.get("goal",spec["description"])
    return _result(spec["tool_name"],{"title":spec["title"],"objective":goal,"audience":audience,"source_material":source,"deliverable_sections":["Purpose and context","Key information and evidence","Main output","Assumptions and limitations","Recommended next actions"],"workflow":["Clarify the desired outcome","Organize supplied facts","Draft the deliverable","Check completeness and consistency","Flag assumptions and unresolved questions"],"note":"This local workflow scaffold does not call an external language model. An AI agent can use the accompanying skill instructions to complete the generative work."})
def execute_tool(name,payload=None):
    p=payload or {}
    if not isinstance(p,dict): raise ValueError("payload must be a JSON object")
    spec=TOOLS.get(name)
    if not spec: raise ValueError(f"Unknown tool: {name}")
    s=_text(p)
    if name=="data_csv_profiler":
        rows=_csv(p)
        cols=list(rows[0]) if rows else []
        profile={c:{"missing":sum(not str(r.get(c,"" )).strip() for r in rows),"unique":len({r.get(c) for r in rows}),"sample":list(dict.fromkeys(r.get(c) for r in rows))[:5]} for c in cols}
        return _result(name,{"row_count":len(rows),"columns":cols,"profile":profile})
    if name=="data_csv_filter":
        rows=_csv(p); col=str(p.get("column","")); val=str(p.get("equals","")); out=[r for r in rows if str(r.get(col,""))==val]
        return _result(name,out,row_count=len(out))
    if name=="data_csv_aggregate":
        rows=_csv(p); group=str(p.get("group_by","")); col=str(p.get("value_column","")); op=str(p.get("operation","sum")); groups={}
        for r in rows:
            key=r.get(group,"(blank)"); groups.setdefault(key,[]);
            if op=="count": groups[key].append(1)
            else:
                try: groups[key].append(float(r.get(col,"")))
                except ValueError: continue
        out={k:(len(v) if op=="count" else (sum(v) if op=="sum" else statistics.mean(v) if v else 0)) for k,v in groups.items()}
        return _result(name,out,operation=op)
    if name=="data_csv_to_json": return _result(name,_csv(p))
    if name=="data_json_validator":
        try:
            obj=json.loads(str(p.get("json",s))); return _result(name,{"valid":True,"type":type(obj).__name__,"top_level_keys":list(obj)[:100] if isinstance(obj,dict) else None,"items":len(obj) if isinstance(obj,(list,dict)) else None})
        except json.JSONDecodeError as e: return _result(name,{"valid":False,"error":e.msg,"line":e.lineno,"column":e.colno})
    if name=="data_json_to_csv":
        obj=json.loads(str(p.get("json",s)))
        if not isinstance(obj,list) or (obj and not all(isinstance(x,dict) for x in obj)): raise ValueError("JSON input must be an array of objects")
        fields=list(dict.fromkeys(k for row in obj for k in row)); out=io.StringIO(); w=csv.DictWriter(out,fieldnames=fields); w.writeheader(); w.writerows(obj); return _result(name,out.getvalue())
    if name=="data_deduplicate_rows":
        rows=_csv(p); seen=set(); out=[]
        for r in rows:
            key=tuple(sorted(r.items()))
            if key not in seen: seen.add(key); out.append(r)
        return _result(name,out,removed=len(rows)-len(out))
    if name=="data_normalize_headers":
        raw=str(p.get("csv",s)); reader=csv.reader(io.StringIO(raw)); allrows=list(reader)
        if not allrows: return _result(name,"")
        headers=[re.sub(r"[^a-z0-9]+","_",x.strip().lower()).strip("_") for x in allrows[0]]; out=io.StringIO(); w=csv.writer(out); w.writerow(headers); w.writerows(allrows[1:]); return _result(name,out.getvalue())
    if name=="data_text_to_csv":
        lines=_lines(s); delimiter=str(p.get("delimiter","|")); rows=[x.split(delimiter) for x in lines]; out=io.StringIO(); csv.writer(out).writerows(rows); return _result(name,out.getvalue())
    if name=="data_statistics_summary":
        vals=p.get("values"); vals=[float(x) for x in (vals if isinstance(vals,list) else re.findall(r"-?\d+(?:\.\d+)?",s))]
        if not vals: raise ValueError("Provide a non-empty numeric values list")
        return _result(name,{"count":len(vals),"mean":statistics.mean(vals),"median":statistics.median(vals),"min":min(vals),"max":max(vals),"stdev":statistics.stdev(vals) if len(vals)>1 else 0})
    if name=="coding_python_ast_summary":
        try: tree=ast.parse(str(p.get("code",s))); return _result(name,{"imports":[n.names[0].name for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom)) and n.names],"functions":[n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))],"classes":[n.name for n in ast.walk(tree) if isinstance(n,ast.ClassDef)],"lines":len(str(p.get("code",s)).splitlines())})
        except SyntaxError as e: return _result(name,{"valid":False,"error":e.msg,"line":e.lineno,"offset":e.offset})
    if name=="coding_regex_tester":
        pattern=str(p.get("pattern","")); flags=re.I if p.get("ignore_case") else 0; matches=[{"match":m.group(0),"start":m.start(),"end":m.end()} for m in re.finditer(pattern,s,flags)]; return _result(name,matches,count=len(matches))
    if name=="coding_dependency_inventory":
        code=str(p.get("code",s)); imports=sorted(set(re.findall(r"^\s*(?:from|import)\s+([A-Za-z_][\w.]*)",code,re.M))); return _result(name,{"imports":imports,"count":len(imports)})
    if name=="coding_config_validator":
        fmt=str(p.get("format","json")).lower()
        try: obj=json.loads(s) if fmt=="json" else tomllib.loads(s) if fmt=="toml" else None
        except Exception as e: return _result(name,{"valid":False,"error":str(e)})
        if obj is None: raise ValueError("Supported formats: json, toml")
        return _result(name,{"valid":True,"type":type(obj).__name__,"keys":list(obj) if isinstance(obj,dict) else None})
    if name=="productivity_compound_interest":
        principal=_number(p,"principal"); rate=_number(p,"annual_rate")/100; years=_number(p,"years"); freq=_number(p,"compounds_per_year",1); future=principal*(1+rate/freq)**(freq*years); return _result(name,{"future_value":round(future,2),"interest_earned":round(future-principal,2),"assumptions":{"annual_rate_percent":rate*100,"compounds_per_year":freq,"years":years}})
    if name=="productivity_loan_calculator":
        principal=_number(p,"principal"); annual=_number(p,"annual_rate")/1200; months=int(_number(p,"months")); payment=principal/months if annual==0 else principal*annual/(1-(1+annual)**(-months)); return _result(name,{"monthly_payment":round(payment,2),"total_paid":round(payment*months,2),"total_interest":round(payment*months-principal,2)})
    if name=="business_break_even_calculator":
        fixed=_number(p,"fixed_costs"); price=_number(p,"unit_price"); variable=_number(p,"variable_cost_per_unit"); margin=price-variable
        if margin<=0: raise ValueError("Unit price must exceed variable cost")
        units=math.ceil(fixed/margin); return _result(name,{"contribution_per_unit":margin,"break_even_units":units,"break_even_revenue":round(units*price,2)})
    if name=="business_pricing_calculator":
        cost=_number(p,"unit_cost"); margin=_number(p,"target_margin_percent")/100
        if not 0<=margin<1: raise ValueError("Target margin must be between 0 and 100")
        price=cost/(1-margin); return _result(name,{"suggested_price":round(price,2),"gross_profit":round(price-cost,2),"gross_margin_percent":margin*100,"markup_percent":(price-cost)/cost*100 if cost else None})
    if name=="learning_spaced_repetition":
        start=date.fromisoformat(str(p.get("start_date",date.today().isoformat()))); intervals=[1,3,7,14,30,60]; return _result(name,[{"review":i+1,"date":(start+timedelta(days=d)).isoformat(),"days_after_start":d} for i,d in enumerate(intervals)])
    if name=="productivity_expense_categorizer":
        rules={"housing":["rent","mortgage","utility"],"transport":["uber","taxi","fuel","bus","train"],"food":["restaurant","grocery","coffee","food"],"health":["pharmacy","doctor","clinic"],"subscriptions":["subscription","netflix","spotify"],"shopping":["store","purchase","amazon"]}; rows=[]
        for line in _lines(s):
            low=line.lower(); cat=next((k for k,v in rules.items() if any(x in low for x in v)),"uncategorized"); rows.append({"item":line,"category":cat})
        return _result(name,rows)
    if name=="learning_concept_explainer":
        topic=str(p.get("topic",s)); level=str(p.get("level","beginner")); return _result(name,{"topic":topic,"level":level,"explanation_framework":["One-sentence definition","Why it matters","How it works step by step","Concrete example","Common misconception","Quick self-check"],"note":"Add subject-specific facts using a trusted source or an AI model; this scaffold does not invent an explanation."})
    if name=="learning_flashcard_generator":
        lines=_lines(s); cards=[]
        for line in lines:
            if ":" in line:
                q,a=line.split(":",1); cards.append({"front":q.strip(),"back":a.strip()})
            elif " - " in line:
                q,a=line.split(" - ",1); cards.append({"front":q.strip(),"back":a.strip()})
        return _result(name,cards if cards else {"source_text":s,"instruction":"Convert each key concept into one atomic question and answer; do not add facts absent from the source."})
    if name=="learning_quiz_generator":
        return _result(name,{"source_text":s,"question_types":["multiple choice","true or false","short answer","application scenario"],"recommended_mix":{"multiple_choice":5,"true_false":3,"short_answer":2},"answer_key_required":True})
    if name=="coding_sql_query_helper":
        question=str(p.get("question",s)); table=str(p.get("table","your_table")); cols=p.get("columns",[]); return _result(name,{"question":question,"schema":{"table":table,"columns":cols},"sql_draft":"SELECT * FROM "+table+";","safety":"Use parameterized values and verify table and column names before execution."})
    if name=="data_csv_aggregate" and str(p.get("operation","sum")) not in {"sum","avg","count"}: raise ValueError("operation must be sum, avg or count")
    if name=="productivity_mindfulness_exercise":
        duration=int(_number(p,"minutes",3)); duration=max(1,min(duration,10)); return _result(name,["Sit comfortably and notice your surroundings.","Breathe gently without forcing or holding your breath.","Notice sensations and thoughts without judging them.","Return attention to the next breath when distracted.","Finish by noticing one thing you can do next."],duration_minutes=duration)
    if name=="productivity_workout_planner":
        days=int(_number(p,"days_per_week",3)); days=max(1,min(days,5)); return _result(name,{"days_per_week":days,"schedule":[{"day":i+1,"session":["warm-up","comfortable strength or cardio activity","cool-down"]} for i in range(days)],"safety":"Adjust to your ability, stop if you feel pain or unwell, and seek professional advice for medical concerns."})
    return _template(spec,p)
def list_tools(category=None):
    return [v for v in TOOLS.values() if category is None or v["category"]==category]
