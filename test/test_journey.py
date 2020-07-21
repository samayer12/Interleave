import unittest
from src import interleave
import textract


class PDFJourneyTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.complex_PDF_1 = textract.process('PDFs/Complex_1.pdf', method='pdfminer').decode()

        cls.complex_PDF_2 = textract.process('PDFs/Complex_2.pdf', method='pdfminer').decode()

        cls.complex_PDF_3 = textract.process('PDFs/Complex_3.pdf', method='pdfminer').decode()

        cls.complex_PDF_4 = textract.process('PDFs/Complex_4.pdf', method='pdfminer').decode()

        cls.complex_PDF_5 = textract.process('PDFs/Complex_5.pdf', method='pdfminer').decode()

        cls.complex_PDF_6 = textract.process('PDFs/Complex_6.pdf', method='pdfminer').decode()

    def test_counts_correct_amount_of_paragraphs_for_complex_12(self):
        result = interleave.zip_sentences(interleave.build_paragraphs(interleave.sanitize_text(self.complex_PDF_1)),
                                          interleave.build_paragraphs(interleave.sanitize_text(self.complex_PDF_2)))
        self.assertEqual(166, len(result))

    def test_counts_correct_amount_of_paragraphs_for_complex_34(self):
        result = interleave.zip_sentences(interleave.build_paragraphs(interleave.sanitize_text(self.complex_PDF_3)),
                                          interleave.build_paragraphs(interleave.sanitize_text(self.complex_PDF_4)))
        self.assertEqual(64, len(result))

    def test_counts_correct_amount_of_paragraphs_for_complex_56(self):
        result = interleave.zip_sentences(interleave.build_paragraphs(interleave.sanitize_text(self.complex_PDF_5)),
                                          interleave.build_paragraphs(interleave.sanitize_text(self.complex_PDF_6)))
        self.assertEqual(69, len(result))


if __name__ == '__main__':
    unittest.main()
