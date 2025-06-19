"""
Image Processing Module for document enhancement and extraction
"""

import asyncio
import logging
import io
from pathlib import Path
from typing import Dict, List, Optional
import cv2
import numpy as np
from PIL import Image
import fitz  # PyMuPDF

class ImageProcessor:
    """Process and enhance images from documents"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def extract_and_process_images(self, file_path: Path, enhance: bool = True) -> List[Dict]:
        """Extract images from documents and optionally enhance them"""
        
        try:
            if file_path.suffix.lower() == '.pdf':
                return await self._extract_pdf_images(file_path, enhance)
            elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                return await self._process_single_image(file_path, enhance)
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Image processing failed: {str(e)}")
            return []
    
    async def _extract_pdf_images(self, file_path: Path, enhance: bool) -> List[Dict]:
        """Extract images from PDF document"""
        
        images = []
        
        try:
            doc = fitz.open(str(file_path))
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    try:
                        # Extract image
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        
                        if pix.n - pix.alpha < 4:  # GRAY or RGB
                            img_data = pix.tobytes("png")
                            
                            # Process image
                            image_info = await self._analyze_image(
                                img_data, page_num + 1, img_index + 1, enhance
                            )
                            
                            if image_info:
                                images.append(image_info)
                        
                        pix = None
                        
                    except Exception as e:
                        self.logger.warning(f"Failed to extract image {img_index} from page {page_num}: {e}")
            
            doc.close()
            return images
            
        except Exception as e:
            self.logger.error(f"PDF image extraction failed: {e}")
            return []
    
    async def _process_single_image(self, file_path: Path, enhance: bool) -> List[Dict]:
        """Process a single image file"""
        
        try:
            with open(file_path, 'rb') as f:
                img_data = f.read()
            
            image_info = await self._analyze_image(img_data, 1, 1, enhance)
            return [image_info] if image_info else []
            
        except Exception as e:
            self.logger.error(f"Single image processing failed: {e}")
            return []
    
    async def _analyze_image(self, img_data: bytes, page_num: int, img_num: int, enhance: bool) -> Optional[Dict]:
        """Analyze and optionally enhance image"""
        
        try:
            # Load image with PIL
            image = Image.open(io.BytesIO(img_data))
            
            # Basic image information
            image_info = {
                'page_number': page_num,
                'image_number': img_num,
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'width': image.size[0],
                'height': image.size[1],
                'aspect_ratio': image.size[0] / image.size[1],
                'file_size': len(img_data)
            }
            
            # Quality assessment
            quality_metrics = await self._assess_image_quality(image)
            image_info.update(quality_metrics)
            
            # Enhancement if requested and needed
            if enhance and quality_metrics.get('needs_enhancement', False):
                enhanced_image = await self._enhance_image(image)
                if enhanced_image:
                    image_info['enhanced'] = True
                    # Update size info for enhanced image
                    image_info['enhanced_size'] = enhanced_image.size
            
            return image_info
            
        except Exception as e:
            self.logger.warning(f"Image analysis failed: {e}")
            return None
    
    async def _assess_image_quality(self, image: Image.Image) -> Dict:
        """Assess image quality metrics"""
        
        try:
            # Convert to OpenCV format for analysis
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale for quality metrics
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # Calculate sharpness using Laplacian variance
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Calculate brightness
            brightness = np.mean(gray)
            
            # Calculate contrast
            contrast = gray.std()
            
            # Determine if enhancement is needed
            needs_enhancement = (
                sharpness < 100 or  # Low sharpness
                brightness < 50 or brightness > 200 or  # Too dark or bright
                contrast < 20  # Low contrast
            )
            
            return {
                'sharpness': float(sharpness),
                'brightness': float(brightness),
                'contrast': float(contrast),
                'needs_enhancement': needs_enhancement,
                'quality_score': min(1.0, (sharpness / 200 + contrast / 50) / 2)
            }
            
        except Exception as e:
            self.logger.warning(f"Quality assessment failed: {e}")
            return {'needs_enhancement': False, 'quality_score': 0.5}
    
    async def _enhance_image(self, image: Image.Image) -> Optional[Image.Image]:
        """Enhance image quality"""
        
        try:
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2LAB)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            # Apply noise reduction
            denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
            
            # Apply sharpening
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            
            # Convert back to PIL
            enhanced_image = Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
            
            return enhanced_image
            
        except Exception as e:
            self.logger.warning(f"Image enhancement failed: {e}")
            return None