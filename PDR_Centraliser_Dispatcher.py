# Exemple d'utilisiation de nos classes
if __name__ == "__main__":
    # --- 1. CRÉATION DU GRAPHE (Grande ville en grille 4x4) ---
    g = Graphe(oriente=False)
    depot = 15
    # Création d'un camion
    camion1 = Camion("Camion-01", capacite=50, position_depart=depot)
    camion2 = Camion("Camion-02", capacite=50, position_depart=depot)
    camion3 = Camion("Camion-03", capacite=50, position_depart=depot)
    
    noeuds_data = [
        # Ligne 0 (y=0)
        (0, "A", 0, 0),   (1, "B", 5, 0),   (2, "C", 10, 0),  (3, "D", 15, 0),  (4, "E", 20, 0),  (5, "F", 25, 0),
        # Ligne 1 (y=5)
        (6, "G", 0, 5),   (7, "H", 5, 5),   (8, "I", 10, 5),  (9, "J", 15, 5),  (10, "K", 20, 5), (11, "L", 25, 5),
        # Ligne 2 (y=10)
        (12, "M", 0, 10), (13, "N", 5, 10), (14, "O", 10, 10),(15, "P", 15, 10),(16, "Q", 20, 10),(17, "R", 25, 10),
        # Ligne 3 (y=15)
        (18, "S", 0, 15), (19, "T", 5, 15), (20, "U", 10, 15),(21, "V", 15, 15),(22, "W", 20, 15),(23, "X", 25, 15),
        # Ligne 4 (y=20)
        (24, "Y", 0, 20), (25, "Z", 5, 20), (26, "A1", 10, 20),(27, "B1", 15, 20),(28, "C1", 20, 20),(29, "D1", 25, 20),
        # Ligne 5 (y=25)
        (30, "E1", 0, 25),(31, "F1", 5, 25),(32, "G1", 10, 25),(33, "H1", 15, 25),(34, "I1", 20, 25),(35, "J1", 25, 25)
    ]
    
    for id_n, nom, x, y in noeuds_data:
        g.ajouter_noeud(Noeud(id_n, nom, x, y, (0, 0), 100))

    # Ligne 0 : Axe fluide
    g.ajouter_arete(0, 1, poids=2); g.ajouter_arete(1, 2, poids=3); g.ajouter_arete(2, 3, poids=2); g.ajouter_arete(3, 4, poids=3); g.ajouter_arete(4, 5, poids=2)
    # Ligne 1 : Zone de travaux
    g.ajouter_arete(6, 7, poids=8); g.ajouter_arete(7, 8, poids=9); g.ajouter_arete(8, 9, poids=7); g.ajouter_arete(9, 10, poids=8); g.ajouter_arete(10, 11, poids=9)
    # Ligne 2 : Mixte
    g.ajouter_arete(12, 13, poids=4); g.ajouter_arete(13, 14, poids=2); g.ajouter_arete(14, 15, poids=5); g.ajouter_arete(15, 16, poids=3); g.ajouter_arete(16, 17, poids=6)
    # Ligne 3 : Axe résidentiel lent
    g.ajouter_arete(18, 19, poids=6); g.ajouter_arete(19, 20, poids=7); g.ajouter_arete(20, 21, poids=6); g.ajouter_arete(21, 22, poids=7); g.ajouter_arete(22, 23, poids=6)
    # Ligne 4 : Voie rapide Est-Ouest
    g.ajouter_arete(24, 25, poids=2); g.ajouter_arete(25, 26, poids=2); g.ajouter_arete(26, 27, poids=2); g.ajouter_arete(27, 28, poids=3); g.ajouter_arete(28, 29, poids=2)
    # Ligne 5 : Sortie de ville
    g.ajouter_arete(30, 31, poids=5); g.ajouter_arete(31, 32, poids=4); g.ajouter_arete(32, 33, poids=5); g.ajouter_arete(33, 34, poids=4); g.ajouter_arete(34, 35, poids=5)

    # Colonne 0 : Boulevard Ouest
    g.ajouter_arete(0, 6, poids=3); g.ajouter_arete(6, 12, poids=4); g.ajouter_arete(12, 18, poids=3); g.ajouter_arete(18, 24, poids=4); g.ajouter_arete(24, 30, poids=3)
    # Colonne 1 : Rue commerçante encombrée
    g.ajouter_arete(1, 7, poids=7); g.ajouter_arete(7, 13, poids=8); g.ajouter_arete(13, 19, poids=7); g.ajouter_arete(19, 25, poids=8); g.ajouter_arete(25, 31, poids=7)
    # Colonne 2 : Axe Central
    g.ajouter_arete(2, 8, poids=4); g.ajouter_arete(8, 14, poids=3); g.ajouter_arete(14, 20, poids=4); g.ajouter_arete(20, 26, poids=3); g.ajouter_arete(26, 32, poids=4)
    # Colonne 3 : Transit Nord-Sud
    g.ajouter_arete(3, 9, poids=5); g.ajouter_arete(9, 15, poids=6); g.ajouter_arete(15, 21, poids=5); g.ajouter_arete(21, 27, poids=6); g.ajouter_arete(27, 33, poids=5)
    # Colonne 4 : Quartier d'affaires lent
    g.ajouter_arete(4, 10, poids=8); g.ajouter_arete(10, 16, poids=9); g.ajouter_arete(16, 22, poids=8); g.ajouter_arete(22, 28, poids=7); g.ajouter_arete(28, 34, poids=8)
    # Colonne 5 : Boulevard Est
    g.ajouter_arete(5, 11, poids=3); g.ajouter_arete(11, 17, poids=3); g.ajouter_arete(17, 23, poids=3); g.ajouter_arete(23, 29, poids=3); g.ajouter_arete(29, 35, poids=3)

    # Liaisons directes ultra-rapides pour casser la monotonie de la grille
    g.ajouter_arete(5, 10, poids=2)   # Raccourci diagonal Nord-Est
    g.ajouter_arete(6, 9, poids=3)    # Pont entre l'Ouest et le centre haut
    g.ajouter_arete(0, 5, poids=6)    # La "Transversale Nord" (très long mais poids faible)
    g.ajouter_arete(10, 15, poids=2)  # Tunnel quartier d'affaires
    g.ajouter_arete(19, 21, poids=1)  # Le "Cœur de ville" ultra-rapide
    g.ajouter_arete(30, 35, poids=5)  # La "Transversale Sud"
    g.ajouter_arete(12, 26, poids=4)  # Grande diagonale traversante Ouest -> Centre Bas

    # --- 2. CRÉATION DE LA FLOTTE (Seulement 2 camions !) ---
    flotte = [camion1,camion2,camion3]

    # --- 3. GESTION DYNAMIQUE DES DEMANDES (Avalanche de requêtes) ---
    demandes_futures = {
        # Tour 2 : Les coins opposés pour forcer les longs trajets
        # Format : (nœud, quantité, (tw_debut, tw_fin))
        2: [(5, 10, (2, 25)), (30, 12, (5, 35))], 
        
        # Tour 5 : Une grappe au centre-nord (proche des raccourcis 6 et 9)
        5: [(7, 4, (5, 30)), (13, 3, (10, 40)), (8, 5, (5, 35))], 
        
        # Tour 10 : Énorme vague dispersée
        10: [(0, 6, (10, 50)), (35, 6, (15, 60)), (17, 4, (10, 30)), (18, 4, (15, 45)), (21, 5, (20, 50))], 
        
        # Tour 20 : Le "Cœur de ville" (Zone fluide, urgence modérée)
        20: [(19, 8, (20, 50)), (20, 10, (25, 60)), (14, 2, (20, 40))], 
        
        # Tour 35 : Test de la zone "Travaux" (Des livraisons avec des marges larges car la route est lente)
        35: [(10, 3, (35, 80)), (11, 3, (40, 90)), (4, 5, (35, 75))], 
        
        # Tour 50 : Ravitaillement lointain au Sud-Est
        50: [(29, 15, (50, 100)), (34, 10, (60, 120))],
        
        # Tour 70 : Dernière petite requête isolée (pas très pressée)
        70: [(25, 2, (70, 150))]
    }
    
    demandes_en_attente = []

    print("\n--- DÉBUT DE LA SIMULATION (MODE SURCHARGE) ---")
    tour_actuel = 1

    id_carg = 1
    while any(c.route or c.cible_actuelle is not None for c in flotte) or demandes_futures or demandes_en_attente:
        print(f"\n--- TOUR {tour_actuel} ---")
        
        # 1. APPARITION DES NOUVELLES DEMANDES
        if tour_actuel in demandes_futures:
            nouvelles_destinations = demandes_futures.pop(tour_actuel)
            print(f">>> [ALERTE] Nouvelles demandes apparues pour les destinations : {nouvelles_destinations} ! <<<")
                
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

        # 2. DISPATCHER INTELLIGENT (Gestion de Stock Corrigée)
        demandes_non_assignees = []
        for dest in demandes_en_attente:
            qte_requise = g.noeuds[dest].quantite
            
            camions_eligibles = []
            for c in flotte:
                # CORRECTION : On calcule TOUT ce qui est réservé dans la file (y compris la destination actuelle si elle existe)
                liste_totale = c.file_destinations.copy()
                if c.destination is not None and c.destination != depot:
                    liste_totale.append(c.destination)
                    
                poids_deja_reserve = sum(g.noeuds[d].quantite for d in liste_totale if d != depot and g.noeuds[d].requete_presente)
                stock_futur = c.charge_actuelle - poids_deja_reserve
                
                if stock_futur >= qte_requise:
                    camions_eligibles.append((c, stock_futur)) # On garde le stock futur pour l'affichage
            
            if camions_eligibles:
                meilleur_camion = None
                meilleur_index_global = 0
                meilleur_cout_global = float('inf')
                stock_futur_meilleur = 0
                
                # On évalue l'insertion seulement sur les camions (le [0] du tuple)
                for tuple_camion in camions_eligibles:
                    camion = tuple_camion[0]
                    stock_futur = tuple_camion[1]
                    index_opti, surcout = camion.evaluer_meilleure_insertion(g, dest)
                    
                    if surcout < meilleur_cout_global:
                        meilleur_cout_global = surcout
                        meilleur_index_global = index_opti
                        meilleur_camion = camion
                        stock_futur_meilleur = stock_futur
                
                # Le stock futur devient: ancien stock_futur - qte_requise
                print(f"--> [DISPATCH] {meilleur_camion.id} ajoute {dest} à sa tournée. (Stock futur garanti : {stock_futur_meilleur - qte_requise}/{meilleur_camion.capacite} kg)")
                meilleur_camion.assigner_demande(g, dest, index_insertion=meilleur_index_global)
            else:
                # Aucun camion n'a de stock pour ça
                demandes_non_assignees.append(dest)

        # 3. GESTION DU RETOUR AU DÉPÔT (Sorti de la boucle 'for dest' !)
        for c in flotte:
            # S'il est libre, qu'il a très peu de stock, et qu'il n'est PAS DÉJÀ au dépôt
            if not c.file_destinations and c.cible_actuelle is None and c.position != depot and c.charge_actuelle < 5:
                print(f"--- [LOGISTIQUE] {c.id} n'a plus assez de stock ({c.charge_actuelle}kg), retour au Depot ({depot}) ---")
                c.assigner_demande(g, depot)
                
        # Affichage critique : La file d'attente s'allonge !
        if demandes_non_assignees:
            print(f"!!! [SURCHARGE] {len(demandes_non_assignees)} requêtes en attente de stock/camion : {demandes_non_assignees} !!!")
                
        demandes_en_attente = demandes_non_assignees

        # =====================================================================
        # -> TABLEAU DE BORD DE LA FLOTTE
        # =====================================================================
        print("\n--- ETAT DES CAMIONS ---")
        for c in flotte:
            pos_actuelle = str(c.position) if c.position is not None else f"Vers {c.cible_actuelle}"
            dest_actuelle = str(c.destination) if c.destination is not None else "-"
            file_attente = str(c.file_destinations) if c.file_destinations else "[]"
            
            # Affichage de la charge avec une sécurité visuelle
            charge_affichee = max(0, c.charge_actuelle)
            print(f" {c.id} | Pos: {pos_actuelle:<7} | Objectif: {dest_actuelle:<3} | "
                  f"File d'attente: {file_attente:<12} | Charge actuelle: {charge_affichee}/{c.capacite}")
        print("---------------------------\n")

        # 4. FAIRE AVANCER LES CAMIONS
        for camion in flotte:
            camion.faire_un_tour(g, tour_actuel)
            
        tour_actuel += 1
        
        if tour_actuel > 250: 
            print("Limite de tours atteinte.")
            break
            
    print("\n--- FIN DE LA SIMULATION ---")
