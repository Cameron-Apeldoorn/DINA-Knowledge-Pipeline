from pathlib import Path

class PDFFinder:
    """
    Class to find all docling convertible files in a folder and its subfolders.
    """

    def __init__(self, root_folder):
        """
        Initialize the PDFFinder with a root folder.

        Parameters
        ----------
        root_folder : str or Path
            Path to the folder where the search should begin.
        """
        self.root_folder = Path(root_folder)

    def find_pdfs(self):
        """
        Find all PDF files in the root folder and its subfolders.

        Returns
        -------
        list of str
            List of Path to all PDF files.
        """
        return [path for path in self.root_folder.rglob("*.pdf")]
    
    def find_ppts(self):
        """
        Find all PPT files in the root folder and its subfolders.

        Returns
        -------
        list of str
            List of Path to all PPT files.
        """
        return [path for path in self.root_folder.rglob("*.pptx")]
    
    def find_docs(self):
        """
        Find all DOC files in the root folder and its subfolders.

        Returns
        -------
        list of str
            List of Path to all DOC files.
        """
        return [path for path in self.root_folder.rglob("*.docx")]
    
