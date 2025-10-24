"""
Content Processor Module
Handles file uploads and text extraction from PDF, TXT, and DOCX files
"""
import io
from typing import Optional
import PyPDF2

class ContentProcessor:
    """Process different file formats and extract text"""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_content: PDF file content as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """
        Extract text from TXT file
        
        Args:
            file_content: TXT file content as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            text = file_content.decode('utf-8')
            return text.strip()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                text = file_content.decode('latin-1')
                return text.strip()
            except Exception as e:
                raise Exception(f"Error decoding text file: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """
        Extract text from DOCX file
        
        Args:
            file_content: DOCX file content as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            from docx import Document
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except ImportError:
            raise Exception("python-docx not installed. Install it with: pip install python-docx")
        except Exception as e:
            raise Exception(f"Error extracting DOCX text: {str(e)}")
    
    @staticmethod
    def process_file(file_content: bytes, file_name: str) -> str:
        """
        Process uploaded file and extract text based on file extension
        
        Args:
            file_content: File content as bytes
            file_name: Name of the file with extension
            
        Returns:
            Extracted text content
        """
        file_extension = file_name.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return ContentProcessor.extract_text_from_pdf(file_content)
        elif file_extension == 'txt':
            return ContentProcessor.extract_text_from_txt(file_content)
        elif file_extension == 'docx':
            return ContentProcessor.extract_text_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 5000) -> str:
        """
        Truncate text to maximum length while trying to preserve complete sentences
        
        Args:
            text: Input text
            max_length: Maximum character length
            
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        
        # Truncate and try to find the last complete sentence
        truncated = text[:max_length]
        last_period = truncated.rfind('.')
        
        if last_period > max_length * 0.8:  # If we found a period in the last 20%
            return truncated[:last_period + 1]
        
        return truncated + "..."