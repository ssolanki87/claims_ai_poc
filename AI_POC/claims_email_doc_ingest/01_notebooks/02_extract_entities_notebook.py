# Databricks notebook for claims email entity extraction and triage
import os
import yaml
import pandas as pd
from 07_models.entity_classifier import EntityClassifier
from 12_integration.email_parser import EmailParser
from 12_integration.blob_connector import BlobConnector
from 12_integration.sql_writer import SQLWriter

CONFIG_PATH = "/Workspace/AI_POC/claims_email_doc_ingest/00_configs/config_poc.json"
PATTERNS_PATH = "/Workspace/AI_POC/claims_email_doc_ingest/00_configs/entity_patterns.yaml"
EMAILS_PATH = "/Workspace/AI_POC/claims_email_doc_ingest/data/sample_emails.json"

# Load config
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

# Load emails (replace with blob ingestion in production)
emails = pd.read_json(EMAILS_PATH)

classifier = EntityClassifier(config)
parser = EmailParser()

results = []
for idx, row in emails.iterrows():
    entities = classifier.extract_all_entities(row['body_text'])
    doc_type = parser.classify_attachment_type(row.get('attachment_filename', ''))
    priority, confidence = classifier.classify_priority(row['body_text'], config)
    claim_type, claim_conf = classifier.classify_claim_type(row['body_text'], config)
    high_risk = classifier.is_high_risk(row['body_text'], config)
    results.append({
        "entities": entities,
        "doc_type": doc_type,
        "priority": priority,
        "claim_type": claim_type,
        "high_risk": high_risk
    })
    if high_risk:
        print(f"ALERT: High risk claim detected: {entities.get('claim_number')}")
print("Processing complete.")
