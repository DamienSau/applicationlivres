#!/bin/env python3

import fitz            # pymupdf, pour gerer les pdf et EPUBs
from langdetect import detect
import os
from os import walk
import aspose.words as aw
from operator import itemgetter


import livres

# un livre doit contenir toute les informations sur le livre

class unLivre:

    def __init__(self, fichier, nomfichier):       # fichier = Document(nomfichier)
        mda = fichier.metadata
        self.titre = mda['title']                  # titre du livre
        self.auteur = mda['author']                # auteur(s) du livre
        TDM = fichier.get_toc()                    # table des matieres
        TDM2 = str(TDM)                            # on transforme en str pour avoir la langue
        self.langue = detect(TDM2)                 # langue (detectee a partir de la table des matiere)
        self.nomfichier = nomfichier               # nom du fichier
        self.tdm = TDM2

    def TDM(self):
        with open(f"{self.titre}.txt", "w") as file:
            file.write("Table des matieres :\n")
            file.write("\n")
            file.write(f"{self.tdm}")
        doc = aw.Document(f"{self.titre}.txt")
        doc.save(f"{self.titre}.pdf")    # sauvegarde en pdf
        doc.save(f"{self.titre}.epub")   # sauvegarde en epub

class bibliotheque:

    def __init__(self):
        self.livres = []
        self.curentpath = os.getcwd()
        self.path = self.curentpath + "/livres"

# a partir du nom du repertoire dans lequel se trouve le repertoire livres, 
# on peut ajouter des livres a la bibliotheque

    def completebibli(self, path):
        # pour chaque fichier, on construit un livre que l'on ajoute a la bibliotheque
        # on n'ajoute que les pfd et les epub, le reste est traité par le log
        os.chdir(path)
        for objet in os.listdir():
            if objet[-3:]=="pdf" or objet[-4:]=="epub":
                # objet est le nom d'un fichier pdf ou epub
                fichier = fitz.open(objet)
                lv = unLivre(fichier, objet)
                os.chdir(self.curentpath)     # pour les TDM
                lv.TDM()                      #
                os.chdir(path)                #
                self.livres.append(lv)
            elif objet[-3:]=="zip":
                # objet est le nom d'un fichier zip
                print(f"{objet} n'a pas ete traite")
            else:
                # objet est le nom d'un dossier
                newpath = path + "/" + objet
                self.completebibli(newpath)
                os.chdir(path)
        os.chdir(self.curentpath)

    def ouvrages(self):
        # on cree un fichier texte dans le repertoire courant pour les ouvrages
        os.chdir(self.curentpath)
        with open("ouvrages.txt", "w") as file:
            file.write("ouvrages :\n")
            file.write("\n")
        # on complete la bibliotheque
        self.completebibli(self.path)
        # on ajoute les ouvrages dans le texte ouvrages.txt
        for livre in range(len(self.livres)):
            with open("ouvrages.txt", "a") as file:
                file.write(f"titre : {self.livres[livre].titre}\n")
                file.write(f"auteur : {self.livres[livre].auteur}\n")
                file.write(f"langue : {self.livres[livre].langue}\n")
                file.write(f"fichier : {self.livres[livre].nomfichier}\n")
                file.write("\n")
        ouvrages = aw.Document("ouvrages.txt")
        ouvrages.save("ouvrages.pdf")    # sauvegarde en pdf
        ouvrages.save("ouvrages.epub")   # sauvegarde en epub

    def auteurs(self):
        # on cree un fichier texte dans le repertoire courant pour les auteurs
        os.chdir(self.curentpath)
        with open("auteurs.txt", "w") as file:
            file.write("auteurs :\n")
            file.write("\n")
        # initialisation de la liste des auteurs et de la liste des ouvrages de chaque auteur
        aut = []
        tit = []
        for livre in self.livres:

            if type(livre.auteur)==str:   # cas ou le livre n'a qu'un seul auteur
                if livre.auteur not in aut:
                    aut.append(livre.auteur)
                    tit.append([[livre.titre, livre.nomfichier]])
                else:
                    # l'auteur est deja dans la liste, donc on le cherche
                    for a in range(len(aut)):
                        if aut[a] == livre.auteur:
                            tit[a].append([livre.titre, livre.nomfichier])

            else:                         # cas ou le livre a plusieurs auteurs, dans ce cas livre.auteur est une liste
                for auteur in livre.auteur:
                    if auteur not in aut:
                        aut.append(auteur)
                        tit.append([[livre.titre, livre.nomfichier]])
                    else:
                        for a in range(len(aut)):
                            if auteur==aut[a]:
                                tit[a].append([livre.titre, livre.nomfichier])

        with open("auteur.txt", "w") as file:
            for a in range(len(aut)):
                file.write(f"auteur : {aut[a]}")
                file.write("\n")
                for t in range(len(tit[a])):
                    file.write(f"titre : {tit[a][t][0]}")
                    file.write("\n")
                    file.write(f"nomfichier : {tit[a][t][1]}")
                    file.write("\n")
                file.write("\n")

    def update(self):
        # identifier les fichiers supprimes et ceux ajoutés
        # on va comparer les fichiers dans ouvrages.txt a ceux du nouveau dossier livre
        #    si un fichier de ouvrages.txt n'est pas dans livre, il a ete supprime
        #    si un fichier de livre n'est pas dans ouvrages.txt, il a ete ajoute
        # on veut recuperer la liste des noms de fichier de ouvrages.txt et de livre
        # pour livre:
        #    os.chdir(path) où path est le chemin d'accees de livre
        #    os.listdir() est la liste des noms de fichier de livre
        # pour ouvrages.txt:
        #    with open("ouvrages.txt", "r") as file:
        #        lignes = file.readlines() est la liste des lignes de ouvrages.txt
        # lignes[5] est la ligne du premier nom de fichier
        # donc c'est un str, il faut enlever "fichier : ", cad les 10 premiers caractere de la chaine
        # donc on prend : lignes[5][10:] pour avoir les caracteres a partir du 11eme caractere inclu
        # en parcourant les lignes de 5 en 5, on peut construire la liste des nom de fichier de l'ancienne bibliotheque
        # donc les lignes sont lignes[5], lignes[10], ..., lignes[5*i]

        # construction de la liste des noms de fichiers de l'ancienne bibliotheque:
        os.chdir(self.curentpath)
        with open("ouvrages.txt", "r") as file:
            lignes = file.readlines()
        liv1 = []
        for l in range(len(lignes)):
            if l%5==0:
                liv1.append(lignes[l][10:-1])
        # construction de la liste des noms de fichiers de la nouvelle bibliotheque:
        liv2 = bibliotheque()
        liv2.completebibli(self.path, True)
        os.chdir(self.curentpath)
        print(liv1)
        print(liv2)
        
B = bibliotheque()
B.ouvrages()
B.auteurs()
# B.update()  # ne fonctionne pas



