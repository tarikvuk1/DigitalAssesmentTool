import io
from datetime import datetime

import pandas as pd
import streamlit as st

from recommender import generate_recommendations, generate_roadmap
from scorer import get_maturity_level
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


# ---------------- PDF ----------------
# ---------------- PDF ----------------
def build_company_pdf(company_name, level, company_row):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    margin = 50
    y = height - 50

    primary = colors.HexColor("#163B65")
    accent = colors.HexColor("#2F6FED")
    light_bg = colors.HexColor("#F4F7FB")
    text_dark = colors.HexColor("#1F2937")
    text_muted = colors.HexColor("#6B7280")
    border = colors.HexColor("#D9E2F1")

    def reset_font(font_name="Helvetica", size=11, color=text_dark):
        pdf.setFont(font_name, size)
        pdf.setFillColor(color)

    def ensure_space(required_height=80):
        nonlocal y
        if y < required_height:
            draw_footer()
            pdf.showPage()
            y = height - 50

    def draw_footer():
        pdf.setStrokeColor(border)
        pdf.line(margin, 35, width - margin, 35)
        reset_font("Helvetica", 9, text_muted)
        pdf.drawString(margin, 22, "Digital Maturity Assessment Tool")
        pdf.drawRightString(width - margin, 22, f"Page {pdf.getPageNumber()}")

    def write_wrapped_text(text, x, max_width, font_name="Helvetica", size=11, color=text_dark, line_gap=15):
        nonlocal y
        reset_font(font_name, size, color)
        lines = simpleSplit(str(text), font_name, size, max_width)
        for line in lines:
            ensure_space(70)
            pdf.drawString(x, y, line)
            y -= line_gap

    def write_section_title(title):
        nonlocal y
        ensure_space(100)
        y -= 8
        reset_font("Helvetica-Bold", 13, primary)
        pdf.drawString(margin, y, title)
        y -= 10
        pdf.setStrokeColor(accent)
        pdf.line(margin, y, width - margin, y)
        y -= 18

    def draw_score_card(x, top_y, card_width, card_height, label, value):
        pdf.setFillColor(light_bg)
        pdf.setStrokeColor(border)
        pdf.roundRect(x, top_y - card_height, card_width, card_height, 10, fill=1, stroke=1)
        reset_font("Helvetica", 10, text_muted)
        pdf.drawString(x + 12, top_y - 18, label)
        reset_font("Helvetica-Bold", 18, primary)
        pdf.drawString(x + 12, top_y - 42, value)

    def format_pdf_score(val):
        try:
            return f"{float(val):.2f}"
        except Exception:
            return "N/A"

    def split_bullets(value):
        if value is None:
            return ["N/A"]
        parts = [part.strip() for part in str(value).split("|") if part.strip()]
        return parts if parts else ["N/A"]

    pdf.setFillColor(primary)
    pdf.rect(0, height - 140, width, 140, fill=1, stroke=0)

    reset_font("Helvetica-Bold", 22, colors.white)
    pdf.drawString(margin, height - 75, "Digital Maturity Assessment Report")

    reset_font("Helvetica", 11, colors.white)
    pdf.drawString(margin, height - 100, f"Company: {company_name}")
    pdf.drawString(margin, height - 118, f"Maturity Level: {level}")
    pdf.drawRightString(width - margin, height - 100, f"Generated: {datetime.now().strftime('%d %b %Y')}")

    y = height - 175

    write_section_title("Executive Summary")
    summary_text = (
        f"{company_name} is currently assessed at the {level} stage of digital maturity. "
        f"This report summarizes performance across infrastructure, business processes, marketing, HR, innovation, and security, "
        f"and outlines prioritized actions to support the next phase of digital transformation."
    )
    write_wrapped_text(summary_text, margin, width - 2 * margin)
    y -= 6

    write_section_title("Score Overview")
    card_width = 155
    card_height = 56
    gap = 12
    left_x = margin
    middle_x = margin + card_width + gap
    right_x = margin + (card_width + gap) * 2

    top_row_y = y
    draw_score_card(left_x, top_row_y, card_width, card_height, "Infrastructure", format_pdf_score(company_row.get("infrastructure_score")))
    draw_score_card(middle_x, top_row_y, card_width, card_height, "Processes", format_pdf_score(company_row.get("process_score")))
    draw_score_card(right_x, top_row_y, card_width, card_height, "Marketing", format_pdf_score(company_row.get("marketing_score")))

    second_row_y = top_row_y - card_height - 14
    draw_score_card(left_x, second_row_y, card_width, card_height, "HR", format_pdf_score(company_row.get("hr_score")))
    draw_score_card(middle_x, second_row_y, card_width, card_height, "Innovation", format_pdf_score(company_row.get("innovation_score")))
    draw_score_card(right_x, second_row_y, card_width, card_height, "Security", format_pdf_score(company_row.get("security_score")))

    y = second_row_y - card_height - 22

    ensure_space(140)
    pdf.setFillColor(colors.white)
    pdf.setStrokeColor(border)
    pdf.roundRect(margin, y - 62, width - 2 * margin, 62, 10, fill=1, stroke=1)
    reset_font("Helvetica", 11, text_muted)
    pdf.drawString(margin + 16, y - 22, "Overall Digital Maturity Score")
    reset_font("Helvetica-Bold", 22, accent)
    pdf.drawString(margin + 16, y - 46, format_pdf_score(company_row.get("overall_score")))
    y -= 82

    write_section_title("Strategic Recommendations")
    for item in split_bullets(company_row.get("recommendations", "N/A")):
        write_wrapped_text(f"• {item}", margin, width - 2 * margin)

    y -= 6
    write_section_title("Transformation Roadmap")
    roadmap_sections = [
        ("Short-Term Priorities", company_row.get("short_term", "N/A")),
        ("Mid-Term Priorities", company_row.get("mid_term", "N/A")),
        ("Long-Term Priorities", company_row.get("long_term", "N/A")),
    ]

    for title, value in roadmap_sections:
        ensure_space(120)
        pdf.setFillColor(light_bg)
        pdf.setStrokeColor(border)
        pdf.roundRect(margin, y - 16, width - 2 * margin, 24, 8, fill=1, stroke=1)
        reset_font("Helvetica-Bold", 11, primary)
        pdf.drawString(margin + 10, y, title)
        y -= 28
        items = split_bullets(value)
        for item in items:
            write_wrapped_text(f"• {item}", margin + 4, width - 2 * margin - 4)
        y -= 8

    draw_footer()
    pdf.save()
    buffer.seek(0)
    return buffer


# ---------------- HELPERS ----------------
def format_score(value):
    try:
        return f"{float(value):.2f}"
    except Exception:
        return "N/A"


def get_questions_template_path():
    possible_paths = [
        "data/Test digitalne konkurentnosti.xlsx",
        "Test digitalne konkurentnosti.xlsx",
    ]
    for path in possible_paths:
        try:
            with open(path, "rb"):
                return path
        except FileNotFoundError:
            continue
    return None


ORDERED_QUESTIONS = [
    "Naziv kompanije",
    "ID broj",
    "Email",
    "Šta je za vas digitalna transformacija?",
    "Šta vas je motivisalo da krenete u digitalnu transformaciju?",
    "Kojoj industriji pripada kompanija?",
    "Gdje je lokacija kompanije?",
    "Da li imate interno IT odjeljenje ili koristite usluge drugih kompanija za svoje IT potrebe?",
    "Da li planirate da investirate u digitalne projekte?",
    "Koji softver koristite?",
    "Da li vaši zaposleni na personalnom kompjuteru (ili sličnim uređajima) koriste ili imaju pristup internetu?",
    "Da li koristite elektronsku poštu? Da li imate elektronsku poštu na domenu vaše kompanije (na primjer, ime.prezime@kompanija.ba)?",
    "Da li u okviru vaše kompanije koristite alate za zajednički rad (Google Drive, One Drive) i čuvanje, kako bi se svi relevanti dokumenti nalazili na jednom mjestu za sve uključene u proces?",
    "Da li ste pretraživali internet zbog novih dobavljača za proizvode i usluge u posljednje 2 godine ili da li ste se kvalifikovali za online dobavljača?",
    "Da li od vaših glavnih dobavljača poručujete elektronski (ne faksom)?",
    "Ukoliko od vaših glavnih dobavljača poručujete elektronski, kako to činite? Molimo vas da odaberete sve primjenjive odgovore.",
    "Da li (bar neke) fakture primate elektronski ?",
    "Da li elektronski obrađujete elektronske fakture u vašem sopstvenom sistemu upravljanja preduzećem, na primjer ERP, itd.?",
    "Da li se podaci u lancu procesa (od prodaje preko proizvodnje do administracije i obrnuto) prenose elektronski u vašem sopstvenom sistemu upravljanja preduzećem, na primjer ERP, itd.?",
    "Da li koristite online alate, platforme, itd. prilikom angažovanja novih radnika?",
    "Kako upravljate kadrovskom administracijom (na primjer, godišnji odmori, platni spiskovi ili prekovremeni rad)?",
    "Da li koristite sljedeće elektronske alate za obuku ili dalje usavršavanje zaposlenih? Molimo vas da odaberete sve primenjive odgovore.",
    "Kako vidite digitalne vještine u vašoj kompaniji?",
    "Kada razmišljate o svojim proizvodima / uslugama: kakve koristi možete da ponudite svojim klijentima putem digitalne transformacije?",
    "Da li ste uveli / razvili novu uslugu / proizvod na tržištu u poslednje dvije godine?",
    "Da li ste se bavili razvojem i/ili istraživanjem novih proizvoda/usluga u saradnji sa klijentima, inovativnim firmama (startup kompanije) u posljednje dvije godine?",
    "Da li ste u posljednje dvije godine stupili u kontakt sa firmom/firmama (startup kompanije) koje se bave inovacijama u vašoj industriji?",
    "Da li ste u posljednje dvije godine bavili pravljenjem procesa za upravljanje inovacijama?",
    "Na osnovu tradicionalnog poslovnog modela (prodaja ili iznajmljivanje robe i usluga), sljedeći dodatni elementi bi mogli da budu interesantni za vašu kompaniju: Besplatan osnovni proizvod/osnovna usluga i prodaja dodatnog proizvoda/usluge, Model operatera (iznajmljivanje umjesto prodaje), Strukturirana prodaja klijenta klijentu (naknada), Prodaja reklamnog prostora, Prodaja podataka, Ustupanje licenci, Prodaja slobodnog kapaciteta (model deljenja). Da li ste se ovim već bavili?",
    "Da li znate neke konkurente koji su promijenili svoj model poslovanja?",
    "Da li koristite mogućnosti digitalne transformacije za saradnju sa partnerima?",
    "Da li koristite digitalne mogućnosti za finansiranje (na primjer, grupno (Crowd) finansiranje?",
    "Da li je imenovan rukovodilac u organizaciji za digitalnu transformaciju radnih mjesta?",
    "Da li imate web-site?",
    "Ako imate web - site, kada je on napravljen i kada je bilo posljednje veliko ažuriranje?",
    "Gdje i na kojim kanalima se klijent susreće sa vašim brendom / proizvodom? Molimo vas da odaberete sve primenjive odgovore.",
    "Da li imate opciju online plaćanja (plaćanje karticom, PayPal, iPay, itd) na vašem web-site-u?",
    "Da li pratite / radite na onlajn reputaciji vaše kompanije i na prometu na web-site-u (na primjer, rezultati pretrage na Google, teme foruma, razgovori na Facebook-u/Twiter-u)?",
    "Da li se bavite praćenjem ponašanja korisnika na vašem web-site-u zarad veće prodaje i boljeg razumijevanja potrošača (Google analitika, Matomo, Facebook pixsel, HotJar, itd.)",
    "Da li pratite podatke o potrošnji/kupovini individualnih klijenata i da li imate razrađenu šemu lojalnosti za najvjernije mušterije?",
    "Da li ste ikada vodili kampanju na društvenim medijima koja je trajala najmanje šest mjeseci?",
    "Da li ste se ikada bavili segmentacijom kupaca na osnovu podataka koje ste generisali na društvenim mrežama?",
    "Ko su vaši klijenti? Molimo vas da odaberete sve primenjive odgovore.",
    "Da li imate internog menadžera za društvene medije ili i koristite usluge drugih kompanija za svoje potrebe?",
    "Koje mjere za IT bezbjednost ste uspostavili? Molimo vas da odaberete sve primenljive odgovore.",
    "Na snazi su opšti propisi o zaštiti podataka (General Data Protection Regulation - GDPR). Čuvanje i obradu ličnih podataka kompanija mora da dokumentuje. Da li ste to već uradili?",
]


def load_question_rows():
    template_path = get_questions_template_path()
    extracted = {}

    if template_path is not None:
        df = pd.read_excel(template_path, header=None)
        df = df.dropna(axis=1, how="all").dropna(how="all").reset_index(drop=True)

        for _, row in df.iterrows():
            values = [str(v).strip() for v in row.tolist() if pd.notna(v) and str(v).strip()]
            if not values:
                continue

            filtered = [v for v in values if not v.lower().startswith("unnamed") and "table" not in v.lower()]
            if not filtered:
                continue

            question_text = filtered[0]
            options = []
            for value in filtered[1:]:
                if value == question_text:
                    continue
                if value not in options:
                    options.append(value)

            extracted[question_text] = {"question": question_text, "options": options}

    ordered_rows = []
    for question in ORDERED_QUESTIONS:
        if question in extracted:
            ordered_rows.append(extracted[question])
        else:
            ordered_rows.append({"question": question, "options": []})

    return ordered_rows


def is_yes_no(options):
    lowered = {str(opt).strip().lower() for opt in options}
    return lowered == {"da", "ne"} or lowered == {"yes", "no"}


def is_multi_select_question(question_text):
    text = question_text.lower()
    return "odaberete sve" in text or "select all" in text or "sve primjenjive" in text

# Helper to check if a response is empty
def is_response_empty(value):
    if value is None:
        return True
    if isinstance(value, list):
        return len(value) == 0
    return str(value).strip() == ""


def calculate_user_scores(responses):
    def yn(value):
        value = str(value).strip().lower()
        if value in {"da", "yes"}:
            return 1.0
        if value in {"ne", "no"}:
            return 0.0
        return 0.0

    def has_choice(value):
        return 1.0 if str(value).strip() else 0.0

    infrastructure_score = (
        yn(responses.get("Da li vaši zaposleni na personalnom kompjuteru (ili sličnim uređajima) koriste ili imaju pristup internetu?", ""))
        + yn(responses.get("Da li koristite elektronsku poštu? Da li imate elektronsku poštu na domenu vaše kompanije (na primjer, ime.prezime@kompanija.ba)?", ""))
        + yn(responses.get("Da li imate web-site?", ""))
    ) / 3

    process_score = (
        yn(responses.get("Da li ste pretraživali internet zbog novih dobavljača za proizvode i usluge u posljednje 2 godine ili da li ste se kvalifikovali za online dobavljača?", ""))
        + yn(responses.get("Da li (bar neke) fakture primate elektronski ?", ""))
        + yn(responses.get("Da li elektronski obrađujete elektronske fakture u vašem sopstvenom sistemu upravljanja preduzećem, na primjer ERP, itd.?", ""))
    ) / 3

    marketing_score = (
        yn(responses.get("Da li pratite / radite na onlajn reputaciji vaše kompanije i na prometu na web-site-u (na primjer, rezultati pretrage na Google, teme foruma, razgovori na Facebook-u/Twiter-u)?", ""))
        + yn(responses.get("Da li ste ikada vodili kampanju na društvenim medijima koja je trajala najmanje šest mjeseci?", ""))
        + yn(responses.get("Da li se bavite praćenjem ponašanja korisnika na vašem web-site-u zarad veće prodaje i boljeg razumijevanja potrošača (Google analitika, Matomo, Facebook pixsel, HotJar, itd.)", ""))
    ) / 3

    hr_score = (
        yn(responses.get("Da li koristite online alate, platforme, itd. prilikom angažovanja novih radnika?", ""))
        + has_choice(responses.get("Da li koristite sljedeće elektronske alate za obuku ili dalje usavršavanje zaposlenih? Molimo vas da odaberete sve primjenjive odgovore.", ""))
        + yn(responses.get("Da li je imenovan rukovodilac u organizaciji za digitalnu transformaciju radnih mjesta?", ""))
    ) / 3

    innovation_score = (
        yn(responses.get("Da li ste uveli / razvili novu uslugu / proizvod na tržištu u posljednje dvije godine?", ""))
        + yn(responses.get("Da li ste se bavili razvojem i/ili istraživanjem novih proizvoda/usluga u saradnji sa klijentima, inovativnim firmama (startup kompanije) u posljednje dvije godine?", ""))
        + yn(responses.get("Da li ste u posljednje dvije godine bavili pravljenjem procesa za upravljanje inovacijama?", ""))
    ) / 3

    security_score = (
        has_choice(responses.get("Koje mjere za IT bezbjednost ste uspostavili? Molimo vas da odaberete sve primjenjive odgovore.", ""))
        + yn(responses.get("Na snazi su opšti propisi o zaštiti podataka (General Data Protection Regulation - GDPR). Čuvanje i obradu ličnih podataka kompanija mora da dokumentuje. Da li ste to već uradili?", ""))
    ) / 2

    overall_score = (
        infrastructure_score
        + process_score
        + marketing_score
        + hr_score
        + innovation_score
        + security_score
    ) / 6

    return {
        "infrastructure_score": infrastructure_score,
        "process_score": process_score,
        "marketing_score": marketing_score,
        "hr_score": hr_score,
        "innovation_score": innovation_score,
        "security_score": security_score,
        "overall_score": overall_score,
    }


def save_responses_to_excel(final_responses):
    df = pd.DataFrame([final_responses])

    try:
        existing = pd.read_excel("responses.xlsx")
        df = pd.concat([existing, df], ignore_index=True)
    except Exception:
        pass

    df.to_excel("responses.xlsx", index=False)


def build_report_from_responses(final_responses):
    scores = calculate_user_scores(final_responses)
    report_df = pd.DataFrame([{**final_responses, **scores}])

    report_df["maturity_level"] = report_df["overall_score"].apply(get_maturity_level)
    report_df["recommendations"] = report_df.apply(generate_recommendations, axis=1)

    roadmaps = report_df.apply(generate_roadmap, axis=1)
    report_df["short_term"] = roadmaps.apply(lambda x: x["short_term"])
    report_df["mid_term"] = roadmaps.apply(lambda x: x["mid_term"])
    report_df["long_term"] = roadmaps.apply(lambda x: x["long_term"])

    return report_df.iloc[0]


# ---------------- APP ----------------
st.set_page_config(page_title="Digital Maturity Assessment Tool", page_icon="📊", layout="wide")

st.markdown(
    """
    <div style="
        padding: 40px;
        border-radius: 16px;
        background: linear-gradient(135deg, #163B65, #2F6FED);
        color: white;
        margin-bottom: 25px;
        text-align: center;
    ">
        <h1>📊 Digital Maturity Assessment Tool</h1>
        <p style="opacity:0.9; max-width:700px; margin:auto;">
            Analyze companies, calculate digital maturity scores, and generate AI-powered recommendations.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# session state
defaults = {
    "page": "home",
    "survey_started": False,
    "current_question_index": 0,
    "survey_responses": {},
    "is_admin": False,
    "admin_login_error": False,
    "latest_report": None,
    "latest_company_name": "",
    "admin_entry": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

admin_query_value = st.query_params.get("admin", "0")
st.session_state.admin_entry = str(admin_query_value) == "1"

if st.session_state.admin_entry and st.session_state.page == "home":
    st.session_state.page = "admin_login"

question_rows = load_question_rows()

# ---------------- HOME ----------------
if st.session_state.page == "home":
    st.subheader("📋 Company Digital Assessment")

    st.markdown(
        """
        <div style="padding:20px;border-radius:12px;background-color:#111827;border:1px solid #1F2937; margin-bottom:16px;">
            <h3 style="margin-top:0;">Welcome</h3>
            <p style="margin-bottom:0; color:#9CA3AF;">
                Start the assessment and answer the questions step by step. At the end, you will receive your digital maturity report.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Start Assessment", use_container_width=True):
        st.session_state.page = "user"
        st.rerun()

# ---------------- ADMIN LOGIN ----------------
elif st.session_state.page == "admin_login":
    st.subheader("🔐 Administrator Login")

    admin_password = st.text_input("Enter admin password", type="password")

    if st.session_state.admin_login_error:
        st.error("Wrong password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", use_container_width=True):
            if admin_password == "admin123":
                st.session_state.is_admin = True
                st.session_state.admin_login_error = False
                st.session_state.page = "admin_panel"
                st.rerun()
            else:
                st.session_state.admin_login_error = True
                st.rerun()

    with col2:
        if st.button("Back", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.admin_login_error = False
            st.query_params.clear()
            st.rerun()

# ---------------- USER ----------------
elif st.session_state.page == "user":
    st.subheader("📋 Company Digital Assessment")

    if not question_rows:
        st.error("Questions template file was not found or could not be loaded.")
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()
        st.stop()

    if not st.session_state.survey_started:
        st.markdown(
            """
            <div style="padding:20px;border-radius:12px;background-color:#111827;border:1px solid #1F2937; margin-bottom:16px;">
                <h3 style="margin-top:0;">Welcome to the assessment</h3>
                <p style="margin-bottom:0; color:#9CA3AF;">
                    Click the button below to start the company digital assessment. You will answer the questions one by one and receive your report at the end.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Assessment", use_container_width=True):
                st.session_state.survey_started = True
                st.session_state.current_question_index = 0
                st.session_state.survey_responses = {}
                st.rerun()
        with col2:
            if st.button("Back", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()

    else:
        total_questions = len(question_rows)
        current_index = st.session_state.current_question_index
        current_item = question_rows[current_index]

        question_text = current_item["question"]
        question_options = current_item["options"]
        stored_value = st.session_state.survey_responses.get(question_text)

        st.progress((current_index + 1) / total_questions)
        st.caption(f"Question {current_index + 1} of {total_questions}")
        st.markdown(f"### {question_text}")

        response_value = None
        validation_message = "Please answer this question before continuing."

        if question_text in ["Naziv kompanije", "ID broj", "Email"]:
            response_value = st.text_input(
                "Your answer",
                value=stored_value if isinstance(stored_value, str) else "",
                key=f"question_{current_index}",
            )
        elif is_yes_no(question_options):
            normalized_options = ["Da", "Ne"] if {o.lower() for o in question_options} == {"da", "ne"} else ["Yes", "No"]
            default_index = 0
            if stored_value in normalized_options:
                default_index = normalized_options.index(stored_value)

            response_value = st.radio(
                "Select one option",
                normalized_options,
                index=default_index,
                key=f"question_{current_index}",
            )
        elif question_options:
            if is_multi_select_question(question_text):
                default_values = stored_value if isinstance(stored_value, list) else []
                response_value = st.multiselect(
                    "Select one or more options",
                    question_options,
                    default=default_values,
                    key=f"question_{current_index}",
                )
            else:
                default_index = 0
                if stored_value in question_options:
                    default_index = question_options.index(stored_value)
                response_value = st.selectbox(
                    "Select one option",
                    question_options,
                    index=default_index,
                    key=f"question_{current_index}",
                )
        else:
            response_value = st.text_area(
                "Your answer",
                value=stored_value if isinstance(stored_value, str) else "",
                key=f"question_{current_index}",
            )

        nav_col1, nav_col2, nav_col3 = st.columns(3)

        with nav_col1:
            if current_index > 0 and st.button("Previous", use_container_width=True):
                st.session_state.survey_responses[question_text] = response_value
                st.session_state.current_question_index -= 1
                st.rerun()

        with nav_col2:
            if current_index < total_questions - 1 and st.button("Next", use_container_width=True):
                if is_response_empty(response_value):
                    st.warning(validation_message)
                else:
                    st.session_state.survey_responses[question_text] = response_value
                    st.session_state.current_question_index += 1
                    st.rerun()

        with nav_col3:
            if current_index == total_questions - 1 and st.button("Submit Assessment", use_container_width=True):
                if is_response_empty(response_value):
                    st.warning(validation_message)
                else:
                    st.session_state.survey_responses[question_text] = response_value

                    final_responses = {}
                    for item in question_rows:
                        q_text = item["question"]
                        value = st.session_state.survey_responses.get(q_text, "")
                        if isinstance(value, list):
                            final_responses[q_text] = ", ".join(value)
                        else:
                            final_responses[q_text] = value

                    save_responses_to_excel(final_responses)
                    company_row = build_report_from_responses(final_responses)

                    company_name = final_responses.get("Naziv kompanije", "Company")

                    st.session_state.latest_report = company_row.to_dict()
                    st.session_state.latest_company_name = company_name
                    st.session_state.survey_started = False
                    st.session_state.current_question_index = 0
                    st.session_state.survey_responses = {}
                    st.session_state.page = "user_report"
                    st.rerun()

# ---------------- USER REPORT ----------------
elif st.session_state.page == "user_report":
    company_row = st.session_state.latest_report
    company_name = st.session_state.latest_company_name or "Company"

    if not company_row:
        st.warning("No report found.")
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()
        st.stop()

    level = company_row.get("maturity_level", "N/A")
    color = {
        "Beginner": "#ff4b4b",
        "Basic": "#ffa500",
        "Intermediate": "#1f77b4",
        "Advanced": "#2ca02c",
    }.get(level, "#888888")

    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.subheader("📊 Your Company Report")
    with top_col2:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.success("Your responses have been saved successfully.")

    st.markdown(
        f"""
        <div style="padding:16px;border-radius:14px;background-color:{color};color:white;margin:16px 0;">
            <h3 style="margin:0;">{company_name}</h3>
            <p style="margin:6px 0 0 0;font-size:18px;"><strong>Maturity Level:</strong> {level}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_col1, score_col2, score_col3, score_col4 = st.columns(4)
    score_col1.metric("Infrastructure", format_score(company_row.get("infrastructure_score")))
    score_col2.metric("Processes", format_score(company_row.get("process_score")))
    score_col3.metric("Marketing", format_score(company_row.get("marketing_score")))
    score_col4.metric("Overall", format_score(company_row.get("overall_score")))

    extra_col1, extra_col2, extra_col3 = st.columns(3)
    extra_col1.metric("HR", format_score(company_row.get("hr_score")))
    extra_col2.metric("Innovation", format_score(company_row.get("innovation_score")))
    extra_col3.metric("Security", format_score(company_row.get("security_score")))

    st.subheader("Recommendations")
    st.info(company_row.get("recommendations", "N/A"))

    st.subheader("Roadmap")
    roadmap_col1, roadmap_col2, roadmap_col3 = st.columns(3)
    with roadmap_col1:
        st.subheader("Short-Term")
        st.success(company_row.get("short_term", "N/A"))
    with roadmap_col2:
        st.subheader("Mid-Term")
        st.warning(company_row.get("mid_term", "N/A"))
    with roadmap_col3:
        st.subheader("Long-Term")
        st.error(company_row.get("long_term", "N/A"))

    pdf = build_company_pdf(company_name, level, company_row)
    st.download_button(
        "Download PDF Report",
        pdf,
        file_name=f"{company_name}_report.pdf",
        mime="application/pdf",
    )

# ---------------- ADMIN PANEL ----------------
elif st.session_state.page == "admin_panel":
    st.subheader("📂 Administrator Panel")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Logout", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.page = "home"
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.query_params.clear()
            st.rerun()

    try:
        responses_df = pd.read_excel("responses.xlsx")
    except Exception:
        responses_df = pd.DataFrame()

    if responses_df.empty:
        st.warning("No responses found yet.")
    else:
        result_rows = []

        for _, row in responses_df.iterrows():
            final_responses = row.to_dict()
            company_row = build_report_from_responses(final_responses)
            merged = {**final_responses, **company_row.to_dict()}
            result_rows.append(merged)

        admin_df = pd.DataFrame(result_rows)
        st.dataframe(admin_df, use_container_width=True)