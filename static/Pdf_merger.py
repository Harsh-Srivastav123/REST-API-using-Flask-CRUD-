from pikepdf import Pdf
from glob import glob
new_pdf=Pdf.new()
for file in glob("*.pdf"):
    old_pdf=Pdf.open(file)
    new_pdf.pages.extend(old_pdf.pages)
new_pdf.save("final.pdf")
print("Successfully created")