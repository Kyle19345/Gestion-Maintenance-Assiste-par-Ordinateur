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
# Refactoriser completement la BDD (priorité haute)


from typing import List, Tuple

import sqlite3
import logging

from dataclasses import asdict

from models.machine import Machine, EtatMachine
from models.intervention import Intervention, StatutIntervention


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
                            description TEXT,
                            date_intervention TEXT NOT NULL,
                            machine_id TEXT,
                            dure INTEGER,
                            outils TEXT,
                            executant TEXT NOT NULL,
                            statut TEXT NOT NULL,
                            FOREIGN KEY (machine_id)
                                REFERENCES machine (machine_id)
                                ON DELETE CASCADE
                        )
                        """)

        self.com.commit()
        logger.info("Base de données initialisée")

    def _execute_sql(
            self,
            sql: str,
            values: tuple,
            log_success: str = "",
            log_error: str = ""
    ) -> None:
        try: 
            self.cur.execute(sql, values)
            self.com.commit()
            logger.info(log_success)

        except Exception:
            logger.exception(log_error)
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

    
    def add_intervention(self, intervention: Intervention) -> None:
        """
        Fonction permettant d'ajouer une intervention
        dans la table Intervention
        Args:
            intervention: Objet Intervention
        """
        data = asdict(intervention)
        if isinstance(data["statut"], StatutIntervention):
            data["statut"] = data["statut"].value

        columns = ",".join(data.keys())
        placeholders = ",".join("?" for _ in data)

        sql = f"""
        INSERT INTO intervention ({columns})
        VALUES ({placeholders})
        """

        values = tuple(data.values())
        self._execute_sql(
            sql=sql,
            values = values,
            log_success = f"Interveniton {data['ref']} ajouter dans la db",
            log_error = f"Erreur lors de l'enregistrement de l'intervention {data['ref']} "
        )
    
    def add_machine(self, machine: Machine) -> None:
        """
        Fonction permettant d'ajouter une machine dans la table machine
        Args:
            machine: Objet Machine
        """
        data = asdict(machine)
        if isinstance(data["etat"], EtatMachine):
            data["etat"] = data["etat"].value

        columns = ",".join(data.keys())
        placeholders = ",".join("?" for _ in data)

        sql = f"""
        INSERT INTO machine ({columns})
        VALUES ({placeholders})
        """
        values = tuple(data.values())
        self._execute_sql(
            sql=sql,
            values=values,
            log_success=f"Machine {data['ref']} enregistrer dans la db",
            log_error=f"Erreur lors de l'enregistrement de la machine {data['ref']} dans la db"
        )
    
    def update_intervention(self, intervention: Intervention) -> None:
        """
        Met à jour une intervention en fonction de ref
        """
        data = asdict(intervention)
        if isinstance(data["statut"], StatutIntervention):
            data["statut"] = data["statut"].value
        
        data_update = {k: v for k, v in data.items() if k != "intervention_id"}
        set_clause = ", ".join(f"{col} = ?" for col in data_update)
        
        sql = f"""
        UPDATE intervention SET {set_clause}
        WHERE intervention_id = ?
        """
        values = list(data_update.values())
        values.append(intervention.intervention_id)

        self._execute_sql(
            sql=sql,
            values=values,
            log_success=f"Mise à jour de l'intervention {data['ref']} effectué",
            log_error=f"Erreur lors de la mise à jour de l'intervention {data['ref']}"
        )
        
    def update_machine(self, machine: Machine) -> None:
        """
        Met à jour une machine
        """
        data = asdict(machine)
        if isinstance(data["etat"], EtatMachine):
            data["etat"] = data["etat"].value

        data_update = {k: v for k, v in data.items() if k != "machine_id"}
        set_clause = ", ".join(f"{col} = ?" for col in data_update)

        sql = f"""
        UPDATE machine SET {set_clause}
        WHERE machine_id = ?
        """        
        values = list(data_update.values())
        values.append(machine.machine_id)

        self._execute_sql(
            sql=sql,
            values=values,
            log_success=f"Mise à jour de la machine {data['ref']} effectué.",
            log_error=f"Erreur lors de la mise à jour de la machine {data['ref']}."
        )
       
    def get_intervention_asset(
            self,
            machine_id: str
    ) -> List[Intervention]:
        """
        Récupère les interventions assignées à une machine.
        """
        self.cur.execute(
            """
            SELECT * FROM intervention WHERE machine_id = ? AND statut = 'Planifié'
                ORDER BY date_intervention ASC
            """,
            (machine_id, )
        )
        rows = self.cur.fetchall()
        return [Intervention(*row) for row in rows]

    def delete_machine(self, machine_id: str) -> None:
        """
        Supprime une machine par rapport à son ID
        Args:
            machine_id: ID machine
        """
        sql = f"""
        DELETE FROM machine
             WHERE machine_id = ?
        """
        values = (machine_id, )

        self._execute_sql(
            sql=sql,
            values=values,
            log_success=f"Suppression effectué {machine_id}",
            log_error=f"Erreur lors de la suppression de l'élément {machine_id}"
        )

    def delete_intervention(self, intervention_id: str) -> None:
        """
        Supprime une intervention
        Args:
            intervention_id: l'id de l'intervention
        """
        sql = f"""
        DELETE FROM intervention
            WHERE intervention_id = ?
        """

        values = (intervention_id, )

        self._execute_sql(
            sql=sql,
            values=values,
            log_success=f"Suppression intervention {intervention_id} effectué.",
            log_error=f"Erreur lors de la suppression de l'intervention {intervention_id}."
        )
       
    def find_intervention(
            self,
            intervention_ref: str
    ) -> List[Intervention]:
        """
        Retrouve une Intervention
        """
        self.cur.execute(
            """
            SELECT * FROM intervention WHERE ref LIKE ?
            """,
            (f"%{intervention_ref}%", )
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
