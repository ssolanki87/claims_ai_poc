import json
import requests
from typing import Dict, Optional
from datetime import datetime

class TeamsNotifier:
    """Send notifications to Microsoft Teams via webhook"""
    def __init__(self, webhook_url: str, logger=None):
        self.webhook_url = webhook_url
        self.logger = logger
    def send_notification(self, message: Dict) -> bool:
        if not self.webhook_url:
            if self.logger:
                self.logger.warning("Teams webhook URL not configured")
            return False
        try:
            response = requests.post(
                self.webhook_url,
                json=message,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            if response.status_code == 200:
                if self.logger:
                    self.logger.info("Teams notification sent successfully")
                return True
            else:
                if self.logger:
                    self.logger.error(f"Teams notification failed: {response.status_code}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error sending Teams notification: {str(e)}")
            return False
    def send_pipeline_completion(self, pipeline_name: str, stats: Dict) -> bool:
        color = "00FF00" if stats.get("status") != "FAILED" else "FF0000"
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color,
            "summary": f"{pipeline_name} Completed",
            "sections": [{
                "activityTitle": f"📊 {pipeline_name} Completed",
                "activitySubtitle": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "facts": [
                    {"name": key.replace("_", " ").title(), "value": str(value)}
                    for key, value in stats.items()
                    if key not in ["errors", "start_time", "end_time"]
                ],
                "markdown": True
            }]
        }
        return self.send_notification(message)
    def send_error_alert(self, pipeline_name: str, error_message: str) -> bool:
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FF0000",
            "summary": f"{pipeline_name} Failed",
            "sections": [{
                "activityTitle": f"🚨 {pipeline_name} Failed",
                "activitySubtitle": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "text": f"**Error:** {error_message}",
                "markdown": True
            }]
        }
        return self.send_notification(message)
    def send_high_risk_alert(self, email_data: Dict) -> bool:
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FFA500",
            "summary": "High-Risk Claim Detected",
            "sections": [{
                "activityTitle": "⚠️ High-Risk Claim Requires Attention",
                "activitySubtitle": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "facts": [
                    {"name": "Claim Number", "value": email_data.get('claim_number', 'N/A')},
                    {"name": "Policy Number", "value": email_data.get('policy_number', 'N/A')},
                    {"name": "Insured Name", "value": email_data.get('insured_name', 'N/A')},
                    {"name": "Priority", "value": email_data.get('priority_level', 'N/A')},
                    {"name": "Risk Level", "value": email_data.get('risk_level', 'N/A')},
                    {"name": "Claim Amount", "value": email_data.get('claim_amount', 'N/A')}
                ],
                "markdown": True
            }]
        }
        return self.send_notification(message)
