import os, docx

def save_docx(CATALOGUE: str):
    
    slides = [f"{CATALOGUE}/{x}" for x in os.listdir(CATALOGUE) if '.png' in x and x != 'screen.png']

    doc = docx.Document()

    p = doc.add_paragraph()
    p.add_run('Enjoy your slides ').font.name = 'Lato'
    p.add_run('https://github.com/tomWitkowski').font.name = 'Lato'
    p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

    for slide in slides:
        doc.add_picture(slide, width=docx.shared.Inches(5))
        doc.paragraphs[-1].alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

    doc.save(f'{CATALOGUE}.docx')
    