import j2l.pytactx.agent as pytactx
from datetime import datetime
agent=None
etatFSM1 = "recherche"  # valeurs possibles : "recherche", "poursuite", "veille"
etatFSMRonde = "gauche"  # valeurs possibles : "gauche", "haut", "droite", "bas"
xEnnemi, yEnnemi = 0, 0
debutVeille = datetime.now()
def setAgent(nouvelagent):
  global agent 
  agent = nouvelagent

def agentArrive():
  ancienAgentVoisin = dict(agent.voisins)
  agent.actualiser()
  for playerId, playerInfo in agent.voisins.items():
    if playerId not in ancienAgentVoisin:
      print("nouvel agent :", playerId)

def agentParti():
  ancienAgentVoisin = dict(agent.voisins)
  agent.actualiser()
  for playerId, playerInfo in ancienAgentVoisin.items():
    if playerId not in agent.voisins:
      print("agent partie :", playerId)

def rechercheMin(dictionnaire):
  """
    Renvoie la valeur min et sa clé associée dans le dictionnaire spécifié en paramètre
    :param dictionnaire: dictionnaire de clé et valeurs entières
    :type dictionnaire: dict de clé Any, valeur int or float
    :return: tuple comprenant la clé, la valeur minimale
    """
  minValue = None
  minKey = None
  for key, value in dictionnaire.items():
    if minValue is None or value < minValue:
      minValue = value
      minKey = key
  return minKey, minValue

def eval(agentRef, voisin):
  """
    Renvoie un nombre représentant le coût pour notre agent de référence pour aller abattre le voisin spécifié. Un coût faible indique un voisin intéressant à aller abattre.
    :param agentRef: dictionnaire avec des clés de l'agent "x", "y", ...
    :type agentRef: dict avec clé str, valeur int ou float
    :param voisin: dictionnaire avec des clés de l'agent "x", "y", ...
    :type voisin: dict avec clé str, valeur int ou float
    :return: coût du voisin
    :rtype: int or float
    """
  dx = (agentRef["x"] - voisin["x"])**2
  dy = (agentRef["y"] - voisin["y"])**2
  # Ajoutez d'autres critères pour prendre en compte des heuristiques supplémentaires
  return dx + dy

def actualiserEnnemi():
  global xEnnemi
  global yEnnemi
  if agent.distance != 0 and agent.vie >= 50:
    agent.tirer(True)
    if agent.orientation == 0:
      xEnnemi = agent.x + agent.distance - 2
      yEnnemi = agent.y
      agent.orienter(0)  # Orient towards the enemy
    elif agent.orientation == 2:
      xEnnemi = agent.x - agent.distance + 2
      yEnnemi = agent.y
      agent.orienter(2)  # Orient towards the enemy
    elif agent.orientation == 1:
      xEnnemi = agent.x
      yEnnemi = agent.y - agent.distance + 2
      agent.orienter(1)  # Orient towards the enemy
    elif agent.orientation == 3:
      xEnnemi = agent.x
      yEnnemi = agent.y + agent.distance - 2
      agent.orienter(3)  # Orient towards the enemy
  elif agent.distance != 0 and agent.vie < 50:
    agent.tirer(False)
    changerEtatFSM1("fuite")
  else:
    agent.tirer(False)

def changerEtatFSM1(nouvelEtat):
  global etatFSM1
  etatFSM1 = nouvelEtat

def changerEtatFSMRonde(nouvelEtat):
  global etatFSMRonde
  etatFSMRonde = nouvelEtat

def allerGauche():
  if agent.x == 5 and agent.y == 25:
    changerEtatFSMRonde("haut")
  else:
    agent.deplacerVers(5, 25)
    agent.orienter((agent.orientation + 1) % 4)

def allerHaut():
  if agent.x == 5 and agent.y == 5:
    changerEtatFSMRonde("droite")
  else:
    agent.deplacerVers(5, 5)
    agent.orienter((agent.orientation + 1) % 4)

def allerDroite():
  if agent.x == 35 and agent.y == 5:
    changerEtatFSMRonde("bas")
  else:
    agent.deplacerVers(35, 5)
    agent.orienter((agent.orientation + 1) % 4)

def allerBas():
  if agent.x == 35 and agent.y == 25:
    changerEtatFSMRonde("gauche")
  else:
    agent.deplacerVers(35, 25)
    agent.orienter((agent.orientation + 1) % 4)
    
def rechercher():
  if agent.distance != 0 and agent.vie >= 50:
    changerEtatFSM1("poursuite")
  elif agent.distance != 0 and agent.vie < 50:
    changerEtatFSM1("fuite")
  else:
    agent.tirer(False)
    if etatFSMRonde == "gauche":
      allerGauche()
    elif etatFSMRonde == "haut":
      allerHaut()
    elif etatFSMRonde == "droite":
      allerDroite()
    elif etatFSMRonde == "bas":
      allerBas()

def poursuivre():
  global xEnnemi
  global yEnnemi
  global debutVeille
  if agent.x == xEnnemi and agent.y == yEnnemi:
    agent.tirer(False)
    if agent.distance != 0 and agent.vie < 50:
      changerEtatFSM1("fuite")
    else:
      changerEtatFSM1("veille")
      debutVeille = datetime.now()
  else:
    agent.tirer(True)

def veiller():
  if agent.distance != 0:
    changerEtatFSM1("poursuite")
  elif (datetime.now() - debutVeille).total_seconds() > 2:
    changerEtatFSM1("recherche")
    agent.tirer(False)
  elif agent.distance != 0 and agent.vie < 50:
    changerEtatFSM1("fuite")
  else:
    agent.orienter((agent.orientation + 1) % 4)
    agent.tirer(False)

def fuite():
  global etatFSM1
  if agent.vie < 50 and agent.distance != 0:
    if xEnnemi <= 19:
      xFuite = 39
    else:
      xFuite = 0
    if yEnnemi <= 14:
      yFuite = 29
    else:
      yFuite = 0
    agent.deplacerVers(xFuite, yFuite)
  elif len(agent.voisins) == 0:
    changerEtatFSM1("recherche")

def actualiserAgent():
  agentArrive()
  agentParti()
  actualiserEnnemi()
  if etatFSM1 == "recherche":
    rechercher()
  elif etatFSM1 == "poursuite":
    poursuivre()
  elif etatFSM1 == "veille":
    veiller()
  elif etatFSM1 == "fuite":
    fuite()
  possibilites = {}
  for voisinId, voisinInfos in agent.voisins.items():
    agentInfo = {"x": agent.x, "y": agent.y}
    possibilites[voisinId] = eval(agentInfo, voisinInfos)
  if len(possibilites) > 0:
    voisinCibleId, voisinCibleCout = rechercheMin(possibilites)
    voisinCibleInfos = agent.voisins[voisinCibleId]
    agent.deplacerVers(voisinCibleInfos["x"], voisinCibleInfos["y"])