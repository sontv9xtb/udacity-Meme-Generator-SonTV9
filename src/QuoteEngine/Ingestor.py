"""Author by SonTV9"""

from .TxtIngestor import TxtIngestor
from .CSVImporter import CsvIngestor
from .DocxIngestor import DocxIngestor
from .IngestorInterface import IngestorInterface
from .PDFIngestor import PdfIngestor


class Ingestor(IngestorInterface):
    ingestorList = [CsvIngestor, PdfIngestor, DocxIngestor, TxtIngestor]

    @classmethod
    def parse(cls, path: str):
        for ingestor in cls.ingestorList:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"No suitable ingestor found for the file: {path}")
