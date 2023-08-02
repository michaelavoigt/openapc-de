#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv

import openapc_toolkit as oat

parser = argparse.ArgumentParser()
parser.add_argument("xml_file", help="An openCost XML file which should validate against the official openCost XSD schema")
args = parser.parse_args()

articles = None

with open(args.xml_file) as f:
    content = f.read()
    articles = oat.process_opencost_xml(content)

ror_map = {}
with open(oat.INSTITUTIONS_FILE, "r") as ins_file:
    reader = csv.DictReader(ins_file)
    for line in reader:
        ror_map[line["ror_id"]] = line["institution"]

for article in articles:
    ror_id = article["institution_ror"]
    if oat.has_value(ror_id) and ror_id not in ror_map:
        ror_request = oat.get_metadata_from_ror(ror_id)
        if ror_request["success"]:
            ror_map[ror_id] = ror_request["data"]["institution"]
        else:
            oat.print_r(ror_request["error_msg"])
    article["institution"] = ror_map.get(ror_id, "")

fieldnames = ["institution"] + list(oat.OPENCOST_EXTRACTION_FIELDS.keys())
with open("out.csv", "w") as out:
    writer = csv.DictWriter(out, fieldnames)
    writer.writeheader()
    for article in articles:
        writer.writerow(article)
