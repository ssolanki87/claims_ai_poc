import re
from typing import Dict, List, Optional
from pathlib import Path

class EmailParser:
    """Parse email content and extract structured data"""
    @staticmethod
    def parse_email_structure(email_data: Dict) -> Dict:
        parsed = {
            "message_id": email_data.get("message_id", ""),
            "subject": email_data.get("subject", ""),
            "from": email_data.get("from", ""),
            "to": email_data.get("to", []),
            "cc": email_data.get("cc", []),
            "date": email_data.get("date", ""),
            "body_text": email_data.get("body_text", ""),
            "body_html": email_data.get("body_html", ""),
            "attachments": email_data.get("attachments", []),
            "headers": email_data.get("headers", {})
        }
        return parsed
    @staticmethod
    def extract_email_addresses(text: str) -> List[str]:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return list(set(re.findall(pattern, text)))
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        patterns = [
            r'\+?1?\s*\(?([0-9]{3})\)?[\s.-]?([0-9]{3})[\s.-]?([0-9]{4})',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        ]
        phones = []
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                phones.append(match.group(0))
        return list(set(phones))
    @staticmethod
    def extract_dates(text: str) -> List[str]:
        patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b'
        ]
        dates = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        return list(set(dates))
    @staticmethod
    def extract_amounts(text: str) -> List[str]:
        pattern = r'\$\s*[\d,]+\.?\d{0,2}'
        amounts = re.findall(pattern, text)
        return list(set(amounts))
    @staticmethod
    def classify_attachment_type(filename: str) -> Dict[str, str]:
        ext = Path(filename).suffix.lower()
        classifications = {
            '.pdf': {'type': 'document', 'category': 'pdf_document'},
            '.doc': {'type': 'document', 'category': 'word_document'},
            '.docx': {'type': 'document', 'category': 'word_document'},
            '.xls': {'type': 'spreadsheet', 'category': 'excel'},
            '.xlsx': {'type': 'spreadsheet', 'category': 'excel'},
            '.csv': {'type': 'spreadsheet', 'category': 'csv'},
            '.jpg': {'type': 'image', 'category': 'photo'},
            '.jpeg': {'type': 'image', 'category': 'photo'},
            '.png': {'type': 'image', 'category': 'photo'},
            '.gif': {'type': 'image', 'category': 'photo'},
            '.tiff': {'type': 'image', 'category': 'photo'},
            '.mp4': {'type': 'video', 'category': 'video'},
            '.avi': {'type': 'video', 'category': 'video'},
            '.mov': {'type': 'video', 'category': 'video'},
            '.eml': {'type': 'email', 'category': 'email_file'},
            '.msg': {'type': 'email', 'category': 'email_file'}
        }
        return classifications.get(ext, {'type': 'unknown', 'category': 'other'})
