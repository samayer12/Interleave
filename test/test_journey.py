import unittest
from src import interleave
import textract


class PDFJourneyTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.complex_PDF_1 = textract.process('PDFs/Complex_1.pdf', method='pdfminer').decode()

        cls.complex_PDF_2 = textract.process('PDFs/Complex_2.pdf', method='pdfminer').decode()

    def test_counts_correct_amount_of_paragraphs_for_complex_documents(self):
        result = interleave.zip_sentences(interleave.build_paragraphs(interleave.sanitize_text(self.complex_PDF_1)),
                                          interleave.build_paragraphs(interleave.sanitize_text(self.complex_PDF_2)))
        self.assertEqual(166, len(result))


if __name__ == '__main__':
    unittest.main()
