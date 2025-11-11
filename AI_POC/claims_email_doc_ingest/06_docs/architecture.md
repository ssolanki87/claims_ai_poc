# Architecture Overview

## Data Flow

1. **Blob Storage**: Emails and attachments are ingested from Azure Blob Storage.
2. **Email Ingest Pipeline**: Parses and stores emails in SQL Server.
3. **Entity Extraction**: Uses regex and GenAI to extract claim entities.
4. **Document Analysis**: Classifies attachments and extracts invoice data.
5. **Triage**: Classifies claims by risk and type.
6. **Monitoring**: Health checks and alerting via Teams webhook.
7. **Dashboards**: PowerBI and SQL dashboards for metrics and triage.

## Modular Components
- **00_configs**: Configuration and secrets
- **01_notebooks**: Databricks notebooks for POC/UAT/Prod
- **02_pipelines**: Python pipeline scripts
- **03_sql_queries**: SQL schema and queries
- **04_logs**: Logging utilities
- **05_tests**: Unit tests
- **06_docs**: Documentation
- **07_models**: ML models and entity classifiers
- **08_rag_kb**: RAG knowledge base and embeddings
- **09_dashboards**: PowerBI and SQL dashboards
- **10_monitoring**: Health monitoring and alerting
- **11_jobs**: Job scheduling and triggers
- **12_integration**: Integration connectors
- **13_archives**: Data archives and cleanup
