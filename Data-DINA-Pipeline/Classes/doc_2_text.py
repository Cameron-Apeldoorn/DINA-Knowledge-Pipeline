
import logging
logging.getLogger('docling').setLevel(logging.ERROR)
from docling.document_converter import DocumentConverter

class Doc_2_Text:
    """
    This class converts documents to the docling doc output.
    """

    def __init__(self):
        """
        Initialize a new instance of Doc_2_Text.
        """
        

    def convert(self, source_doc):
        """
        Converts a document to the docling doc output.

        Parameters
        ----------
        source_doc : Path
            A Path pointing to a pdf file to be converted via docling.

        Returns
        -------
        doc : doc
            A converted pdf file.
        """
        # Example implementation
        converter = DocumentConverter()
        doc = converter.convert(source_doc).document
        return doc
    
    def convert_batch(self, list_of_docs):
        """
        Converts a set of documents to the docling doc output.

        Parameters
        ----------
        list_of_docs : list
            A list of Paths pointing to pdf files to be converted via docling.

        Returns
        -------
        doc_list : list
            A list containing converted pdf files.
        """
        # Example implementation
        converted_list = []
        for doc in list_of_docs:
            converted_list.append(self.convert(doc))

        return converted_list