"""
Ce module permet la création des tables de la Base de donné,
et regroupe les différents fonctions pour manipuler chaque table.

La Base de donné est composé de la table machine permettant la gestion
des machines et de la table intervention
permettant la gestion des interventions
et planing sur chaque machine.
"""
#TODO: 
# création classe exceptions pour les lever d'exception 
# dans chaque fonction.
# Optimisation de la BDD.
# Système Backup des données.
# Identifiant unique, utilisation uuid.


from typing import List, Tuple

import sqlite3
import logging

from models.machine import Machine
from models.intervention import Intervention


logger = logging.getLogger(__name__)


class BaseDeDonne:
    """
    Base de donné principal de l'application
    """
    def __init__(self, path="DataBase.db"):
        self.com = sqlite3.connect(path)
        self.cur = self.com.cursor()

        self.cur.execute("PRAGMA foreign_keys = ON")

        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS machine(
                            ID TEXT UNIQUE,
                            nom TEXT NOT NULL,
                            categorie TEXT NOT NULL,
                            date_service TEXT NOT NULL,
                            fabricant TEXT NOT NULL,
                            etat TEXT NOT NULL,
                            compteur INTEGER
                        )
                        """)

        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS intervention (
                            ref TEXT UNIQUE,
                            description TEXT NOT NULL,
                            date_intervention TEXT NOT NULL,
                            machine TEXT NOT NULL,
                            dure INTEGER,
                            outils TEXT NOT NULL,
                            executant TEXT NOT NULL,
                            statut TEXT NOT NULL,
                            FOREIGN KEY (machine)
                                REFERENCES machine (ID)
                                ON DELETE CASCADE
                        )
                        """)

        self.com.commit()
        logger.info("Base de données initialisée")

    def add_intervention(self, intervention: Intervention) -> None:
        """
        Fonction permettant d'ajouer une intervention
        dans la table Intervention
        Args:
            intervention: Objet Intervention
        """
        try:
            self.cur.execute(
                """
                INSERT INTO intervention
                    (ref,description,date_intervention,machine,dure,outils,executant,statut)
                    VALUES(?,?,?,?,?,?,?,?)
                """,
                (
                    intervention.ref,
                    intervention.description,
                    intervention.date_intervention,
                    intervention.machine,
                    intervention.dure,
                    intervention.outils,
                    intervention.executant,
                    intervention.statut
                )
            )
            self.com.commit()
            logger.info("Intervention ajouter")

        except Exception as e:
            logger.exception("Erreur lors de l'ajout", e)
            raise

    def add_machine(self, machine: Machine) -> None:
        """
        Fonction permettant d'ajouter une machine dans la table machine
        Args:
            machine: Objet Machine
        """
        try:
            self.cur.execute(
                """
                INSERT INTO machine
                    (ID,nom,categorie,date_service,fabricant,etat,compteur)
                    VALUES(?,?,?,?,?,?,?)
                """,
                (
                    machine.ID,
                    machine.nom,
                    machine.categorie,
                    machine.date_service,
                    machine.fabricant,
                    machine.etat,
                    machine.compteur
                )
            )
            self.com.commit()
            logger.info("Machine ajouter")

        except Exception as e:
            logger.exception("Erreur lors de l'ajout", e)
            raise

    def get_all_intervention(self) -> List[Intervention]:
        """
        Recupère toutes les interventions avec le statut réalisé
        """
        self.cur.execute(
            """
            SELECT ref,description,date_intervention,machine,dure,outils,executant,statut
                FROM intervention WHERE statut='Réalisé'
            """
        )
        rows = self.cur.fetchall()
        logger.info("Extraction intervention effectué depuis la Bdd")
        return [Intervention(*row) for row in rows]

    def get_all_machine(self) -> List[Machine]:
        """
        Récupère toutes les machines de la table machine
        """
        self.cur.execute(
            """
            SELECT ID,nom,categorie,date_service,fabricant,etat,compteur
                FROM machine
            """
        )
        rows = self.cur.fetchall()
        logger.info("Extraction machine effectué depuis la Bdd")
        return [Machine(*row) for row in rows]

    def get_planing(self) -> List[Intervention]:
        """
        Récupère toutes les interventions qui n'ont pas encore été réalisé
        """
        self.cur.execute(
            """
            SELECT ref,description,date_intervention,machine,dure,outils,executant,statut
                FROM intervention WHERE statut != 'Réalisé' ORDER BY date_intervention ASC
            """
        )
        rows = self.cur.fetchall()
        logger.info("Extraction planing effectué depuis la Bdd")
        return [Intervention(*row) for row in rows]

    def update_intervention(self, intervention: Intervention) -> None:
        """
        Met à jour une intervention en fonction de ref
        """
        try:
            self.cur.execute(
                """
                UPDATE intervention
                    SET description = ?,
                    date_intervention = ?,
                    dure = ?,
                    outils = ?,
                    executant = ?,
                    statut = ?
                    WHERE ref = ?
                """,
                (
                    intervention.description,
                    intervention.date_intervention,
                    intervention.dure,
                    intervention.outils,
                    intervention.executant,
                    intervention.statut,
                    intervention.ref
                )
            )
            self.com.commit()
            logger.info("Mise à jour effectué")

        except Exception as e:
            logger.exception("Erreur dans la mise à jour des données", e)
            raise

    def update_machine(self, machine: Machine) -> None:
        """
        Met à jour une machine en fonction de son ID
        """
        try:
            self.cur.execute(
                """
                UPDATE machine
                    SET nom = ?,
                    categorie = ?,
                    date_service = ?,
                    fabricant = ?,
                    etat = ?,
                    compteur = ?
                    WHERE ID = ?
                """,
                (
                    machine.nom,
                    machine.categorie,
                    machine.date_service,
                    machine.fabricant,
                    machine.etat,
                    machine.compteur,
                    machine.ID
                )
            )
            self.com.commit()
            logger.info("Mise à jour effectué")

        except Exception as e:
            logger.exception("Erreur dans la mise à jour des données", e)
            raise

    def get_intervention_asset(
            self,
            machine: Machine
    ) -> List[Tuple[str, str, str]]:
        """
        Récupère les interventions assignées à chaque machine
        """
        self.cur.execute(
            """
            SELECT ref,description,date_intervention
                FROM intervention WHERE machine = ? AND statut = 'Planifié'
                ORDER BY date_intervention ASC
            """,
            (machine, )
        )
        return self.cur.fetchall()

    def delete_machine(self, machine: Machine) -> None:
        """
        Supprime une machine par rapport à son ID
        """
        try:
            self.cur.execute(
                """
                DELETE FROM machine
                    WHERE ID = ?
                """,
                (machine, )
            )
            self.com.commit()
            logger.info("Suppression effectué %s", machine)

        except Exception as e:
            logger.info("Erreur lors de la suppression de l'élement", e)
            raise

    def delete_intervention(self, intervention: Intervention) -> None:
        """
        Supprime une intervention
        """
        try:
            self.cur.execute(
                """
                DELETE FROM intervention
                    WHERE ref = ?
                """,
                (intervention, )
            )
            self.com.commit()
            logger.info("Suppression intervention effectué")

        except Exception as e:
            logger.info("Erreur lors de la suppression de l'élement", e)
            raise

    def find_intervention(
            self,
            intervention: Intervention
    ) -> List[Intervention]:
        """
        Retrouve une Intervention
        """
        self.cur.execute(
            """
            SELECT ref,description,date_intervention,machine,dure,outils,executant,statut
                FROM intervention WHERE ref LIKE ?
            """,
            (f"%{intervention}%", )
        )
        rows = self.cur.fetchall()
        return [Intervention(*row) for row in rows]

    def close(self) -> None:
        "Ferme la BDD"
        self.com.commit()
        try:
            self.com.close()
            logger.info("Bdd fermé ")

        except Exception as e:
            logger.exception("Erreur dans la fermeture de la Bdd", e)
            raise
