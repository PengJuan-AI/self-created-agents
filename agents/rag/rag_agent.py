from langchain_deepseek import ChatDeepSeek
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from typing import Annotated, Sequence, Dict, List, TypedDict, Union
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
import os

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    encode_kwargs={"normalize_embeddings": True},
)

pdf_path = 'the 7 habits.pdf'
pdf_loader = PyPDFLoader(pdf_path)
pages = pdf_loader.load()
print(f"PDF has bee loaded and has {len(pages)} pages")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

page_splitter = text_splitter.split_documents(pages)
persist_directory = "/Users/pengjuan/Documents/projects/agents-design-practice/langGraph/Agents"
collection_name = "learning_pdf"

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

# actuall create the chroma database using embedding model
try:
    vectorstore = Chroma.from_documents(
        documents=page_splitter,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    print("Created ChromaDB vector store")
except Exception as e:
    print(f"Error setting up Chroma, {e}")
    raise

retriever = vectorstore.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 5}
)


@tool
def retriever_tool(query: str) -> str:
    """
    This tool searches and returns the information from the document.
    """

    docs = retriever.invoke(query)

    if not docs:
        return "I found no relevant information in the document."

    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i + 1}:\n{doc.page_content}")

    return "\n\n".join(results)


tools = [retriever_tool]

llm = llm = ChatDeepSeek(
    model='deepseek-v4-pro',
    max_tokens=1000,
).bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def should_continue(state: AgentState) -> AgentState:
    result = state['messages'][-1]
    return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0


system_prompt = """
You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024 based on the PDF document loaded into your knowledge base.
Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
"""
tools_dict = {our_tool.name: our_tool for our_tool in tools}  # Creating a dictionary of our tools


def call_llm(state: AgentState) -> AgentState:
    """"Function to call the llm with the current state"""
    messages = [SystemMessage(content=system_prompt)] + list(state['messages'])
    response = llm.invoke(messages)
    return {'messages': [response]}


def take_action(state: AgentState) -> AgentState:
    """execute tool calls from the LLM's response"""

    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")

        if not t['name'] in tools_dict:  # Checks if a valid tool is present
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."

        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")

        # Appends the Tool Message
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}


graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever", take_action)
graph.add_conditional_edges("llm", should_continue, {
    True: "retriever",
    False: END
})
graph.add_edge("retriever", "llm")
graph.set_entry_point("llm")

agent = graph.compile()


def running_agent():
    print("\n=== RAG AGENT===")

    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        messages = [HumanMessage(content=user_input)]  # converts back to a HumanMessage type

        result = agent.invoke({"messages": messages})

        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)


running_agent()
