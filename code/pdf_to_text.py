import fitz


def convert_pdf_to_text(pdf_path, txt_path):
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for page_num in range(total_pages):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            txt_file.write(text)
            txt_file.write("\n")


if __name__ == "__main__":
    pdf_path = "input.pdf"
    txt_path = "output.txt"
    
    convert_pdf_to_text(pdf_path, txt_path)
