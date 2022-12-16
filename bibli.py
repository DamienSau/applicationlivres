#!/bin/env python3

# Nous avons utilisé la partie 1 de BEQUET Clément et ANDRIANJAFY Koloina sous le nom Livre.py
# "Livre.py" et le répertoire "livres" doivent se trouver dans le répertoire courant

import sys
import Livre as L

if sys.argv[1] == "init":
    B = L.Bibliotheque()
    B.recup()
    B.DataFrame()
elif sys.argv[1] == "update":
    B = L.Bibliotheque()
    B.update()

