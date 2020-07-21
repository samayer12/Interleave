import unittest
from src import interleave
from unittest.mock import patch
from random import randint



class PDFUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('text/short_text.txt', 'r') as file:
            cls.short_text = file.read()

        with open('text/multiline_text.txt', 'r') as file:
            cls.multiline_text = file.read()

        with open('text/multipage_text.txt', 'r') as file:
            cls.multipage_text = file.read()

        with open('text/1000_paragraphs.txt', 'r') as file:
            cls.thousand_paragraphs = '\n\n' + file.read()

        with open('text/pagenumbers.txt', 'r') as file:
            cls.pagenumbers = '\n\n' + file.read()

        with open('text/headers.txt', 'r') as file:
            cls.headers = '\n\n' + file.read()

        with open('text/nbsp_formfeed.txt', 'r') as file:
            cls.nbsp_formfeed = '\n\n' + file.read()

        with open('text/edge_EPA_signature_block_1.txt', 'r') as file:
            cls.edge_EPA_sigblock_1 = file.read()

        with open('text/edge_EPA_signature_block_2.txt', 'r') as file:
            cls.edge_EPA_sigblock_2 = file.read()

        with open('text/paragraph_variable_spacing.txt', 'r') as file:
            cls.paragraph_variable_spaced = file.read()

        with open('text/roman_numerals.txt', 'r') as file:
            cls.roman_numerals = file.read()

        with open('text/section_titles.txt', 'r') as file:
            cls.section_titles = file.read()

        with open('text/trailing_table.txt', 'r') as file:
            cls.trailing_table = file.read()

        cls.split_simple_text = ['1. First Entry.', '2. Second Entry.', '3. Third Entry.']

        cls.split_multiline_text = ['1. First Entry. This is a really long entry. It spans multiple lines. Very long. '
                                    'So tall. Can you believe how many words are here?',
                                    '2. Second Entry. This is an even longer entry! This one spans three lines. '
                                    'Ha, and you thought the last guy was verbose. '
                                    'Wait until I tell you a story my great-great grandfather once told me. '
                                    'Four score and seven years ago...',
                                    '3. Third Entry.']

        cls.split_multipage_text = ['1. First Entry.',
                                    '2. Second Entry. This paragraphs spans multiple pages. Words enable the document '
                                    'to automatically handle a page-break. This paragraph splits to the next page and '
                                    'continues with a normal word.',
                                    '3. Third Entry. This paragraphs spans multiple pages. Words enable the document '
                                    'to automatically handle a page-break. This paragraph splits to the next page and '
                                    'continues with a number so it is 1234 words.']

        cls.processed_text = [('1. First Entry.', '1. First Entry.'),
                              ('2. Second Entry.', '2. Second Entry.'),
                              ('3. Third Entry.', '3. Third Entry.')]

        cls.EPA_signature_1 = '/s/'

        cls.EPA_signature_2 = 'Respectfully submitted,'

    def test_opens_PDF(self):
        self.assertEqual(self.short_text, interleave.convert_pdf_to_txt('PDFs/Simple.pdf'))

    def test_opens_multiline_PDF(self):
        self.assertEqual(self.multiline_text, interleave.convert_pdf_to_txt('PDFs/Multiline.pdf'))

    def test_opens_multipage_PDF(self):
        self.assertEqual(self.multipage_text, interleave.convert_pdf_to_txt('PDFs/Multipage.pdf'))

    def test_counts_up_to_1000_paragraphs(self):
        result = interleave.build_paragraphs(interleave.sanitize_text(self.thousand_paragraphs))
        self.assertEqual(1000, len(result))

    def test_builds_paragraphs_correctly(self):
        self.assertEqual(self.split_simple_text, interleave.build_paragraphs('\n\n' + self.short_text))

    def test_splits_short_sentences(self):
        result = interleave.build_paragraphs(interleave.sanitize_text('\n\n' + self.short_text))
        self.assertEqual(self.split_simple_text, result)

    def test_splits_multiline_sentences(self):
        result = interleave.build_paragraphs(interleave.sanitize_text('\n\n' + self.multiline_text))
        self.assertEqual(self.split_multiline_text, result)

    def test_splits_multipage_paragraphs(self):
        result = interleave.build_paragraphs(interleave.sanitize_text('\n\n' + self.multipage_text))
        self.assertEqual(self.split_multipage_text, result)

    def test_removes_page_numbers(self):
        self.assertNotRegex('\n'.join(interleave.sanitize_text(self.pagenumbers)),
                            r'\n\d+ \n')

    def test_removes_page_headers(self):
        self.assertNotRegex('\n'.join(interleave.sanitize_text(self.headers)),
                            r'(\fC.*\d\n)')

    def test_removes_section_titles(self):
        result = (interleave.remove_headers(self.section_titles)).split('\n\n')
        self.assertEqual(18, len(result))
        self.assertNotIn('\n', result)

    def test_removes_roman_numerals(self):
        result = interleave.remove_headers(self.roman_numerals)
        self.assertNotRegex(result, r'[IVXCMD]+\.')

    def test_removes_nbsp_formfeed_page_breaks(self):
        result = interleave.sanitize_text(self.nbsp_formfeed)
        self.assertNotIn(chr(160), result)
        self.assertNotIn(chr(12), result)

    def test_applies_consistent_paragraph_spacing(self):
        result = (interleave.prepare_body_text(self.paragraph_variable_spaced)).split('\n\n')
        self.assertEqual(5, len(result))
        self.assertNotIn('\n', result)

    def test_applies_consistent_text_spacing(self):
        result = interleave.prepare_body_text('first second' + (' ' * randint(2, 1024))
                                              + 'third  fourth')
        self.assertNotRegex(result, r' {2,}')

    def test_removes_tables_after_doc_body(self):
        result = interleave.remove_trailing_content(self.trailing_table)
        self.assertNotIn('Table 1:', result)
        self.assertEqual(2, len(result.split('\n\n')))

    def test_edge_case_strip_EPA_sigblock_1(self):
        result = '\n'.join(interleave.sanitize_text(self.edge_EPA_sigblock_1))
        self.assertNotIn(self.EPA_signature_1, result)

    def test_edge_case_strip_EPA_sigblock_2(self):
        result = '\n'.join(interleave.sanitize_text(self.edge_EPA_sigblock_2))
        self.assertNotIn(self.EPA_signature_2, result)
        
    def test_zip_sentences_to_tuple(self):
        list1 = '\n\n' + self.short_text
        list2 = '\n\n' + self.short_text

        self.assertEqual(self.processed_text,
                         interleave.zip_sentences(interleave.build_paragraphs(interleave.sanitize_text(list1)),
                                                  interleave.build_paragraphs(interleave.sanitize_text(list2))))

    @patch('builtins.open')
    @patch('src.interleave.writer', autospec=True)
    def test_writes_csv(self, mock_writer, mock_open):
        interleave.create_csv(self.processed_text, 'fake/path/file.csv', ('Doc1', 'Doc2'))
        self.assertEqual(1, mock_open.call_count)
        self.assertEqual(2, mock_writer.call_count)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
