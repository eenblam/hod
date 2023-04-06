#!/usr/bin/env python3

"""
Solution to problem #2 using only SQL and a regex.
"""

import re
import sqlite3

statement_one = """
SELECT c.name, c.phone, c.citystatezip
FROM customers c
INNER JOIN orders o
ON c.customerid = o.customerid
WHERE strftime('%Y', o.ordered) = '2017'
AND c.citystatezip LIKE 'Manhattan%';
"""

# Hmm, still not getting it...
# I can see two other pieces of info:
# 1. contractor is local to NY
# 2. haven't ordered in a few years
#
# It turns out "haven't ordered in a few years" means "since 2017."

statement = """
SELECT c.name, c.phone, c.citystatezip
FROM customers c
INNER JOIN(

SELECT o.customerid customerid, strftime('%Y', o.ordered) order_year
FROM orders o
INNER JOIN(
SELECT customerid
FROM (
  SELECT customerid, MAX(ordered) latest
  FROM orders
  GROUP BY customerid
)
WHERE strftime('%Y', latest) = '2017'
) AS ids
WHERE o.customerid = ids.customerid
AND order_year = '2017'

) AS ords
WHERE c.customerid = ords.customerid
AND c.citystatezip LIKE '%NY%'
;
"""
# It was unclear if "they’re right across the street from Noah’s"
# refers to the cleaner or the contractor. Guess it was the cleaner!
#WHERE c.citystatezip LIKE 'Manhattan%'

# Regex for J... (optional middle names) D... (optional suffix)
# Use a non-matching group for possible middle name(s)
# Use a non-matching group for roman numerals, Jr., and Sr.
pat = re.compile('J\w+ (?:\w+ )*D\w+(?: ([IVX]+)|(Jr.)|(Sr.))?')
# Now that I know the answer, it looks like 'J.*D.*' will also solve the puzzle ;)

with sqlite3.connect("noahs.sqlite") as conn:
    cur = conn.cursor()
    result = cur.execute(statement)
    for name, phone, citystatezip in result.fetchall():
        if re.match(pat, name) is not None:
            print(name, phone, citystatezip)
