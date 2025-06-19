"""
Table Extraction Module using pdfplumber for PDF tables
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
import pdfplumber
import pandas as pd

class TableExtractor:
    """Extract tables from PDF documents"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def extract_tables(self, file_path: Path) -> List[Dict]:
        """Extract tables from PDF document"""
        
        try:
            if file_path.suffix.lower() != '.pdf':
                return []
            
            return await self._extract_pdf_tables(file_path)
            
        except Exception as e:
            self.logger.error(f"Table extraction failed: {str(e)}")
            return []
    
    async def _extract_pdf_tables(self, file_path: Path) -> List[Dict]:
        """Extract tables from PDF using pdfplumber"""
        
        tables = []
        
        try:
            with pdfplumber.open(str(file_path)) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    
                    for table_num, table in enumerate(page_tables):
                        if table and len(table) > 1:  # Must have header + at least one row
                            processed_table = await self._process_table(
                                table, page_num + 1, table_num + 1
                            )
                            if processed_table:
                                tables.append(processed_table)
            
            return tables
            
        except Exception as e:
            self.logger.error(f"PDF table extraction failed: {e}")
            return []
    
    async def _process_table(self, raw_table: List[List], page_num: int, table_num: int) -> Optional[Dict]:
        """Process and clean extracted table data"""
        
        try:
            # Clean the raw table data
            cleaned_table = []
            for row in raw_table:
                cleaned_row = []
                for cell in row:
                    # Clean cell content
                    if cell is not None:
                        cleaned_cell = str(cell).strip()
                        cleaned_row.append(cleaned_cell)
                    else:
                        cleaned_row.append('')
                
                # Only add rows that have some content
                if any(cell for cell in cleaned_row):
                    cleaned_table.append(cleaned_row)
            
            if not cleaned_table:
                return None
            
            # Create DataFrame for better processing
            df = pd.DataFrame(cleaned_table[1:], columns=cleaned_table[0])
            
            # Remove completely empty rows/columns
            df = df.dropna(how='all').dropna(axis=1, how='all')
            
            if df.empty:
                return None
            
            # Convert back to list format
            table_data = [df.columns.tolist()] + df.values.tolist()
            
            return {
                'page_number': page_num,
                'table_number': table_num,
                'data': table_data,
                'rows': len(table_data) - 1,  # Excluding header
                'columns': len(table_data[0]) if table_data else 0,
                'header': table_data[0] if table_data else [],
                'csv_string': df.to_csv(index=False),
                'json_records': df.to_dict('records')
            }
            
        except Exception as e:
            self.logger.warning(f"Table processing failed: {e}")
            return None