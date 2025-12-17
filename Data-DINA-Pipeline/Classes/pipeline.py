from Classes.doc_finder import PDFFinder
from Classes.doc_2_text import Doc_2_Text
from Classes.text_2_chonk import Text_2_Chonk
from Classes.chonk_2_database import Chonk_2_Database

class Pipeline_Handler:
    """
    Class to handle the overall pipeline process.
    """

    def __init__(self, root_folder):
        """
        Initialize the Pipeline Handler with the root folder.
        """
        self.root_folder = root_folder
        self.file_finder = PDFFinder(root_folder)
        self.doc_converter = Doc_2_Text()
        self.text_chonker = Text_2_Chonk()
        self.database = None
        self.database_status = False

        self.reset_document_collection()

    def reset_document_collection(self):
        """
        Clear the current document collection.
        """
        self.document_collection = []


    def set_root_folder(self, new_root_folder):
        """
        Update the root folder for the pipeline.

        Parameters
        ----------
        new_root_folder : str or Path
            New path to the folder where the search should begin.
        """
        self.root_folder = new_root_folder
        self.file_finder = PDFFinder(new_root_folder)

    def process_files(self,process_pdfs=True, process_ppts=True, process_docs=True):
        """
        Process the files in the root folder through the pipeline.

        Parameters
        ----------
        process_pdfs : bool, optional
            Whether to process PDF files. Default is True.
        process_ppts : bool, optional
            Whether to process PPT files. Default is True.
        process_docs : bool, optional
            Whether to process DOC files. Default is True.  

        Returns
        -------
        processed_documents : list
            A list of Document objects containing file name, path, docling representation, and chunks.
        """
        list_of_files = []
        if process_docs:
            list_of_docs = self.file_finder.find_docs()
            list_of_files.extend(list_of_docs)

        if process_ppts:
            list_of_ppts = self.file_finder.find_ppts()
            list_of_files.extend(list_of_ppts)

        if process_pdfs:
            list_of_pdfs = self.file_finder.find_pdfs()
            list_of_files.extend(list_of_pdfs)

        processed_documents = []

        for file_path in list_of_files:
            file_name = file_path.stem       # name without extension
            file_suffix = file_path.suffix   # extension (e.g. ".pdf")

            document = Document.initalize_doc(file_name, file_path, file_suffix)
            docling_representation = self.doc_converter.convert(file_path)
            document.set_docling_representation(docling_representation)

            chunks = self.text_chonker.chonk(docling_representation)
            document.set_chunks(chunks)

            processed_documents.append(document)

        self.document_collection.extend(processed_documents)

        return self.document_collection
    
    def activate_database(self,handshake_name:str):
        """
        Activate the database with the specified handshake name.
        Parameters
        ----------
        handshake_name : str
            The handshake name for the database.  

        Returns
        -------
        None
            The database is activated and ready to use.
        """

        self.database = Chonk_2_Database(handshake_name)
        self.database_status = True

    def database_chunks(self, processed_documents:list=None):
        """
        Save the chunks of the processed documents using the database.
        Parameters
        ----------
        processed_documents : list, optional
            A list of chunked Document objects to add to the database. If None, uses all processed documents in the pipeline
            (default is None).

        Returns
        -------
        None
            The chunks are stored in the vector database.
        """

        if not self.database_status:
            raise Exception("Database not activated. Please activate the database first.")
        if processed_documents is None:
            processed_documents = self.document_collection
        if not processed_documents:
            raise Exception("No processed documents available for saving to the database.")

        chunk_collection = []
        for document in processed_documents:
            chunk_collection.extend(document.chunks)


        self.chunk_collection = chunk_collection
        self.database.embed(chunk_collection)


        

class Document:
    """
    Class to hold the file name, file path, docling representation, and chunk of a file.
    """

    def __init__(self, file_name, file_path, file_suffix):
        """
        Initialize the File.
        
        Parameters
        ----------
        file_name : str
            The name of the file.
        file_path : str or Path
            The path to the file.
        file_suffix : str
            The suffix/type of the file (e.g., 'pdf', 'docx', 'pptx').
        """
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = file_suffix
        self.docling_representation = None
        self.chunks = None

    @classmethod
    def initalize_doc(cls, file_name, file_path, file_suffix):
        """
        Factory method to create a new Document instance.
        
        Parameters
        ----------
        file_name : str
            The name of the file.
        file_path : str or Path
            The path to the file.
        file_suffix : str
            The suffix/type of the file (e.g., 'pdf', 'docx', 'pptx').

        Returns
        -------
        Document
            A new instance of Document.
        """
        return cls(file_name, file_path, file_suffix)
    
    def set_docling_representation(self, docling_representation):
        """
        Set the docling representation of the document.
        """
        self.docling_representation = docling_representation

    def set_chunks(self, chunks):
        """
        Set the chunks of the document.
        """
        self.chunks = chunks

    def get_file_name(self):
        """
        Get the file name of the document.
        """
        return self.file_name
    
    def __str__(self):
        """
        String representation of the Document.
        """
        string = (
            f"Document:\n"
            f"  Name: {self.file_name}\n"
            f"  Path: {self.file_path}\n"
            f"  Type: {self.file_type}\n"
            f"  Chunks: {len(self.chunks) if self.chunks else 0}\n"
        )

        # for chunk in self.chunks or []:
        #     string += f"  Embedding: {chunk.embedding if chunk.embedding is not None else False}\n"

        return string
