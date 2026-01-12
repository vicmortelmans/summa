# Reads PDF files from ../docs/bronbestanden/*/*.pdf and writes OCR text to *.txt in the same directory.

from mistralai import Mistral
from dotenv import load_dotenv
import os
import glob

script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, "api_key"))  # contains MISTRAL_API_KEY

with Mistral(api_key=os.getenv("MISTRAL_API_KEY", "")) as mistral:
    docs_dir = os.path.join(script_dir, "../docs/bronbestanden")
    pdf_files = glob.glob(os.path.join(docs_dir, "*", "*.pdf"))

    for file_path in pdf_files:
        # break if the output file already exists
        output_file_path = file_path.replace(".pdf", ".txt")
        if os.path.exists(output_file_path):
            print(f"Skipping (already processed): {file_path}")
            continue

        print(f"Processing: {file_path}")
        with open(file_path, "rb") as f:
            uploaded = mistral.files.upload(
                file={
                    "file_name": os.path.basename(file_path),
                    "content": f,
                },
                purpose="ocr"
            )

        file_id = uploaded.id

        res = mistral.ocr.process(model="mistral-ocr-latest", document={
            "type": "file",
            "file_id": file_id,
        })

        # Save to a text file with the same name as the pdf
        with open(output_file_path, "w") as out_file:
            out_file.write(res.pages[0].markdown)
