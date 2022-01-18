# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 17:42:05 2020

@author: Ugo
"""
from tkinter import*
from random import*


class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.__title = "Jeu du pendu"
        
        #boutons nouvelle partie et quitter
        f1 = Frame(self) # on créé une frame
        f1.pack(side=TOP, padx=5, pady=5)
            #on créé les boutons et on les ajoute à la frame
        Button(f1, text ='Nouvelle partie', width=15, command = self.nouvellePartie).pack(side=LEFT, padx = 5,pady = 5)
        Button(f1, text = 'Quitter', width = 15, command = self.destroy).pack(side = LEFT, padx = 5, pady = 5)
        Button(f1, text = 'Reset Score', width = 15, command = self.resetScore).pack(side = LEFT, padx = 5, pady = 5)
        
        
        #Entrée du nom
        self.playing = False # booléen représente si l'on est en train de jouer la partie ou si le joueur doit d'abord entrer son nom
        self.__sv = StringVar()
        self.__label_nom = Label(self)
        self.__label_nom.config(text = 'Veuillez entrer votre nom')
        self.__label_nom.pack(side = TOP, padx = 5, pady = 5)
        self.__f3 = Frame(self)   
        self.__f3.pack(side = TOP, padx = 5, pady = 5)
        self.__nom = Entry(self.__f3, text = 'Entrez votre nom',  textvariable = self.__sv)
        self.__nom.pack(side = LEFT, padx = 5, pady = 5)
        self.__bouton_envoi = Button(self.__f3, text = 'Envoyer', width = 15, command =  self.envoiNom)
        self.__bouton_envoi.pack(side = LEFT, padx = 5, pady = 5)
        
        #gestion du score
        self.__score = self.chargeScore()
        self.__label_score = Label(self.__f3)
        
        #zone affichage
        self.__zone_affichage = ZoneAffichage(self, 350,320,'white')
        self.__zone_affichage.pack(padx=5, pady=5)
        
        #label mot
        self.__lmot = Label(self)
        self.__lmot.pack(side=TOP)
        
        #gestion des mots
        self.__mots = self.chargeMots()
               
        #boutons clavier
        self.__boutons = []
        f2 = Frame(self)
        for i in range(26):
            button = MonBouton(f2, chr(ord('A')+i), self)
            button.grid(row = (i//7)+1, column = i%7 + (i//7)//3)
            self.__boutons.append(button)
        f2.pack()
        
        #bouton historique
        Button(f1, text = 'Historique', width = 15, command = self.historique).pack(side = LEFT, padx = 5, pady = 5)
        #lancement partie
        self.nouvellePartie()
            
    def envoiNom(self):
        self.__nom_joueur = self.__sv.get() #on récupère le nom du joueur
        print("Votre nom est : "+self.__sv.get())
        self.__nom.pack_forget() #on supprime l'Entry du nom du joueur
        self.__bouton_envoi.pack_forget() #on supprime le bouton d'envoi du nom du joueur
        self.__label_nom.pack_forget()# on Supprime le label nom du joueur
        self.playing = True #on met la partie comme étant en cours
        self.__player_score = self.calculeScore() #on Calcule le score du joueur
        self.__label_score.config(text = 'Votre score actuel est de : '+str(self.__player_score)+' %') #on affiche le score du joueur
        self.__label_score.pack(side = LEFT, padx = 5, pady = 5)
        return
    
    def chargeScore(self):
        print('Je charge les parties')
        with open('score.txt', 'r') as f: #on ouvre le fichier score
            l = f.read().splitlines()        #on lit les lignes
        for i in range(len(l)):
            l[i] = l[i].split(',') #on range les information dans un tableau de tableau
        print(l)
        return l
    
    def saveScore(self):
        print('Je sauvegarde les parties')
        with open('score.txt', 'w') as f: #on ouvre le fichier score
            for t in self.__score:
                f.write(','.join(t)+'\n') #on éecrit chaque ligne de la liste score dans le fichier score
                
    def resetScore(self):
        l = []
        if self.playing: #on verifie que le joueur a déjà entré son prénom
            for t in self.__score:
                if t[0] != self.__nom_joueur:#on vérifie toutes les parties que le joueur n'a pas joué
                    l.append(t) #on les ajoutes dans la nouvelle liste
            self.__score = l
            print('Le score a été reset')
            self.saveScore() #on enregiste le nouveau score
            self.__player_score = self.calculeScore()#on calcule le nouveau scole du joueur
            self.__label_score.config(text = 'Votre score actuel est de : '+str(self.__player_score)+' %')
        else:
            print('/!\ Le joueur n\'est pas encore défini')
    
    def calculeScore(self):
        p = 0 #nombre de parties jouées par e joueur
        v = 0#nombre de victoires du joueur
        for t in self.__score: #onb parcourt les parties
            if t[0] == self.__nom_joueur: #on regarde celles que le joueur actuel a joué
                if t[2] == 'True': #on regarde celles qu'il a gagné
                    v+=1
                p+=1
        if p!=0: #si le joueur n'a joué aucune partie
            return v/p*100
        else :
            return 0
        
    def historique(self):
        if self.playing:
            print('Historique de tes parties :')
            for t in self.__score: #On parcourt la liste des parties et on affiche celle du joueur actuel
                if t[0] == self.__nom_joueur:
                    print('mot : '+t[1]+ ', Gagné : '+t[2])
        else :
            print('/!\ Le joueur n\'est pas défini')
            
    def nouvellePartie(self):
        #gesttion du mot
        self.__mot = self.nouveauMot() #on choisit un nouveau mot
        self.__motAffiche = '*'*len(self.__mot) #on reset le mot a afficher
        self.__lmot.config(text=self.__motAffiche)
        
        #gestion des boutons
        for i in range(26):
            self.__boutons[i].config(state = 'active') #on remet actif chaque bouton du clavier
        
        #gestion du jeu
        self.__nbManques = 0 #on réinitialise le nombre d'erreurs
        self.__zone_affichage.change_image(0) #on remet le pendu à 0
    
    def traitement(self, lettre): 
        print('La lettre '+lettre+' a été reçu')
        b = False
        for i in range(len(self.__mot)): #on parcourt les lettres du mot recherché
            if self.__mot[i] == lettre:
                print('Changement de la '+str(i)+'e lettre du mot affiché' )
                l = list(self.__motAffiche)
                l[i] = lettre #on change la lettre du mot à afficher si elle est bonne
                self.__motAffiche = "".join(l)
                b = True
                self.__lmot.config(text=self.__motAffiche)# on réaffiche le nouveau motAffiche
                
        if self.__motAffiche == self.__mot: # si le mot entièrement trouvé on fini la partie
            self.finPartie(True)
            
        if not b: #si on a proposé une mauvaise lettre
            print('La lettre n\'était pas bonne')
            self.__nbManques+=1 
            print('Le nombre d\'erreurs actuel est de : '+str(self.__nbManques))
            if self.__nbManques < 8 : #s'il nous reste des essais à faire
                self.__zone_affichage.change_image(self.__nbManques)
            if self.__nbManques == 7: #si l'on a plus d'essais
                self.finPartie(False)
            
    def chargeMots(self):
        with open('mots.txt','r') as f:
            l = f.read().splitlines() #on stock les mots du fichier mot dans un tableau
        print(l)
        return l
    
    def nouveauMot(self):
        mot = choice(self.__mots) #on choisit un mot dans la liste de mots
        print('Le mot choisit est : '+mot)
        return mot
    
    def finPartie(self, b):
        for i in range(26):
            self.__boutons[i].config(state = 'disabled') #on désactive tous les boutons du clavier
        
        if b :
            self.__lmot.config(text='Bravo tu as trouvé le mot')
        else:
            self.__lmot.config(text='Dommage tu as perdu, le mot était : '+self.__mot)
        
        self.__score.append([self.__nom_joueur, self.__mot, str(b)]) #on ajoute la partie à la liste des parties
        self.saveScore() #on sauvegarde le nouveau score
        self.chargeScore()#on récupère le score
        self.__player_score = self.calculeScore()
        self.__label_score.config(text = 'Votre score actuel est de : '+str(self.__player_score)+' %')
        

class ZoneAffichage(Canvas):
    def __init__(self, parent, w, h, c):
        Canvas.__init__(self, width = w, height = h, bg = c)
        self.__images = []
        chemin = 'ImagesPendu/pendu' #chemin d'accès aux images
        
        #Recupération de chaque image du pendu
        for i in range(1,9,1):
            self.__images.append(PhotoImage(file=chemin + str(i) +'.gif'))
        
        print(self.__images)
        self.create_image(0,0, anchor=NW, image=self.__images[5]) #affichage de la première image
        #dans la zone d'affichage
    
    def change_image(self, i):
        self.delete('All') #on supprime l'image actuelle
        self.create_image(0,0, anchor=NW, image=self.__images[i]) #on la remplace par une nouvelle
    
class MonBouton(Button):
    def __init__(self,frame, lettre, parent):
        Button.__init__(self, frame, text = lettre, command = self.cliquer)
        self.__lettre = lettre
        self.__parent = parent
        
    def cliquer(self):
        print('Le bouton ' +self.__lettre+' a été cliqué')
        if self.__parent.playing :
            self.config(state = "disabled") #on désactive le bouton
            print('Envoi de la lettre '+self.__lettre+' à la fenêtre principale')
            self.__parent.traitement(self.__lettre) #on envoi le traitement à la fenetre parente
        return
    
fen = FenPrincipale()
fen.mainloop()
