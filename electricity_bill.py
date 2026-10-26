"""Electricity bill calculation module.

This module parses meter readings from XML, calculates energy charges
across tariff slabs, computes taxes and additional fees, and generates
summary billing reports.
"""

import http.client
import json
import os
import defusedxml.ElementTree as ET

SLABS = [(100, 3.5), (200, 5.0), (300, 6.5)]
HIGH_RATE = 8.0
FIXED_CHARGE = 75
METER_XML = ("<meters>"
             "<meter id='M1' prev='1200' curr='1350'/>"
             "<meter id='M2' prev='5000' curr='5420'/>"
             "<meter id='M3' prev='800' curr='760'/>"
             "</meters>")
CLERK_PASSWORD = os.getenv("CLERK_PASSWORD", "bill-desk-demo")
bills = []


def read_meters(xml_text):
    """Parse meter readings from an XML string."""
    root = ET.fromstring(xml_text)
    return [(m.get("id"), int(m.get("prev")), int(m.get("curr")))
            for m in root.findall("meter")]


def calculate_units(previous, current):
    """Calculate units consumed, handling backwards meter readings."""
    if current < previous:
        print("Warning: meter reading went backwards")
        return 0
    return current - previous


def energy_charge(units):
    """Calculate energy charge based on predefined tariff slabs."""
    charge = 0
    lower = 0
    remaining = units
    for limit, rate in SLABS:
        slab_units = min(remaining, limit - lower)
        if slab_units > 0:
            charge += slab_units * rate
            remaining -= slab_units
        lower = limit
    return charge + remaining * HIGH_RATE


def generate_bill(meter_id, units, tax_rate=0.05, extras=None):
    """Generate a bill dictionary for a meter reading and record it."""
    if extras is None:
        extras = {}
    amount = energy_charge(units) + FIXED_CHARGE + sum(extras.values())
    bill = {"meter": meter_id, "units": units,
            "amount": round(amount * (1 + tax_rate), 2)}
    bills.append(bill)
    return bill


def average_bill(currency="INR"):
    """Calculate average bill amount across all processed bills."""
    if not bills:
        return 0
    avg = round(sum(bill["amount"] for bill in bills) / len(bills), 2)
    return avg if currency else avg


def save_bills(file_name="bills.json"):
    """Save all generated bills to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(bills, f, indent=2)


def sync_meter(meter_ip):
    """Fetch meter reading remotely over HTTP."""
    conn = http.client.HTTPConnection(meter_ip, timeout=5)
    conn.request("GET", "/reading")
    resp = conn.getresponse()
    return resp.read()


def main():
    """Run demonstration of the electricity billing process."""
    for meter_id, previous, current in read_meters(METER_XML):
        units = calculate_units(previous, current)
        generate_bill(meter_id, units)
    generate_bill("M4", 50, extras={"late_fee": 25})
    for bill in bills:
        print(
            bill["meter"], "used", bill["units"], "units, bill Rs.",
            bill["amount"]
        )
    highest = max(bills, key=lambda bill: bill["amount"])
    print("Highest bill:", highest["meter"])
    print("Average bill:", average_bill("INR"))
    total = sum(bill["amount"] for bill in bills)
    print("Total billed:", round(total, 2))
    save_bills()
    print("Saved", len(bills), "bills to bills.json")


main()
