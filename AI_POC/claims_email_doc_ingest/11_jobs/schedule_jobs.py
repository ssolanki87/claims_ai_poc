import schedule
import time
from datetime import datetime
from 04_logs.log_utils import LogUtils
from 02_pipelines.pipeline_master_orchestrator import MasterOrchestrator
from 10_monitoring.monitor_pipeline_health import PipelineHealthMonitor

logger = LogUtils.setup_logger("job_scheduler", log_dir="../04_logs")
config_path = "../00_configs/config_poc.json"

def run_full_pipeline():
    try:
        logger.info("Starting scheduled full pipeline execution")
        orchestrator = MasterOrchestrator(config_path)
        results = orchestrator.run()
        logger.info(f"Pipeline completed: {results['status']}")
    except Exception as e:
        logger.error(f"Scheduled pipeline failed: {str(e)}")

def run_health_check():
    try:
        logger.info("Starting scheduled health check")
        monitor = PipelineHealthMonitor(config_path)
        report = monitor.run_health_check()
        logger.info(f"Health check completed: {report['status']}")
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")

def setup_schedules():
    schedule.every(4).hours.do(run_full_pipeline)
    schedule.every(1).hours.do(run_health_check)
    schedule.every().day.at("08:00").do(run_full_pipeline)
    schedule.every().day.at("13:00").do(run_full_pipeline)
    schedule.every().day.at("18:00").do(run_full_pipeline)
    logger.info("Job schedules configured")
    logger.info("- Full pipeline: Every 4 hours + 08:00, 13:00, 18:00")
    logger.info("- Health check: Every hour")

if __name__ == "__main__":
    logger.info("Starting job scheduler")
    setup_schedules()
    run_health_check()
    while True:
        schedule.run_pending()
        time.sleep(60)
