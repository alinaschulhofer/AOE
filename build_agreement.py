"""
Build Psychotherapist-Patient Services Agreement PDF (template).
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black
import os

W, H = letter
DARK = HexColor("#1a1a1a")
MID  = HexColor("#555555")

FOOTER_TEXT = "Dr. Alina Schulhofer  Licensed Psychologist #PY12365,  Licensed Psychologist #027009  (786) 671-4945"

def on_every_page(canvas, doc):
    canvas.saveState()
    margin = 54
    canvas.setStrokeColor(HexColor("#999999"))
    canvas.setLineWidth(0.4)
    canvas.line(margin, 38, W - margin, 38)
    canvas.setFillColor(MID)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(W / 2, 26, FOOTER_TEXT + f"    Page {doc.page} of 5")
    canvas.restoreState()

def build():
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "assets", "services-agreement-template.pdf")

    margin = 54
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=margin, rightMargin=margin,
        topMargin=54, bottomMargin=52,
    )

    header_name = ParagraphStyle("hn", fontName="Helvetica", fontSize=11,
                                 textColor=DARK, spaceAfter=1)
    header_title = ParagraphStyle("ht", fontName="Helvetica", fontSize=11,
                                  textColor=DARK, spaceAfter=20)
    doc_title = ParagraphStyle("dt", fontName="Helvetica-Bold", fontSize=11,
                               textColor=DARK, spaceAfter=12, alignment=TA_LEFT)
    body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=15,
                          textColor=DARK, spaceAfter=10, alignment=TA_JUSTIFY)
    section = ParagraphStyle("sec", fontName="Helvetica-Bold", fontSize=10,
                             textColor=DARK, spaceBefore=10, spaceAfter=6)
    bullet = ParagraphStyle("bul", fontName="Helvetica", fontSize=10, leading=15,
                            textColor=DARK, spaceAfter=8, leftIndent=18,
                            alignment=TA_JUSTIFY)
    bold_body = ParagraphStyle("bb", fontName="Helvetica-Bold", fontSize=10, leading=15,
                               textColor=DARK, spaceAfter=10, alignment=TA_JUSTIFY)
    sig_label = ParagraphStyle("sl", fontName="Helvetica-Bold", fontSize=10,
                               textColor=DARK, spaceBefore=16, spaceAfter=4)
    sig_line  = ParagraphStyle("sln", fontName="Helvetica", fontSize=10,
                               textColor=DARK, spaceAfter=2)
    closing_caps = ParagraphStyle("cc", fontName="Helvetica-Bold", fontSize=10,
                                  leading=15, textColor=DARK, spaceAfter=14,
                                  alignment=TA_JUSTIFY)

    e = []

    e.append(Paragraph("Dr. Alina Schulhofer, PsyD", header_name))
    e.append(Paragraph("Licensed Psychologist (FL #PY12365, NY #027009)", header_title))
    e.append(Paragraph("PSYCHOTHERAPIST-PATIENT SERVICES AGREEMENT", doc_title))

    e.append(Paragraph(
        "This document (the Agreement) contains important information about my professional "
        "services and business policies. It also contains summary information about the Health "
        "Insurance Portability and Accountability Act (HIPAA), a federal law that provides privacy "
        "protections and patient rights with regard to the use and disclosure of your Protected "
        "Health Information (PHI) used for the purpose of treatment, payment, and health care "
        "operations. HIPAA requires that I provide you with a Notice of Privacy Practices (the Notice) "
        "for use and disclosure of PHI for treatment, payment and health care operations. The "
        "Notice, which is attached to this Agreement, explains HIPAA and its application to your "
        "personal health information in greater detail. The law requires that I obtain your signature "
        "acknowledging that I have provided you with this information. Although these documents "
        "are long and sometimes complex, it is very important that you read them carefully before "
        "our next session. We can discuss any questions you have about the procedures at that time. "
        "When you sign this document, it will also represent an agreement between us. You may "
        "revoke this Agreement in writing at any time.", body))

    e.append(Paragraph("PSYCHOLOGICAL SERVICES", section))
    e.append(Paragraph(
        "I am a licensed psychologist in the states of Florida (PY12365) and New York (027009). My "
        "approach to treatment is psychoanalytically informed, which is a type of psychotherapy that "
        "fosters personal development and liberation from unsatisfying or painful patterns of living. "
        "Patient and therapist work together to understand the meaning of the patient’s emotional "
        "reactions, thoughts, memories, fantasies, and dreams in an effort to alleviate suffering and "
        "to expand the capacity for various personal and professional pursuits. Since therapy often "
        "involves discussing unpleasant aspects of your life, you may experience uncomfortable "
        "feelings like sadness, guilt, anger, frustration, loneliness, and helplessness. On the other "
        "hand, psychotherapy often leads to better relationships, solutions to specific problems, and "
        "significant reductions in feelings of distress. Our first few sessions will involve an evaluation "
        "of you and your needs. Therapy involves a large commitment of time, money, and energy, "
        "so you should be very careful about the therapist you select. If you have questions about my "
        "procedures, we should discuss them whenever they arise. If doubts persist, I will be happy "
        "to help you set up a meeting with another mental health professional for a second opinion.", body))

    e.append(Paragraph("SESSIONS", section))
    e.append(Paragraph(
        "During our initial sessions, we can both decide if I am the best person to provide the "
        "services that you need in order to meet your goals. My therapy sessions are 50 minutes long "
        "and are scheduled at a frequency of one to three times per week. Extended sessions may be "
        "possible at request at an additional fee (to be discussed prior to scheduling individually). "
        "Session length and frequency will be determine collaboratively based on your particular "
        "needs. We will meet on the same days, at the same times, each week. Once our times are "
        "scheduled, you will be expected to pay for all sessions unless you provide 24 hours advance "
        "notice of cancellation. I may make exceptions, at my discretion, for emergency or unusual "
        "circumstances.", body))

    e.append(Paragraph("PROFESSIONAL FEES", section))
    e.append(Paragraph(
        "My fee for a 50-minute individual psychotherapy session is $300, and my fee for a 50-minute "
        "couples therapy session is $350, unless we have already discussed alternative fee "
        "arrangements based on individual circumstances. Fees includes time you arrive late In "
        "addition to appointments, I charge this hourly amount for other professional services you "
        "may need, including but not limited to reviewing medical records, collateral meetings or "
        "phone calls longer than 15 minutes. I will break down the hourly cost for periods of less than "
        "one hour.", body))
    e.append(Paragraph(
        "Payment is due at time of service. I accept all major credit cards and Zelle. A card will be "
        "required to schedule our initial meeting and will be kept on file to be charged in the event of "
        "no shows or cancellations within 24 hours.", body))
    e.append(Paragraph(
        "Psychological evaluations are billed at my hourly rate, including assessment, scoring and "
        "interpretation of testing. When scheduling assessments, we will discuss the likely time and "
        "costs required to the best of my abilities.  However, some individuals may take longer to "
        "complete the same assessment than others, and unforeseen issues may arise. I will inform "
        "you of any substantial changes in our estimates.", body))
    e.append(Paragraph(
        "If you become involved in legal proceedings that require my participation, you will be "
        "expected to pay for all of my professional time, including preparation and transportation "
        "costs, even if I am called to testify by another party. Because of the difficulty of legal "
        "involvement, I charge $400 per hour for preparation and attendance at legal proceedings. If "
        "I am required to appear in court, my fee is $800 per hour, with a minimum of three hours.", body))

    e.append(Paragraph("CONTACT BETWEEN SESSIONS", section))
    e.append(Paragraph(
        "Even during my business hours, I am often not immediately available to respond to calls or "
        "emails. I make every effort to return communications within 24 hours, excluding weekends. "
        "If you are unable to reach me and feel that you can’t wait for me to return your call, contact "
        "911 or your nearest emergency room.", body))

    e.append(Paragraph("LIMITS ON CONFIDENTIALITY", section))
    e.append(Paragraph(
        "The law protects the privacy of all communications between a patient and a psychologist, "
        "but some situations are excluded by law. In most situations, we can only release information "
        "about your treatment to others if you sign a written Authorization form that meets certain "
        "legal requirements imposed by HIPAA and/or other Federal or State law.", body))
    e.append(Paragraph(
        "There are other situations that require only that you provide written, advance consent. Your "
        "signature on this Agreement provides consent for the following activities and those provided "
        "in the attached Notice:", body))
    e.append(Paragraph(
        "·       We may occasionally find it helpful to consult other health and mental health "
        "professionals about a case. During a consultation, we make every effort to avoid revealing "
        "the identity of our patients. The other professionals are also legally bound to keep the "
        "information confidential.  If you don’t object, we will not tell you about these consultations "
        "unless we feel that it is important to our work together.  I will note all consultations in your "
        "Clinical Record (which is called “PHI” in my Notice of Psychologist’s Policies and Practices to "
        "Protect the Privacy of Your Health Information).", bullet))
    e.append(Paragraph(
        "·       Disclosures required by health insurers or to collect overdue fees are discussed "
        "elsewhere in this Agreement.", bullet))
    e.append(Paragraph(
        "There are some situations where we are permitted or required to disclose information "
        "without either your consent or Authorization:", bold_body))
    e.append(Paragraph(
        "·       If you are involved in a court proceeding and a request is made for information "
        "concerning your diagnosis and treatment, such information is protected by the psychologist-"
        "patient privilege law.  We cannot provide any information without your (or your legal "
        "representative’s) written authorization, or a court order, or if we receive a subpoena of "
        "which you have been properly notified and you have failed to inform me that you oppose "
        "the subpoena.  If you are involved in or contemplating litigation, you should consult with "
        "your attorney to determine whether a court would be likely to order me to disclose "
        "information.", bullet))
    e.append(Paragraph(
        "·       If a government agency is requesting the information for health oversight activities, "
        "within its appropriate legal authority, we may be required to provide it for them.", bullet))
    e.append(Paragraph(
        "If a patient files a complaint or lawsuit against us, we may disclose relevant information "
        "regarding that patient in order to defend ourselves.", body))
    e.append(Paragraph(
        "·       If a patient files a worker’s compensation claim, and we are providing necessary "
        "treatment related to that claim, we must, upon appropriate request, submit treatment "
        "reports to the appropriate parties, including the patient’s employer, the insurance carrier or "
        "an authorized qualified rehabilitation provider.  HIPAA rules also do not protect your "
        "information when applying for governmental or private disability, or when you are covered "
        "by automobile insurance.", bullet))
    e.append(Paragraph(
        "There are some situations in which we are legally obligated to take actions, which we "
        "believe are necessary to attempt to protect others from harm and we may have to reveal "
        "some information about a patient’s treatment.  If such situations arise, we will make a "
        "reasonable effort to fully discuss it with you before taking any action and we will limit my "
        "disclosure to what is necessary.", bold_body))
    e.append(Paragraph(
        "§      If we know, or have reason to suspect, that a child under 18 is abused, abandoned, or "
        "neglected by a parent, legal custodian, caregiver, or any other person responsible for the "
        "child’s welfare, the law requires that we file a report with the Department of Child and "
        "Family Services. Once such a report is filed, we may be required to provide additional "
        "information.", bullet))
    e.append(Paragraph(
        "§      If we know or have reasonable cause to suspect, that a vulnerable adult has been or is "
        "being abused, neglected, or exploited, the law requires that we file a report with the central "
        "abuse hotline.  Once such a report is filed, we may be required to provide additional "
        "information.", bullet))
    e.append(Paragraph(
        "§      If we believe that there is a clear and immediate probability of physical harm to the "
        "patient, to other individuals, or to society, we may be required to disclose information to "
        "take protective action, including communicating the information to the potential victim, "
        "and/or appropriate family member, and/or the police or seeking hospitalization of the "
        "patient.", bullet))
    e.append(Paragraph(
        "While this written summary of exceptions to confidentiality should prove helpful in "
        "informing you about potential problems, it is important that we discuss any questions or "
        "concerns that you may have now or in the future. The laws governing confidentiality can "
        "be quite complex, and we are not attorneys. In situations where specific advice is "
        "required, formal legal advice may be needed.", bold_body))

    e.append(Paragraph("PROFESSIONAL RECORDS", section))
    e.append(Paragraph(
        "The laws and standards of my profession require that we keep Protected Health Information "
        "about you in your Clinical Record. Except in unusual circumstances that disclosure would "
        "physically endanger you and/or others or makes reference to another person (other than a "
        "health care provider) and we believe that access is reasonably likely to cause substantial "
        "harm to such other person, you may examine and/or receive a copy of your Clinical Record, "
        "if you request it in writing. Because these are professional records, they can be "
        "misinterpreted and/or upsetting to untrained readers.  For this reason, we recommend that "
        "you initially review them in our presence or have them forwarded to another mental health "
        "professional so you can discuss the contents.  In most circumstances, we are allowed to "
        "charge a copying fee as well as postage or other costs including time spent associated with "
        "furnishing you these records.  We may withhold copies of your records until payment of the "
        "copying fees has been made. If we refuse your request for access to your records, you have "
        "a right of review, which we will discuss with you upon request.", body))

    e.append(Paragraph("PATIENT RIGHTS", section))
    e.append(Paragraph(
        "HIPAA provides you with several new or expanded rights regarding your Clinical Records "
        "and disclosures of protected health information. These rights include requesting that we "
        "amend your record; requesting restrictions on what information from your Clinical Records "
        "is disclosed to others; requesting an accounting of most disclosures of protected health "
        "information that you have neither consented to nor authorized; determining the location to "
        "which protected information disclosures are sent; having any complaints you make about "
        "our policies and procedures recorded in your records; and the right to a paper copy of this "
        "Agreement, the attached Notice form, and my privacy policies and procedures. I am happy "
        "to discuss any of these rights with you.", body))

    e.append(Paragraph("BILLING AND PAYMENTS", section))
    e.append(Paragraph(
        "Depositions, court appearances, attorney conferences, including preparation for "
        "such, are charged as discussed above. Should deposition and/or expert testimony be "
        "required, an estimation of the fee(retainer) will be provided "
        "and must be paid 10 business days in advance of the hearing date or the scheduled time "
        "may be released by me.", body))
    e.append(Paragraph(
        "Any cancellations or postponement of these services must be made within 3 business days’ "
        "notice of appearance, or the fees are nonrefundable. The person subpoenaing me to appear "
        "at court, deposition, or similar litigation events is responsible for 100% of my fees unless "
        "previous arrangements have been made through the court.", body))
    e.append(Paragraph(
        "If your account has not been paid for more than 60 days and arrangements for payment "
        "have not been agreed upon, we have the option of using legal means to secure the "
        "payment. This may involve hiring a collection agency or going through court which will "
        "require us to disclose otherwise confidential information. In most collection situations, the "
        "only information we release regarding a patient’s treatment is his/her name, personal "
        "identifying information, payment history, information about any agreements or "
        "authorizations made regarding payment or responsibility for services, the nature of services "
        "provided, and the amount due.  If such legal action is necessary, its costs will be included by "
        "us or our attorney in the claim.  By signing this agreement, you understand that you are "
        "responsible for reasonable attorney and legal fees for accounts that go to collections.  We "
        "will also release information necessary to file an adverse credit report with Equifax or other "
        "such agency.", body))

    e.append(Paragraph("INSURANCE REIMBURSEMENT", section))
    e.append(Paragraph(
        "If you have a health insurance policy, it may provide some coverage for mental health "
        "treatment. At your request, I will provide a Superbill at the end of each month for you to file "
        "for reimbursement. However, it is you and not your insurance company who is responsible "
        "for the full payment of my fee.", body))

    # SIGNATURE BLOCK
    e.append(Spacer(1, 8))
    e.append(Paragraph(
        "YOUR SIGNATURE BELOW INDICATES THAT YOU HAVE READ THIS AGREEMENT, AGREE TO "
        "ITS TERMS, AND CONSENT TO TREATMENT. IT ALSO SERVES AS AN ACKNOWLEDGEMENT "
        "THAT YOU HAVE RECEIVED THE HIPAA NOTICE FORM DESCRIBED ABOVE.",
        closing_caps))

    e.append(Paragraph("Client", sig_label))
    e.append(Spacer(1, 10))

    line_style = ParagraphStyle("ls", fontName="Helvetica", fontSize=9,
                                textColor=MID, spaceAfter=0)
    spacer_style = ParagraphStyle("sp", fontName="Helvetica", fontSize=10,
                                  spaceAfter=0)

    sig_col_w = 300
    date_col_w = 180

    def sig_row(label, col_w):
        return Table(
            [[Paragraph("", spacer_style)],
             [Paragraph(label, line_style)]],
            colWidths=[col_w],
            rowHeights=[28, 16],
            style=TableStyle([
                ("LINEBELOW",    (0, 0), (0, 0), 0.5, DARK),
                ("TOPPADDING",   (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
                ("LEFTPADDING",  (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ])
        )

    e.append(sig_row("Signature", sig_col_w))
    e.append(Spacer(1, 16))
    e.append(sig_row("Printed Name", sig_col_w))
    e.append(Spacer(1, 16))
    e.append(sig_row("Date", date_col_w))

    doc.build(e, onFirstPage=on_every_page, onLaterPages=on_every_page)
    print(f"PDF written to: {out_path}")


if __name__ == "__main__":
    build()
