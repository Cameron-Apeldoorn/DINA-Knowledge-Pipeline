from chonkie import LateChunker, RecursiveRules, SemanticChunker
from chonkie.refinery import OverlapRefinery, EmbeddingsRefinery

class Text_2_Chonk:
    """
    This class converts docling docs into chonkie chunks for later embedding.
    """

    def __init__(self):
        """
        Initialize a new instance of Text_2_Chonk.
        """

        # self.chunker  = LateChunker(
        #     embedding_model="all-MiniLM-L6-v2",
        #     chunk_size=512,
        #     rules=RecursiveRules(),
        #     min_characters_per_chunk=24,
        #     )

        # Semantic Chunker setup
        self.chunker = SemanticChunker(
            embedding_model="minishlab/potion-base-32M",    # Default model
            threshold=0.6,                                  # Similarity threshold (0-1)
            chunk_size=2048,                                 # Maximum tokens per chunk
            similarity_window=3,                            # Window for similarity calculation
            skip_window=1                                   # Skip-and-merge window (0=disabled)
        )

        # Add refineries for RAG optimization
        self.overlap_refinery = OverlapRefinery(
            tokenizer_or_token_counter="character",
            context_size=0.25,
            method="suffix",
            merge=True
        )

        self.embeddings_refinery = EmbeddingsRefinery(
            embedding_model="minishlab/potion-base-32M"
        )
        
    def chonk(self, docling_doc):
        """
        Converts a document to the docling doc output.

        Parameters
        ----------
        docling_doc : doc
            A docling doc file that needs to be chunked via chonkie.

        Returns
        -------
        chunks : list
            A list of chunks that represent the docling doc file.
        """
        # Example implementation
        markdowned_doc = docling_doc.export_to_markdown()
        chunks = self.chunker.chunk(markdowned_doc)

        
        # Apply refinements
        chunks = self.overlap_refinery.refine(chunks)
        chunks = self.embeddings_refinery.refine(chunks)  # Add embeddings

        return chunks
    
    def chonk_batch(self, list_of_docs):
        """
        Converts a list of docling docs into chonkie chunks.

        Parameters
        ----------
        list_of_docs : List
            A list of docling doc file that needs to be chunked via chonkie.

        Returns
        -------
        chunks_list : list
            A list of the list of chunks representing each docling doc file.
        """
        chunks_list = []
        for doc in list_of_docs:
            chunks_list.append(self.chonk(doc))

        return chunks_list