#!/usr/bin/env python3

import sqlite3

# Chinese zodiac dates from https://en.wikipedia.org/wiki/Dog_(zodiac)#Years_and_the_Five_Elements
# Assume no earlier than 1958 to allow a reasonable working age,
# and no later than 1995 so neighbor isn't a child.

# Aries dates from https://en.wikipedia.org/wiki/Aries_(astrology)

statement = """
SELECT name,
       phone,
       strftime('%Y-%m-%d', birthdate) bday,
       strftime('%m-%d', birthdate) bdayshort
FROM customers
WHERE (bdayshort BETWEEN '03-21' AND '04-19')      -- Aries
AND ((bday BETWEEN '1958-02-18' AND '1959-02-07')  -- Year of the Dog, but not late 70s
  OR (bday BETWEEN '1970-02-06' AND '1971-01-26')
  OR (bday BETWEEN '1982-01-25' AND '1983-02-12')
  OR (bday BETWEEN '1994-02-10' AND '1995-01-30')) -- Year of the Dog, but not a child
AND citystatezip LIKE 'South Ozone Park%'          -- Lives in contractor's neighborhood
;
"""

with sqlite3.connect("noahs.sqlite") as conn:
    cur = conn.cursor()
    result = cur.execute(statement)
    for name, phone, birthdate, _ in result.fetchall():
        print(name, phone, birthdate)
