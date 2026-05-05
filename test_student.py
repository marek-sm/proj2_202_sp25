import unittest
from typing import Optional, Union
from proj2 import (
    Row,
    Node,
    read_csv_lines,
    listlen,
    filter_rows,
    parse_row
)


class TestStructureBasics(unittest.TestCase):

    def test_row_instantiation(self):
        r = Row(
            country="Mexico",
            year=1990,
            electricity_and_heat_co2_emissions=10.5,
            electricity_and_heat_co2_emissions_per_capita=0.9,
            energy_co2_emissions=15.0,
            energy_co2_emissions_per_capita=1.2,
            total_co2_emissions_excluding_lucf=20.3,
            total_co2_emissions_excluding_lucf_per_capita=1.7
        )
        self.assertEqual(r.country, "Mexico")
        self.assertEqual(r.year, 1990)

    def test_node_instantiation(self):
        r = Row("USA", 2020, 1000.0, 15.0, 2000.0, 30.0, 5000.0, 75.0)
        n = Node(value=r, next=None)
        self.assertEqual(n.value.country, "USA")
        self.assertIsNone(n.next)

    def test_node_chain(self):
        r1 = Row("A", 2000, 1.0, 0.1, 2.0, 0.2, 3.0, 0.3)
        r2 = Row("B", 2001, 1.1, 0.2, 2.1, 0.3, 3.1, 0.4)
        n2 = Node(value=r2, next=None)
        n1 = Node(value=r1, next=n2)
        self.assertEqual(n1.value.country, "A")
        assert n1.next is not None
        self.assertEqual(n1.next.value.country, "B")


class TestFunctionSignatures(unittest.TestCase):

    def test_parse_row_type(self):
        row = parse_row([
            "USA", "1990", "100.0", "1.5", "200.0", "2.5", "300.0", "3.5"
        ])
        self.assertIsInstance(row, Row)
        self.assertEqual(row.country, "USA")

    def test_read_csv_lines_type(self):
        result = read_csv_lines("sample.csv")
        self.assertTrue(result is None or isinstance(result, Node))

    def test_listlen_none(self):
        self.assertEqual(listlen(None), 0)

    def test_listlen_chain(self):
        r1 = Row("X", 2000, None, None, None, None, None, None)
        r2 = Row("Y", 2001, None, None, None, None, None, None)
        lst = Node(r1, Node(r2, None))
        self.assertEqual(listlen(lst), 2)

    def test_filter_rows_returns_node_or_none(self):
        r = Row("USA", 2020, 100.0, 2.0, 200.0, 3.0, 300.0, 4.0)
        lst = Node(r, None)
        result = filter_rows(lst, "country", "equal", "USA")
        self.assertTrue(result is None or isinstance(result, Node))


class TestStudent(unittest.TestCase):

    def test_parse_row_handles_missing(self):
        row = parse_row(["Andorra", "2010", "", "", "", "", "", ""])
        self.assertEqual(row.country, "Andorra")
        self.assertIsNone(row.electricity_and_heat_co2_emissions)

    def test_read_csv_lines_loads_sample(self):
        result = read_csv_lines("sample.csv")
        self.assertEqual(listlen(result), 8)

    def test_listlen_counts_correctly(self):
        r = Row("X", 2000, None, None, None, None, None, None)
        lst = Node(r, Node(r, Node(r, None)))
        self.assertEqual(listlen(lst), 3)

    def test_filter_rows_filters(self):
        r1 = Row("USA", 1990, None, None, None, None, None, None)
        r2 = Row("Mexico", 1990, None, None, None, None, None, None)
        lst = Node(r1, Node(r2, None))
        result = filter_rows(lst, "country", "equal", "USA")
        self.assertEqual(listlen(result), 1)


if __name__ == "__main__":
    unittest.main()