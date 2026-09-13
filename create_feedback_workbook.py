from datetime import date
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape

OUTPUT = Path(__file__).with_name("hotel_booking_feedback.xlsx")

records = [
    ("Application UI", 5, "The booking steps are clear and easy to follow.", "Positive"),
    ("Application UI", 4, "Search filters are useful, but the date picker could be faster.", "Positive"),
    ("Application UI", 3, "The room photos take a while to load on mobile.", "Neutral"),
    ("Application UI", 5, "The confirmation screen gives me all important details.", "Positive"),
    ("Application UI", 4, "It is easy to compare prices between different room types.", "Positive"),
    ("Application UI", 2, "The back button sometimes resets my selected filters.", "Negative"),
    ("Application UI", 5, "The map view helped me choose a convenient hotel location.", "Positive"),
    ("Application UI", 4, "The app layout feels clean and responds quickly.", "Positive"),
    ("Application UI", 3, "I had trouble finding the option to modify a booking.", "Neutral"),
    ("Application UI", 5, "The booking summary is accurate and easy to review.", "Positive"),
    ("User-friendly", 5, "I completed my reservation without needing help.", "Positive"),
    ("User-friendly", 4, "Instructions are simple, though cancellation terms could be more visible.", "Positive"),
    ("User-friendly", 5, "The process is straightforward even for a first-time user.", "Positive"),
    ("User-friendly", 3, "Some labels are unclear when selecting additional services.", "Neutral"),
    ("User-friendly", 4, "The booking form remembers my details and saves time.", "Positive"),
    ("User-friendly", 5, "I could easily book a room from my phone.", "Positive"),
    ("User-friendly", 4, "The checkout process is much simpler than other travel sites.", "Positive"),
    ("User-friendly", 2, "The error message did not explain how to fix my input.", "Negative"),
    ("User-friendly", 5, "The language is friendly and the instructions are helpful.", "Positive"),
    ("User-friendly", 4, "Everything needed for the reservation is available in one place.", "Positive"),
    ("Billing", 4, "The price breakdown clearly shows taxes and service fees.", "Positive"),
    ("Billing", 5, "My payment was processed quickly and the receipt arrived immediately.", "Positive"),
    ("Billing", 3, "The final total was slightly higher than the initial estimate.", "Neutral"),
    ("Billing", 5, "Multiple payment methods made checkout convenient.", "Positive"),
    ("Billing", 4, "The invoice is easy to download for business expenses.", "Positive"),
    ("Billing", 2, "My card was charged twice and I had to contact support.", "Negative"),
    ("Billing", 4, "The currency selector worked as expected.", "Positive"),
    ("Billing", 5, "The refund was credited within the timeframe provided.", "Positive"),
    ("Billing", 3, "I would like to see a clearer explanation of the deposit hold.", "Neutral"),
    ("Billing", 5, "The booking confirmation included the correct payment details.", "Positive"),
    ("Rooms", 5, "The room matched the photos and description exactly.", "Positive"),
    ("Rooms", 4, "The bed was comfortable and the room was well maintained.", "Positive"),
    ("Rooms", 3, "The room was clean, but smaller than expected.", "Neutral"),
    ("Rooms", 5, "The view from the room was excellent.", "Positive"),
    ("Rooms", 4, "The room had all the amenities listed during booking.", "Positive"),
    ("Rooms", 2, "The air conditioning was noisy during the night.", "Negative"),
    ("Rooms", 5, "Check-in was smooth and the room was ready on arrival.", "Positive"),
    ("Rooms", 4, "The bathroom was spotless and supplied with fresh towels.", "Positive"),
    ("Rooms", 3, "Sound from the hallway was noticeable in the evening.", "Neutral"),
    ("Rooms", 5, "The room upgrade was worth the additional cost.", "Positive"),
    ("Customer Assistance", 5, "The support agent answered my question quickly.", "Positive"),
    ("Customer Assistance", 4, "The agent was polite and helped change my arrival time.", "Positive"),
    ("Customer Assistance", 3, "It took longer than expected to receive a response by email.", "Neutral"),
    ("Customer Assistance", 5, "The support team resolved my cancellation request in one conversation.", "Positive"),
    ("Customer Assistance", 4, "The help center articles covered most of my questions.", "Positive"),
    ("Customer Assistance", 2, "I was transferred between agents before getting an answer.", "Negative"),
    ("Customer Assistance", 5, "The live chat representative was knowledgeable and efficient.", "Positive"),
    ("Customer Assistance", 4, "The response included useful instructions and next steps.", "Positive"),
    ("Customer Assistance", 3, "Weekend support availability should be extended.", "Neutral"),
    ("Customer Assistance", 5, "The team followed up to confirm that my issue was resolved.", "Positive"),
]

categories = ["Application UI", "User-friendly", "Billing", "Rooms", "Customer Assistance"]
headers = ["Feedback ID", "Date", "Category", "Rating", "Feedback", "Sentiment"]

def col_name(number):
    name = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        name = chr(65 + remainder) + name
    return name

def cell_ref(row, column):
    return f"{col_name(column)}{row}"

def inline_cell(reference, value, style=0):
    return f'<c r="{reference}" s="{style}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>'

def number_cell(reference, value, style=0):
    return f'<c r="{reference}" s="{style}"><v>{value}</v></c>'

def row_xml(row_number, values, styles=None):
    styles = styles or [0] * len(values)
    cells = []
    for column, value in enumerate(values, 1):
        reference = cell_ref(row_number, column)
        if isinstance(value, (int, float)):
            cells.append(number_cell(reference, value, styles[column - 1]))
        else:
            cells.append(inline_cell(reference, value, styles[column - 1]))
    return f'<row r="{row_number}">{"".join(cells)}</row>'

def worksheet_xml():
    rows = [row_xml(1, headers, [1] * 6)]
    for index, record in enumerate(records, 2):
        feedback_id = f"FB-{index - 1:03d}"
        feedback_date = date(2026, 1 + ((index - 2) % 9), 1 + ((index * 3) % 27)).isoformat()
        category, rating, feedback, sentiment = record
        rows.append(row_xml(index, [feedback_id, feedback_date, category, rating, feedback, sentiment], [0, 0, 0, 2, 3, 4]))
    dimension = '<cols><col min="1" max="1" width="14" customWidth="1"/><col min="2" max="2" width="14" customWidth="1"/><col min="3" max="3" width="22" customWidth="1"/><col min="4" max="4" width="10" customWidth="1"/><col min="5" max="5" width="72" customWidth="1"/><col min="6" max="6" width="16" customWidth="1"/></cols>'
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" activeCell="A2" sqref="A2"/></sheetView></sheetViews>
  {dimension}
  <sheetData>{"".join(rows)}</sheetData>
  <autoFilter ref="A1:F51"/>
</worksheet>'''

def summary_xml():
    counts = {category: [0, 0] for category in categories}
    for category, rating, _, _ in records:
        counts[category][0] += 1
        counts[category][1] += rating
    rows = [row_xml(1, ["Hotel Booking Feedback Summary"], [5]), row_xml(3, ["Category", "Record Count", "Average Rating"], [1, 1, 1])]
    for row_number, category in enumerate(categories, 4):
        count, total = counts[category]
        rows.append(row_xml(row_number, [category, count, round(total / count, 2)], [0, 2, 2]))
    rows.append(row_xml(10, ["Overall", len(records), round(sum(item[1] for item in records) / len(records), 2)], [1, 2, 2]))
    rows.append(row_xml(12, ["Rating scale: 1 (lowest) to 5 (highest)"], [6]))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheetViews><sheetView workbookViewId="0"/></sheetViews>
  <cols><col min="1" max="1" width="28" customWidth="1"/><col min="2" max="2" width="16" customWidth="1"/><col min="3" max="3" width="18" customWidth="1"/></cols>
  <sheetData>{"".join(rows)}</sheetData>
</worksheet>'''

styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="1"><numFmt numFmtId="164" formatCode="0.00"/></numFmts>
  <fonts count="3"><font><sz val="11"/><color rgb="FF1F2937"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font><font><b/><sz val="16"/><color rgb="FF123B4A"/><name val="Calibri"/></font></fonts>
  <fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF123B4A"/><bgColor indexed="64"/></patternFill></fill></fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="7"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf><xf numFmtId="0" fontId="0" fillId="0" borderId="0" applyAlignment="1"><alignment horizontal="center"/></xf><xf numFmtId="0" fontId="0" fillId="0" borderId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf><xf numFmtId="0" fontId="0" fillId="0" borderId="0" applyAlignment="1"><alignment horizontal="center"/></xf><xf numFmtId="0" fontId="2" fillId="0" borderId="0"/><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellXfs>
</styleSheet>'''

workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Feedback Data" sheetId="1" r:id="rId1"/><sheet name="Summary" sheetId="2" r:id="rId2"/></sheets></workbook>'''

content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>'''

root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'''

workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''

with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as workbook:
    workbook.writestr("[Content_Types].xml", content_types_xml)
    workbook.writestr("_rels/.rels", root_rels)
    workbook.writestr("xl/workbook.xml", workbook_xml)
    workbook.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
    workbook.writestr("xl/styles.xml", styles_xml)
    workbook.writestr("xl/worksheets/sheet1.xml", worksheet_xml())
    workbook.writestr("xl/worksheets/sheet2.xml", summary_xml())

print(f"Created {OUTPUT} with {len(records)} feedback records.")
