"""
Full Academic Project Report Builder in DOCX Format
Project Title: TRAVEL TICKET BOOKING SYSTEM
Destination: Desktop and Project Directory
"""

import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_helpers import (
    set_cell_background,
    set_cell_margins,
    set_table_borders,
    add_page_number_to_footer,
    format_paragraph,
    add_heading_1,
    add_heading_2,
    add_heading_3,
    add_body_p,
    add_bullet_p,
    add_figure_image
)

def create_full_report():
    print("Initiating full college project report compilation...")
    doc = docx.Document()

    # Section 1 Setup: A4, 1-inch margins
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = True

    # Setup Running Header & Footer for Subsequent Pages
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("TRAVEL TICKET BOOKING SYSTEM — PROJECT REPORT")
    hrun.font.name = 'Times New Roman'
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(100, 116, 139)

    footer = section.footer
    add_page_number_to_footer(footer)

    # =========================================================================
    # PRELIMINARY PAGES
    # =========================================================================

    # 1. COVER PAGE
    if os.path.exists("diagrams/college_logo.jpg"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_paragraph(p_logo, space_before=0, space_after=6, line_spacing=1.0)
        r_logo = p_logo.add_run()
        r_logo.add_picture("diagrams/college_logo.jpg", width=Inches(1.75))

    p_pre = doc.add_paragraph()
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_paragraph(p_pre, space_before=2, space_after=6, line_spacing=1.1)
    r = p_pre.add_run("A MINOR PROJECT REPORT ON")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(71, 85, 105)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_paragraph(p_title, space_before=4, space_after=6, line_spacing=1.1)
    r_title = p_title.add_run("TRAVEL TICKET BOOKING SYSTEM")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(229, 43, 80)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_paragraph(p_sub, space_before=2, space_after=12, line_spacing=1.15)
    r_sub = p_sub.add_run("A Responsive Web-Based Platform for Intercity Bus & Express Train Reservation")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_paragraph(p_deg, space_before=6, space_after=14, line_spacing=1.2)
    r_deg = p_deg.add_run(
        "Submitted in partial fulfillment of the requirements for the award of the degree of\n"
        "BACHELOR OF COMPUTER APPLICATIONS (BCA)\n"
        "5th Semester"
    )
    r_deg.font.name = 'Times New Roman'
    r_deg.font.size = Pt(11)
    r_deg.font.bold = True
    r_deg.font.color.rgb = RGBColor(30, 41, 59)

    # Submission Meta Table
    meta_table = doc.add_table(rows=1, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_table.columns[0].width = Inches(3.2)
    meta_table.columns[1].width = Inches(3.2)

    cell_left = meta_table.cell(0, 0)
    p_l = cell_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    format_paragraph(p_l, space_before=0, space_after=2, line_spacing=1.15)
    r_l1 = p_l.add_run("SUBMITTED BY:\n")
    r_l1.font.bold = True
    r_l1.font.size = Pt(10.5)
    r_l2 = p_l.add_run("SHIVANI\nRoll Number: 2448361\nClass & Sem: BCA, 5th Sem")
    r_l2.font.size = Pt(10.5)

    cell_right = meta_table.cell(0, 1)
    p_r = cell_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    format_paragraph(p_r, space_before=0, space_after=2, line_spacing=1.15)
    r_r1 = p_r.add_run("SUBMITTED TO:\n")
    r_r1.font.bold = True
    r_r1.font.size = Pt(10.5)
    r_r2 = p_r.add_run("MRS. JYOTI\nAssistant Professor\nDept. of Computer Applications")
    r_r2.font.size = Pt(10.5)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_paragraph(p_inst, space_before=16, space_after=0, line_spacing=1.15)
    r_inst = p_inst.add_run(
        "DEPARTMENT OF COMPUTER APPLICATIONS\n"
        "RAM DEVI JINDAL GROUP OF COLLEGES, LALRU, DISTT. MOHALI\n"
        "Affiliated to I.K. Gujral Punjab Technical University, Jalandhar\n"
        "ACADEMIC SESSION: 2026-2027"
    )
    r_inst.font.name = 'Times New Roman'
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_page_break()

    # 2. CERTIFICATE
    add_heading_1(doc, "CERTIFICATE OF APPROVAL")
    p_cert = doc.add_paragraph()
    format_paragraph(p_cert, space_before=10, space_after=12, line_spacing=1.4)
    r_c = p_cert.add_run(
        "This is to certify that the project report entitled \"TRAVEL TICKET BOOKING SYSTEM\" submitted by "
        "SHIVANI (Roll No: 2448361) in partial fulfillment of the requirements for the "
        "award of the degree of Bachelor of Computer Applications (BCA) at Ram Devi Jindal Group of Colleges, "
        "Lalru, Distt. Mohali (Affiliated to I.K. Gujral Punjab Technical University, Jalandhar), is an authentic record of bonafide project work carried out under my "
        "guidance and supervision during the academic session 2026-2027."
    )
    r_c.font.name = 'Times New Roman'
    r_c.font.size = Pt(11.5)

    p_cert2 = doc.add_paragraph()
    format_paragraph(p_cert2, space_before=4, space_after=28, line_spacing=1.4)
    r_c2 = p_cert2.add_run(
        "To the best of my knowledge, the matter embodied in this project report has not been submitted to any "
        "other University or Institute for the award of any degree or diploma."
    )
    r_c2.font.name = 'Times New Roman'
    r_c2.font.size = Pt(11.5)

    sig_table = doc.add_table(rows=2, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    for col in sig_table.columns:
        col.width = Inches(2.1)

    sig_headers = ["MRS. JYOTI", "MISS MANISHA", "External Examiner"]
    sig_desigs = [
        "Project Supervisor\nDept. of Computer Applications",
        "Head of Department (HOD)\nDept. of Computer Applications",
        "External Examiner\nUniversity Nominee (IKGPTU)"
    ]

    for i in range(3):
        c_top = sig_table.cell(0, i)
        c_bot = sig_table.cell(1, i)
        c_top.paragraphs[0].text = "____________________\n" + sig_headers[i]
        c_top.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_top.paragraphs[0].runs[0].font.size = Pt(10)
        c_top.paragraphs[0].runs[0].font.bold = True
        c_bot.paragraphs[0].text = sig_desigs[i]
        c_bot.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_bot.paragraphs[0].runs[0].font.size = Pt(9)
        c_bot.paragraphs[0].runs[0].font.italic = True

    doc.add_page_break()

    # 3. DECLARATION
    add_heading_1(doc, "DECLARATION OF ORIGINALITY")
    p_dec = doc.add_paragraph()
    format_paragraph(p_dec, space_before=10, space_after=12, line_spacing=1.4)
    r_d = p_dec.add_run(
        "I, SHIVANI, student of Bachelor of Computer Applications (BCA, 5th Semester), Roll Number: 2448361, "
        "hereby declare that the project entitled \"TRAVEL TICKET BOOKING SYSTEM\" "
        "is an original piece of academic work undertaken by me under the supervision of MRS. JYOTI, Assistant Professor, "
        "Department of Computer Applications, Ram Devi Jindal Group of Colleges, Lalru, Distt. Mohali (Affiliated to I.K. Gujral Punjab Technical University, Jalandhar)."
    )
    r_d.font.name = 'Times New Roman'
    r_d.font.size = Pt(11.5)

    add_body_p(doc, "I further declare that this report represents my own ideas and analysis, and wherever other sources, reference works, or technical specifications have been cited, appropriate references and acknowledgements have been made. This work has not been previously submitted in part or full for the award of any other academic degree, diploma, or certificate at this or any other educational institution.")

    p_dsig = doc.add_paragraph()
    format_paragraph(p_dsig, space_before=30, space_after=4, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.RIGHT)
    r_dsig = p_dsig.add_run("______________________________\nSignature of Student\nSHIVANI\nRoll No: 2448361\nClass & Sem: BCA, 5th Sem\nDate: 31st October 2026")
    r_dsig.font.name = 'Times New Roman'
    r_dsig.font.size = Pt(10.5)
    r_dsig.font.bold = True

    doc.add_page_break()

    # 4. ACKNOWLEDGEMENT
    add_heading_1(doc, "ACKNOWLEDGEMENT")
    add_body_p(doc, "The completion of this college project report and the implementation of the Travel Ticket Booking System would not have been possible without the invaluable guidance, constructive criticism, and encouragement extended by several individuals.")
    add_body_p(doc, "First and foremost, I wish to express my deepest gratitude and sincere appreciation to my esteemed Project Guide, MRS. JYOTI, Assistant Professor, Department of Computer Applications, for her continuous support, technical mentorship, and patient reviews throughout the conceptualization, system design, and coding stages of this project.")
    add_body_p(doc, "I also extend my heartfelt thanks to the Head of Department (HOD), MISS MANISHA, Department of Computer Applications, Ram Devi Jindal Group of Colleges, for granting access to the necessary computing facilities, internet resources, and laboratory infrastructure that facilitated the successful realization of this application.")
    add_body_p(doc, "I express my sincere thanks to the Management and Director of Ram Devi Jindal Group of Colleges, Lalru, Distt. Mohali for providing an academic environment that fosters innovation, practical problem-solving, and hands-on software development.")
    add_body_p(doc, "Lastly, I am thankful to my family members and friends whose constant encouragement, constructive feedback during user interface testing, and moral support inspired me to bring this project to a successful conclusion.")

    p_asig = doc.add_paragraph()
    format_paragraph(p_asig, space_before=24, space_after=4, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.RIGHT)
    r_asig = p_asig.add_run("SHIVANI\nRoll No: 2448361\nBCA, 5th Semester\nDepartment of Computer Applications\nRam Devi Jindal Group of Colleges, Lalru, Distt. Mohali")
    r_asig.font.name = 'Times New Roman'
    r_asig.font.size = Pt(10.5)
    r_asig.font.bold = True

    doc.add_page_break()

    # 5. ABSTRACT
    add_heading_1(doc, "ABSTRACT")
    p_abs = doc.add_paragraph()
    format_paragraph(p_abs, space_before=12, space_after=12, line_spacing=1.5)
    r_abs = p_abs.add_run(
        "The Travel Ticket Booking System is a comprehensive, responsive web-based ticketing solution engineered "
        "to digitize and streamline the intercity passenger reservation experience for buses and express trains. "
        "Traditional travel ticketing methodologies—characterized by long physical queues at booking terminals, "
        "restricted operational hours, lack of seat arrangement transparency, and dependency on intermediary booking "
        "agents—incur substantial delays and logistical friction. The primary purpose of developing this project is "
        "to eliminate these inefficiencies by providing an accessible, transparent, and direct booking portal inspired "
        "by industry standards such as RedBus and MakeMyTrip.\n\n"
        "Constructed entirely using standard client-side technologies—HTML5 for semantic structure, CSS3 for modern responsive "
        "styling, and Vanilla JavaScript (ES6+) for dynamic behavior—the application operates self-contained directly within "
        "any modern web browser without requiring heavy external frameworks, server-side runtimes, or backend databases. Data "
        "persistence, active session management, and inventory tracking are robustly handled utilizing the HTML5 LocalStorage "
        "API. The platform encompasses a complete passenger lifecycle including secure user registration, email-based authentication, "
        "intelligent multi-criteria schedule search, visual seat map selection with color-coded occupancy indicators (available, "
        "selected, booked), dynamic fare computation with promotional discounting, simulated payment gateway checkout, and "
        "printable boarding pass generation featuring custom SVG QR code verification.\n\n"
        "Crucially, the system features dynamic seat restoration upon booking cancellation and incorporates a dedicated "
        "Administrative Console equipped with real-time KPI metrics, fleet management CRUD operations, and CSV financial reporting. "
        "This project successfully proves that modern client-side web technologies can deliver an intuitive, high-performance, and "
        "feature-rich transaction simulation ideal for practical academic study and college demonstration."
    )
    r_abs.font.name = 'Times New Roman'
    r_abs.font.size = Pt(12)

    p_kw = doc.add_paragraph()
    format_paragraph(p_kw, space_before=10, space_after=6, line_spacing=1.3)
    r_kw_bold = p_kw.add_run("Keywords: ")
    r_kw_bold.font.name = 'Times New Roman'
    r_kw_bold.font.size = Pt(11.5)
    r_kw_bold.font.bold = True
    r_kw = p_kw.add_run("Travel Ticket Booking, Responsive Web Design, Vanilla JavaScript, HTML5 LocalStorage, Visual Seat Selection, E-Ticket Generation, Admin Analytics, Client-Side Persistence.")
    r_kw.font.name = 'Times New Roman'
    r_kw.font.size = Pt(11.5)
    r_kw.font.italic = True

    doc.add_page_break()

    # 6. TABLE OF CONTENTS
    add_heading_1(doc, "TABLE OF CONTENTS")
    
    toc_data = [
        ("Certificate of Approval", "ii"),
        ("Declaration of Originality", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "viii"),
        ("List of Tables", "viii"),
        ("List of Abbreviations", "x"),
        ("CHAPTER 1: INTRODUCTION", "11"),
        ("    1.1 Introduction", "11"),
        ("    1.2 Background of the Project", "11"),
        ("    1.3 Problem Statement", "11"),
        ("    1.4 Objectives of the Project", "12"),
        ("    1.5 Scope of the Project", "12"),
        ("CHAPTER 2: LITERATURE REVIEW AND EXISTING SYSTEM", "13"),
        ("    2.1 Existing System", "13"),
        ("    2.2 Limitations of Existing System", "13"),
        ("    2.3 Proposed System", "13"),
        ("    2.4 Advantages of Proposed System", "14"),
        ("CHAPTER 3: SYSTEM ANALYSIS AND REQUIREMENTS", "15"),
        ("    3.1 Functional Requirements", "15"),
        ("    3.2 Non-Functional Requirements", "15"),
        ("    3.3 Hardware Requirements", "15"),
        ("    3.4 Software Requirements", "16"),
        ("    3.5 Feasibility Study", "16"),
        ("CHAPTER 4: TECHNOLOGIES USED", "17"),
        ("    4.1 HTML5", "17"),
        ("    4.2 CSS3", "17"),
        ("    4.3 JavaScript (ES6+)", "17"),
        ("    4.4 LocalStorage API", "18"),
        ("    4.5 Development & Testing Tools", "18"),
        ("CHAPTER 5: SYSTEM DESIGN", "19"),
        ("    5.1 System Architecture", "19"),
        ("    5.2 Data Flow Diagram (DFD Level 0 and Level 1)", "19"),
        ("    5.3 Use Case Diagram (User and Administrator)", "20"),
        ("    5.4 Flowchart (End-to-End Booking Process)", "21"),
        ("    5.5 Database / Data Storage Design", "22"),
        ("    5.6 Module Description", "23"),
        ("CHAPTER 6: IMPLEMENTATION", "24"),
        ("    6.1 Home Page & Hero Search Interface", "24"),
        ("    6.2 User Registration and Login Modules", "24"),
        ("    6.3 Ticket Search & Multi-Facet Filtering Engine", "24"),
        ("    6.4 Bus and Train Details & Amenities Representation", "24"),
        ("    6.5 Interactive Visual Seat Selection & Color Cues", "24"),
        ("    6.6 Passenger Details Collection", "25"),
        ("    6.7 Booking & Simulated Payment Gateway Integration", "25"),
        ("    6.8 Booking History & Cancellation Seat Restoration", "25"),
        ("    6.9 Boarding Pass E-Ticket Generation & QR Visuals", "25"),
        ("    6.10 Admin Dashboard, Analytics & CSV Export", "25"),
        ("CHAPTER 7: TESTING", "26"),
        ("    7.1 Testing Introduction & Methodologies", "26"),
        ("    7.2 Functional Testing", "26"),
        ("    7.3 Validation Testing", "26"),
        ("    7.4 Comprehensive Test Cases & Matrix", "26"),
        ("    7.5 Testing Results & Verification Summary", "27"),
        ("CHAPTER 8: RESULTS AND SCREENSHOTS", "28"),
        ("    8.1 Home Page Interface", "28"),
        ("    8.2 User Authentication & Registration", "28"),
        ("    8.3 Ticket Search Results & Filter Sidebar", "29"),
        ("    8.4 Interactive Visual Seat Selection", "29"),
        ("    8.5 Passenger Details Collection & Checkout", "30"),
        ("    8.6 Passenger Booking History & Cancellation", "30"),
        ("    8.7 Official Boarding Pass E-Ticket", "31"),
        ("    8.8 Admin Analytics Dashboard & Fleet Control", "31"),
        ("CHAPTER 9: CONCLUSION AND FUTURE SCOPE", "33"),
        ("    9.1 Conclusion", "33"),
        ("    9.2 Limitations", "33"),
        ("    9.3 Future Enhancements", "33"),
        ("CHAPTER 10: REFERENCES", "35"),
        ("    10.1 Books and Study Materials", "35"),
        ("    10.2 Websites and Online Documentation", "35")
    ]

    toc_table = doc.add_table(rows=len(toc_data), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.autofit = False
    toc_table.columns[0].width = Inches(5.8)
    toc_table.columns[1].width = Inches(0.8)

    for i, (title, page) in enumerate(toc_data):
        c0 = toc_table.cell(i, 0)
        c1 = toc_table.cell(i, 1)
        set_cell_margins(c0, 10, 10, 20, 20)
        set_cell_margins(c1, 10, 10, 20, 20)
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(1)
        p0.paragraph_format.line_spacing = 1.05
        r0 = p0.add_run(title)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(9.5)
        if title.startswith("CHAPTER") or not title.startswith("    "):
            r0.font.bold = True
            
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.line_spacing = 1.05
        r1 = p1.add_run(page)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(9.5)
        if title.startswith("CHAPTER"):
            r1.font.bold = True

    doc.add_page_break()

    # 7. LIST OF FIGURES
    add_heading_1(doc, "LIST OF FIGURES")
    figures_list = [
        ("Figure 5.1", "Three-Tier Client-Side System Architecture Diagram", "19"),
        ("Figure 5.2", "Data Flow Diagram (Level 0 - Context Level Diagram)", "20"),
        ("Figure 5.3", "Data Flow Diagram (Level 1 - Functional Decomposition)", "20"),
        ("Figure 5.4", "User Scope UML Use Case Diagram", "21"),
        ("Figure 5.5", "Admin Management Scope UML Use Case Diagram", "21"),
        ("Figure 5.6", "End-to-End Booking and Ticket Issuance Flowchart", "22"),
        ("Figure 8.1", "Home Page & Hero Search Interface Screenshot", "28"),
        ("Figure 8.2", "User Authentication & Sign-In Interface Screenshot", "28"),
        ("Figure 8.3", "User Registration & Form Validation Screenshot", "29"),
        ("Figure 8.4", "Live Ticket Search Results & Filter Sidebar Screenshot", "29"),
        ("Figure 8.5", "Interactive Visual Seat Layout & Fare Calculation Screenshot", "30"),
        ("Figure 8.6", "Passenger Details Collection & Payment Checkout Screenshot", "30"),
        ("Figure 8.7", "Passenger Booking History & Cancellation Management Screenshot", "31"),
        ("Figure 8.8", "Official Boarding Pass E-Ticket with QR Code Screenshot", "31"),
        ("Figure 8.9", "Admin Analytics Dashboard & Real-Time Fleet Control Screenshot", "32")
    ]

    fig_table = doc.add_table(rows=len(figures_list) + 1, cols=3)
    fig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    fig_table.autofit = False
    fig_table.columns[0].width = Inches(1.3)
    fig_table.columns[1].width = Inches(4.5)
    fig_table.columns[2].width = Inches(0.8)

    # Header
    for j, htext in enumerate(["Figure No.", "Title / Caption", "Page"]):
        cell = fig_table.cell(0, j)
        set_cell_background(cell, "0077ED")
        p = cell.paragraphs[0]
        r = p.add_run(htext)
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        if j == 2: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for i, (f_num, f_cap, f_pg) in enumerate(figures_list):
        row_cells = fig_table.rows[i+1].cells
        if i % 2 == 1:
            for c in row_cells: set_cell_background(c, "F8FAFC")
        row_cells[0].paragraphs[0].text = f_num
        row_cells[0].paragraphs[0].runs[0].font.bold = True
        row_cells[0].paragraphs[0].runs[0].font.size = Pt(10)
        row_cells[1].paragraphs[0].text = f_cap
        row_cells[1].paragraphs[0].runs[0].font.size = Pt(10)
        row_cells[2].paragraphs[0].text = f_pg
        row_cells[2].paragraphs[0].runs[0].font.size = Pt(10)
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # 8. LIST OF TABLES
    add_heading_1(doc, "LIST OF TABLES")
    tables_list = [
        ("Table 3.1", "Client & Demonstration Hardware Requirements Specification", "16"),
        ("Table 3.2", "Operating Environment & Browser Software Requirements", "16"),
        ("Table 5.1", "Functional Modules Description & Implementation Mapping", "23"),
        ("Table 5.2", "LocalStorage Key-Value Entity Schema & Structural Design", "23"),
        ("Table 7.1", "System Test Cases, Validation Scenarios & Verification Matrix", "27")
    ]

    tbl_list_tbl = doc.add_table(rows=len(tables_list) + 1, cols=3)
    tbl_list_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_list_tbl.autofit = False
    tbl_list_tbl.columns[0].width = Inches(1.3)
    tbl_list_tbl.columns[1].width = Inches(4.5)
    tbl_list_tbl.columns[2].width = Inches(0.8)

    for j, htext in enumerate(["Table No.", "Table Title / Description", "Page"]):
        cell = tbl_list_tbl.cell(0, j)
        set_cell_background(cell, "E52B50")
        p = cell.paragraphs[0]
        r = p.add_run(htext)
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        if j == 2: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for i, (t_num, t_cap, t_pg) in enumerate(tables_list):
        row_cells = tbl_list_tbl.rows[i+1].cells
        if i % 2 == 1:
            for c in row_cells: set_cell_background(c, "F8FAFC")
        row_cells[0].paragraphs[0].text = t_num
        row_cells[0].paragraphs[0].runs[0].font.bold = True
        row_cells[0].paragraphs[0].runs[0].font.size = Pt(10)
        row_cells[1].paragraphs[0].text = t_cap
        row_cells[1].paragraphs[0].runs[0].font.size = Pt(10)
        row_cells[2].paragraphs[0].text = t_pg
        row_cells[2].paragraphs[0].runs[0].font.size = Pt(10)
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_page_break()

    # 9. LIST OF ABBREVIATIONS
    add_heading_1(doc, "LIST OF ABBREVIATIONS")
    abbr_data = [
        ("HTML5", "Hypertext Markup Language (Version 5)"),
        ("CSS3", "Cascading Style Sheets (Version 3)"),
        ("JS", "JavaScript Programming Language (ECMAScript 6+)"),
        ("DOM", "Document Object Model"),
        ("UI / UX", "User Interface / User Experience"),
        ("API", "Application Programming Interface"),
        ("URL", "Uniform Resource Locator"),
        ("CSV", "Comma-Separated Values"),
        ("QR Code", "Quick Response Matrix Barcode"),
        ("UPI", "Unified Payments Interface"),
        ("VPA", "Virtual Payment Address"),
        ("SSL", "Secure Sockets Layer"),
        ("ISBT", "Inter-State Bus Terminal"),
        ("GST", "Goods and Services Tax"),
        ("PNR", "Passenger Name Record / Booking Reference"),
        ("KPI", "Key Performance Indicator"),
        ("CRUD", "Create, Read, Update, Delete Operations"),
        ("DFD", "Data Flow Diagram")
    ]

    abbr_table = doc.add_table(rows=len(abbr_data) + 1, cols=2)
    abbr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    abbr_table.autofit = False
    abbr_table.columns[0].width = Inches(2.0)
    abbr_table.columns[1].width = Inches(4.6)

    for j, htext in enumerate(["Abbreviation", "Full Expansion / Description"]):
        cell = abbr_table.cell(0, j)
        set_cell_background(cell, "0F172A")
        p = cell.paragraphs[0]
        r = p.add_run(htext)
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, (ab, full) in enumerate(abbr_data):
        row_cells = abbr_table.rows[i+1].cells
        if i % 2 == 1:
            for c in row_cells: set_cell_background(c, "F8FAFC")
        row_cells[0].paragraphs[0].text = ab
        row_cells[0].paragraphs[0].runs[0].font.bold = True
        row_cells[0].paragraphs[0].runs[0].font.size = Pt(10)
        row_cells[1].paragraphs[0].text = full
        row_cells[1].paragraphs[0].runs[0].font.size = Pt(10)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 1: INTRODUCTION")
    
    add_heading_2(doc, "1.1 Introduction")
    add_body_p(doc, "In the modern digital era, the transportation and intercity travel sector forms the critical economic backbone of India. With rapid urban growth, commercial expansion, and rising tourism, millions of commuters travel daily between major metropolitan centers and regional towns such as Delhi, Chandigarh, Shimla, Bilaspur, Manali, Mumbai, and Jaipur. However, securing intercity passenger tickets through conventional physical counters remains cumbersome, time-consuming, and prone to logistical bottlenecks.")
    add_body_p(doc, "The Travel Ticket Booking System (branded as TravelEase) is an advanced, fully responsive web application engineered to modernize the passenger booking experience. Designed to deliver an intuitive, clean interface inspired by commercial platforms like MakeMyTrip and RedBus, the platform enables users to search comprehensive transport schedules, review vehicle amenities, inspect real-time visual seat layouts, dynamically calculate fare structures, simulate payment checkouts, and instantly generate printable electronic boarding passes with custom QR codes.")

    add_heading_2(doc, "1.2 Background of the Project")
    add_body_p(doc, "Historically, bus and railway ticketing in India necessitated physical visits to bus terminals (ISBTs) or railway reservation counters. Commuters frequently endured extensive queues, faced arbitrary ticket pricing from unregulated intermediaries, and possessed no mechanism to view or select their desired seat configurations prior to departure.")
    add_body_p(doc, "While commercial online travel agencies (OTAs) have revolutionized ticketing, developing a full-featured, zero-dependency demonstration application that accurately replicates real-time seat locks, dynamic pricing, and administrative fleet management without complex server frameworks presents a valuable academic challenge. This project demonstrates how modern browser capabilities—specifically semantic HTML5, advanced CSS3 Grid/Flexbox, Vanilla JavaScript ES6+, and client-side LocalStorage—can be orchestrated into an enterprise-grade ticketing prototype suitable for college evaluation and practical demonstration.")

    add_heading_2(doc, "1.3 Problem Statement")
    add_body_p(doc, "Traditional ticketing practices suffer from several critical shortcomings:")
    add_bullet_p(doc, "Physical Presence and Long Queues: Commuters waste significant productive time traveling to ticket counters and waiting in congested queues.", "1. ")
    add_bullet_p(doc, "Opaque Seat Allocation: Passengers are frequently allocated arbitrary seats without prior visibility into whether they have received window seats, aisle seats, or sleeper berths.", "2. ")
    add_bullet_p(doc, "Inflexible Cancellation Processes: Manual cancellation policies often involve tedious administrative paperwork, delayed refund handoffs, and seats left vacant due to slow reallocation.", "3. ")
    add_bullet_p(doc, "Absence of Centralized Fleet Monitoring: Small and regional transport operators struggle to analyze booking metrics, track revenue flows, and adjust seat quotas without costly infrastructure.", "4. ")

    add_heading_2(doc, "1.4 Objectives of the Project")
    add_body_p(doc, "The key technical and functional objectives of this project are:")
    add_bullet_p(doc, "To design an attractive, accessible, and 100% responsive user interface that functions flawlessly across desktop monitors, laptops, tablets, and smartphones.", "• ")
    add_bullet_p(doc, "To implement an interactive, visual 2D seat selection grid allowing users to choose up to 6 seats in real time with distinct visual states (available, selected, booked).", "• ")
    add_bullet_p(doc, "To establish strict client-side validation ensuring that only authenticated users can proceed to checkout and reserve travel inventory.", "• ")
    add_bullet_p(doc, "To simulate a complete multi-tab checkout gateway supporting UPI QR codes, credit/debit card entries, and pay-at-boarding methods with automated reference generation.", "• ")
    add_bullet_p(doc, "To develop a dynamic seat restoration mechanism ensuring that when a booking is cancelled, reserved seats immediately return to open availability for other passengers.", "• ")
    add_bullet_p(doc, "To build an executive Admin Management Console delivering real-time KPI metrics, HTML5 Canvas revenue charts, transport CRUD controls, and CSV report export.", "• ")

    add_heading_2(doc, "1.5 Scope of the Project")
    add_body_p(doc, "The project scope encompasses both client passenger workflows and administrative operational supervision:")
    add_bullet_p(doc, "Passenger Module: Schedule discovery across 15+ curated routes, interactive seat visualizer, coupon code engine, passenger manifest input, simulated payment, and e-ticket generation.", "• ")
    add_bullet_p(doc, "Administrative Module: Fleet catalog management (buses and trains), passenger reservation inspection, manual cancellation override, transaction logging, and financial summaries.", "• ")
    add_bullet_p(doc, "Technical Boundary: The current implementation operates as a standalone client-side system using browser LocalStorage. Live commercial deployment would naturally require integrating an asynchronous backend server (e.g. Node.js/Java), a persistent relational database (MySQL/PostgreSQL), and official banking payment gateway APIs (Razorpay/Stripe).", "• ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: LITERATURE REVIEW AND EXISTING SYSTEM
    # =========================================================================
    add_heading_1(doc, "CHAPTER 2: LITERATURE REVIEW AND EXISTING SYSTEM")

    add_heading_2(doc, "2.1 Existing System")
    add_body_p(doc, "The existing intercity passenger transport booking landscape comprises two dominant paradigms: physical counter booking and centralized commercial booking portals.")
    add_body_p(doc, "Physical booking centers require passengers to travel to bus depots (such as Kashmere Gate ISBT in Delhi or Sector 43 ISBT in Chandigarh) or railway ticketing windows. Clerks manually check paper ledgers or legacy green-screen terminals, issue paper tickets, and collect physical cash. In parallel, while web portals like MakeMyTrip and RedBus exist commercially, their underlying architectures rely on complex multi-tiered enterprise frameworks, heavy client bundles (React/Angular), and continuous backend server roundtrips, making them challenging for academic institutions to deploy for offline demonstration or lightweight study.")

    add_heading_2(doc, "2.2 Limitations of Existing System")
    add_body_p(doc, "A comprehensive analysis reveals major bottlenecks across traditional systems:")
    add_bullet_p(doc, "Time Consumption: High transaction time per passenger leads to severe crowding during peak festival seasons (e.g., Diwali, Holi).", "• ")
    add_bullet_p(doc, "High Operational Overhead: Maintaining distributed physical ticketing booths, staffing personnel across shifts, and printing paper passes incurs substantial recurring costs.", "• ")
    add_bullet_p(doc, "Human Error & Discrepancies: Manual data entry frequently produces misspelled passenger names, erroneous journey dates, and double-booking conflicts.", "• ")
    add_bullet_p(doc, "Lack of Customer Autonomy: Passengers have zero real-time visibility into the vehicle's physical chassis layout, luggage provisions, or exact berth dimensions.", "• ")

    add_heading_2(doc, "2.3 Proposed System")
    add_body_p(doc, "The proposed Travel Ticket Booking System provides a lightweight, highly responsive, web-native solution that runs immediately in any browser with zero installation overhead. By adopting a pure HTML5, CSS3, and Vanilla JavaScript architecture backed by LocalStorage, it provides an instantaneous, zero-latency user experience.")
    add_body_p(doc, "Key innovations in the proposed system include:")
    add_bullet_p(doc, "Instant Client-Side State Persistence: Bookings, transport catalogs, user accounts, and seat occupancy matrices are stored locally and survive browser refreshes without requiring a remote database.", "• ")
    add_bullet_p(doc, "Interactive Visual Seat Selection: Users interact with an intuitive graphic representation of bus and train cabins, selecting specific seats with immediate fare updating.", "• ")
    add_bullet_p(doc, "Dynamic Cancellation & Seat Recycling: When a reservation is cancelled, the system immediately recalculates available quotas and restores seat availability for the specific route and date.", "• ")
    add_bullet_p(doc, "High-Performance Analytics: Built-in HTML5 Canvas charts render visual monthly revenue trends without relying on bloated external charting libraries.", "• ")

    add_heading_2(doc, "2.4 Advantages of Proposed System")
    add_body_p(doc, "The proposed architecture introduces numerous tangible benefits:")
    add_bullet_p(doc, "24/7 Availability: Passengers can browse routes, compare fares, and book tickets at any time from any device.", "1. ")
    add_bullet_p(doc, "Zero Server Cost: Entirely runs client-side, making it exceptionally economical for academic demonstrations, training simulations, and lightweight kiosks.", "2. ")
    add_bullet_p(doc, "Paperless Environmental Friendly: Digital e-tickets with embedded SVG QR codes eliminate physical paper waste.", "3. ")
    add_bullet_p(doc, "Fast and Responsive: Zero network latency results in instantaneous page transitions and search filtering.", "4. ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: SYSTEM ANALYSIS AND REQUIREMENTS
    # =========================================================================
    add_heading_1(doc, "CHAPTER 3: SYSTEM ANALYSIS AND REQUIREMENTS")

    add_heading_2(doc, "3.1 Functional Requirements")
    add_body_p(doc, "Functional requirements define the core operational features provided by the application:")
    add_bullet_p(doc, "User Authentication & Registration: Users must register with full name, email, 10-digit mobile number, and password. The system must enforce unique emails and validate password matching.", "• ")
    add_bullet_p(doc, "Route & Schedule Search: The system must allow users to filter transports by source city, destination city, departure date, and transport type (bus/train).", "• ")
    add_bullet_p(doc, "Interactive Seat Selection: The visual seat layout must dynamically render available seats in green, selected seats in blue, and already-booked seats in gray (disabled). Multi-seat selection must cap at 6 seats per transaction.", "• ")
    add_bullet_p(doc, "Dynamic Fare Calculation: The system must compute base fare, apply a 5% GST calculation, and process promotional discount codes (e.g., TRAVEL50 for 10% discount, FIRSTBOOK for ₹150 flat discount).", "• ")
    add_bullet_p(doc, "Simulated Checkout & Ticket Issuance: The checkout engine must simulate UPI QR, Card, and Cash payments, issuing an immutable Booking ID (e.g. TRV-XXXXXX).", "• ")
    add_bullet_p(doc, "Booking Cancellation & Seat Restoration: Users must have the ability to cancel confirmed bookings, with the system immediately releasing occupied seats back into the date pool.", "• ")
    add_bullet_p(doc, "Admin Management: Authorized administrators must access KPI statistics, create/update/delete vehicle fleets, monitor bookings, and export transaction records to CSV.", "• ")

    add_heading_2(doc, "3.2 Non-Functional Requirements")
    add_body_p(doc, "Non-functional requirements describe the quality attributes and constraints of the platform:")
    add_bullet_p(doc, "Usability & Accessibility: The design system utilizes high-contrast color palettes, intuitive typography (Plus Jakarta Sans), and clear status badges.", "• ")
    add_bullet_p(doc, "Performance & Speed: Page load times and search filter operations must execute in under 100 milliseconds due to client-side data handling.", "• ")
    add_bullet_p(doc, "Reliability & Data Integrity: LocalStorage operations must utilize defensive JSON parsing and structured schemas to prevent data corruption.", "• ")
    add_bullet_p(doc, "Cross-Platform Responsiveness: The interface must seamlessly adapt to mobile screens (320px+), tablets (768px+), and desktops (1024px+) using CSS Flexbox and Grid.", "• ")

    add_heading_2(doc, "3.3 Hardware Requirements")
    add_body_p(doc, "Because the system operates entirely within the client's web browser, its hardware prerequisites are modest:")
    
    # Table 3.1
    t31 = doc.add_table(rows=5, cols=3)
    t31.alignment = WD_TABLE_ALIGNMENT.CENTER
    t31.autofit = False
    t31.columns[0].width = Inches(1.8)
    t31.columns[1].width = Inches(2.4)
    t31.columns[2].width = Inches(2.4)

    t31_headers = ["Hardware Component", "Minimum Specification", "Recommended Specification"]
    for j, htext in enumerate(t31_headers):
        cell = t31.cell(0, j)
        set_cell_background(cell, "0077ED")
        p = cell.paragraphs[0]
        r = p.add_run(htext)
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t31_rows = [
        ("Processor", "Dual-Core 1.6 GHz Intel/AMD", "Intel Core i3 / i5 2.0 GHz+ or Apple M-series"),
        ("System Memory (RAM)", "2 GB DDR3", "4 GB to 8 GB DDR4+"),
        ("Storage Drive Space", "200 MB free disk space", "500 MB+ SSD storage"),
        ("Display Resolution", "1024 x 768 pixels", "1920 x 1080 Full HD or higher")
    ]
    for i, row in enumerate(t31_rows):
        cells = t31.rows[i+1].cells
        if i % 2 == 1:
            for c in cells: set_cell_background(c, "F8FAFC")
        for j, val in enumerate(row):
            cells[j].paragraphs[0].text = val
            cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
            if j == 0: cells[j].paragraphs[0].runs[0].font.bold = True

    add_body_p(doc, "Table 3.1: Client & Demonstration Hardware Requirements Specification", bold_prefix="")

    add_heading_2(doc, "3.4 Software Requirements")
    add_body_p(doc, "The platform is fully standards-compliant and executes on all modern operating systems:")
    
    # Table 3.2
    t32 = doc.add_table(rows=5, cols=3)
    t32.alignment = WD_TABLE_ALIGNMENT.CENTER
    t32.autofit = False
    t32.columns[0].width = Inches(1.8)
    t32.columns[1].width = Inches(2.4)
    t32.columns[2].width = Inches(2.4)

    for j, htext in enumerate(["Software Component", "Supported Platforms", "Recommended Environment"]):
        cell = t32.cell(0, j)
        set_cell_background(cell, "E52B50")
        p = cell.paragraphs[0]
        r = p.add_run(htext)
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t32_rows = [
        ("Operating System", "Windows 10/11, macOS, Linux, Android, iOS", "Windows 11 / macOS Sonoma / Ubuntu 22.04"),
        ("Web Browser", "Chrome 90+, Edge 90+, Firefox 88+, Safari 14+", "Google Chrome or Microsoft Edge (Latest)"),
        ("Code Editor / IDE", "Any text editor (Notepad, Sublime Text)", "Visual Studio Code (v1.85+)"),
        ("Local Web Server", "Direct file:// or HTTP Server", "Built-in Node server.js or VS Code Live Server")
    ]
    for i, row in enumerate(t32_rows):
        cells = t32.rows[i+1].cells
        if i % 2 == 1:
            for c in cells: set_cell_background(c, "F8FAFC")
        for j, val in enumerate(row):
            cells[j].paragraphs[0].text = val
            cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
            if j == 0: cells[j].paragraphs[0].runs[0].font.bold = True

    add_body_p(doc, "Table 3.2: Operating Environment & Browser Software Requirements", bold_prefix="")

    add_heading_2(doc, "3.5 Feasibility Study")
    add_body_p(doc, "A feasibility evaluation assesses the viability of the project across three dimensions:")
    add_bullet_p(doc, "Technical Feasibility: The project relies strictly on standardized, universally supported web technologies (HTML5/CSS3/ES6). No proprietary runtime, commercial license, or specialized hardware is mandated. The technical risk is negligible.", "1. ")
    add_bullet_p(doc, "Economic Feasibility: Because the system leverages open-source development tools and operates serverless using client browser storage, infrastructure costs are zero. Development requires only standard personal computing equipment.", "2. ")
    add_bullet_p(doc, "Operational Feasibility: The user interface is intentionally structured to match widely accepted Indian booking conventions (MakeMyTrip, RedBus). Both passengers and administrators can navigate the system intuitively with zero specialized training.", "3. ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: TECHNOLOGIES USED
    # =========================================================================
    add_heading_1(doc, "CHAPTER 4: TECHNOLOGIES USED")

    add_heading_2(doc, "4.1 HTML5")
    add_body_p(doc, "HTML5 (Hypertext Markup Language 5) provides the core structural backbone of the entire web application. Key features utilized include:")
    add_bullet_p(doc, "Semantic Layout Tags: Extensive use of <header>, <nav>, <main>, <section>, <article>, <aside>, and <footer> ensures clean document hierarchy and improved accessibility.", "• ")
    add_bullet_p(doc, "Interactive Input Controls: Native <input type=\"date\"> with dynamic minimum constraints prevents booking dates in the past, while <datalist> enables seamless autocomplete for major Indian cities.", "• ")
    add_bullet_p(doc, "Vector Graphics & Canvas: HTML5 <svg> elements render custom responsive QR codes, passenger icons, and steering wheels, while the HTML5 <canvas> API dynamically renders administrative revenue bar charts.", "• ")

    add_heading_2(doc, "4.2 CSS3")
    add_body_p(doc, "CSS3 (Cascading Style Sheets 3) delivers a state-of-the-art visual presentation layer without relying on external CSS frameworks like Bootstrap or Tailwind CSS:")
    add_bullet_p(doc, "CSS Custom Properties (Variables): Defined at the :root pseudo-class, variables govern color palettes (--primary, --secondary, --dark), radii (--radius-md), and transitions for consistent theming across all 17 HTML files.", "• ")
    add_bullet_p(doc, "CSS Grid & Flexbox: Complex responsive layouts—such as the hero search grid, the 2+2 and 2+1 bus chassis seat layout, and the admin dashboard—are constructed using modern Grid and Flexbox modules.", "• ")
    add_bullet_p(doc, "Glassmorphism & Shadows: Header navigation bars feature backdrop-filter: blur(16px) with translucent background colors for an elevated, polished modern finish.", "• ")
    add_bullet_p(doc, "Print Media Styling: Dedicated @media print directives format the e-ticket for clean A4 printing, suppressing web chrome, navigation bars, and buttons while preserving high-contrast text.", "• ")

    add_heading_2(doc, "4.3 JavaScript (ES6+)")
    add_body_p(doc, "Vanilla JavaScript provides all client-side logic, data manipulation, validation, and dynamic UI rendering:")
    add_bullet_p(doc, "Modular Separation of Concerns: Application logic is organized into distinct files (data.js, storage.js, auth.js, search.js, seats.js, booking.js, ticket.js, admin.js) rather than a monolithic script.", "• ")
    add_bullet_p(doc, "DOM Manipulation & Event Listeners: Dynamic rendering of search results, seat toggling, coupon code validation, and modal transitions occur via lightweight DOM operations.", "• ")
    add_bullet_p(doc, "Asynchronous Simulation: Web animations such as simulated payment processing spinners and city swapping rotation utilize setTimeout and requestAnimationFrame to emulate production gateway flows.", "• ")

    add_heading_2(doc, "4.4 LocalStorage API")
    add_body_p(doc, "The HTML5 LocalStorage interface serves as the primary data storage tier. It provides synchronous, persistent key-value storage within the client's web browser, maintaining data across browser sessions and reloads without network communication.")
    add_body_p(doc, "Key implementation characteristics include:")
    add_bullet_p(doc, "Structured JSON Serialization: Complex data entities (Users, Bookings, Transports, Payments) are serialized into JSON strings upon write and deserialized into native JavaScript objects upon read.", "• ")
    add_bullet_p(doc, "Automated Seeding: On first visit, the storage manager checks for existing keys and auto-seeds realistic Indian routes, bus fleets, express trains, and admin credentials.", "• ")
    add_bullet_p(doc, "Transactional Seat Quotas: Seat availability is calculated dynamically by filtering active (non-cancelled) bookings for a specific transport ID and journey date, ensuring strict real-time accuracy.", "• ")

    add_heading_2(doc, "4.5 Development & Testing Tools")
    add_bullet_p(doc, "Visual Studio Code: Source code authoring, syntax highlighting, and project navigation.", "• ")
    add_bullet_p(doc, "Node.js (v20+): Executing headless unit tests and hosting the lightweight built-in server.js.", "• ")
    add_bullet_p(doc, "Microsoft Edge / Google Chrome Developer Tools: Live DOM inspection, CSS debugging, responsive device emulation, and LocalStorage inspection.", "• ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: SYSTEM DESIGN
    # =========================================================================
    add_heading_1(doc, "CHAPTER 5: SYSTEM DESIGN")

    add_heading_2(doc, "5.1 System Architecture")
    add_body_p(doc, "The Travel Ticket Booking System is structured around an elegant Three-Tier Client-Side Architecture. Unlike traditional server-heavy applications, all three tiers reside natively within the browser environment:")
    add_bullet_p(doc, "1. Presentation Tier: Comprises the HTML5 and CSS3 views rendered by the browser engine. It captures user interactions (city searches, seat clicks, button presses) and displays formatted data.", "• ")
    add_bullet_p(doc, "2. Business Logic Tier: Managed by dedicated Vanilla JavaScript controllers. It validates form entries, filters routes, enforces seat limits (max 6 seats), executes coupon discounts, and manages authentication sessions.", "• ")
    add_bullet_p(doc, "3. Data Storage Tier: Governed by the Storage manager (storage.js) communicating directly with the browser's LocalStorage API for CRUD operations and seat tracking.", "• ")

    add_figure_image(doc, "diagrams/fig_architecture.png", "Figure 5.1: Three-Tier Client-Side System Architecture Diagram")

    add_heading_2(doc, "5.2 Data Flow Diagram (DFD)")
    add_body_p(doc, "Data Flow Diagrams illustrate the trajectory of data into, through, and out of the application.")
    add_heading_3(doc, "Level 0 DFD (Context Level Diagram)")
    add_body_p(doc, "The Level 0 DFD portrays the macro interaction between external entities (Passenger and Administrator) and the central Travel Ticket Booking System process. Passengers transmit search criteria and receive itineraries and tickets, while administrators submit transport updates and receive analytical reports.")

    add_figure_image(doc, "diagrams/fig_dfd_lvl0.png", "Figure 5.2: Data Flow Diagram (Level 0 - Context Level Diagram)")

    add_heading_3(doc, "Level 1 DFD (Functional Decomposition Diagram)")
    add_body_p(doc, "The Level 1 DFD decomposes the system into six interconnected sub-processes: Authentication, Search, Seat Allocation, Simulated Payment, Ticket Generation, and Admin Fleet Control, all reading and writing to the central LocalStorage repository.")

    add_figure_image(doc, "diagrams/fig_dfd_lvl1.png", "Figure 5.3: Data Flow Diagram (Level 1 - Functional Decomposition)")

    add_heading_2(doc, "5.3 Use Case Diagram")
    add_body_p(doc, "Use Case Diagrams define the behavioral boundaries and operational responsibilities of the system's human actors.")
    add_heading_3(doc, "User Use Case Model")
    add_body_p(doc, "The Passenger actor interacts with seven core use cases: Register Account, Login, Search Schedules, Select Visual Seats, Apply Coupons, Simulate Payment, and View/Cancel Bookings.")

    add_figure_image(doc, "diagrams/fig_usecase_user.png", "Figure 5.4: User Scope UML Use Case Diagram")

    add_heading_3(doc, "Admin Use Case Model")
    add_body_p(doc, "The System Administrator actor commands specialized operational use cases: Admin Login, Dashboard KPI Monitoring, Fleet Transport CRUD, Booking Cancellation Management, Payment Ledger Review, and CSV Report Export.")

    add_figure_image(doc, "diagrams/fig_usecase_admin.png", "Figure 5.5: Admin Management Scope UML Use Case Diagram")

    add_heading_2(doc, "5.4 Flowchart (End-to-End Booking Process)")
    add_body_p(doc, "The process flowchart depicts the end-to-end lifecycle of a ticket reservation, including the critical decision checkpoint requiring user authentication before entering the checkout stage.")

    add_figure_image(doc, "diagrams/fig_flowchart.png", "Figure 5.6: End-to-End Booking and Ticket Issuance Flowchart")

    add_heading_2(doc, "5.5 Database / Data Storage Design")
    add_body_p(doc, "Rather than deploying a heavyweight relational SQL server, the system manages data through structured key-value entities within browser LocalStorage. Each entity adheres to a strict schema design outlined in Table 5.2.")

    # Table 5.2
    t52 = doc.add_table(rows=7, cols=3)
    t52.alignment = WD_TABLE_ALIGNMENT.CENTER
    t52.autofit = False
    t52.columns[0].width = Inches(1.8)
    t52.columns[1].width = Inches(3.2)
    t52.columns[2].width = Inches(1.6)

    for j, htext in enumerate(["Storage Key", "Schema Fields / Attributes", "Purpose / Context"]):
        cell = t52.cell(0, j)
        set_cell_background(cell, "0F172A")
        p = cell.paragraphs[0]
        r = p.add_run(htext)
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t52_rows = [
        ("tb_users", "id, name, email, phone, password, createdAt", "Registered passenger credentials"),
        ("tb_transports", "id, name, type, category, source, destination, departureTime, arrivalTime, duration, price, totalSeats, rating, amenities", "Bus and train fleet inventory"),
        ("tb_bookings", "id, userId, userName, userEmail, userPhone, transportId, transportName, transportType, source, destination, journeyDate, seats[], passengers[], totalFare, tax, discount, finalAmount, paymentMethod, paymentStatus, bookingStatus, bookedAt", "Master reservation records"),
        ("tb_payments", "transactionId, bookingId, userId, userName, amount, method, status, date", "Payment transaction logs"),
        ("tb_reviews", "name, city, route, rating, comment, date", "Passenger customer testimonials"),
        ("tb_feedback", "name, email, subject, message, date", "Help & support queries")
    ]
    for i, row in enumerate(t52_rows):
        cells = t52.rows[i+1].cells
        if i % 2 == 1:
            for c in cells: set_cell_background(c, "F8FAFC")
        for j, val in enumerate(row):
            cells[j].paragraphs[0].text = val
            cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
            if j == 0: cells[j].paragraphs[0].runs[0].font.bold = True

    add_body_p(doc, "Table 5.2: LocalStorage Key-Value Entity Schema & Structural Design", bold_prefix="")

    add_heading_2(doc, "5.6 Module Description")
    add_body_p(doc, "The software is partitioned into four modular functional areas summarized in Table 5.1:")

    # Table 5.1
    t51 = doc.add_table(rows=5, cols=3)
    t51.alignment = WD_TABLE_ALIGNMENT.CENTER
    t51.autofit = False
    t51.columns[0].width = Inches(1.8)
    t51.columns[1].width = Inches(3.0)
    t51.columns[2].width = Inches(1.8)

    for j, htext in enumerate(["Module Name", "Functional Scope & Responsibilities", "Associated Files"]):
        cell = t51.cell(0, j)
        set_cell_background(cell, "0077ED")
        p = cell.paragraphs[0]
        r = p.add_run(htext)
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t51_rows = [
        ("User Auth Module", "User registration, password hashing check, session persistence, forgot password simulator.", "login.html, register.html, auth.js"),
        ("Search & Discovery", "Schedule queries, price sliders, time-of-day filters, sorting algorithms, amenities chips.", "index.html, search.html, search.js"),
        ("Seat & Booking Engine", "Visual seat layout, dynamic seat lock, passenger forms, promo discounts, simulated gateway.", "seat-selection.html, booking.html, ticket.html, seats.js, booking.js"),
        ("Admin Portal", "KPI dashboard, Canvas charts, fleet transport CRUD, booking cancellation, CSV report export.", "admin/*, admin.js, admin.css")
    ]
    for i, row in enumerate(t51_rows):
        cells = t51.rows[i+1].cells
        if i % 2 == 1:
            for c in cells: set_cell_background(c, "F8FAFC")
        for j, val in enumerate(row):
            cells[j].paragraphs[0].text = val
            cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
            if j == 0: cells[j].paragraphs[0].runs[0].font.bold = True

    add_body_p(doc, "Table 5.1: Functional Modules Description & Implementation Mapping", bold_prefix="")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: IMPLEMENTATION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 6: IMPLEMENTATION")

    add_heading_2(doc, "6.1 Home Page & Hero Search Interface")
    add_body_p(doc, "The Home Page (index.html) serves as the primary visual entrance. It features a sticky navigation bar with glassmorphism styling, user profile avatar badges, and a mobile hamburger drawer. The flagship component is the Hero Search Widget, offering:")
    add_bullet_p(doc, "Transport Toggle Tabs: Instant switching between Bus Booking and Train Booking modes.", "• ")
    add_bullet_p(doc, "City Autocomplete & Swapper: An interactive city swapper button (⇄) rotates 180 degrees and inverts source and destination inputs instantly.", "• ")
    add_bullet_p(doc, "Date Constraints: Automated setting of today's date as minimum selectable date via JavaScript.", "• ")

    add_heading_2(doc, "6.2 User Registration and Login Modules")
    add_body_p(doc, "User security is handled via register.html and login.html. The registration controller validates full name length (>= 3 chars), valid email regex patterns, exact 10-digit numeric phone numbers, and matching password strings. The login controller verifies credentials against tb_users in LocalStorage and sets an active session. If a user is redirected from the seat selection page, the system stores the target redirect URL and forwards them directly back to checkout post-authentication.")

    add_heading_2(doc, "6.3 Ticket Search & Multi-Facet Filtering Engine")
    add_body_p(doc, "The search engine (search.html / search.js) parses query parameters from the URL string. Results are filtered by matching source and destination cities, vehicle types, price range slider values, and departure time bands (Morning 06:00-12:00, Afternoon 12:00-18:00, Evening 18:00-23:00, Night 23:00-06:00). Sorting algorithms dynamically re-order results by fare, rating, or departure hour.")

    add_heading_2(doc, "6.4 Bus and Train Details & Amenities Representation")
    add_body_p(doc, "Each transport result card highlights comprehensive travel metrics: operator name, luxury category (e.g. Volvo Multi-Axle AC Sleeper), user ratings, boarding terminal, dropping terminal, journey duration timeline with visual directional arrows, starting fare, and remaining seat quota badges.")

    add_heading_2(doc, "6.5 Interactive Visual Seat Selection")
    add_body_p(doc, "The seat selection interface (seat-selection.html / seats.js) renders a realistic vehicle chassis with driver cabin and steering wheel. It calculates currently booked seats for that transport and journey date by querying Storage.getBookedSeats(id, date). Booked seats are greyed out and unclickable. Clicking available green seats turns them blue, adds them to the selection array (capped at 6), and updates the floating fare summary bar in real time.")

    add_heading_2(doc, "6.6 Passenger Details Collection")
    add_body_p(doc, "On booking.html, the system dynamically iterates over the chosen seats and generates an individualized passenger input card for each seat (collecting Full Name, Age, and Gender). Primary contact details (Email and Phone) are pre-filled if the user is authenticated.")

    add_heading_2(doc, "6.7 Booking & Simulated Payment Gateway Integration")
    add_body_p(doc, "The payment engine supports simulated UPI QR scanning, Credit/Debit card entries, and pay-at-boarding cash options. Upon form submission, an animated modal dialog with a rotating CSS spinner simulates bank gateway processing for 1.8 seconds before confirming success, generating a unique booking reference (TRV-XXXXXX), and logging transaction records in tb_payments.")

    add_heading_2(doc, "6.8 Booking History & Cancellation Seat Restoration")
    add_body_p(doc, "In my-bookings.html, travelers review their active and completed trips. Confirmed tickets display an active 'Cancel Ticket' trigger. Clicking cancel activates a modal confirmation dialog; once confirmed, the booking status updates to 'Cancelled' and the occupied seats are immediately freed back into the date pool.")

    add_heading_2(doc, "6.9 Boarding Pass E-Ticket Generation & QR Visuals")
    add_body_p(doc, "The ticket view (ticket.html) renders an airline-style boarding pass featuring perforated tear edges, passenger manifest tables, route timelines, and custom vector QR codes. A 1-click 'Print Ticket' button executes window.print() under dedicated print media rules.")

    add_heading_2(doc, "6.10 Admin Dashboard, Analytics & CSV Export")
    add_body_p(doc, "The admin suite (admin/dashboard.html) provides dynamic KPI cards, HTML5 Canvas revenue graphs, transport fleet CRUD forms, and automated CSV report generation that downloads directly as an Excel-compatible spreadsheet.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: TESTING
    # =========================================================================
    add_heading_1(doc, "CHAPTER 7: TESTING")

    add_heading_2(doc, "7.1 Testing Introduction & Methodologies")
    add_body_p(doc, "Software testing is a rigorous verification discipline performed to confirm that the developed software satisfies specified requirements, handles boundary conditions gracefully, and prevents data anomalies. The Travel Ticket Booking System was subjected to extensive functional testing, boundary validation, and end-to-end integration workflows using both headless automated Node.js test harnesses and interactive browser testing.")

    add_heading_2(doc, "7.2 Functional Testing")
    add_body_p(doc, "Functional tests verified each feature against expected outcomes: account creation, credential matching, search query filtration, seat locking, promotional coupon deduction, and boarding pass rendering.")

    add_heading_2(doc, "7.3 Validation Testing")
    add_body_p(doc, "Input validation testing evaluated the application's response to invalid inputs:")
    add_bullet_p(doc, "Submitting empty passenger names or non-numeric age values triggers visual error cues and halts submission.", "• ")
    add_bullet_p(doc, "Entering phone numbers with fewer or more than 10 digits prevents account registration.", "• ")
    add_bullet_p(doc, "Attempting to select more than 6 seats produces an animated toast notification enforcing the limit.", "• ")

    add_heading_2(doc, "7.4 Comprehensive Test Cases & Matrix")
    add_body_p(doc, "Table 7.1 details ten verified test cases spanning both user and admin modules:")

    # Table 7.1
    t71 = doc.add_table(rows=11, cols=5)
    t71.alignment = WD_TABLE_ALIGNMENT.CENTER
    t71.autofit = False
    t71.columns[0].width = Inches(0.8)
    t71.columns[1].width = Inches(1.5)
    t71.columns[2].width = Inches(1.8)
    t71.columns[3].width = Inches(1.9)
    t71.columns[4].width = Inches(0.8)

    for j, htext in enumerate(["Test ID", "Scenario Description", "Test Input Data", "Expected Output", "Status"]):
        cell = t71.cell(0, j)
        set_cell_background(cell, "0077ED")
        p = cell.paragraphs[0]
        r = p.add_run(htext)
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t71_rows = [
        ("TC-01", "User Registration Validation", "Name: 'Al', Phone: '123'", "Halt with error: Name >= 3 chars, Phone = 10 digits", "PASS"),
        ("TC-02", "Valid Registration & Session", "Name: 'Kavita', Phone: '9876501234'", "Create user in tb_users, set active session", "PASS"),
        ("TC-03", "Search Schedule Filtering", "Source: 'Delhi', Dest: 'Shimla'", "Display only matching Delhi-Shimla bus/train cards", "PASS"),
        ("TC-04", "Visual Seat Selection", "Click available seat L1A", "Seat turns blue, chips update, fare increments", "PASS"),
        ("TC-05", "Max Seat Selection Cap", "Attempt selecting 7th seat", "Toast warning displayed, 7th seat rejected", "PASS"),
        ("TC-06", "Login Gate on Checkout", "Guest clicks 'Continue to Booking'", "Prevent checkout, redirect to login.html?redirect=...", "PASS"),
        ("TC-07", "Coupon Code Application", "Code: 'TRAVEL50'", "Apply 10% discount to base fare immediately", "PASS"),
        ("TC-08", "Simulated Payment & Pass", "Submit valid UPI demo payment", "Display spinner, generate TRV-XXXXXX e-ticket", "PASS"),
        ("TC-09", "Ticket Cancellation & Seats", "Cancel booking TRV-894120", "Status -> Cancelled, occupied seats restored in pool", "PASS"),
        ("TC-10", "Admin Fleet Transport CRUD", "Add bus 'Himachal Super Express'", "Persist in tb_transports, appear in search results", "PASS")
    ]

    for i, row in enumerate(t71_rows):
        cells = t71.rows[i+1].cells
        if i % 2 == 1:
            for c in cells: set_cell_background(c, "F8FAFC")
        for j, val in enumerate(row):
            cells[j].paragraphs[0].text = val
            cells[j].paragraphs[0].runs[0].font.size = Pt(9)
            if j == 0: cells[j].paragraphs[0].runs[0].font.bold = True
            if j == 4:
                cells[j].paragraphs[0].runs[0].font.bold = True
                cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(5, 150, 105)

    add_body_p(doc, "Table 7.1: System Test Cases, Validation Scenarios & Verification Matrix", bold_prefix="")

    add_heading_2(doc, "7.5 Testing Results & Verification Summary")
    add_body_p(doc, "All 10 test scenarios achieved a 100% pass rate. Automated execution verified that LocalStorage accurately maintained data across reloads, seat quotas recalculated instantaneously upon cancellation, and the admin analytics suite matched actual booking totals.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: RESULTS AND SCREENSHOTS
    # =========================================================================
    add_heading_1(doc, "CHAPTER 8: RESULTS AND SCREENSHOTS")
    add_body_p(doc, "This chapter documents the verified visual output of the Travel Ticket Booking System captured directly from the live running application interface.")

    add_heading_2(doc, "8.1 Home Page Interface")
    add_body_p(doc, "The Home Page presents the flagship hero search card with bus and train selection tabs, city autocomplete datalists, popular travel route highlights, and customer reviews.")
    add_figure_image(doc, "diagrams/screen_home.png", "Figure 8.1: Home Page & Search Interface")

    add_heading_2(doc, "8.2 User Authentication & Registration")
    add_body_p(doc, "The login and registration interfaces feature a split-screen design with travel perk banners, floating input validation indicators, and quick-fill test credentials.")
    add_figure_image(doc, "diagrams/screen_login.png", "Figure 8.2: User Authentication & Sign-In Interface")
    add_figure_image(doc, "diagrams/screen_register.png", "Figure 8.3: User Registration & Form Validation Interface")

    add_heading_2(doc, "8.3 Ticket Search Results & Filter Sidebar")
    add_body_p(doc, "The search results screen displays dynamic transport cards alongside an interactive filter sidebar with price sliders and time-slot buttons.")
    add_figure_image(doc, "diagrams/screen_search.png", "Figure 8.4: Live Ticket Search Results & Multi-Facet Filter Sidebar")

    add_heading_2(doc, "8.4 Interactive Visual Seat Selection")
    add_body_p(doc, "The visual seat selection canvas displays a 2+2 / 2+1 chassis with driver cabin, color-coded availability cues, seat chips, and a sticky fare summary.")
    add_figure_image(doc, "diagrams/screen_seats.png", "Figure 8.5: Interactive Visual Seat Layout & Real-Time Fare Calculator")

    add_heading_2(doc, "8.5 Passenger Details Collection & Simulated Checkout")
    add_body_p(doc, "The checkout interface captures traveler demographic details, displays order summary with base fare, applicable GST, dynamic promo code discounts, and simulates instant digital payment confirmation.")
    add_figure_image(doc, "diagrams/screen_checkout.png", "Figure 8.6: Passenger Details Collection & Simulated Checkout Interface")

    add_heading_2(doc, "8.6 Passenger Booking History & Cancellation Management")
    add_body_p(doc, "The passenger booking history page allows travelers to review confirmed reservations, trigger 1-click cancellations with seat recycling, and view tickets.")
    add_figure_image(doc, "diagrams/screen_mybookings.png", "Figure 8.7: Passenger Booking History & Cancellation Management Interface")

    add_heading_2(doc, "8.7 Official Boarding Pass E-Ticket")
    add_body_p(doc, "The generated electronic boarding pass showcases realistic perforated tear notches, passenger manifest details, and a high-contrast vector QR code.")
    add_figure_image(doc, "diagrams/screen_ticket.png", "Figure 8.8: Official Boarding Pass E-Ticket with QR Code Verification")

    add_heading_2(doc, "8.8 Admin Analytics Dashboard & Fleet Management")
    add_body_p(doc, "The admin console features real-time KPI metric cards, HTML5 Canvas revenue trend bars, transport fleet management tools, and CSV report export.")
    add_figure_image(doc, "diagrams/screen_admin.png", "Figure 8.9: Admin Analytics Dashboard & Fleet Management Console")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 9: CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    add_heading_1(doc, "CHAPTER 9: CONCLUSION AND FUTURE SCOPE")

    add_heading_2(doc, "9.1 Conclusion")
    add_body_p(doc, "The Travel Ticket Booking System successfully demonstrates the design and implementation of a professional, modern, and responsive online ticketing platform using pure client-side web technologies (HTML5, CSS3, Vanilla JavaScript, and LocalStorage). The application resolves the core friction points of traditional passenger booking by delivering 24/7 self-service scheduling, visual seat selection, instant simulated payment checkouts, automated e-ticket issuance, and dynamic seat restoration upon cancellation.")
    add_body_p(doc, "By eliminating reliance on heavy frameworks or external backend dependencies, the system delivers instantaneous page response times, exceptional accessibility, and zero-cost hosting feasibility, making it an exemplary model for college mini-project demonstration and practical software engineering education.")

    add_heading_2(doc, "9.2 Limitations")
    add_body_p(doc, "While fully functional for demonstration and evaluation, the current standalone architecture presents certain inherent boundaries:")
    add_bullet_p(doc, "Client-Side Isolation: Data stored in LocalStorage is confined to the specific browser and machine in use; bookings made on one computer do not synchronize automatically across other devices without a network backend.", "• ")
    add_bullet_p(doc, "Absence of Distributed Concurrency Locks: Real-time simultaneous seat contention between multiple remote users requires a server-side WebSocket or transactional locking mechanism.", "• ")
    add_bullet_p(doc, "Simulated Financial Gateway: Financial transactions are simulated for demonstration purposes and are not linked to actual commercial banking institutions.", "• ")

    add_heading_2(doc, "9.3 Future Enhancements")
    add_body_p(doc, "Planned future enhancements to evolve the prototype into a commercial enterprise product include:")
    add_bullet_p(doc, "Node.js / Express Backend & RESTful APIs: Transitioning business logic to a secure Node.js server with JWT authentication and SSL encryption.", "1. ")
    add_bullet_p(doc, "Relational Database Integration (MySQL / PostgreSQL): Storing millions of passenger records, audit trails, and multi-tenant operator catalogs in an ACID-compliant database.", "2. ")
    add_bullet_p(doc, "Live Commercial Payment Gateways: Integrating certified payment SDKs (e.g., Razorpay, PayU, Stripe) supporting real-time UPI intents, net banking, and international cards.", "3. ")
    add_bullet_p(doc, "GPS Live Bus & Train Tracking: Incorporating GPS IoT sensors and Leaflet/Mapbox maps to provide passengers with live vehicle arrival tracking.", "4. ")
    add_bullet_p(doc, "Automated SMS and WhatsApp Notifications: Integrating communication gateways (Twilio/Gupshup) to transmit booking confirmations and PDF tickets directly to mobile phones.", "5. ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 10: REFERENCES
    # =========================================================================
    add_heading_1(doc, "CHAPTER 10: REFERENCES")

    add_heading_2(doc, "10.1 Books and Study Materials")
    add_bullet_p(doc, "Flanagan, David. JavaScript: The Definitive Guide (7th Edition). O'Reilly Media, 2020.", "[1] ")
    add_bullet_p(doc, "Robbins, Jennifer. Learning Web Design: A Beginner's Guide to HTML, CSS, JavaScript, and Web Graphics (5th Edition). O'Reilly Media, 2018.", "[2] ")
    add_bullet_p(doc, "Duckett, Jon. HTML and CSS: Design and Build Websites. John Wiley & Sons, 2011.", "[3] ")
    add_bullet_p(doc, "Duckett, Jon. JavaScript and JQuery: Interactive Front-End Web Development. John Wiley & Sons, 2014.", "[4] ")
    add_bullet_p(doc, "Pressman, Roger S. Software Engineering: A Practitioner's Approach (8th Edition). McGraw-Hill Education, 2014.", "[5] ")

    add_heading_2(doc, "10.2 Websites and Online Documentation")
    add_bullet_p(doc, "MDN Web Docs: Web Storage API (localStorage) — https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API", "[6] ")
    add_bullet_p(doc, "MDN Web Docs: CSS Grid Layout — https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout", "[7] ")
    add_bullet_p(doc, "W3Schools Online Web Tutorials: JavaScript DOM Methods — https://www.w3schools.com/js/", "[8] ")
    add_bullet_p(doc, "RedBus Online Ticket Booking Interface Guidelines — https://www.redbus.in", "[9] ")
    add_bullet_p(doc, "MakeMyTrip Bus & Train Travel System Architecture — https://www.makemytrip.com", "[10] ")

    # =========================================================================
    # SAVE FILE
    # =========================================================================
    local_filename = "Travel_Ticket_Booking_System_Project_Report.docx"
    doc.save(local_filename)
    print(f"[OK] Generated report in workspace: {local_filename}")

    desktop_names = [local_filename, "Travel_Ticket_Booking_System_Project_Report_Shivani.docx"]
    desktop_dirs = [
        os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop"),
        os.path.join(os.path.expanduser("~"), "Desktop"),
        r"C:\Users\vijay\OneDrive\Desktop"
    ]
    for dname in desktop_names:
        for ddir in desktop_dirs:
            if os.path.exists(ddir):
                target_path = os.path.join(ddir, dname)
                try:
                    shutil.copyfile(local_filename, target_path)
                    print(f"[OK] Saved copy directly to Desktop: {target_path}")
                    break
                except Exception as e:
                    pass

if __name__ == "__main__":
    create_full_report()
