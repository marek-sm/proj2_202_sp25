from __future__ import annotations
import sys
import csv
from typing import *
from dataclasses import dataclass
import math

sys.setrecursionlimit(10_000)


# Put your data definitions first!
@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: Optional[float]
    electricity_and_heat_co2_emissions_per_capita: Optional[float]
    energy_co2_emissions: Optional[float]
    energy_co2_emissions_per_capita: Optional[float]
    total_co2_emissions_excluding_lucf: Optional[float]
    total_co2_emissions_excluding_lucf_per_capita: Optional[float]

@dataclass(frozen=True)
class Node:
    value: Row
    next: Optional[Node]
# ...

# Then your functions.
def parse_row(fields: list[str]) -> Row:
    # Parses (and returns) a row from the given CSV file.
    return Row(
        country=fields[0],
        year=int(fields[1]),
        electricity_and_heat_co2_emissions=None if fields[2] == "" else float(fields[2]),
        electricity_and_heat_co2_emissions_per_capita=None if fields[3] == "" else float(fields[3]),
        energy_co2_emissions=None if fields[4] == "" else float(fields[4]),
        energy_co2_emissions_per_capita=None if fields[5] == "" else float(fields[5]),
        total_co2_emissions_excluding_lucf=None if fields[6] == "" else float(fields[6]),
        total_co2_emissions_excluding_lucf_per_capita=None if fields[7] == "" else float(fields[7]),
    )

def read_csv_lines(filename: str) -> Optional[Node]:
    # Reads a CSV file and recursively builds a linked list of Rows.

    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        if header != [
            "country",
            "year",
            "electricity_and_heat_co2_emissions",
            "electricity_and_heat_co2_emissions_per_capita",
            "energy_co2_emissions",
            "energy_co2_emissions_per_capita",
            "total_co2_emissions_excluding_lucf",
            "total_co2_emissions_excluding_lucf_per_capita",
        ]:
            raise ValueError(f"Invalid header: {header}")
        rows = list(reader)

    def build(i: int) -> Optional[Node]:
        # Constructs the linked list of Rows from the given CSV file, starting at index i.
        if i == len(rows):
            return None
        return Node(parse_row(rows[i]), build(i+1))
    
    return build(0)


def listlen(data: Optional[Node]) -> int:
    # Recursively counts and returns the number of rows in the passed linked list.
    if data is None:
        return 0
    return 1 + listlen(data.next)


def filter_rows(
        data: Optional[Node],
        field_name: str,
        comparison: str,
        value: Union[str, float, int]
) -> Optional[Node]:
    # Recursively filters a given linked list, given a query.

    def matches(r: Row) -> bool:
        # Checks if a row fits the query requirements
        field_value = getattr(r, field_name) # Automatically raises an AttributeError if field_name isn't a real attribute on the Row
        if field_value is None:
            return False
        if field_name == "country" and comparison != "equal":
            raise ValueError(f'Country field can only be "equal"')
        if comparison == "equal":
            return field_value == value
        if comparison == "less_than":
            return field_value < value
        if comparison == "greater_than":
            return field_value > value
        raise ValueError("Not a valid comparison")
    
    if data is None:
        return None
    rest = filter_rows(data.next, field_name, comparison, value)
    if matches(data.value):
        return Node(data.value, rest)
    return rest
# ...