import unittest
from 12_integration.email_parser import EmailParser

class TestEmailParser(unittest.TestCase):
    def setUp(self):
        self.parser = EmailParser()
    def test_extract_email_addresses(self):
        text = "Contact us at support@company.com or claims@insurance.com"
        emails = self.parser.extract_email_addresses(text)
        self.assertEqual(len(emails), 2)
        self.assertIn("support@company.com", emails)
        self.assertIn("claims@insurance.com", emails)
    def test_extract_phone_numbers(self):
        text = "Call 555-123-4567 or (555) 987-6543"
        phones = self.parser.extract_phone_numbers(text)
        self.assertGreater(len(phones), 0)
    def test_extract_amounts(self):
        text = "Total claim: $15,000.50 and deductible: $500"
        amounts = self.parser.extract_amounts(text)
        self.assertEqual(len(amounts), 2)
        self.assertIn("$15,000.50", amounts)
        self.assertIn("$500", amounts)
    def test_classify_attachment_pdf(self):
        result = self.parser.classify_attachment_type("invoice.pdf")
        self.assertEqual(result['type'], 'document')
        self.assertEqual(result['category'], 'pdf_document')
    def test_classify_attachment_image(self):
        result = self.parser.classify_attachment_type("accident_photo.jpg")
        self.assertEqual(result['type'], 'image')
        self.assertEqual(result['category'], 'photo')

if __name__ == "__main__":
    unittest.main()
