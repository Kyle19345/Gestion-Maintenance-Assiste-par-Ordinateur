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
# Ajout relation entre intervention et machine
# Table Enum pour intervention
# Modification fonction pour Les interventions (priorité haute)
# Refactoriser completement la BDD (priorité haute)


from typing import List, Tuple

import sqlite3
import logging

from dataclasses import asdict

from models.machine import Machine
from models.intervention import Intervention


logger = logging.getLogger(__name__)


class BaseDeDonne:
    """
    Base de donné principal de l'application
    """
    def __init__(self, path="config/database.db"):
        self.com = sqlite3.connect(path)
        self.cur = self.com.cursor()

        self.cur.execute("PRAGMA foreign_keys = ON")

        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS machine(
                            machine_id PRIMARY KEY NOT NULL,
                            ref TEXT UNIQUE,
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
                            intervention_id PRIMARY KEY NOT NULL, 
                            ref TEXT UNIQUE,
                            description TEXT NOT NULL,
                            date_intervention TEXT NOT NULL,
                            machine_id TEXT NOT NULL,
                            dure INTEGER,
                            outils TEXT NOT NULL,
                            executant TEXT NOT NULL,
                            statut TEXT NOT NULL,
                            FOREIGN KEY (machine_id)
                                REFERENCES machine (machine_id)
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
            data = asdict(intervention)
            columns = ",".join(data.keys())
            placeholders = ",".join("?" for _ in data)

            sql = f"""
            INSERT INTO intervention ({columns})
            VALUES ({placeholders})
            """

            self.cur.execute(sql, tuple(data.values()))
            self.com.commit()
            logger.info("Intervention ajouter")

        except Exception:
            logger.exception("Erreur lors de l'ajout")
            raise

    def add_machine(self, machine: Machine) -> None:
        """
        Fonction permettant d'ajouter une machine dans la table machine
        Args:
            machine: Objet Machine
        """
        try:
            data = asdict(machine)
            columns = ",".join(data.keys())
            placeholders = ",".join("?" for _ in data)

            sql = f"""
            INSERT INTO machine ({columns})
            VALUES ({placeholders})
            """

            self.cur.execute(sql, tuple(data.values()))
            self.com.commit()
            logger.info("Machine ajouter")

        except Exception:
            logger.exception("Erreur lors de l'ajout")
            raise

    def get_all_intervention(self) -> List[Intervention]:
        """
        Recupère toutes les interventions avec le statut réalisé
        """
        self.cur.execute(
            """
            SELECT * FROM intervention 
            WHERE statut='Réalisé'
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
            SELECT * FROM machine
            """
        )
        rows = self.cur.fetchall()
        logger.info("Extraction machine effectué depuis la Bdd")
        return [Machine(*row) for row in rows]

    def get_every_intervention(self):
        """
        Récupère toutes les interventions avec toutes les status
        """
        self.cur.execute(
            """
            SELECT * FROM intervention
            """
        )
        rows = self.cur.fetchall()
        logger.info("Extraction intervention effectué depuis la Bdd")
        return [Intervention(*row) for row in rows]

    def get_planing(self) -> List[Intervention]:
        """
        Récupère toutes les interventions qui n'ont pas encore été réalisé
        """
        self.cur.execute(
            """
            SELECT * FROM intervention 
            WHERE statut != 'Réalisé' ORDER BY date_intervention ASC
            """
        )
        rows = self.cur.fetchall()
        logger.info("Extraction planing effectué depuis la Bdd")
        return [Intervention(*row) for row in rows]

    def update_intervention(self, intervention: Intervention) -> None:
        """
        Met à jour une intervention en fonction de ref
        """
        data = asdict(intervention)
        
        data_update = {k: v for k, v in data.items() if k != "intervention_id"}
        set_clause = ", ".join(f"{col} = ?" for col in data_update)
        
        sql = f"""
        UPDATE intervention SET {set_clause}
        WHERE intervention_id = ?
        """
        try:
            values = list(data_update.values())
            values.append(intervention.intervention_id)

            self.cur.execute(sql, values)
            self.com.commit()
            logger.info("Mise à jour effectué")

        except Exception:
            logger.exception("Erreur dans la mise à jour des données")
            raise

    def update_machine(self, machine: Machine) -> None:
        """
        Met à jour une machine en 
        """
        data = asdict(machine)

        data_update = {k: v for k, v in data.items() if k != "machine_id"}
        set_clause = ", ".join(f"{col} = ?" for col in data_update)

        sql = f"""
        UPDATE machine SET {set_clause}
        WHERE machine_id = ?
        """        
        try:
            values = list(data_update.values())
            values.append(machine.machine_id)

            self.cur.execute(sql, values)
            self.com.commit()
            logger.info("Mise à jour effectué")

        except Exception:
            logger.exception("Erreur dans la mise à jour des données")
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

    def delete_machine(self, machine_id: str) -> None:
        """
        Supprime une machine par rapport à son ID
        Args:
            machine_id: ID machine
        """
        try:
            self.cur.execute(
                """
                DELETE FROM machine
                    WHERE machine_id = ?
                """,
                (machine_id, )
            )
            self.com.commit()
            logger.info("Suppression effectué %s", machine_id)

        except Exception:
            logger.info("Erreur lors de la suppression de l'élement")
            raise

    def delete_intervention(self, intervention_id: str) -> None:
        """
        Supprime une intervention
        Args:
            intervention_id: l'id de l'intervention
        """
        try:
            self.cur.execute(
                """
                DELETE FROM intervention
                    WHERE intervention_id = ?
                """,
                (intervention_id, )
            )
            self.com.commit()
            logger.info("Suppression intervention effectué")

        except Exception:
            logger.info("Erreur lors de la suppression de l'élement")
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

        except Exception:
            logger.exception("Erreur dans la fermeture de la Bdd")
            raise
