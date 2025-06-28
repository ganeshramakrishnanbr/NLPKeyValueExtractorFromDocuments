import layoutparser as lp
from transformers import LayoutLMForTokenClassification, LayoutLMTokenizerFast
from PIL import Image
import pytesseract
import torch
import os

def process_document_with_layoutlm(image_path):
    # OCR
    image = Image.open(image_path)
    ocr_agent = lp.TesseractAgent(languages='eng')
    layout = ocr_agent.detect(image)
    words = [block.text for block in layout]
    boxes = [block.block.bounding_box for block in layout]
    # LayoutLM
    tokenizer = LayoutLMTokenizerFast.from_pretrained("microsoft/layoutlm-base-uncased")
    model = LayoutLMForTokenClassification.from_pretrained("microsoft/layoutlm-base-uncased")
    encoding = tokenizer(words, boxes=boxes, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**encoding)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2)
    return {
        "words": words,
        "predictions": predictions.tolist()
    }
