from mistralai import Mistral
from dotenv import load_dotenv
import os

load_dotenv("ai/api_key")  # contains MISTRAL_API_KEY

with Mistral(api_key=os.getenv("MISTRAL_API_KEY", "")) as mistral:
    with open("/home/vic/summa/docs/bronbestanden/Aquino_Summa_05/Aquino_Summa_05_109.pdf", "rb") as f:
        uploaded = mistral.files.upload(
            file={
                "file_name": "Aquino_Summa_05_109.pdf",
                "content": f,
            },
            purpose="ocr"
        )

    file_id = uploaded.id

    res = mistral.ocr.process(model="mistral-ocr-latest", document={
        "type": "file",
        "file_id": file_id,
    })

    # Handle response
    print(res)

