from typing import Optional, Dict, Any
import os
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

from custom_llm import get_llm_agent
from utils.doc_util import DocumentOutputResult, DocumentCategories, DocumentTypeOutput
from utils.pdf_utils import get_files_in_directory, extract_pdf_content
from utils.prompt_template import doc_classification_template, document_verify_template, deciding_agent_template, \
    shipping_bill_template
from langchain_chroma import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))


class AgentState(TypedDict):
    export_doc_path: str
    lc_text: Optional[Dict[str, Any]]
    doc_extract_dict: Optional[Dict[dict, Any]]
    final_response: Optional[Dict[dict, Any]]
    certificate_of_origin: DocumentOutputResult
    bill_of_lading: DocumentOutputResult
    inspection_certificate: DocumentOutputResult
    insurance_certificate: DocumentOutputResult
    fumigation_certificate: DocumentOutputResult
    packing_list: DocumentOutputResult
    phytosanitary_certificate: DocumentOutputResult
    shipping_bill: DocumentOutputResult


document_agent_llm = get_llm_agent()
document_verifier_agent_llm = get_llm_agent()
deciding_agent_llm = get_llm_agent()


def extract_documents_data(AgentState):
    doc_extract_dict = {}
    files = get_files_in_directory(AgentState.get("export_doc_path"))
    for file in files:
        prompt = doc_classification_template
        file_text = extract_pdf_content(file)
        user_input = prompt.format(categories=DocumentCategories.get_categories(), input_text=file_text)
        structured_llm = document_agent_llm.with_structured_output(DocumentTypeOutput)
        response = structured_llm.invoke(user_input)
        print(response)
        doc_type = response.doc_type
        doc_extract_dict[doc_type] = file_text

    print("Documents data extracted")
    return {"doc_extract_dict": doc_extract_dict}


def doc_verify_llm_utility(document_type, letter_of_credit_data, document_data,
                           prompt_template=document_verify_template):
    prompt = prompt_template
    user_input = prompt.format(input_doc_type=document_type, lc_detail=letter_of_credit_data,
                               input_doc_detail=document_data)
    structured_llm = document_verifier_agent_llm.with_structured_output(DocumentOutputResult)
    response = structured_llm.invoke(user_input)
    print(f"Response of {document_type}: {response} ")

    return response


def certificate_of_origin_node(AgentState):
    CERTIFICATE_OF_ORIGIN = DocumentCategories.CERTIFICATE_OF_ORIGIN
    extracted_docs_dict = AgentState.get('doc_extract_dict', {})
    coo_text = extracted_docs_dict.get(CERTIFICATE_OF_ORIGIN, None)
    letter_of_credit_data = extracted_docs_dict.get(DocumentCategories.LETTER_OF_CREDIT, None)

    response = doc_verify_llm_utility(CERTIFICATE_OF_ORIGIN, letter_of_credit_data, coo_text)
    return {"certificate_of_origin": response}


def bill_of_lading_node(AgentState):
    BILL_OF_LADING = DocumentCategories.BILL_OF_LADING
    extracted_docs_dict = AgentState.get('doc_extract_dict', {})
    bol_text = extracted_docs_dict.get(BILL_OF_LADING, None)
    letter_of_credit_data = extracted_docs_dict.get(DocumentCategories.LETTER_OF_CREDIT, None)

    response = doc_verify_llm_utility(BILL_OF_LADING, letter_of_credit_data, bol_text)
    return {"bill_of_lading": response}


def inspection_certificate_node(AgentState):
    INSPECTION_CERTIFICATE = DocumentCategories.INSPECTION_CERTIFICATE
    extracted_docs_dict = AgentState.get('doc_extract_dict', {})
    inspection_text = extracted_docs_dict.get(INSPECTION_CERTIFICATE, None)
    letter_of_credit_data = extracted_docs_dict.get(DocumentCategories.LETTER_OF_CREDIT, None)

    response = doc_verify_llm_utility(INSPECTION_CERTIFICATE, letter_of_credit_data, inspection_text)
    return {"inspection_certificate": response}


def insurance_certificate_node(AgentState):
    INSURANCE_CERTIFICATE = DocumentCategories.INSURANCE_CERTIFICATE
    extracted_docs_dict = AgentState.get('doc_extract_dict', {})
    insurance_text = extracted_docs_dict.get(INSURANCE_CERTIFICATE, None)
    letter_of_credit_data = extracted_docs_dict.get(DocumentCategories.LETTER_OF_CREDIT, None)

    response = doc_verify_llm_utility(INSURANCE_CERTIFICATE, letter_of_credit_data, insurance_text)
    return {"insurance_certificate": response}


def fumigation_certificate_node(AgentState):
    FUMIGATION_CERTIFICATE = DocumentCategories.FUMIGATION_CERTIFICATE
    extracted_docs_dict = AgentState.get('doc_extract_dict', {})
    fumigation_text = extracted_docs_dict.get(FUMIGATION_CERTIFICATE, None)
    letter_of_credit_data = extracted_docs_dict.get(DocumentCategories.LETTER_OF_CREDIT, None)

    response = doc_verify_llm_utility(FUMIGATION_CERTIFICATE, letter_of_credit_data, fumigation_text)
    return {"fumigation_certificate": response}


def packing_list_node(AgentState):
    PACKING_LIST = DocumentCategories.PACKING_LIST
    extracted_docs_dict = AgentState.get('doc_extract_dict', {})
    packing_list_text = extracted_docs_dict.get(PACKING_LIST, None)
    letter_of_credit_data = extracted_docs_dict.get(DocumentCategories.LETTER_OF_CREDIT, None)

    response = doc_verify_llm_utility(PACKING_LIST, letter_of_credit_data, packing_list_text)
    return {"packing_list": response}


def pytosanitary_certificate_node(AgentState):
    PHYTOSANITARY_CERTIFICATE = DocumentCategories.PHYTOSANITARY_CERTIFICATE
    extracted_docs_dict = AgentState.get('doc_extract_dict', {})
    pytosanitary_cetificate_text = extracted_docs_dict.get(PHYTOSANITARY_CERTIFICATE, None)
    letter_of_credit_data = extracted_docs_dict.get(DocumentCategories.LETTER_OF_CREDIT, None)

    response = doc_verify_llm_utility(PHYTOSANITARY_CERTIFICATE, letter_of_credit_data, pytosanitary_cetificate_text)
    return {"phytosanitary_certificate": response}


def shipping_bill_node(AgentState):
    SHIPPING_BILL = DocumentCategories.SHIPPING_BILL
    extracted_docs_dict = AgentState.get('doc_extract_dict', {})
    shipping_bill_text = extracted_docs_dict.get(SHIPPING_BILL, None)
    letter_of_credit_data = extracted_docs_dict.get(DocumentCategories.LETTER_OF_CREDIT, None)
    vector_db = Chroma(collection_name="pdf_documents", embedding_function=embeddings, persist_directory=r"rag/chroma_db")
    ftp_text = " ".join(vector_db.get()['documents'])  # Joins with a space

    prompt = shipping_bill_template
    user_input = prompt.format(input_doc_type=SHIPPING_BILL, lc_detail=letter_of_credit_data,
                               input_doc_detail=shipping_bill_text, ftp_india=ftp_text)
    structured_llm = document_verifier_agent_llm.with_structured_output(DocumentOutputResult)
    response = structured_llm.invoke(user_input)
    print(f"Response of {SHIPPING_BILL}: {response} ")

    return {"shipping_bill": response}


def deciding_agent_node(AgentState):
    prompt = deciding_agent_template
    final_dict = {
        "certificate_of_origin": AgentState.get("certificate_of_origin", None),
        "bill_of_lading": AgentState.get("bill_of_lading", None),
        "inspection_certificate": AgentState.get("inspection_certificate", None),
        "insurance_certificate": AgentState.get("insurance_certificate", None),
        "fumigation_certificate": AgentState.get("fumigation_certificate", None),
        "packing_list": AgentState.get("packing_list", None),
        "phytosanitary_certificate": AgentState.get("phytosanitary_certificate", None),
        "shipping_bill": AgentState.get("shipping_bill", None),
    }

    user_input = prompt.format(document_inputs_dict=final_dict)
    response = deciding_agent_llm.invoke(user_input)
    print(f"Response of deciding agent: {response} ")

    return {"final_response": response}


builder = StateGraph(AgentState)
builder.add_node("doc_agent", extract_documents_data)
builder.add_node(DocumentCategories.BILL_OF_LADING, bill_of_lading_node)
builder.add_node(DocumentCategories.CERTIFICATE_OF_ORIGIN, certificate_of_origin_node)
builder.add_node(DocumentCategories.INSPECTION_CERTIFICATE, inspection_certificate_node)
builder.add_node(DocumentCategories.INSURANCE_CERTIFICATE, insurance_certificate_node)
builder.add_node(DocumentCategories.FUMIGATION_CERTIFICATE, fumigation_certificate_node)
builder.add_node(DocumentCategories.PACKING_LIST, packing_list_node)
builder.add_node(DocumentCategories.PHYTOSANITARY_CERTIFICATE, pytosanitary_certificate_node)
builder.add_node(DocumentCategories.SHIPPING_BILL, shipping_bill_node)
builder.add_node("deciding_agent", deciding_agent_node)

builder.set_entry_point("doc_agent")
builder.add_edge("doc_agent", DocumentCategories.CERTIFICATE_OF_ORIGIN)
builder.add_edge("doc_agent", DocumentCategories.BILL_OF_LADING)
builder.add_edge("doc_agent", DocumentCategories.INSPECTION_CERTIFICATE)
builder.add_edge("doc_agent", DocumentCategories.INSURANCE_CERTIFICATE)
builder.add_edge("doc_agent", DocumentCategories.FUMIGATION_CERTIFICATE)
builder.add_edge("doc_agent", DocumentCategories.PACKING_LIST)
builder.add_edge("doc_agent", DocumentCategories.PHYTOSANITARY_CERTIFICATE)
builder.add_edge("doc_agent", DocumentCategories.SHIPPING_BILL)

builder.add_edge(DocumentCategories.BILL_OF_LADING, "deciding_agent")
builder.add_edge(DocumentCategories.CERTIFICATE_OF_ORIGIN, "deciding_agent")
builder.add_edge(DocumentCategories.INSPECTION_CERTIFICATE, "deciding_agent")
builder.add_edge(DocumentCategories.INSURANCE_CERTIFICATE, "deciding_agent")
builder.add_edge(DocumentCategories.FUMIGATION_CERTIFICATE, "deciding_agent")
builder.add_edge(DocumentCategories.PACKING_LIST, "deciding_agent")
builder.add_edge(DocumentCategories.PHYTOSANITARY_CERTIFICATE, "deciding_agent")
builder.add_edge(DocumentCategories.SHIPPING_BILL, "deciding_agent")
builder.add_edge("deciding_agent", END)

app = builder.compile()

# Run the graph with an initial message
initial_state = {"export_doc_path": "export_docs"}

print("Running LangGraph workflow with LLM mcp...")
final_state = app.invoke(initial_state)
print(final_state)
