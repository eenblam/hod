#!/usr/bin/env python3

import sqlite3

keypad = {
        'A': '2',
        'B': '2',
        'C': '2',
        'D': '3',
        'E': '3',
        'F': '3',
        'G': '4',
        'H': '4',
        'I': '4',
        'J': '5',
        'K': '5',
        'L': '5',
        'M': '6',
        'N': '6',
        'O': '6',
        'P': '7',
        'Q': '7',
        'R': '7',
        'S': '7',
        'T': '8',
        'U': '8',
        'V': '8',
        'W': '9',
        'X': '9',
        'Y': '9',
        'Z': '9',
        }

with sqlite3.connect("noahs.sqlite") as conn:
    cur = conn.cursor()
    result = cur.execute('SELECT name, phone FROM customers;')
    for name, phone in result.fetchall():
        # Assume that a mononym is also a last name
        last = name.split(' ')[-1].upper()
        # Drop hyphens from number
        number = phone.replace('-', '')
        # Don't bother mapping name unless it's the right length
        if len(last) == len(number):
            typed = ''.join(keypad[c] for c in last)
            if typed == number:
                print(name, typed, phone)

