# pdf_utils.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class PDFGenerator:
    def __init__(self, student, assignments):
        self.student = student
        self.assignments = assignments

    def generate_pdf(self, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 750, f"Student: {self.student.name}")
        c.drawString(100, 730, f"Registration Number: {self.student.registration_number}")

        y = 700
        for assignment in self.assignments:
            c.drawString(100, y, f"Assignment: {assignment.title} - Status: {assignment.submission_status}")
            y -= 20
            if y < 50:
                c.showPage()
                y = 750

        c.save()
