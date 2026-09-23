import os
import json
from fpdf import FPDF
from chart_engine import generate_comparative_chart

class EPTReportPDF(FPDF):
    def __init__(self, periods=None, fecha_corta="22/09/2026", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.periods = periods or ["Diagnóstica", "I Bimestre"]
        self.fecha_corta = fecha_corta

    def header(self):
        if self.page_no() > 1:
            self.set_fill_color(30, 58, 96) # Deep Corporate Blue
            self.rect(0, 0, 210, 15, "F")
            self.set_text_color(255, 255, 255)
            self.set_font("Helvetica", "B", 8)
            self.set_xy(15, 3)
            p_text = " VS. ".join(self.periods).upper()
            self.cell(0, 10, f"INFORME COMPARATIVO PEDAGÓGICO: {p_text}", align="L")
            self.cell(0, 10, "ÁREA: EDUCACIÓN PARA EL TRABAJO (EPT)  ", align="R")
            self.ln(12)
            
    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f"Agente Estadístico EPT 2026 | Fecha de Emisión: {self.fecha_corta}", align="L")
            self.set_x(-40)
            self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", align="R")

def draw_data_cell(pdf, text, width, height=7, bg_color=(255, 255, 255), text_color=(33, 37, 41), align="C", is_bold=False):
    pdf.set_fill_color(*bg_color)
    pdf.set_text_color(*text_color)
    font_style = "B" if is_bold else ""
    pdf.set_font("Helvetica", font_style, 8)
    pdf.cell(width, height, text, border=1, align=align, fill=True)

def generate_pdf_report(json_path="evaluaciones_2026.json", output_pdf="Reporte_Comparativo_Estadisticas_EPT_2026.pdf", periods=None):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return False
        
    from datetime import datetime
    months_es = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    now = datetime.now()
    fecha_larga = f"{now.day} de {months_es[now.month - 1]} de {now.year}"
    fecha_corta = now.strftime("%d/%m/%Y")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    meta = data.get("meta", {})
    available_periods = meta.get("periodos_disponibles", ["Diagnóstica", "I Bimestre"])
    
    if periods is None:
        periods = available_periods

    # Make sure chart image is freshly generated
    chart_img = "comparativa_logros.png"
    generate_comparative_chart(json_path=json_path, output_image=chart_img, periods_to_compare=periods)

    pdf = EPTReportPDF(periods=periods, fecha_corta=fecha_corta, orientation="portrait", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    # -------------------------------------------------------------------------
    # PAGE 1: PORTADA Y PRESENTACIÓN
    # -------------------------------------------------------------------------
    pdf.add_page()
    
    # Cover Decorative Banner
    pdf.set_fill_color(30, 58, 96) # Primary deep blue
    pdf.rect(0, 0, 210, 25, "F")
    pdf.set_fill_color(46, 196, 182) # Teal accent line
    pdf.rect(0, 25, 210, 4, "F")
    
    # Title Text
    pdf.set_y(40)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 10, "INFORME TÉCNICO PEDAGÓGICO", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    ano_academico = meta.get("ano_academico", 2026)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(100, 110, 120)
    pdf.cell(0, 8, f"ANÁLISIS COMPARATIVO DE LOGROS DE APRENDIZAJE {ano_academico}", align="C", new_x="LMARGIN", new_y="NEXT")
    
    period_title = " VS. ".join(periods).upper()
    pdf.cell(0, 8, period_title, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Metadata Box
    pdf.set_fill_color(245, 247, 250)
    pdf.rect(15, 75, 180, 50, "F")
    pdf.set_xy(20, 78)
    
    metadata_items = [
        ("INSTITUCIÓN EDUCATIVA:", meta.get("institucion", "I.E. 2026")),
        ("ÁREA CURRICULAR:", meta.get("area", "Educación para el Trabajo (EPT)")),
        ("COMPETENCIA:", meta.get("especialidad", "Gestiona proyectos de emprendimiento")),
        ("DOCENTE RESPONSABLE:", meta.get("docente", "Segundo Antonio Guanilo Cacho")),
        ("AÑO ACADÉMICO:", str(meta.get("ano_academico", 2026))),
        ("PERIODOS EVALUADOS:", ", ".join(periods)),
        ("FECHA DE EMISIÓN:", fecha_larga)
    ]
    
    for label, value in metadata_items:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(30, 58, 96)
        pdf.cell(48, 6, label, align="L")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(33, 37, 41)
        pdf.cell(0, 6, value, align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(20)
    
    # Introduction Section
    pdf.set_xy(15, 135)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 8, "PRESENTACIÓN EJECUTIVA", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(15, 138, 30, 1, "F")
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(33, 37, 41)
    
    p1 = ("El presente informe ofrece un análisis estadístico y pedagógico detallado de los logros de "
          "aprendizaje en el área de Educación para el Trabajo (EPT). Contrata de forma cuantitativa y "
          f"cualitativa los resultados de los periodos: {', '.join(periods)}, abarcando a la totalidad "
          "de estudiantes de 1° a 5° grado de secundaria.")
    pdf.multi_cell(0, 5.5, p1, align="J")
    pdf.ln(3)
    
    p2 = ("El propósito fundamental es evaluar la efectividad de las estrategias pedagógicas aplicadas, "
          "identificar avances en las competencias de emprendimiento, visibilizar brechas entre secciones "
          "y fundamentar las decisiones pedagógicas e intervenciones focalizadas para los periodos siguientes.")
    pdf.multi_cell(0, 5.5, p2, align="J")
    
    # Bottom Banner
    pdf.set_fill_color(30, 58, 96)
    pdf.rect(0, 280, 210, 17, "F")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(0, 277, 210, 3, "F")

    # -------------------------------------------------------------------------
    # PAGE 2: TABLA POR GRADOS Y GRÁFICO
    # -------------------------------------------------------------------------
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 8, "1. CUADRO COMPARATIVO GENERAL POR GRADOS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(15, 23, 50, 1, "F")
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(33, 37, 41)
    # Bimester comparison setup (omitting Diagnóstica from table if bimesters exist)
    bimester_periods = [p for p in periods if "Bimestre" in p or "bimestre" in p.lower()]
    if not bimester_periods:
        bimester_periods = [p for p in periods if "Diagnóstica" not in p and "Diagnostica" not in p]
    if not bimester_periods:
        bimester_periods = periods

    p1_name = bimester_periods[0]
    p2_name = bimester_periods[-1] if len(bimester_periods) > 1 else bimester_periods[0]
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(33, 37, 41)
    p_tab1 = ("Consolidado de porcentajes de niveles de logro (Satisfactorio [AD/A], En Proceso [B] y En Inicio [C]) "
              f"comparando {p1_name} vs. {p2_name} por cada grado académico de secundaria:")
    pdf.multi_cell(0, 4.5, p_tab1, align="J")
    pdf.ln(3)
    
    # 10 columns total (24mm + 3x52mm = 180mm)
    col_w = [24, 18, 18, 16, 18, 18, 16, 18, 18, 16]
    
    pdf.set_fill_color(30, 58, 96)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 7.5)
    
    pdf.cell(24, 10, "GRADO", border=1, align="C", fill=True)
    pdf.cell(52, 5, "LOGRO SATISFACTORIO (AD/A)", border=1, align="C", fill=True)
    pdf.cell(52, 5, "EN PROCESO (B)", border=1, align="C", fill=True)
    pdf.cell(52, 5, "EN INICIO (C)", border=1, align="C", fill=True)
    pdf.ln(5)
    
    pdf.set_x(15 + 24)
    # Under AD/A
    pdf.cell(18, 5, p1_name[:8].upper(), border=1, align="C", fill=True)
    pdf.cell(18, 5, p2_name[:8].upper(), border=1, align="C", fill=True)
    pdf.cell(16, 5, "VAR. %", border=1, align="C", fill=True)
    # Under B
    pdf.cell(18, 5, p1_name[:8].upper(), border=1, align="C", fill=True)
    pdf.cell(18, 5, p2_name[:8].upper(), border=1, align="C", fill=True)
    pdf.cell(16, 5, "VAR. %", border=1, align="C", fill=True)
    # Under C
    pdf.cell(18, 5, p1_name[:8].upper(), border=1, align="C", fill=True)
    pdf.cell(18, 5, p2_name[:8].upper(), border=1, align="C", fill=True)
    pdf.cell(16, 5, "VAR. %", border=1, align="C", fill=True)
    pdf.ln(5)
    
    grades_list = ["1° Grado", "2° Grado", "3° Grado", "4° Grado", "5° Grado", "Promedio General"]
    
    for i, g in enumerate(grades_list):
        g_data = data["grados"].get(g, {})
        d_p1 = g_data.get(p1_name, {"pct_AD_A": 0, "pct_B": 0, "pct_C": 0})
        d_p2 = g_data.get(p2_name, {"pct_AD_A": 0, "pct_B": 0, "pct_C": 0})
        
        var_ada = d_p2.get("pct_AD_A", 0) - d_p1.get("pct_AD_A", 0)
        var_b = d_p2.get("pct_B", 0) - d_p1.get("pct_B", 0)
        var_c = d_p2.get("pct_C", 0) - d_p1.get("pct_C", 0)
        
        is_total = (g == "Promedio General")
        bg = (230, 240, 250) if is_total else ((245, 247, 250) if i % 2 == 0 else (255, 255, 255))
        bold = is_total
        
        color_ada = (40, 150, 80) if var_ada > 0 else ((180, 40, 40) if var_ada < 0 else (33, 37, 41))
        color_b = (40, 150, 80) if var_b < 0 else ((217, 119, 6) if var_b > 0 else (33, 37, 41))
        color_c = (40, 150, 80) if var_c < 0 else ((180, 40, 40) if var_c > 0 else (33, 37, 41))
        
        draw_data_cell(pdf, g, col_w[0], bg_color=bg, is_bold=bold, align="L")
        
        # AD/A
        draw_data_cell(pdf, f"{d_p1.get('pct_AD_A',0):.1f}%", col_w[1], bg_color=bg, is_bold=bold)
        draw_data_cell(pdf, f"{d_p2.get('pct_AD_A',0):.1f}%", col_w[2], bg_color=bg, is_bold=bold)
        draw_data_cell(pdf, f"{var_ada:+.1f}%", col_w[3], bg_color=bg, text_color=color_ada, is_bold=True)
        
        # B
        draw_data_cell(pdf, f"{d_p1.get('pct_B',0):.1f}%", col_w[4], bg_color=bg, is_bold=bold)
        draw_data_cell(pdf, f"{d_p2.get('pct_B',0):.1f}%", col_w[5], bg_color=bg, is_bold=bold)
        draw_data_cell(pdf, f"{var_b:+.1f}%", col_w[6], bg_color=bg, text_color=color_b, is_bold=True)
        
        # C
        draw_data_cell(pdf, f"{d_p1.get('pct_C',0):.1f}%", col_w[7], bg_color=bg, is_bold=bold)
        draw_data_cell(pdf, f"{d_p2.get('pct_C',0):.1f}%", col_w[8], bg_color=bg, is_bold=bold)
        draw_data_cell(pdf, f"{var_c:+.1f}%", col_w[9], bg_color=bg, text_color=color_c, is_bold=True)
        pdf.ln()

    pdf.ln(3)
    
    # Embed Matplotlib Chart with clean spacing below image
    if os.path.exists(chart_img):
        pdf.image(chart_img, x=15, y=86, w=180)
        pdf.set_y(202)
    else:
        pdf.ln(50)
        
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 6, "Análisis de Resultados Agregados:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(33, 37, 41)
    
    pg_p1 = data["grados"].get("Promedio General", {}).get(p1_name, {})
    pg_p2 = data["grados"].get("Promedio General", {}).get(p2_name, {})
    c_p1_val = pg_p1.get("pct_C", 0.0)
    c_p2_val = pg_p2.get("pct_C", 0.0)
    ada_p1_val = pg_p1.get("pct_AD_A", 0.0)
    ada_p2_val = pg_p2.get("pct_AD_A", 0.0)
    var_gen_ada = ada_p2_val - ada_p1_val
    
    p_an = (f"En el periodo {p2_name}, se registra un {ada_p2_val:.1f}% de logro satisfactorio (AD/A) a nivel institucional "
            f"(con una variación de {var_gen_ada:+.1f}% respecto a {p1_name} que fue {ada_p1_val:.1f}%). "
            f"El porcentaje en nivel de Inicio (C) se ubica en {c_p2_val:.1f}% (frente a {c_p1_val:.1f}% en {p1_name}). "
            "Estos datos reflejan el avance continuo en el desarrollo de competencias del área de EPT.")
    pdf.multi_cell(0, 4.5, p_an, align="J")

    # -------------------------------------------------------------------------
    # PAGE 3: DESGLOSE POR SECCIONES
    # -------------------------------------------------------------------------
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 8, "2. DESGLOSE DETALLADO POR SECCIONES", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(15, 23, 60, 1, "F")
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 5, f"Estadísticas detalladas por sección ({p2_name}) para identificar necesidades de refuerzo focalizado:", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    
    sec_w = [22, 23, 20, 40, 40, 35]
    pdf.set_fill_color(30, 58, 96)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8.5)
    
    headers2 = ["SECCIÓN", "MATRICULADOS", "EVALUADOS", "SATISFACTORIO (AD/A)", "EN PROCESO (B)", "EN INICIO (C)"]
    for h, w in zip(headers2, sec_w):
        pdf.cell(w, 8, h, border=1, align="C", fill=True)
    pdf.ln()
    
    # Use bimester sections for p2_name if available, else fall back to flat secciones
    bim_sections = data.get("secciones_bimestres", {}).get(p2_name, {})
    sections_dict = bim_sections if bim_sections else data.get("secciones", {})
    
    tot_mat = 0
    tot_eval = 0
    tot_ada = 0
    tot_b = 0
    tot_c = 0
    priority_alerts = []
    
    for idx, (sec_name, sec_info) in enumerate(sections_dict.items()):
        bg = (245, 247, 250) if idx % 2 == 0 else (255, 255, 255)
        
        m = sec_info.get("matriculados", 0)
        e = sec_info.get("evaluados", 0)
        ada = sec_info.get("AD_A", 0)
        b_cnt = sec_info.get("B", 0)
        c_cnt = sec_info.get("C", 0)
        
        tot_mat += m
        tot_eval += e
        tot_ada += ada
        tot_b += b_cnt
        tot_c += c_cnt
        
        p_ada = sec_info.get("pct_AD_A", 0.0)
        p_b = sec_info.get("pct_B", 0.0)
        p_c = sec_info.get("pct_C", 0.0)
        
        if p_c > 5.0:
            priority_alerts.append(f"Sección '{sec_name}': Presenta {p_c:.1f}% de estudiantes en nivel Inicio (C) ({c_cnt} casos). Requiere nivelación focalizada.")
        elif p_b > 60.0:
            priority_alerts.append(f"Sección '{sec_name}': Presenta {p_b:.1f}% en nivel Proceso (B). Se sugiere reforzar estrategias para impulsarlos al nivel AD/A.")

        draw_data_cell(pdf, sec_name, sec_w[0], bg_color=bg, align="L", is_bold=True)
        draw_data_cell(pdf, str(m), sec_w[1], bg_color=bg)
        draw_data_cell(pdf, str(e), sec_w[2], bg_color=bg)
        draw_data_cell(pdf, f"{ada}  /  {p_ada:.1f}%", sec_w[3], bg_color=bg)
        draw_data_cell(pdf, f"{b_cnt}  /  {p_b:.1f}%", sec_w[4], bg_color=bg)
        
        c_color = (180, 40, 40) if c_cnt > 0 else (33, 37, 41)
        draw_data_cell(pdf, f"{c_cnt}  /  {p_c:.1f}%", sec_w[5], bg_color=bg, text_color=c_color, is_bold=c_cnt > 0)
        pdf.ln()

    # Total row
    bg_tot = (230, 240, 250)
    p_t_ada = (tot_ada / tot_eval * 100) if tot_eval > 0 else 0
    p_t_b = (tot_b / tot_eval * 100) if tot_eval > 0 else 0
    p_t_c = (tot_c / tot_eval * 100) if tot_eval > 0 else 0
    
    draw_data_cell(pdf, "TOTAL", sec_w[0], bg_color=bg_tot, align="L", is_bold=True)
    draw_data_cell(pdf, str(tot_mat), sec_w[1], bg_color=bg_tot, is_bold=True)
    draw_data_cell(pdf, str(tot_eval), sec_w[2], bg_color=bg_tot, is_bold=True)
    draw_data_cell(pdf, f"{tot_ada}  /  {p_t_ada:.1f}%", sec_w[3], bg_color=bg_tot, is_bold=True)
    draw_data_cell(pdf, f"{tot_b}  /  {p_t_b:.1f}%", sec_w[4], bg_color=bg_tot, is_bold=True)
    draw_data_cell(pdf, f"{tot_c}  /  {p_t_c:.1f}%", sec_w[5], bg_color=bg_tot, is_bold=True)
    pdf.ln(10)

    # Priority Sections Alert
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(180, 40, 40)
    pdf.cell(0, 6, "Secciones Prioritarias de Intervención (Alerta Pedagógica):", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(33, 37, 41)
    
    if priority_alerts:
        p_sec_alert = "\n".join(f"- {alert}" for alert in priority_alerts)
    else:
        p_sec_alert = "- Todas las secciones presentan un desempeño estable sin alertas críticas de nivel Inicio (C)."
        
    pdf.multi_cell(0, 4.5, p_sec_alert, align="L")

    # -------------------------------------------------------------------------
    # PAGE 4: CONCLUSIONES Y COMPROMISOS PEDAGÓGICOS
    # -------------------------------------------------------------------------
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 8, "3. CONCLUSIONES Y PLAN DE COMPROMISOS PEDAGÓGICOS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(15, 23, 70, 1, "F")
    pdf.ln(6)

    # Dynamic calculations for Conclusions Page
    c_p2_count = tot_c
    c_p2_pct = (tot_c / tot_eval * 100) if tot_eval > 0 else 0.0

    # 1. Fortalezas Identificadas
    high_ada_grades = []
    for g_item in ["1° Grado", "2° Grado", "3° Grado", "4° Grado", "5° Grado"]:
        g_st = data["grados"].get(g_item, {}).get(p2_name, {})
        if g_st.get("pct_AD_A", 0) >= 60.0:
            high_ada_grades.append(g_item.split("°")[0] + "°")
    
    if high_ada_grades:
        ada_str = f"Alta receptividad y desarrollo de competencias en los grados {', '.join(high_ada_grades)}, donde el logro satisfactorio supera el 60%."
    else:
        ada_str = "Consolidación progresiva de competencias en el área de EPT a nivel institucional."

    if c_p2_count == 0:
        c_str = f"Erradicación total del nivel de Inicio (C) a nivel institucional (0.0% / 0 estudiantes en inicio) en {p2_name}."
    else:
        c_str = f"Control y reducción de la brecha de inicio (C), representando únicamente el {c_p2_pct:.1f}% ({c_p2_count} estudiante{'s' if c_p2_count > 1 else ''}) en {p2_name}."

    fortalezas_items = [
        ada_str,
        c_str,
        "Compromiso activo de los estudiantes en proyectos de emprendimiento práctico y trabajo colaborativo."
    ]

    # 2. Oportunidades de Mejora
    high_b_sections = []
    for sec_n, sec_i in sections_dict.items():
        pb = sec_i.get("pct_B", 0.0)
        if pb >= 50.0:
            high_b_sections.append(f"{sec_n} ({pb:.1f}%)")

    if high_b_sections:
        b_str = f"Elevado porcentaje de estudiantes concentrados en el nivel de Proceso (B) en {', '.join(high_b_sections[:3])}."
    else:
        b_str = "Reforzar estrategias pedagógicas para impulsar a los estudiantes de nivel Proceso (B) hacia el nivel Satisfactorio (AD/A)."

    oportunidades_items = [
        b_str,
        "Reforzar el uso de rúbricas de evaluación formativa y retroalimentación oportuna en cada sesión del área de EPT."
    ]

    # 3. Compromisos Pedagógicos
    if c_p2_count > 0:
        comp_c_str = f"Implementar sesiones de nivelación personalizada para los {c_p2_count} estudiante{'s' if c_p2_count > 1 else ''} que permanecen en nivel Inicio (C)."
    else:
        comp_c_str = "Mantener la meta de 0 estudiantes en nivel Inicio (C) mediante acompañamiento preventivo y tutoría pedagógica continua."

    compromisos_items = [
        comp_c_str,
        "Diseñar estrategias de aprendizaje basado en proyectos (ABP) diferenciados para impulsar a los estudiantes de nivel B hacia AD/A.",
        "Realizar seguimiento quincenal de asistencia y avances prácticos en el área de EPT."
    ]

    subsections = [
        ("Fortalezas Identificadas", fortalezas_items),
        ("Oportunidades de Mejora", oportunidades_items),
        ("Compromisos Pedagógicos para el Próximo Periodo", compromisos_items)
    ]

    for title, items in subsections:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 58, 96)
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(33, 37, 41)
        for item in items:
            pdf.set_x(20)
            pdf.cell(5, 4.5, "-", align="C")
            pdf.set_x(25)
            pdf.multi_cell(170, 4.5, item, align="J")
        pdf.ln(2)

    # Signatures block
    pdf.set_y(-52)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(100, 110, 120)
    pdf.cell(0, 5, f"Fecha de emisión del informe: {fecha_larga}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 9)
    pdf.cell(85, 5, "___________________________________", align="C")
    pdf.cell(10)
    pdf.cell(85, 5, "___________________________________", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(85, 5, meta.get("docente", "Segundo Antonio Guanilo Cacho"), align="C")
    pdf.cell(10)
    pdf.cell(85, 5, "V° B° Dirección / Coordinación Pedagógica", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(85, 4, "Docente del Área de EPT", align="C")
    pdf.cell(10)
    pdf.cell(85, 4, "I.E. 2026", align="C")

    pdf.output(output_pdf)
    print(f"PDF report successfully generated: {output_pdf}")
    return True

if __name__ == "__main__":
    generate_pdf_report()
