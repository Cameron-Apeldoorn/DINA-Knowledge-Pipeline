from chonkie import ChromaHandshake
import chromadb

class Chonk_2_Database:
    """
    This class converts chonkie chunks into a vector database for later use.
    """

    def __init__(self,handshake_name:str):
        """
        Initialize a new instance of Chonk_2_Database.

        Parameters
        ----------
        handshake_name : str
            The name of the chroma handshake.
        """

        # Or specify a persistent storage path
        self.handshake = ChromaHandshake(collection_name=handshake_name,path="./chroma_db")

    def embed(self, chunks):
        """
        Converts a list of chonkie chunks into a vector database.

        Parameters
        ----------
        chunks : list
            A list of chonkie chunks to be embedded.

        Returns
        -------
        None
            The chunks are embedded and stored in the vector database.
        """
        # Example implementation
        self.handshake.write(chunks)