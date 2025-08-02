"""
Create a simple test PDF for file upload testing
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_test_pdf():
    """Create a simple test PDF file"""
    filename = "test_document.pdf"
    
    try:
        # Create a simple PDF
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Add some content
        c.setFont("Helvetica", 16)
        c.drawString(100, height - 100, "Test Document for HackRX 5.0")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 140, "This is a test document for file upload functionality.")
        c.drawString(100, height - 160, "")
        c.drawString(100, height - 180, "Key Information:")
        c.drawString(120, height - 200, "• Grace period: 30 days")
        c.drawString(120, height - 220, "• Coverage: Comprehensive health insurance")
        c.drawString(120, height - 240, "• Premium payment: Monthly")
        c.drawString(120, height - 260, "• Waiting period: 2 years for pre-existing conditions")
        
        c.drawString(100, height - 300, "This document can be used to test the file upload endpoint")
        c.drawString(100, height - 320, "of the HackRX 5.0 intelligent query-retrieval system.")
        
        c.save()
        print(f"✅ Test PDF created: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Could not create PDF with reportlab: {e}")
        
        # Create a simple text file as fallback
        txt_filename = "test_document.txt"
        with open(txt_filename, 'w') as f:
            f.write("""Test Document for HackRX 5.0

This is a test document for file upload functionality.

Key Information:
• Grace period: 30 days
• Coverage: Comprehensive health insurance  
• Premium payment: Monthly
• Waiting period: 2 years for pre-existing conditions

This document can be used to test the file upload endpoint
of the HackRX 5.0 intelligent query-retrieval system.
""")
        print(f"✅ Test text file created: {txt_filename}")
        return txt_filename

if __name__ == "__main__":
    create_test_pdf()
