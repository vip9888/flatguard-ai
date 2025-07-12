import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from apps.alerts.models import Alert


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# --- Load sample alert logs ---
def load_docs():
    # Get the project root directory (where manage.py is located)
    # project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # alert_logs_path = os.path.join(project_root, "alerts_logs.txt")
    
    try:
        # loader = TextLoader(alert_logs_path)
        # documents = loader.load()
        alert_logs_text=get_alert_logs_from_db()
        documents=[Document(page_content=alert_logs_text, metadata={})]
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return splitter.split_documents(documents)
    except FileNotFoundError:
        print(f"Warning: alert_logs.txt not found at {alert_logs_path}. Creating sample data.")
        # Create sample alert log data if file doesn't exist
        sample_data = """
        Alert: Motion detected at camera 1 - 2024-01-15 14:30:22
        Alert: Unknown person detected at camera 2 - 2024-01-15 14:35:15
        Alert: System status check - All cameras operational - 2024-01-15 14:40:00
        Alert: Motion detected at camera 3 - 2024-01-15 15:20:45
        Alert: Known person identified: John Doe at camera 1 - 2024-01-15 15:25:30
        Alert: Motion detected at camera 2 - 2024-01-15 16:10:15
        Alert: Unknown person detected at camera 1 - 2024-01-15 16:15:30
        Alert: Known person identified: Jane Smith at camera 3 - 2024-01-15 16:20:45
        Alert: System status check - Camera 2 offline - 2024-01-15 16:25:00
        Alert: Motion detected at camera 1 - 2024-01-15 17:05:22
        """
        # Write sample data to file
        with open(alert_logs_path, "w") as f:
            f.write(sample_data)
        
        # Now load the created file
        loader = TextLoader(alert_logs_path)
        documents = loader.load()
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return splitter.split_documents(documents)
    except Exception as e:
        print(f"Error loading alert_logs.txt: {str(e)}")
        # Return a minimal document if everything fails
        from langchain.schema import Document
        return [Document(page_content="Alert: System error - Unable to load alert logs", metadata={})]


# --- Build vectorstore + QA chain ---
def build_agent():
    docs = load_docs()
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=api_key, temperature=0),
        retriever=vectorstore.as_retriever()
    )
    return chain

# --- Final callable function ---
def chat_with_agent(query: str):
    try:
        chain = build_agent()
        response = chain.run(query)
        return response
    except Exception as e:
        return f"Error: {str(e)}"


# --- Fetch Alert Logs from Database ---

def get_alert_logs_from_db():
    alerts=Alert.objects.all().order_by('-timestamp')
    documents=[]
    for alert in alerts:
        doc=doc = f"{alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {alert.name or 'Unknown'} - {alert.status}"
        documents.append(doc)
    return "\n".join(documents)