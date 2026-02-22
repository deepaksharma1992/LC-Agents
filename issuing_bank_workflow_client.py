from dotenv import load_dotenv
from custom_llm import get_llm_agent
from utils.doc_util import DocumentCategories, DocumentTypeOutput
from utils.pdf_utils import get_files_in_directory, extract_pdf_content
from utils.prompt_template import doc_classification_template, lc_prompt_template

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

import asyncio

load_dotenv()

async def main():
    document_agent_llm = get_llm_agent()
    lc_llm = get_llm_agent()

    # Connect to MCP server using config format
    client_config = {
        "default": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http"
        }
    }
    tool_executor = MultiServerMCPClient(client_config)

    # Get tools from MCP server
    tools = await tool_executor.get_tools()

    react_agent = create_react_agent(lc_llm, tools)

    doc_extract_dict = {}
    files = get_files_in_directory("import_docs")
    for file in files:
        prompt = doc_classification_template
        file_text = extract_pdf_content(file)
        user_input = prompt.format(categories=DocumentCategories.get_categories(), input_text=file_text)
        structured_llm = document_agent_llm.with_structured_output(DocumentTypeOutput)
        response = structured_llm.invoke(user_input)
        print(response)
        doc_type = response.doc_type
        doc_extract_dict[doc_type] = file_text

    print(doc_extract_dict)

    document_input = lc_prompt_template.format(
        sales_contract=doc_extract_dict.get(DocumentCategories.SALES_CONTRACT),
        packing_list=doc_extract_dict.get(DocumentCategories.PACKING_LIST)
    )

    #  Let the agent handle everything (tool calls, reasoning, etc.)
    final_result = await react_agent.ainvoke({
        "messages": [{"role": "system", "content": document_input}]
    })

    print("\n Final Agent Response:")
    print(final_result)

    print("\nWorkflow finished.")

# Run the async workflow
if __name__ == "__main__":
    asyncio.run(main())
