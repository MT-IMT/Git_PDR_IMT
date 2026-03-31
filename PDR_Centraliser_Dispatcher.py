import Classe_PDR


def simulation_centralise(g, flotte, demandes_futures, depot=0):
    """
    Lance la simulation avec le Dispatcher centraliser (Heuristique d'Insertion,
    gestion des stocks réelle, retour au dépôt et tableau de bord).
    """
    demandes_en_attente = []
    print("\n=======================================================")
    print("--- DÉBUT DE LA SIMULATION CENTRALISE ---")
    print("=======================================================")
    
    tour_actuel = 1
    id_carg = 1
    
    while any(c.route or c.cible_actuelle is not None for c in flotte) or demandes_futures or demandes_en_attente:
        print(f"\n--- TOUR {tour_actuel} ---")
        
        # 1. APPARITION DES NOUVELLES DEMANDES
        if tour_actuel in demandes_futures:
            nouvelles_destinations = demandes_futures.pop(tour_actuel)
            print(f">>> [ALERTE] Nouvelles demandes apparues : {nouvelles_destinations} ! <<<")
                
            for demande in nouvelles_destinations:
                noeud_demand = demande[0]
                quantite = demande[1]
                fenetre = demande[2]

                demandes_en_attente.append(noeud_demand)
                g.noeuds[noeud_demand].requete_presente = True
                g.noeuds[noeud_demand].quantite = quantite
                g.noeuds[noeud_demand].time_window = fenetre
                g.noeuds[noeud_demand].statut = "en_attente"
                g.noeuds[noeud_demand].id_carg = id_carg
                id_carg += 1

        # 2. DISPATCHER CENTRALISERS (Heuristique d'insertion + Stock futur)
        demandes_non_assignees = []
        for dest in demandes_en_attente:
            qte_requise = g.noeuds[dest].quantite
            
            camions_eligibles = []
            for c in flotte:
                # Calcul du stock virtuel pour éviter les surcharges
                liste_totale = c.file_destinations.copy()
                if c.destination is not None and c.destination != depot:
                    liste_totale.append(c.destination)
                    
                poids_deja_reserve = sum(g.noeuds[d].quantite for d in liste_totale if d != depot and g.noeuds[d].requete_presente)
                stock_futur = c.charge_actuelle - poids_deja_reserve
                
                if stock_futur >= qte_requise:
                    camions_eligibles.append((c, stock_futur))
            
            if camions_eligibles:
                meilleur_camion = None
                meilleur_index_global = 0
                meilleur_cout_global = float('inf')
                stock_futur_meilleur = 0
                
                # Évaluation de l'insertion pour trouver l'emplacement parfait
                for tuple_camion in camions_eligibles:
                    camion = tuple_camion[0]
                    stock_futur = tuple_camion[1]
                    index_opti, surcout = camion.evaluer_meilleure_insertion(g, dest)
                    
                    if surcout < meilleur_cout_global:
                        meilleur_cout_global = surcout
                        meilleur_index_global = index_opti
                        meilleur_camion = camion
                        stock_futur_meilleur = stock_futur
                
                if meilleur_camion is not None:
                    print(f"--> [DISPATCH OPTIMISÉ] {meilleur_camion.id} insère {dest} (Stock futur garanti : {stock_futur_meilleur - qte_requise}/{meilleur_camion.capacite} kg)")
                    meilleur_camion.insertion_demande_centralisee(g, dest, index_insertion=meilleur_index_global)
                
            else:
                demandes_non_assignees.append(dest)

        # 3. GESTION DU RETOUR AU DÉPÔT
        for c in flotte:
            # Si le camion n'a plus rien à faire, qu'il n'est pas au dépôt, et que son stock est très bas
            if not c.file_destinations and c.cible_actuelle is None and c.position != depot and c.charge_actuelle < 5:
                print(f"--- [LOGISTIQUE] {c.id} n'a plus assez de stock ({c.charge_actuelle}kg), retour au Depot ({depot}) ---")
                c.insertion_demande_centralisee(g, depot)
                
        if demandes_non_assignees:
            print(f"!!! [SURCHARGE] {len(demandes_non_assignees)} requetes en attente de stock/camion : {demandes_non_assignees} !!!")
                
        demandes_en_attente = demandes_non_assignees

        # =====================================================================
        # TABLEAU DE BORD DE LA FLOTTE
        # =====================================================================
        print("\n--- ETAT DES CAMIONS ---")
        for c in flotte:
            pos_actuelle = str(c.position) if c.position is not None else f"Vers {c.cible_actuelle}"
            dest_actuelle = str(c.destination) if c.destination is not None else "-"
            file_attente = str(c.file_destinations) if c.file_destinations else "[]"
            
            charge_affichee = max(0, c.charge_actuelle)
            print(f" {c.id} | Pos: {pos_actuelle:<7} | Objectif: {dest_actuelle:<3} | "
                  f"File d'attente: {file_attente:<12} | Charge actuelle: {charge_affichee}/{c.capacite}")
        print("---------------------------\n")

        # 4. FAIRE AVANCER LES CAMIONS
        for camion in flotte:
            camion.faire_un_tour_centraliser(g)
            
        tour_actuel += 1
        
        if tour_actuel > 250: 
            print("Limite de tours atteinte.")
            break
            
    print("\n--- FIN DE LA SIMULATION CENTRALISE ---")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__" :
    # choisir le graphe
    #g, flotte, demandes_futures = Classe_PDR.graphe_exemple()
    g, flotte, demandes_futures = Classe_PDR.graphe_complexe()
    simulation_centralise(g, flotte, demandes_futures, depot=15) # mettre le bon dépôt (15: graphe complexe)(0:graphe exemple)
