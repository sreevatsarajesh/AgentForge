import json
from pathlib import Path
from agentforge.engine import execute_tool,list_tools
from agentforge.registry import TOOLS
def test_exactly_100_tools():
    assert len(TOOLS)==100
    assert len(list_tools())==100
def test_ten_domains_with_ten_tools_each():
    counts={}
    for tool in TOOLS.values(): counts[tool["category"]]=counts.get(tool["category"],0)+1
    assert len(counts)==10
    assert set(counts.values())=={10}
def test_compound_interest():
    result=execute_tool("productivity_compound_interest",{"principal":1000,"annual_rate":5,"years":1,"compounds_per_year":1})
    assert result["result"]["future_value"]==1050
def test_break_even():
    result=execute_tool("business_break_even_calculator",{"fixed_costs":1000,"unit_price":50,"variable_cost_per_unit":30})
    assert result["result"]["break_even_units"]==50
def test_csv_profile():
    result=execute_tool("data_csv_profiler",{"csv":"name,age\nAda,36\nLin,29\n"})
    assert result["result"]["row_count"]==2
    assert result["result"]["columns"]==["name","age"]
def test_json_validation():
    assert execute_tool("data_json_validator",{"json":"{\"ok\":true}"})["result"]["valid"] is True
    assert execute_tool("data_json_validator",{"json":"{"})["result"]["valid"] is False
def test_python_ast():
    result=execute_tool("coding_python_ast_summary",{"code":"import os\ndef run():\n return 1\nclass A: pass"})
    assert result["result"]["functions"]==["run"]
    assert result["result"]["classes"]==["A"]
def test_every_tool_has_skill_file():
    root=Path(__file__).resolve().parents[1]
    for item in TOOLS.values(): assert (root/item["skill_path"]).is_file()
def test_registry_count_matches_skill_count():
    root=Path(__file__).resolve().parents[1]
    assert len(list((root/"skills").rglob("SKILL.md")))==100
