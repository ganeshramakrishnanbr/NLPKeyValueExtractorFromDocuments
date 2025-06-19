"""
OCR Processing Module using Tesseract
"""

import asyncio
import logging
import io
from pathlib import Path
from typing import Dict, List, Optional
import pytesseract
from PIL import Image
import cv2
import numpy as np

class OCRProcessor:
    """OCR processing with Tesseract and image enhancement"""
    
    def __init__(self, languages: List[str] = None):
        self.languages = languages or ['eng']
        self.logger = logging.getLogger(__name__)
        self.lang_string = '+'.join(self.languages)
    
    async def process_document(self, file_path: Path) -> Dict:
        """Process document with OCR"""
        
        try:
            if file_path.suffix.lower() == '.pdf':
                return await self._process_pdf_with_ocr(file_path)
            else:
                return await self._process_image_with_ocr(file_path)
                
        except Exception as e:
            self.logger.error(f"OCR processing failed: {str(e)}")
            return {'text': '', 'confidence': 0.0, 'error': str(e)}
    
    async def _process_pdf_with_ocr(self, file_path: Path) -> Dict:
        """Convert PDF pages to images and apply OCR"""
        
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(str(file_path))
            all_text = []
            total_confidence = 0.0
            page_count = 0
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # Convert page to image
                mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                # Process with PIL
                image = Image.open(io.BytesIO(img_data))
                
                # Apply OCR
                ocr_result = await self._apply_ocr_to_image(image)
                all_text.append(ocr_result['text'])
                total_confidence += ocr_result['confidence']
                page_count += 1
            
            doc.close()
            
            return {
                'text': '\n\n'.join(all_text),
                'confidence': total_confidence / page_count if page_count > 0 else 0.0,
                'pages_processed': page_count
            }
            
        except Exception as e:
            self.logger.error(f"PDF OCR processing failed: {e}")
            return {'text': '', 'confidence': 0.0, 'error': str(e)}
    
    async def _process_image_with_ocr(self, file_path: Path) -> Dict:
        """Process image file with OCR"""
        
        try:
            image = Image.open(str(file_path))
            return await self._apply_ocr_to_image(image)
            
        except Exception as e:
            self.logger.error(f"Image OCR processing failed: {e}")
            return {'text': '', 'confidence': 0.0, 'error': str(e)}
    
    async def _apply_ocr_to_image(self, image: Image.Image) -> Dict:
        """Apply OCR to PIL image with preprocessing"""
        
        try:
            # Enhance image for better OCR
            enhanced_image = await self._enhance_image_for_ocr(image)
            
            # Apply Tesseract OCR
            custom_config = r'--oem 3 --psm 6'
            
            # Get text with confidence
            data = pytesseract.image_to_data(
                enhanced_image, 
                lang=self.lang_string,
                config=custom_config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and calculate confidence
            text_parts = []
            confidences = []
            
            for i, conf in enumerate(data['conf']):
                if int(conf) > 0:  # Only include confident detections
                    text = data['text'][i].strip()
                    if text:
                        text_parts.append(text)
                        confidences.append(int(conf))
            
            extracted_text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                'text': extracted_text,
                'confidence': avg_confidence / 100.0,  # Convert to 0-1 scale
                'word_count': len(text_parts)
            }
            
        except Exception as e:
            self.logger.error(f"OCR application failed: {e}")
            return {'text': '', 'confidence': 0.0, 'error': str(e)}
    
    async def _enhance_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """Enhance image quality for better OCR results"""
        
        try:
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply noise reduction
            denoised = cv2.medianBlur(gray, 3)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Apply morphological operations to clean up
            kernel = np.ones((1, 1), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Convert back to PIL
            enhanced_image = Image.fromarray(cleaned)
            
            return enhanced_image
            
        except Exception as e:
            self.logger.warning(f"Image enhancement failed, using original: {e}")
            return image