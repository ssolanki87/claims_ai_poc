import unittest
from 07_models.entity_classifier import EntityClassifier

class TestEntityClassifier(unittest.TestCase):
    def setUp(self):
        config = {
            "entity_extraction": {
                "entities": {
                    "claim_number": {
                        "patterns": ["CLAIM[\\s#:-]*([A-Z0-9]{6,12})"],
                        "required": True
                    },
                    "policy_number": {
                        "patterns": ["POLICY[\\s#:-]*([A-Z0-9]{8,15})"],
                        "required": True
                    }
                }
            },
            "classification": {
                "priority_levels": {
                    "urgent": ["urgent", "emergency"],
                    "high": ["injury", "hospital"],
                    "medium": ["damage"],
                    "low": ["inquiry"]
                },
                "claim_types": {
                    "auto": ["vehicle", "car", "accident"],
                    "property": ["home", "house", "fire"]
                }
            }
        }
        self.classifier = EntityClassifier(config)
    def test_extract_claim_number(self):
        text = "Regarding CLAIM #ABC123456"
        results = self.classifier.extract_with_patterns(text, 'claim_number')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], 'ABC123456')
    def test_classify_priority(self):
        config = {"classification": {"priority_levels": {
            "urgent": ["urgent", "emergency"],
            "high": ["injury"]
        }}}
        text = "Emergency: Patient injured in accident"
        priority, confidence = self.classifier.classify_priority(text, config)
        self.assertEqual(priority, 'urgent')
        self.assertGreater(confidence, 0)
    def test_classify_claim_type(self):
        config = {"classification": {"claim_types": {
            "auto": ["vehicle", "car"],
            "property": ["home", "house"]
        }}}
        text = "Vehicle collision on Highway 101"
        claim_type, confidence = self.classifier.classify_claim_type(text, config)
        self.assertEqual(claim_type, 'auto')

if __name__ == "__main__":
    unittest.main()
