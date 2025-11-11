import re
from typing import Dict, List, Optional, Tuple

class EntityClassifier:
    """Classify and extract entities from text"""
    def __init__(self, config: Dict):
        self.config = config
        self.entity_patterns = config.get('entity_extraction', {}).get('entities', {})
    def extract_with_patterns(self, text: str, entity_name: str) -> List[str]:
        entity_config = self.entity_patterns.get(entity_name, {})
        patterns = entity_config.get('patterns', [])
        results = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            results.extend(matches)
        return results
    def extract_all_entities(self, text: str) -> Dict[str, any]:
        extracted = {}
        for entity in self.entity_patterns:
            extracted[entity] = self.extract_with_patterns(text, entity)
        return extracted
    def classify_priority(self, text: str, config: Dict) -> Tuple[str, float]:
        levels = config.get('classification', {}).get('priority_levels', {})
        for level, keywords in levels.items():
            for kw in keywords:
                if kw.lower() in text.lower():
                    return level, 1.0
        return 'low', 0.5
    def classify_claim_type(self, text: str, config: Dict) -> Tuple[str, float]:
        types = config.get('classification', {}).get('claim_types', {})
        for claim_type, keywords in types.items():
            for kw in keywords:
                if kw.lower() in text.lower():
                    return claim_type, 1.0
        return 'other', 0.5
    def is_high_risk(self, text: str, config: Dict) -> bool:
        indicators = config.get('triage_rules', {}).get('high_risk_indicators', [])
        return any(kw.lower() in text.lower() for kw in indicators)
