import fpdf





file = fpdf.FPDF(format="A4")
file.add_page()

file.set_font(
    "Arial",
    style="B",
    size=20,

)

file.text(
    10,
    10,
    "ывапвапвапввап".encode('latin-1', 'replace').decode()
)


file.output("test.pdf", "F")
file.close()