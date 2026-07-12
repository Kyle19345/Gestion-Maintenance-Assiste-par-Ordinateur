# GMAO v0.0 — Gestion Machine

## À propos

Première version d'une application GMAO (Gestion de Maintenance Assistée par Ordinateur) destinée à gérer des machines et leurs interventions associées. L'objectif est de fournir une interface simple (Windows) pour enregistrer les machines, planifier et suivre les interventions, et conserver un historique dans une base SQLite locale.

## Table des matières

* 🪧 [À propos](#à-propos)
* 📦 [Prérequis](#prérequis)
* 🚀 [Installation](#installation)
* 🛠️ [Utilisation](#utilisation)
* 🏗️ [Construit avec](#construit-avec)

## Prérequis

Avant d'installer et d'utiliser le projet, assurez-vous d'avoir :

* **Python 3.10+** — Télécharger et installer depuis [https://www.python.org/](https://www.python.org/). Python 3.10 ou supérieur est recommandé pour la compatibilité avec `customtkinter`.
* **pip** — inclus avec Python moderne. Utiliser `python -m pip install --upgrade pip` pour mettre à jour.

### Dépendances 

* `customtkinter` — composants UI modernes.

> Les versions précises des dépendances sont indiquées dans `requirements.txt`.

## Installation

```bash
# 1) Créer et activer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate

# 2) Installer les dépendances
pip install -r requirements.txt

# 3) Lancer l'application
python main.py
```

## Utilisation

L'application fournit une interface graphique pour gérer les machines et les interventions.

### Démarrer en mode développement

```bash
# activer l'environnement virtuel (Windows)
.venv\Scripts\activate
python main.py
```

### Scénarios rapides

* **Ajouter une machine** : Menu `Machines` → `Ajouter` → remplir `ref` (unique), nom, fabricant, année.
* **Lister les machines** : Menu `Machines` → `Liste`.
* **Créer une intervention** : Sélectionner une machine → `Interventions` → `Ajouter` (une intervention doit être liée à une machine).
* **Planifier/Modifier** : Depuis la fiche d'intervention, modifier la date / description / statut.

> L'application crée automatiquement la base SQLite (`gmao.db`) à la première exécution si le script d'initialisation est présent.

## Construit avec

### Langages & Frameworks

* **Python 3.10+** — langage principal.
* **tkinter** / **customtkinter** — interface graphique.
* **SQLite** — base de données embarquée (fichier local `.db`).

### Outils



## Auteur / Contact

Ramanandraibe Kanto Andrianina — [andrianinakanto5@gmail.com](mailto:andrianinakanto5@gmail.com)

