"""Fetch DAQ backend bulk and individual (by ID) endpoints and write combined JSON.

This script requests these endpoints (defaults to localhost:8000):

Bulk endpoints:
- /api/attenuator-information/bulk
- /api/channel-information/bulk
- /api/element-information/bulk
- /api/analytical-conditions/bulk

Individual endpoints (by ID):
- /api/attenuator-information/{id}
- /api/channel-information/{id}
- /api/element-information/{id}
- /api/analytical-conditions/{id}

Workflow:
1. Fetch all bulk endpoints to get all records
2. For each record returned, fetch the individual record by ID
3. Combine all results in `attenuator_info.json`

Run from the `connection` folder:
python integration.py --base-url http://localhost:8000

Output:
A JSON file containing bulk data and individual records retrieved by ID.
If bulk fetch returns no records, individual endpoint fetching is skipped.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any

import requests


DEFAULT_BASE_URL = "http://localhost:8000"
OUTPUT_FILENAME = "attenuator_info.json"
ENDPOINTS = {
	"attenuator_information": {
		"bulk": "/api/attenuator-information/bulk",
		"by_id": "/api/attenuator-information",
	},
	"channel_information": {
		"bulk": "/api/channel-information/bulk",
		"by_id": "/api/channel-information",
	},
	"element_information": {
		"bulk": "/api/element-information/bulk",
		"by_id": "/api/element-information",
	},
	"analytical_conditions": {
		"bulk": "/api/analytical-conditions/bulk",
		"by_id": "/api/analytical-conditions",
	},
}


def fetch_endpoint(base_url: str, path: str, timeout: float = 5.0) -> Dict[str, Any]:
	url = base_url.rstrip("/") + path
	try:
		resp = requests.get(url, timeout=timeout)
	except Exception as e:
		return {"success": False, "error": f"Request failed: {e}"}

	if resp.status_code != 200:
		return {"success": False, "status_code": resp.status_code, "text": resp.text}

	try:
		data = resp.json()
	except Exception as e:
		return {"success": False, "error": f"Invalid JSON response: {e}", "text": resp.text}

	# Many of the bulk endpoints return a wrapper { success, message, count, records }
	# We prefer to store the `records` array when present.
	if isinstance(data, dict) and "records" in data:
		return {"success": True, "records": data.get("records", [])}

	# Otherwise store the whole response
	return {"success": True, "data": data}


def collect_all(base_url: str) -> Dict[str, Any]:
	"""Fetch bulk endpoints, then fetch individual records by ID.
	
	For each endpoint:
	1. Fetch the bulk endpoint to get all records
	2. For each record returned, fetch the individual record by ID
	3. Store both bulk and individual results
	"""
	results: Dict[str, Any] = {}
	
	for endpoint_key, paths in ENDPOINTS.items():
		logging.info(f"Fetching bulk {endpoint_key} from {paths['bulk']}")
		bulk_res = fetch_endpoint(base_url, paths["bulk"])
		
		# Initialize result structure
		results[endpoint_key] = {
			"bulk": bulk_res,
			"by_id": {}
		}
		
		# If bulk fetch was successful and has records, fetch each by ID
		if bulk_res.get("success") and bulk_res.get("records"):
			records = bulk_res["records"]
			logging.info(f"Retrieved {len(records)} {endpoint_key} record(s), fetching each by ID...")
			
			for record in records:
				record_id = record.get("id")
				if record_id:
					individual_path = f"{paths['by_id']}/{record_id}"
					logging.info(f"  Fetching {endpoint_key} ID {record_id}")
					individual_res = fetch_endpoint(base_url, individual_path)
					results[endpoint_key]["by_id"][record_id] = individual_res
		else:
			logging.warning(f"No records returned from bulk {endpoint_key} endpoint")
	
	return results



def write_output_file(output_path: Path, payload: Dict[str, Any]) -> None:
	output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> int:
	parser = argparse.ArgumentParser(description="Fetch DAQ endpoints and write combined JSON")
	parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL of the DAQ backend")
	parser.add_argument("--out", default=OUTPUT_FILENAME, help="Output filename in this folder")
	args = parser.parse_args()

	logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

	script_dir = Path(__file__).resolve().parent
	output_path = script_dir / args.out

	logging.info(f"Collecting data from {args.base_url}")
	payload = collect_all(args.base_url)

	# Add some metadata
	final = {
		"meta": {
			"base_url": args.base_url,
			"source": "integration.py",
		},
		"data": payload,
	}

	try:
		write_output_file(output_path, final)
	except Exception as e:
		logging.error(f"Failed to write output file {output_path}: {e}")
		return 2

	logging.info(f"Wrote collected data to {output_path}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

