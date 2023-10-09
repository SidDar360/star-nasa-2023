FROM ubuntu
RUN apt update
RUN apt install pip --yes
RUN pip install streamlit
RUN apt install git --yes
RUN mkdir -p /src
RUN cd /src
RUN git clone https://github.com/SidDar360/star-nasa-2023.git
RUN cd /star-nasa-2023
RUN pip install -r /star-nasa-2023/requirements.txt
RUN pip install streamlit --upgrade
RUN pip install asposepdfcloud
RUN pip install aspose.words
RUN apt-get install -y dotnet-sdk-7.0
RUN apt-get install libssl-dev
RUN pip install langchain
RUN pip install chromadb
RUN pip install pypdf
RUN pip install pygpt4all
RUN pip install pdf2image
RUN pip install poppler-utils
RUN pip install -U sentence-transformers
RUN pip install openai
COPY docker-entrypoint.sh /docker-entrypoint.sh 
RUN chmod +x /docker-entrypoint.sh 
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]