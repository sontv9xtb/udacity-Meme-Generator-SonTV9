"""Author by SonTV9"""

import os
import random
import subprocess
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteMode import QuoteModel


class PdfIngestor(IngestorInterface):
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f"Error : {path}")

        tmp = f'./_data/{random.randint(0, 1000000)}.txt'
        call_result = subprocess.call(['pdftotext', '-layout', '-nopgbrk', path, tmp])

        if call_result != 0:
            raise Exception(f"Error occurs while covert PDF to text: {call_result}")

        quotes = []
        with open(tmp, 'r') as file_ref:
            for line in file_ref.readlines():
                line = line.strip()
                if len(line) > 0:
                    parsed = line.split('-')
                    if len(parsed) == 2:
                        quote = QuoteModel(parsed[0].strip(), parsed[1].strip())
                        quotes.append(quote)

        os.remove(tmp)
        return quotes
