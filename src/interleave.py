"""A side-project to do some .pdf processing for a friend.

Example Usage: `python interleave.py file1.pdf file2.pdf output.csv`
"""
import argparse
import itertools
import re
import sys
from csv import writer
from typing import List, Tuple

import textract  # type: ignore


def convert_pdf_to_txt(path: str) -> str:
    """Represent .pdf as .txt."""
    return str(textract.process(path, method='pdfminer').decode())


def build_paragraphs(input_text: str) -> List[str]:
    r"""Create a list of paragraphs from a string of sentences.

    :param input_text: Sanitized text to turn into paragraphs
    :return: A list of paragraphs

    >>> build_paragraphs("Header\n\n1. First.\n\n2. Second.\n\n3. Third.")
    ['1. First.', '2. Second.', '3. Third.']
    """
    matches = re.split(r'(\n\n)(\d+\.\s)', input_text)[2:]
    result = ['']
    old_paragraph_number = 0
    for i in range(0, len(matches), 3):
        paragraph_number = int(matches[i].split('.')[0])
        current_line = re.sub(r'[\n\f]', '', ''.join(matches[i:i + 2]).strip())

        if paragraph_number != old_paragraph_number + 1:
            result[-1] += current_line
        else:
            if current_line[:-1].isdigit():
                current_line += ' PARSE ERROR'
            result.append(current_line)
            old_paragraph_number = paragraph_number
    return result[1:]


def remove_headers(input_text: str) -> str:
    """Strip section headers and other titles."""
    sentences = re.sub(r'(\fC.*\d\n)', '', input_text)  # Remove Page Headers
    sentences = re.sub(r'(\n\d+ \n)', '', sentences)  # Remove Page Numbers
    sentences = re.sub(r'\n+[A-Z ]+\n+', '\n\n', sentences)  # Remove Section Titles
    # Remove Roman Numeral Section Titles but allow words like "CD." and "U.S.C."
    sentences = re.sub(r'([^\w .][IVXCMD]+\.[A-Za-z .\'’\n-]+)\n(?!\dA-z)', '\n',
                       sentences)
    sentences = sentences.replace(chr(160), '\n')  # Remove nbsp Page Breaks
    return sentences


def prepare_body_text(input_text: str) -> str:
    """Take raw sentences and standardize them."""
    sentences = re.sub(r'(\n{3,}|\n\n )', '\n\n', input_text)  # Apply Consistent Paragraph Spacing
    sentences = re.sub(r' {2,}', ' ', sentences)  # Apply Consistent Text Spacing
    sentences = re.sub(r'(\S)(\n\n)([A-Za-z])', r'\1 \3', sentences)  # Handle EOL without a space
    sentences = re.sub(r'(\n\) )(1\.\s)', r'\n\n\2', sentences, 1)  # Make first paragraph match others
    return sentences


def remove_trailing_content(input_text: str) -> str:
    """Remove content that comes after the last paragraph (such as Tables)."""
    sentences = re.split(r'\n\nTable 1:', input_text)[0]  # Remove tables that follow document body
    sentences = re.split(r'\s/s/', sentences)[0]  # Remove EPA-style signature blocks
    sentences = re.split(r'Respectfully submitted,', sentences)[0]  # Remove EPA-style signature blocks
    return sentences


def sanitize_text(input_text: str) -> str:
    """Turn raw input into properly-formatted sentences.

    :param input_text: Unsanitized text from PDF parsing
    :return: Cleaner text
    """
    sentences = remove_headers(input_text)
    sentences = prepare_body_text(sentences)
    sentences = remove_trailing_content(sentences)
    return sentences


def zip_sentences(list1: List[str], list2: List[str]) -> List[str]:
    """Create a matched-pairs list of all sentences between two lists.

    :param list1: A list of N paragraphs
    :param list2: A list of N paragraphs
    :return: A combined list from inputs

    >>> zip_sentences(["1. First", "2. Second"], ["1. First", "2. Second"])
    [('1. First', '1. First'), ('2. Second', '2. Second')]
    """
    return list(itertools.zip_longest(list1, list2))


def create_csv(data: List[str], path: str, source_tuple: Tuple[str, str]) -> str:
    """Write data to a .csv file.

    :param data: Matched paragraph data
    :param path: Destination of output
    :param source_tuple: Headers for csv file
    :return: Completion message
    """
    with open(path, 'w', newline='') as csvfile:
        writer(csvfile, delimiter=',').writerows([source_tuple])
        writer(csvfile, delimiter=',').writerows(data)
    return 'Files created.'


def main(argv: List[str]) -> None:
    """Receive .pdfs and input and generate matched-pairs list of paragraphs.

    :param argv: User-provided arguments
    :return: None
    """
    parser = argparse.ArgumentParser(description='Match numbered paragraphs from a PDF and store them in a CSV file.')
    parser.add_argument('input', metavar='I', type=str, nargs=2, help='two files to match and store')
    parser.add_argument('output', metavar='O', type=str, nargs=1, help='name of output file')
    parser.add_argument('-r', '--raw', default=False, action='store_true', help='convert PDFs to raw text')

    args = parser.parse_args(argv)

    print('\nColumn A source: ' + args.input[0] +
          '\nColumn B source: ' + args.input[1])

    if args.raw:
        doc_1_dest = '../output/' + args.input[0].split('/')[-1].split('.')[0] + '.txt'
        doc_2_dest = '../output/' + args.input[1].split('/')[-1].split('.')[0] + '.txt'
        print('\nStoring inputs as raw text.' +
              '\nDocument 1 destination: ' + doc_1_dest +
              '\nDocument 2 destination: ' + doc_2_dest)
        with open(doc_1_dest, 'w') as file:
            file.write(convert_pdf_to_txt(args.input[0]))
        with open(doc_2_dest, 'w') as file:
            file.write(convert_pdf_to_txt(args.input[1]))
    else:
        print('\nOutput File: ' + args.output[0] + '\n')

        text_first_file = convert_pdf_to_txt(args.input[0])
        text_second_file = convert_pdf_to_txt(args.input[1])
        filtered_text = zip_sentences(build_paragraphs(sanitize_text(text_first_file)),
                                      build_paragraphs(sanitize_text(text_second_file)))
        print(create_csv(filtered_text, args.output[0], (args.input[0], args.input[1])))


if __name__ == '__main__':
    main(sys.argv[1:])
