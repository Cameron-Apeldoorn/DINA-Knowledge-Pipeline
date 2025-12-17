from Classes.doc_finder import PDFFinder
from Classes.doc_2_text import Doc_2_Text
from Classes.text_2_chonk import Text_2_Chonk
from Classes.pipeline import Pipeline_Handler, Document
import warnings
import time



def main():
    warnings.filterwarnings("ignore", message=".*pin_memory.*")
    pipeline = None
    # data_folders = ["../NZ_Guidelines","../CandyData"]
    data_folders = ["../NZ_Guidelines"]
    handshake_name = "knowledge-retriever"

    # Process each folder sequentially
    for root_folder in data_folders:
        if pipeline is None:
            pipeline = Pipeline_Handler(root_folder)
        else:
            pipeline.set_root_folder(root_folder)

        start = time.time()
        processed_documents = pipeline.process_files(process_pdfs=True, process_ppts=True, process_docs=True)
        for doc in processed_documents:
            print(doc)
        
        end = time.time()
        print(end - start)

    # Save all processed documents
    start = time.time()
    pipeline.activate_database(handshake_name)
    pipeline.database_chunks(processed_documents)
    end = time.time()
    print(end - start)

    print("Pipeline processing complete.")
    print(f"Chunks stored in database: {len(pipeline.chunk_collection)}")
    i = 1
    for chunk in pipeline.chunk_collection:
        print(f"Chunk {i}:")
        i += 1
        print(chunk)


if __name__ == "__main__":
    main()