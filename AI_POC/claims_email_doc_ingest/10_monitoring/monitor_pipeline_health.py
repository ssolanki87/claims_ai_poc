import json
from datetime import datetime, timedelta
from typing import Dict, List
from 00_configs.env_settings import settings
from 04_logs.log_utils import LogUtils
from 12_integration.sql_writer import SQLWriter
from 10_monitoring.teams_webhook_notifier import TeamsNotifier

class PipelineHealthMonitor:
    """Monitor pipeline health and performance"""
    def __init__(self, config_path: str):
        self.logger = LogUtils.setup_logger("health_monitor", log_dir="../04_logs")
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.sql_writer = SQLWriter(settings.db_connection_string, self.logger)
        self.notifier = TeamsNotifier(settings.TEAMS_WEBHOOK_URL, self.logger)
    def check_pipeline_failures(self, hours: int = 24) -> List[Dict]:
        conn = self.sql_writer.get_connection()
        cursor = conn.cursor()
        query = """
        SELECT pipeline_name, step_name, error_message, created_at, COUNT(*) as failure_count
        FROM tbl_processing_log
        WHERE status = 'failed'
            AND created_at >= DATEADD(hour, -?, GETDATE())
        GROUP BY pipeline_name, step_name, error_message, created_at
        ORDER BY created_at DESC
        """
        cursor.execute(query, (hours,))
        failures = cursor.fetchall()
        conn.close()
        result = []
        for row in failures:
            result.append({
                'pipeline': row[0],
                'step': row[1],
                'error': row[2],
                'timestamp': row[3],
                'count': row[4]
            })
        return result
    def check_unprocessed_emails(self) -> Dict:
        conn = self.sql_writer.get_connection()
        cursor = conn.cursor()
        queries = {
            'no_entities': f"""
                SELECT COUNT(*)
                FROM {self.config['database']['tables']['emails']} e
                LEFT JOIN {self.config['database']['tables']['entities']} ent 
                    ON e.id = ent.email_id
                WHERE ent.email_id IS NULL
                    AND e.created_at < DATEADD(hour, -2, GETDATE())
            """,
            'no_triage': f"""
                SELECT COUNT(*)
                FROM {self.config['database']['tables']['emails']} e
                INNER JOIN {self.config['database']['tables']['entities']} ent 
                    ON e.id = ent.email_id
                LEFT JOIN {self.config['database']['tables']['triage']} t 
                    ON e.id = t.email_id
                WHERE t.email_id IS NULL
                    AND e.created_at < DATEADD(hour, -2, GETDATE())
            """
        }
        results = {}
        for key, query in queries.items():
            cursor.execute(query)
            count = cursor.fetchone()[0]
            results[key] = count
        conn.close()
        return results
    def check_high_risk_unreviewed(self) -> List[Dict]:
        conn = self.sql_writer.get_connection()
        cursor = conn.cursor()
        query = f"""
        SELECT e.id, e.subject, ent.claim_number, t.priority_level, t.created_at
        FROM {self.config['database']['tables']['emails']} e
        INNER JOIN {self.config['database']['tables']['entities']} ent ON e.id = ent.email_id
        INNER JOIN {self.config['database']['tables']['triage']} t ON e.id = t.email_id
        WHERE t.requires_escalation = 1
            AND t.reviewed_at IS NULL
            AND t.created_at < DATEADD(hour, -4, GETDATE())
        ORDER BY t.created_at ASC
        """
        cursor.execute(query)
        unreviewed = cursor.fetchall()
        conn.close()
        result = []
        for row in unreviewed:
            result.append({
                'email_id': row[0],
                'subject': row[1],
                'claim_number': row[2],
                'priority': row[3],
                'pending_since': row[4]
            })
        return result
    def run_health_check(self) -> Dict:
        self.logger.info("Starting pipeline health check")
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'failures': self.check_pipeline_failures(hours=24),
            'unprocessed': self.check_unprocessed_emails(),
            'high_risk_pending': self.check_high_risk_unreviewed()
        }
        has_failures = len(health_report['failures']) > 0
        has_stuck_emails = any(count > 10 for count in health_report['unprocessed'].values())
        has_pending_high_risk = len(health_report['high_risk_pending']) > 5
        if has_failures or has_stuck_emails or has_pending_high_risk:
            health_report['status'] = 'UNHEALTHY'
            self.logger.warning("Pipeline health check: UNHEALTHY")
            alert_message = f"""
Pipeline Health Alert:
- Failures in last 24h: {len(health_report['failures'])}
- Unprocessed emails: {sum(health_report['unprocessed'].values())}
- High-risk pending review: {len(health_report['high_risk_pending'])}
            """
            self.notifier.send_error_alert("Pipeline Health Check", alert_message)
        else:
            health_report['status'] = 'HEALTHY'
            self.logger.info("Pipeline health check: HEALTHY")
        return health_report

if __name__ == "__main__":
    monitor = PipelineHealthMonitor("../00_configs/config_poc.json")
    report = monitor.run_health_check()
    print(json.dumps(report, indent=2, default=str))
