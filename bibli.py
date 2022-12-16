#!/bin/env python3

import sys
import Livre as L

if sys.argv[1] == "init":
    B = L.Bibliotheque()
    B.recup()
    B.DataFrame()
elif sys.argv[1] == "update":
    B = L.Bibliotheque()
    B.update()

