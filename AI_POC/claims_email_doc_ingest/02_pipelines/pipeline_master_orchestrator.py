from 02_pipelines.pipeline_email_ingest import run_email_ingest
from 02_pipelines.pipeline_doc_analysis import run_doc_analysis
from 12_integration.sql_writer import SQLWriter
from 00_configs.env_settings import settings
from 04_logs.log_utils import LogUtils

class MasterOrchestrator:
    """Orchestrates the full claims email pipeline"""
    def __init__(self, config_path: str):
        self.logger = LogUtils.setup_logger("master_orchestrator", log_dir="../04_logs")
        self.sql_writer = SQLWriter(settings.db_connection_string, self.logger)
        self.config_path = config_path
    def run(self):
        self.logger.info("Starting master pipeline orchestration")
        ingest_results = run_email_ingest(self.config_path, self.sql_writer, self.logger)
        doc_results = run_doc_analysis(self.config_path, self.sql_writer, self.logger)
        # Add additional steps as needed
        status = "SUCCESS" if ingest_results and doc_results else "FAILED"
        return {"status": status, "ingest": ingest_results, "doc_analysis": doc_results}
