from __future__ import annotations
import sys
import csv
from typing import *
from dataclasses import dataclass
import math


# Put your data definitions first!
@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: float | None
    electricity_and_heat_co2_emissions_per_capita: float | None
    energy_co2_emissions: float | None
    energy_co2_emissions_per_capita: float | None
    total_co2_emissions_excluding_lucf: float | None
    total_co2_emissions_excluding_lucf_per_capita: float | None

@dataclass(frozen=True)
class Node:
    value: Row
    next: Node | None
# ...

# Then your functions.

# ...
