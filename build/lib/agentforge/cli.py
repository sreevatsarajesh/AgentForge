import argparse
import json
from .engine import execute_tool,list_tools
def main():
    parser=argparse.ArgumentParser(prog="agentforge")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("list")
    run=sub.add_parser("run"); run.add_argument("tool"); run.add_argument("--payload",default="{}")
    args=parser.parse_args()
    if args.command=="list": print(json.dumps(list_tools(),indent=2)); return
    try: payload=json.loads(args.payload); print(json.dumps(execute_tool(args.tool,payload),indent=2,ensure_ascii=False))
    except Exception as e: parser.error(str(e))
if __name__=="__main__": main()
