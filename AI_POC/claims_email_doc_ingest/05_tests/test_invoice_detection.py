import unittest
from 12_integration.email_parser import EmailParser

class TestInvoiceDetection(unittest.TestCase):
    def setUp(self):
        self.parser = EmailParser()
    def test_invoice_attachment(self):
        result = self.parser.classify_attachment_type("invoice.pdf")
        self.assertEqual(result['type'], 'document')
        self.assertEqual(result['category'], 'pdf_document')
    def test_non_invoice_attachment(self):
        result = self.parser.classify_attachment_type("accident_photo.jpg")
        self.assertEqual(result['type'], 'image')
        self.assertEqual(result['category'], 'photo')

if __name__ == "__main__":
    unittest.main()
