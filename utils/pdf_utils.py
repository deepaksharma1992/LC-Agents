import fitz
import os


def extract_pdf_content(input_pdf_path):
    pdf_text = ""
    doc = fitz.open(input_pdf_path)
    for page in doc:
        pdf_text = pdf_text + " " + page.get_text()
    return pdf_text


def get_files_in_directory(directory_path):
    """
    Check if any files are present inside the given directory and return the list of file names.

    Args:
        directory_path (str): The path of the directory to check.

    Returns:
        list: A list of file names present in the directory. Returns an empty list if no files are found.
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"The provided path '{directory_path}' is not a valid directory.")

    # List all files in the directory
    files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if
             os.path.isfile(os.path.join(directory_path, file))]
    return files


if __name__ == "__main__":
    # pdf_path = f"IC_Invoice.pdf"
    # print(extract_pdf_content(pdf_path))

    directory_path = r"../import_docs"
    file_list = get_files_in_directory(directory_path)
    print("Files in directory:", file_list)
