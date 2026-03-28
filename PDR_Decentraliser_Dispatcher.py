import Classe_PDR
from Classe_PDR import  distance_entre


############################################
# Fonctions de Gestion Diponibilité/Chemin
############################################
def demandes_disponibles(graphe):  #On scan toutes les demandes qui sont présente et non prise par un camion à un instant t
    """Retourne la liste des demandes encore non prises."""
    demandes = []

    for noeud in graphe.noeuds.values():
        if noeud.requete_presente and noeud.statut == "en_attente":
            demandes.append(noeud.id)

    return demandes


#################################################
#  Trés important Heuristique de décision
#################################################

def calcul_surcout2(camion, graphe, destination):
    """Heuristique de surcoût pour un camion."""
    
    distance = Classe_PDR.distance_entre(graphe, camion.position, destination)
    if distance == float("inf"):
        return float("inf")

    # HEURISTIQUE (à Ajuster)
    surcout = distance

    return surcout


############################################
# Messages et diffusion des demandes (la clé du décentralisé)
############################################

class Message:
    def __init__(self, type_msg, contenu, expediteur=None):
        self.type = type_msg  # "demande", "surcout", "vainqueur"
        self.contenu = contenu
        self.expediteur = expediteur


def diffuser_demandes(camions, graphe):
    demandes = demandes_disponibles(graphe)

    for demande in demandes:
        for camion in camions:
            camion.recevoir_message(Message("demande", demande))



def collecter_offres(camions, graphe, tour_actuel):
    offres = {}

    for camion in camions:
        # You'll need to modify traiter_messages to accept tour_actuel
        reponses = camion.traiter_messages(graphe, tour_actuel)

        for r in reponses:
            d = r["demande"]
            if d not in offres:
                offres[d] = []
            offres[d].append(r)

    return offres
############################################
# Enchères et assignation de la demande
############################################
def attribuer(offres, graphe):
    camions_utilises = set()  # camions déjà affectés ce tour

    for demande_id, liste_offres in offres.items():

        # Ne garder que les camions disponibles et non déjà affectés
        liste_offres = [
            o for o in liste_offres
            if o["camion"].disponible and o["camion"] not in camions_utilises
        ]

        if not liste_offres:
            continue  # pas de camion libre pour cette demande

        # Choisir le gagnant avec le coût le plus faible
        gagnant = min(liste_offres, key=lambda x: x["cout"])
        camion = gagnant["camion"]

        # Affecter la demande
        camion.assigner_demande(graphe, demande_id)

        # Marquer le camion comme déjà utilisé pour ce tour
        camions_utilises.add(camion)

        print(f"[ENCHERE] {demande_id} → {camion.id}")



####################################
# Liste des camions libres
####################################

def camions_disponibles(camions):
    return [c for c in camions if c.disponible]

####################################

##########################################################################################
# MAIN
##########################################################################################

# Exemple d'utilisiation de nos classes
if __name__ == "__main__":
    g, flotte, demandes_futures = Classe_PDR.graphe_exemple()

    print("\n--- DÉBUT DE LA SIMULATION (MODE SURCHARGE) ---")
    tour_actuel = 1
    offres = collecter_offres(flotte, g, tour_actuel)
    
    while any(c.route or c.cible_actuelle is not None for c in flotte) or demandes_futures or g.demandes:
        id_carg = 1
        print(f"\n--- TOUR {tour_actuel} ---")
        
        # 1. APPARITION DES NOUVELLES DEMANDES
        if tour_actuel in demandes_futures:
            nouvelles_destinations = demandes_futures.pop(tour_actuel)
            print(f">>> [ALERTE] Nouvelles demandes apparues pour les destinations : {nouvelles_destinations} ! <<<")
            for demande in nouvelles_destinations:
                noeud_demand = demande[0]
                quantite = demande[1]
                fenetre = demande[2]
                g.demandes.append(noeud_demand)
                g.noeuds[noeud_demand].requete_presente = True
                g.noeuds[noeud_demand].quantite = quantite
                g.noeuds[noeud_demand].time_window = fenetre
                g.noeuds[noeud_demand].statut = "en_attente"
                g.noeuds[noeud_demand].id_carg = id_carg
                id_carg = id_carg + 1


        # 2. DISPATCHER INTELLIGENT
        demandes_non_assignees = []
        camions=camions_disponibles(flotte) #Donne seulement les camions disponibles
        
        # a. diffusion
        diffuser_demandes(camions, g)
        
        # b. chaque camion calcule
        offres = collecter_offres(camions, g, tour_actuel)

        # c. attribution
        attribuer(offres, g)
        for camion in camions:
            camion.mettre_a_jour(1, g)
        
            
        # 3. FAIRE AVANCER LES CAMIONS
        for camion in flotte:
            camion.faire_un_tour(g)
            
        tour_actuel += 1
        
        # On augmente largement la limite de sécurité car les camions vont mettre du temps !
        if tour_actuel > 60:
            print("Limite de tours atteinte.")
            demandes_non_servees = 0

            for noeud in g.noeuds.values():
                if noeud.requete_presente and noeud.statut == "en_attente":
                    demandes_non_servees += 1
            print(f"Nombre de demandes non servies à la fin : {demandes_non_servees}")
        
            break
            
    print("\n--- FIN DE LA SIMULATION ---")
    
    
    
    

