#!/usr/bin/env python3

import sqlite3

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

statement = """
SELECT customerid, ordered, shipped,
       strftime('%Y-%m-%d', ordered) date
FROM orders
GROUP BY date
;
"""

statement = """
-- Who was earliest the most often?
SELECT c.name, c.phone, count(*) earliest
FROM customers c
INNER JOIN ( -- Customers who ordered first after 4 each day
  SELECT customerid, min(ordered) early,
         strftime('%Y-%m-%d', ordered) date
  FROM ( -- Orders after 4am
    SELECT *
    FROM orders
    WHERE strftime('%H', shipped) BETWEEN '04' AND '05' -- After 4am, since she showed up with pastries at 5am
  )
  GROUP BY date
) AS o
ON c.customerid = o.customerid
GROUP BY c.name
ORDER BY earliest
;
"""

with sqlite3.connect("noahs.sqlite") as conn:
    cur = conn.cursor()
    result = cur.execute(statement)
    for x in result.fetchall():
        print(x)

    # Ultimately just chose the first femme name of the earliest of birds :\
