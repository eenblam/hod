#!/usr/bin/env python3

"""
Solution to problem #2, mostly in Python
"""

import re
import sqlite3

statement = """
SELECT c.name, c.phone, c.citystatezip, strftime('%Y', o.ordered)
FROM customers c
INNER JOIN orders o
ON c.customerid = o.customerid
;
"""

# Regex for J... (middle names) D... (suffix)
# Use a non-matching group for possible middle name(s)
# Use a non-matching group for roman numerals, Jr., and Sr.
pat = re.compile('J\w+ (?:\w+ )*D\w+(?: ([IVX]+)|(Jr.)|(Sr.))?')

with sqlite3.connect("noahs.sqlite") as conn:
    cur = conn.cursor()
    result = cur.execute(statement)
    customers = {}
    for name, phone, citystatezip, year in result.fetchall():
        # GROUP BY name
        try:
            customers[name]['years'].add(int(year))
        except KeyError:
            customers[name] = {
                    'phone': phone,
                    'addr': citystatezip,
                    'years': set([int(year)])
                    }


    old = {name:d for name, d in customers.items() if max(d['years']) < 2021}
    for name, d in old.items():
        if pat.match(name) is not None and 2017 in d['years']:
            print(name, d)

        # Ultimately selected the one who was here in 2017, but stopped the longest ago
