"""Fetch DAQ backend bulk endpoints and write combined JSON.

This script requests these endpoints (defaults to localhost:8000):
- /api/attenuator-information/bulk
- /api/channel-information/bulk
- /api/element-information/bulk
- /api/analytical-conditions/bulk

It creates (or overwrites) a file named `attenuator_info.json` in the
same folder as this script containing the collected `records` for each
endpoint. If a request fails, the error is included in the output JSON
under the corresponding key.

Run from the `connection` folder:
python integration.py --base-url http://localhost:8000

Assumptions made:
- The file to write is named `information.json` (JSON extension added).
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any

import requests


DEFAULT_BASE_URL = "http://localhost:8000"
OUTPUT_FILENAME = "information.json"
ENDPOINTS = {
	"attenuator_information": "/api/attenuator-information/bulk",
	"channel_information": "/api/channel-information/bulk",
	"element_information": "/api/element-information/bulk",
	"analytical_conditions": "/api/analytical-conditions/bulk",
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
	results: Dict[str, Any] = {}
	for key, path in ENDPOINTS.items():
		logging.info(f"Fetching {key} from {path}")
		res = fetch_endpoint(base_url, path)
		results[key] = res
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

