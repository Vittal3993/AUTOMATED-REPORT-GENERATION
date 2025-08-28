import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Read Data
df = pd.read_csv('data.csv')

# Analyze Data
summary = df.describe(include='all')
grouped = df.groupby('Department')['CGPA'].mean().reset_index()

# Generate PDF Report
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Automated Report Generation', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def add_text(self, text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln(2)

pdf = PDFReport()
pdf.add_page()

# Metadata
pdf.add_text(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
pdf.ln(5)

# Summary Statistics
pdf.add_section_title("Summary Statistics")
for col in df.columns:
    if df[col].dtype in ['int64', 'float64']:
        pdf.add_text(f"{col}: Mean = {df[col].mean():.2f}, Max = {df[col].max()}, Min = {df[col].min()}")

# Department-wise Average Scores
pdf.add_section_title("Average CGPA by Department")
for _, row in grouped.iterrows():
    pdf.add_text(f"{row['Department']}: {row['CGPA']:.2f}")

# Raw Data
pdf.add_section_title("Raw Data")
for index, row in df.iterrows():
    pdf.add_text(f"{row['Name']} ({row['Department']}): CGPA = {row['CGPA']}")

# Save PDF
pdf.output("automated_report.pdf")
print("Report generated successfully!")
