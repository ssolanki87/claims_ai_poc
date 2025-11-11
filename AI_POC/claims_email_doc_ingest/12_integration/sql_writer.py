import pyodbc
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd

class SQLWriter:
    """SQL Server database writer for claims data"""
    def __init__(self, connection_string: str, logger=None):
        self.connection_string = connection_string
        self.logger = logger
    def get_connection(self):
        try:
            return pyodbc.connect(self.connection_string)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Database connection error: {str(e)}")
            raise
    def insert_email(self, email_data: Dict, table_name: str = "tbl_claims_emails") -> int:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            INSERT INTO {table_name} (
                message_id, subject, sender, recipients, email_date,
                body_text, body_html, has_attachments, attachment_count,
                blob_path, created_at
            )
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
            """
            cursor.execute(query, (
                email_data.get('message_id'),
                email_data.get('subject'),
                email_data.get('from'),
                json.dumps(email_data.get('to', [])),
                email_data.get('date'),
                email_data.get('body_text'),
                email_data.get('body_html'),
                len(email_data.get('attachments', [])) > 0,
                len(email_data.get('attachments', [])),
                email_data.get('blob_path')
            ))
            email_id = cursor.fetchone()[0]
            conn.commit()
            if self.logger:
                self.logger.info(f"Inserted email with ID: {email_id}")
            return email_id
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error inserting email: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    def insert_entities(self, email_id: int, entities: Dict, table_name: str = "tbl_extracted_entities") -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            INSERT INTO {table_name} (
                email_id, claim_number, policy_number, insured_name,
                date_of_loss, claim_amount, phone_numbers, email_addresses,
                incident_description, confidence_score, extraction_method,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
            """
            cursor.execute(query, (
                email_id,
                entities.get('claim_number'),
                entities.get('policy_number'),
                entities.get('insured_name'),
                entities.get('date_of_loss'),
                entities.get('claim_amount'),
                json.dumps(entities.get('phone_numbers', [])),
                json.dumps(entities.get('email_addresses', [])),
                entities.get('incident_description'),
                entities.get('confidence_score', 0.0),
                entities.get('extraction_method', 'ai')
            ))
            conn.commit()
            if self.logger:
                self.logger.info(f"Inserted entities for email ID: {email_id}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error inserting entities: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    def insert_triage_result(self, email_id: int, triage_data: Dict, table_name: str = "tbl_triage_results") -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            INSERT INTO {table_name} (
                email_id, priority_level, claim_type, risk_level,
                requires_escalation, assigned_to, triage_notes,
                confidence_score, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
            """
            cursor.execute(query, (
                email_id,
                triage_data.get('priority_level'),
                triage_data.get('claim_type'),
                triage_data.get('risk_level'),
                triage_data.get('requires_escalation', False),
                triage_data.get('assigned_to'),
                triage_data.get('triage_notes'),
                triage_data.get('confidence_score', 0.0)
            ))
            conn.commit()
            if self.logger:
                self.logger.info(f"Inserted triage result for email ID: {email_id}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error inserting triage result: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    def insert_attachments(self, email_id: int, attachments: List[Dict], table_name: str = "tbl_attachments") -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            for att in attachments:
                query = f"""
                INSERT INTO {table_name} (
                    email_id, filename, file_type, file_category, file_size,
                    blob_path, is_invoice, is_medical_record, document_type,
                    classification_confidence, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
                """
                cursor.execute(query, (
                    email_id,
                    att.get('filename'),
                    att.get('file_type'),
                    att.get('file_category'),
                    att.get('file_size'),
                    att.get('blob_path'),
                    att.get('is_invoice', False),
                    att.get('is_medical_record', False),
                    att.get('document_type'),
                    att.get('classification_confidence', 0.0)
                ))
            conn.commit()
            if self.logger:
                self.logger.info(f"Inserted {len(attachments)} attachments for email ID: {email_id}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error inserting attachments: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    def bulk_insert_dataframe(self, df: pd.DataFrame, table_name: str) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # This is a placeholder for bulk insert logic
            # Use fast_executemany or SQL bulk copy for production
            for _, row in df.iterrows():
                # Example: insert each row as a dict
                cursor.execute(f"INSERT INTO {table_name} VALUES (...) ")
            conn.commit()
            if self.logger:
                self.logger.info(f"Bulk inserted {len(df)} rows into {table_name}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error bulk inserting dataframe: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
