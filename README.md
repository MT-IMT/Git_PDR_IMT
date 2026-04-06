# Git_PDR_IMT_Approches_centralisé_et_décentralisé_VRP_dynamique

Indication :
Nous considérons que les camions partent de l'entrepôt central (le dépôt) déjà chargé.
A chaque livraison de client, on retire la quantité de produit livré à la charge actuelle du camion. 
La capacité du camion se recharge au maximum en retournant au dépôt.

# 1. La classe Noeud représente un sommet du réseau.
Chaque client sera forcément sur un noeud.
Chaque nœud a notamment :

- id : identifiant unique
- nom : nom du lieu
- x, y : coordonnées spatiales
- time_window : plage horaire d’ouverture/fermeture
- requete_presente : indique s’il y a une demande active (booleen)
- quantite : quantité demandée par le client
- id_carg : identifiant de cargaison
- statut : "en_attente", "servi", "en_cours_livraison"
- heure_apparition : moment(tour) où la demande apparaît

# 2. La classe Arete relie :
- un nœud source
- un nœud cible

De plus, chaque arête possède un poids, ce poids va correspondre au nombre de tours pour parcourir l'arête, si l'arête a un poids de 3, le camion va mettre 3 tours pour la parcourir.

# 3. Graphe : la carte routière
La classe Graphe stocke tout le réseau.
Elle contient :

- noeuds : dictionnaire des nœuds
- aretes : liste de toutes les arêtes
- adjacence : liste d’adjacence pour connaître les voisins
- demandes : liste de demandes construites depuis les nœuds actifs

Méthodes principales :
- ajouter_noeud(noeud) : Ajoute un nœud au graphe.
- ajouter_arete(source_id, cible_id, poids, **attributs) : Ajoute une route entre deux nœuds.
Si le graphe n’est pas orienté (oriente=False), il ajoute aussi la route inverse.
- voisins(noeud_id): Renvoie les voisins d’un nœud.
- poids_arete(source_id, cible_id) : Renvoie le poids d’une route directe entre deux nœuds.
- construire_demandes() : Construit une liste des demandes à partir des nœuds où requete_presente == True.
- dijkstra(depart_idx, arrivee_idx) : Implémente un calcul de plus court chemin.

# 4. Camion
Représente un véhicule de livraison autonome se déplaçant sur le graphe.

Attributs :

- État général : id, capacite, disponible, charge_actuelle, cargaison.

- Déplacement : position, destination, cible_actuelle, route, temps_restant.

- Attributs (Centralisé) : file_destinations (pour gérer les arrêts multiples) et noeud_depot (pour le retour automatique).

Fonctions de base de la classe Camion :

- demander(...) / recharger() / decharger(...) : Gestion du stock physique du camion.

- trouver_chemin_vers(...) : Appelle Dijkstra pour calculer la route jusqu'à l'objectif.

- _demarrer_deplacement(...) / mettre_a_jour(...) / avancer(...) : Logique de déplacement abstrait/continu.

- assigner_demande(...) / faire_un_tour(...) / _arriver_a_destination(...) : Moteur de déplacement "Tour par Tour" classique (un arrêt à la fois).

- recevoir_message(...) / traiter_messages(...) : Ancien système de communication entre agents.

Fonctions centralisés de la classe Camion :

- evaluer_meilleure_insertion(graphe, nouvelle_dest) : Cœur mathématique de l'optimisation. Teste l'insertion d'un nouveau client entre chaque arrêt prévu dans la file d'attente pour trouver la position générant le surcoût kilométrique le plus faible.

- insertion_demande_centralisee(...) : Insère la demande à l'index optimal calculé.

- passer_a_la_prochaine_destination(...) : Permet au camion d'enchaîner directement avec le prochain client de sa file sans s'arrêter.

- faire_un_tour_centralise(...) : Moteur de déplacement de la simulation.

- _arriver_a_destination_centraliser(...) : Gère le déchargement physique, le rechargement automatique si le nœud actuel est le dépôt, puis l'enchaînement avec la mission suivante.

# 5. Utilitaire et Environnement

- distance_entre(graphe, depart, arrivee) : Calcule la distance entre deux nœuds sans modifier l'état des camions (utilisé par le Dispatcher).

- graphe_exemple() : Génère une petite ville de test (4x4, 16 nœuds, 2 camions).

- graphe_complexe() : Génère un environnement massif pour les "Stress Tests" (6x6, 36 nœuds, trafic hétérogène, 3 camions haute capacité).

# 6. Gestion du temps et des tours
Le temps s'écoule de manière séquentielle, où une unité de temps correspond à "1 Tour".
L'horloge globale de la simulation est régie par la variable tour_actuel. À chaque itération de la boucle principale, l'algorithme exécute une séquence d'actions strictes avant de faire avancer le temps :

- A. Émergence des événements (Demandes dynamiques) : Le système interroge le dictionnaire chronologique demandes_futures. Si le tour_actuel correspond à une clé du dictionnaire, les nouvelles requêtes (colis) apparaissent instantanément sur le réseau et sont placées dans la file d'attente globale
- B. Dispatcher centralisé ou décentralisé
- C. Phase d'Action (Mouvement de la flotte) : Chaque camion exécute sa méthode faire_un tour ou faire_un_tour_optimise
- D. Incrémentation: l'horloge augmente de 1 tour.


# 7. Le Dispatcher Centralisé & Heuristique d'Insertion

Plutôt que d'assigner la livraison au camion le plus proche géographiquement et de l'ajouter à la fin de son trajet (approche naïve), le dispatcher optimisé utilise une Cheapest Insertion Heuristic :

- Filtre de Stock Prévisionnel : Avant d'accepter une commande, le dispatcher calcule le "stock futur" du camion (charge actuelle - poids de toutes les commandes déjà présentes dans sa file d'attente). Un camion n'accepte une commande que s'il a une garantie de stock.

- Évaluation de l'Insertion : La méthode evaluer_meilleure_insertion simule l'insertion du nouveau client entre chaque arrêt déjà prévu dans la file_destinations.

- Calcul du Surcoût : Il calcule l'impact kilométrique de ce détour via la formule : Distance(A, Client) + Distance(Client, B) - Distance(A, B). La commande est assignée au camion (et à l'index précis) offrant le surcoût global le plus bas.

Ravitaillement au dépôt: 
Les camions gèrent désormais leurs propres allers-retours au dépôt. Si un camion termine sa tournée (ou est inactif) et que sa charge_actuelle tombe sous un seuil critique (ex: < 5 kg), le système appelle automatiquement la méthode assigner_demande_optimisee(g, depot) pour le renvoyer refaire le plein.

Affichage:
Un tableau de bord s'affiche dans la console à chaque tour de boucle. Il permet de monitorer en direct pour chaque camion :

  - Sa position instantanée (ou sa direction en transit).

  - Son objectif immédiat.

  - Le contenu exact de sa file d'attente (multi-arrêts).

  - Sa charge physique en temps réel.

# 8. Le Dispatcher Décentralisé


Contrairement à l’approche centralisée, il n’existe ici **aucune entité globale** qui prend les décisions. 
Le système repose sur une logique **distribuée et multi-agents**, où chaque camion agit de manière autonome.

Chaque camion est capable de :
* Recevoir les demandes.
* Évaluer leur coût.
* Proposer une offre.
* Être sélectionné pour effectuer la livraison.

Le mécanisme utilisé est inspiré des **systèmes d’enchères (auction-based)**.

## Principe général

À chaque tour de simulation, le dispatcher décentralisé suit une séquence bien définie :

1. **Diffusion** des demandes vers les camions.
2. **Calcul** des surcoûts par chaque camion.
3. **Collecte** des offres.
4. **Attribution** des demandes aux meilleurs camions.

Ce processus est répété dynamiquement à chaque tour.

## a. Diffusion des demandes

La fonction `diffuser_demandes` permet d’envoyer chaque demande active à tous les camions disponibles. Chaque demande est encapsulée dans un objet `Message` :

* **Type :** `"demande"`
* **Contenu :** identifiant du nœud à desservir

Chaque camion stocke ces messages dans une **boîte de réception (`boite_reception`)**. Cela simule une communication simple entre agents dans un système distribué.

## b. Calcul local du surcoût

Chaque camion traite ses messages via la méthode :
`traiter_messages(graphe, tour_actuel)`

Cette méthode parcourt la `boite_reception` du camion et, pour chaque message de type "demande", calcule un coût associé via :
`calcul_surcout(graphe, destination, tour_actuel)`

### Algorithme de calcul
Le surcoût repose sur deux piliers majeurs :
* **La distance** jusqu’à la destination (calculée via l'algorithme de Dijkstra).
* **Une pénalité** si la livraison dépasse la fenêtre temporelle (`time_window`).

$$surcoût = distance + pénalité\_de\_retard$$

> **Cas particuliers :**
> * Si aucun chemin n’existe : $coût = \infty$.
> * Si la contrainte temporelle est violée : application d'une pénalisation forte.

Chaque camion génère ensuite une **offre** contenant l'identifiant de la demande, l'identifiant du camion et le coût calculé.


## c. Collecte des offres

La fonction `collecter_offres` centralise toutes les propositions des camions. Les offres sont structurées sous la forme :
`demande_id` $\rightarrow$ `liste d’offres (camion, coût)`

* Seules les offres valides (coût fini) sont conservées.
* Cette étape simule une remontée d’information sans prise de décision globale immédiate.

## d. Attribution des demandes (enchères)

La fonction `attribuer` sélectionne, pour chaque demande, l’offre ayant le **coût minimal**.

```python
# Logique de sélection simplifiée
gagnant = min(liste_offres, key=lambda x: x["cout"])
```

# 9. Résultat

Graphe exemple:
- Centralisé : 53 tours
- Décentralisé : 52 tours

Graphe deux villes:
- Centralisé: 51 tours
- Décentralisé :

Graphe complexe: 
-Centralisé : 75 tours
-Décentralisé : 77 tours

