"""Post sample test data to all 4 DAQ endpoints to populate the database.

This script creates sample records for:
- Analytical Conditions
- Element Information
- Channel Information
- Attenuator Information

Run this before running integration.py to populate the database with test data.
"""

from __future__ import annotations

import argparse
import json
import logging
import requests
from typing import Dict, Any

DEFAULT_BASE_URL = "http://localhost:8000"


def post_data(base_url: str, endpoint: str, payload: Dict[str, Any], timeout: float = 5.0) -> Dict[str, Any]:
	"""POST data to an endpoint and return the response."""
	url = base_url.rstrip("/") + endpoint
	try:
		resp = requests.post(url, json=payload, timeout=timeout)
	except Exception as e:
		return {"success": False, "error": f"Request failed: {e}"}

	if resp.status_code not in (200, 201):
		return {"success": False, "status_code": resp.status_code, "text": resp.text}

	try:
		data = resp.json()
	except Exception as e:
		return {"success": False, "error": f"Invalid JSON response: {e}", "text": resp.text}

	return {"success": True, "data": data}


def populate_analytical_conditions(base_url: str) -> None:
	"""POST sample analytical condition data."""
	logging.info("Posting analytical conditions...")
	
	payload = {
		"records": [
			{
				"analytical_group": "LAS 2023",
				"analytical_method": "integration Mode",
				"seq": {
					"purge": {"seq1": "30"},
					"source": {
						"seq1": "3 Peak Spark",
						"seq2": "Normal Spark",
						"seq3": "Lamp",
						"clean": "Cleaning"
					},
					"preburn": {"seq1": "10", "seq2": "20", "seq3": "15", "clean": "Pulse"},
					"integ": {"seq1": "50", "seq2": "60", "seq3": "55", "clean": "Pulse"},
					"clean": {"value": "5", "unit": "Pulse"}
				},
				"level_out_information": {
					"monitor_element": {
						"element": "FE",
						"value": "100.0",
						"option1": "C",
						"option2": "Si"
					},
					"h_level_percent": ["95", "96", "97", "98", "99", "100", "101", "102", "103"],
					"l_level_percent": ["80", "81", "82", "83", "84", "85", "86", "87", "88"]
				}
			}
		]
	}
	
	res = post_data(base_url, "/api/analytical-conditions/bulk", payload)
	if res.get("success"):
		logging.info(f"✓ Analytical conditions posted: {res['data'].get('message', 'OK')}")
	else:
		logging.error(f"✗ Failed to post analytical conditions: {res}")


def populate_element_information(base_url: str) -> None:
	"""POST sample element information data."""
	logging.info("Posting element information...")
	
	payload = {
		"records": [
			{
				"analytical_group": "LAS 2023",
				"page": "element_information",
				"ch_value": "22",
				"elements": [
					{
						"ele_name": "Fe",
						"analytical_range_min": "0.001",
						"analytical_range_max": "99.999",
						"asterisk": "*",
						"chemic_ele": "FE",
						"element": "Iron"
					},
					{
						"ele_name": "C",
						"analytical_range_min": "0.001",
						"analytical_range_max": "5.000",
						"asterisk": "",
						"chemic_ele": "C",
						"element": "Carbon"
					},
					{
						"ele_name": "Si",
						"analytical_range_min": "0.001",
						"analytical_range_max": "3.000",
						"asterisk": "",
						"chemic_ele": "SI",
						"element": "Silicon"
					}
				]
			}
		]
	}
	
	res = post_data(base_url, "/api/element-information/bulk", payload)
	if res.get("success"):
		logging.info(f"✓ Element information posted: {res['data'].get('message', 'OK')}")
	else:
		logging.error(f"✗ Failed to post element information: {res}")


def populate_channel_information(base_url: str) -> None:
	"""POST sample channel information data."""
	logging.info("Posting channel information...")
	
	payload = {
		"records": [
			{
				"analytical_group": "LAS 2023",
				"page": "channel_information",
				"channels": [
					{
						"ele_name": "Fe",
						"w_lengh": "259.940",
						"seq": "1",
						"w_no": "1",
						"interval_element": "Ar",
						"interval_value": "0.015"
					},
					{
						"ele_name": "C",
						"w_lengh": "193.091",
						"seq": "2",
						"w_no": "",
						"interval_element": "Fe",
						"interval_value": "0.020"
					},
					{
						"ele_name": "Si",
						"w_lengh": "251.611",
						"seq": "3",
						"w_no": "2",
						"interval_element": "Fe",
						"interval_value": "0.025"
					}
				]
			}
		]
	}
	
	res = post_data(base_url, "/api/channel-information/bulk", payload)
	if res.get("success"):
		logging.info(f"✓ Channel information posted: {res['data'].get('message', 'OK')}")
	else:
		logging.error(f"✗ Failed to post channel information: {res}")


def populate_attenuator_information(base_url: str) -> None:
	"""POST sample attenuator information data."""
	logging.info("Posting attenuator information...")
	
	payload = {
		"records": [
			{
				"analytical_group": "LAS 2023",
				"page": "attenuator_information",
				"left_table": [
					{
						"element": "FE",
						"ele_value": "259.940",
						"att_value": "0"
					},
					{
						"element": "C",
						"ele_value": "193.091",
						"att_value": "2"
					},
					{
						"element": "SI",
						"ele_value": "251.611",
						"att_value": "1"
					}
				],
				"right_table": [
					{
						"element": "FE",
						"ele_value": "259.940",
						"att_value": "1"
					},
					{
						"element": "MN",
						"ele_value": "257.610",
						"att_value": "0"
					}
				]
			}
		]
	}
	
	res = post_data(base_url, "/api/attenuator-information/bulk", payload)
	if res.get("success"):
		logging.info(f"✓ Attenuator information posted: {res['data'].get('message', 'OK')}")
	else:
		logging.error(f"✗ Failed to post attenuator information: {res}")


def main() -> int:
	parser = argparse.ArgumentParser(description="Populate test data to DAQ endpoints")
	parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL of the DAQ backend")
	args = parser.parse_args()

	logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

	logging.info(f"Populating test data to {args.base_url}")
	
	try:
		populate_analytical_conditions(args.base_url)
		populate_element_information(args.base_url)
		populate_channel_information(args.base_url)
		populate_attenuator_information(args.base_url)
		
		logging.info("✓ All test data posted successfully!")
		return 0
	except Exception as e:
		logging.error(f"✗ Error populating data: {e}")
		return 1


if __name__ == "__main__":
	raise SystemExit(main())
