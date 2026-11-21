import argparse
from procurepilot.models import Request
from procurepilot.crew import run
from procurepilot.storage import save

parser = argparse.ArgumentParser()
parser.add_argument("--no-crew", action="store_true", help="Generate a data-only run; not evidence of CrewAI execution")
parser.add_argument("--url", action="append", default=[])
parser.add_argument("--approve-domain", action="append", default=[])
parser.add_argument("--request-json")
args = parser.parse_args()
request = Request.model_validate_json(open(args.request_json).read()) if args.request_json else Request()
result = run(request, seed_urls=args.url, approved_domains=set(args.approve_domain), run_crew=not args.no_crew)
save(result)
print(result.model_dump_json(indent=2))
