class Noeud:
    """Représente un nœud (sommet) du graphe."""
    def __init__(self, identifiant, **donnees):
        """
        :param identifiant: identifiant unique du nœud (str ou int)
        :param donnees: attributs supplémentaires (par exemple, nom, coordonnées)
        """
        self.id = identifiant
        self.donnees = donnees  # dictionnaire pour stocker des informations optionnelles

    def __repr__(self):
        return f"Noeud({self.id})"

    def __str__(self):
        return str(self.id)


class Arete:
    """Représente une arête (lien) entre deux nœuds."""
    def __init__(self, source, cible, poids=1.0, **attributs):
        """
        :param source: nœud de départ (objet Noeud)
        :param cible: nœud d'arrivée (objet Noeud)
        :param poids: poids / coût de l'arête (par défaut 1.0)
        :param attributs: attributs supplémentaires (par exemple, distance, temps, nom de rue)
        """
        self.source = source
        self.cible = cible
        self.poids = poids
        self.attributs = attributs

    def __repr__(self):
        return f"Arete({self.source} -> {self.cible}, poids={self.poids})"


class Graphe:
    """Graphe orienté ou non, avec liste d'adjacence."""
    def __init__(self, oriente=False):
        """
        :param oriente: True si le graphe est orienté, False sinon (par défaut non orienté)
        """
        self.oriente = oriente #on verra si on oriente le graphe ou pas
        self.noeuds = {}        # identifiant -> objet Noeud
        self.aretes = []         # liste de toutes les arêtes (objets Arete)
        self.adjacence = {}      # identifiant_source -> liste de (identifiant_cible, arete)

    def ajouter_noeud(self, noeud):
        """Ajoute un nœud au graphe."""
        if noeud.id in self.noeuds:
            raise ValueError(f"Un nœud avec l'id {noeud.id} existe déjà.")
        self.noeuds[noeud.id] = noeud
        self.adjacence[noeud.id] = []

    def obtenir_noeud(self, identifiant):
        """Retourne l'objet Noeud correspondant à l'identifiant."""
        return self.noeuds.get(identifiant)

    def ajouter_arete(self, source_id, cible_id, poids=1.0, **attributs):
        """
        Ajoute une arête entre deux nœuds (identifiés par leurs id).
        Si le graphe n'est pas orienté, ajoute également l'arête inverse.
        """
        if source_id not in self.noeuds:
            raise ValueError(f"Le nœud source {source_id} n'existe pas.")
        if cible_id not in self.noeuds:
            raise ValueError(f"Le nœud cible {cible_id} n'existe pas.")

        source = self.noeuds[source_id]
        cible = self.noeuds[cible_id]

        arete = Arete(source, cible, poids, **attributs)
        self.aretes.append(arete)

        self.adjacence[source_id].append((cible_id, arete))

        if not self.oriente:
            # Ajouter l'arête dans l'autre sens
            arete_inverse = Arete(cible, source, poids, **attributs)
            self.aretes.append(arete_inverse)
            self.adjacence[cible_id].append((source_id, arete_inverse))

    def voisins(self, noeud_id):
        """Retourne la liste des identifiants des voisins d'un nœud."""
        return [(cid, arete) for cid, arete in self.adjacence.get(noeud_id, [])]

    def poids_arete(self, source_id, cible_id):
        """Retourne le poids de l'arête entre source et cible (ou None si pas d'arête directe)."""
        for cid, arete in self.adjacence.get(source_id, []):
            if cid == cible_id:
                return arete.poids
        return None

    def __repr__(self):
        return f"Graphe({self.oriente=}, {len(self.noeuds)} nœuds, {len(self.aretes)} arêtes)"


class Camion:
    """Classe indépendante représentant un camion pouvant se déplacer sur un graphe."""
    def __init__(self, identifiant, capacite, position_depart):
        """
        :param identifiant: identifiant unique du camion
        :param capacite: capacité maximale de chargement (en tonnes, volume, etc.)
        :param position_depart: identifiant du nœud de départ
        """
        self.id = identifiant
        self.capacite = capacite
        self.position = position_depart    # id du nœud actuel
        self.charge_actuelle = 0            # charge courante
        self.cargaison = []                  # liste des marchandises (peut être une liste d'objets)
        self.route = []                       # liste d'identifiants de nœuds à suivre (itinéraire)

    def charger(self, poids_marchandise, description=""):
        """Charge une marchandise si la capacité le permet."""
        if self.charge_actuelle + poids_marchandise > self.capacite:
            raise ValueError("Capacité insuffisante pour charger ce poids.")
        self.charge_actuelle += poids_marchandise
        self.cargaison.append((poids_marchandise, description))
        print(f"Camion {self.id} : chargé {poids_marchandise} kg. Charge totale = {self.charge_actuelle}")

    def decharger(self, poids_marchandise):
        """Décharge une marchandise (simplifié : enlève le dernier chargement ou par description)."""
        if not self.cargaison:
            raise ValueError("Aucune marchandise à décharger.")
        # Retire le dernier élément pour l'exemple
        dernier = self.cargaison.pop()
        self.charge_actuelle -= dernier[0]
        print(f"Camion {self.id} : déchargé {dernier[0]} kg. Charge restante = {self.charge_actuelle}")

    def definir_itineraire(self, chemin):
        """Définit la liste des nœuds à parcourir (séquence d'identifiants)."""
        self.route = chemin[:]
        print(f"Camion {self.id} : nouvel itinéraire défini : {self.route}")

    def avancer(self, graphe):
        """
        Avance d'un pas le long de l'itinéraire, si possible.
        Met à jour la position et supprime le premier nœud de la route.
        """
        if not self.route:
            print(f"Camion {self.id} : déjà à destination ou aucun itinéraire.")
            return False

        prochain_noeud = self.route[0]
        # Vérifier que l'arête existe (graphe non orienté, donc une direction suffit)
        poids = graphe.poids_arete(self.position, prochain_noeud)
        if poids is None:
            print(f"Erreur : pas d'arête directe de {self.position} vers {prochain_noeud}.")
            return False

        # Effectuer le déplacement
        self.position = prochain_noeud
        self.route.pop(0)
        print(f"Camion {self.id} : arrivé au nœud {self.position}")
        return True

    def trouver_chemin_vers(self, destination, graphe):
        """
        Utilise un algorithme de plus court chemin (Dijkstra simple) pour trouver un itinéraire.
        Met à jour self.route avec le chemin trouvé (liste d'ids).
        """
        # Implémentation basique de Dijkstra (pour des poids positifs)
        from heapq import heappush, heappop

        distances = {noeud_id: float('inf') for noeud_id in graphe.noeuds}
        distances[self.position] = 0
        precedent = {noeud_id: None for noeud_id in graphe.noeuds}
        tas = [(0, self.position)]

        while tas:
            dist_courante, noeud_courant = heappop(tas)
            if noeud_courant == destination:
                break
            if dist_courante > distances[noeud_courant]:
                continue
            for voisin_id, arete in graphe.voisins(noeud_courant):
                nouvelle_dist = dist_courante + arete.poids
                if nouvelle_dist < distances[voisin_id]:
                    distances[voisin_id] = nouvelle_dist
                    precedent[voisin_id] = noeud_courant
                    heappush(tas, (nouvelle_dist, voisin_id))

        # Reconstruction du chemin
        chemin = []
        noeud = destination
        while noeud is not None:
            chemin.append(noeud)
            noeud = precedent[noeud]
        chemin.reverse()
        if chemin[0] == self.position:
            self.route = chemin[1:]   # on exclut la position actuelle
            print(f"Camion {self.id} : chemin trouvé vers {destination} : {self.route}")
        else:
            print(f"Camion {self.id} : aucun chemin vers {destination}.")
            self.route = []

        return self.route

    def __repr__(self):
        return f"Camion({self.id}, capacité={self.capacite}, position={self.position})"


# Exemple d'utilisiation de nos classes
if __name__ == "__main__":
    # Création du graphe
    g = Graphe(oriente=False)

    # Création des nœuds
    A = Noeud("0", nom="Dépôt")
    B = Noeud("1", nom="Magasin 1")
    C = Noeud("2", nom="Magasin 2")
    D = Noeud("3", nom="Magasin 3")

    for noeud in [A, B, C, D]:
        g.ajouter_noeud(noeud)

    # Ajout des arêtes avec poids (distances)
    g.ajouter_arete("0", "1", poids=5) #Ajout du poids sur l'arête entre le noeud 0 (A) et 1 (B)
    g.ajouter_arete("0", "2", poids=10)
    g.ajouter_arete("1", "2", poids=3)
    g.ajouter_arete("2", "3", poids=4)
    g.ajouter_arete("1", "3", poids=8)

    print(g)
    print("Voisins du 1 :", [(cid, arete.poids) for cid, arete in g.voisins("1")])

    # Création d'un camion
    camion1 = Camion("Camion-01", capacite=20, position_depart="1")
    print(camion1)

    # Chargement
    camion1.charger(5, "Colis X")
    camion1.charger(3, "Colis Y")

    # Recherche d'un chemin vers D
    camion1.trouver_chemin_vers("2", g)

    # Déplacement pas à pas
    camion1.avancer(g)   # va en 2 (ou selon le chemin trouvé)
    camion1.avancer(g)   # etc.
    camion1.avancer(g)
    camion1.avancer(g)   # devrait arriver à 2

    # Déchargement
    camion1.decharger(3)
    camion1.decharger(5)

    print(camion1)