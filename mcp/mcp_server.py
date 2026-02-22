from fastmcp import FastMCP
from pathlib import Path
from fpdf import FPDF
import win32com.client

mcp = FastMCP(name="PDF and Email MCP Server")

@mcp.tool
def generate_pdf_tool(content: str, filename: str = "output.pdf") -> str:
    """Generates a PDF from the given content and saves it."""
    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_font("Arial", size=11)
    effective_page_width = pdf.w - 2 * pdf.l_margin

    for paragraph in content.split('\n'):
        if not paragraph.strip():
            pdf.ln(5)
            continue

        words = paragraph.split()
        line = ''
        for word in words:
            test_line = f"{line} {word}".strip()
            if pdf.get_string_width(test_line) > effective_page_width:
                pdf.multi_cell(effective_page_width, 5, line)
                line = word
            else:
                line = test_line

        if line:
            pdf.multi_cell(effective_page_width, 5, line)
        pdf.ln(2)

    output_dir = Path("output_docs")
    output_dir.mkdir(exist_ok=True)
    full_path = output_dir / filename
    pdf.output(str(full_path))
    print('Pdf prepared successfully')
    return str(full_path)

@mcp.tool
def send_email_tool(subject: str, body: str, pdf_path: str, recipient: str) -> dict:
    """Sends an email with the PDF attached using Outlook."""
    try:
        outlook = win32com.client.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)
        mail.Subject = subject
        mail.HTMLBody = body
        mail.To = recipient
        if Path(pdf_path).exists():
            mail.Attachments.Add(str(Path(pdf_path).absolute()))
        mail.Display(False)  # Use mail.Send() to send directly
        print('Email prepared successfully')
        return {"status": "success", "message": "Email would be sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 👇 Add this block to run the server directly
if __name__ == "__main__":
    mcp.run(transport="streamable-http",host="127.0.0.1", port=8000, path="/mcp")


