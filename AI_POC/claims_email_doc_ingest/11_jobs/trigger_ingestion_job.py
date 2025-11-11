from 02_pipelines.pipeline_master_orchestrator import MasterOrchestrator
from 04_logs.log_utils import LogUtils

logger = LogUtils.setup_logger("trigger_job", log_dir="../04_logs")
config_path = "../00_configs/config_poc.json"

def trigger_ingestion():
    logger.info("Triggering ingestion job...")
    orchestrator = MasterOrchestrator(config_path)
    results = orchestrator.run()
    logger.info(f"Ingestion job completed: {results['status']}")

if __name__ == "__main__":
    trigger_ingestion()
