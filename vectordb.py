from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
import config
from ai import AI

class vectorDB:
    def splitText(self, text):
        n = 50000
        docs = [text[i:i+n] for i in range(0, len(text), n)]
        print(len(docs))
        return docs
    def create_db_fromText(self, text, container_name, chunk_size = 1500, chunk_overlap = 50):
        ai = AI()
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_text(text)
        #can be taken as a param
        embeddingsModel = ai.get_embeddings_model()
        db = Chroma.from_texts(docs, embeddingsModel, persist_directory=config.VECTORDB_PERSIST_DIR,collection_name=container_name)
        db.persist()
        db = None

    def init_qa_context(self, container_name):
        ai = AI()
        embeddingsModel = ai.get_embeddings_model()
        db = Chroma(persist_directory=config.VECTORDB_PERSIST_DIR, embedding_function=embeddingsModel, collection_name=container_name)
        #can be taken as a param
        llm = ai.get_llm_model_for_lang_chain()
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            verbose=False,
        )
        return qa
    
    def get_answer_content(self, container_name, query):
        ai = AI()
        embeddingsModel = ai.get_embeddings_model()
        db = Chroma(persist_directory=config.VECTORDB_PERSIST_DIR, embedding_function=embeddingsModel, collection_name=container_name)
        #can be taken as a param
        llm = ai.get_llm_model_for_lang_chain()
        chain = load_qa_chain(llm, chain_type="stuff",verbose=True)
        matching_docs = db.similarity_search(query)
        answer =  chain.run(input_documents=matching_docs, question=query)
        return answer

    def get_summarization_content(self, container_name, query):
        ai = AI()
        embeddingsModel = ai.get_embeddings_model()
        db = Chroma(persist_directory=config.VECTORDB_PERSIST_DIR, embedding_function=embeddingsModel, collection_name=container_name)
        #can be taken as a param
        llm = ai.get_llm_model_for_lang_chain()

        chain = load_summarize_chain(llm, chain_type="refine",verbose=True)
        matching_docs = db.similarity_search(query)
        print(matching_docs)
        output =  chain.run(input_documents=matching_docs)
        return output
    
    def get_context_documents(self, container_name, query):
        ai = AI()
        embeddingsModel = ai.get_embeddings_model()
        db = Chroma(persist_directory=config.VECTORDB_PERSIST_DIR, embedding_function=embeddingsModel, collection_name=container_name)
        matching_docs = db.similarity_search_with_score(query, k=1)
        return matching_docs[0][0]
        #return matching_docs[0].page_content

