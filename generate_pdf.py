from fpdf import FPDF
import os

class EPTReport(FPDF):
    def header(self):
        # We only display the header on pages after the cover page (page 1)
        if self.page_no() > 1:
            self.set_fill_color(30, 58, 96) # Deep Corporate Blue
            self.rect(0, 0, 210, 15, "F")
            self.set_text_color(255, 255, 255)
            self.set_font("Helvetica", "B", 8)
            self.set_xy(15, 3)
            self.cell(0, 10, "INFORME COMPARATIVO: EVALUACIÓN DIAGNÓSTICA VS. I BIMESTRE 2026", align="L")
            self.cell(0, 10, "ÁREA: EDUCACIÓN PARA EL TRABAJO (EPT)  ", align="R")
            self.ln(12)
            
    def footer(self):
        # We only display the footer on pages after the cover page (page 1)
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, "Reporte Generado Automáticamente - Año Escolar 2026", align="L")
            self.set_x(-40)
            self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", align="R")

def draw_header_cell(pdf, text, width, height=8):
    pdf.set_fill_color(30, 58, 96)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(width, height, text, border=1, align="C", fill=True)

def draw_data_cell(pdf, text, width, height=7, bg_color=(255, 255, 255), text_color=(33, 37, 41), align="C", is_bold=False):
    pdf.set_fill_color(*bg_color)
    pdf.set_text_color(*text_color)
    font_style = "B" if is_bold else ""
    pdf.set_font("Helvetica", font_style, 8)
    pdf.cell(width, height, text, border=1, align=align, fill=True)

def main():
    pdf = EPTReport(orientation="portrait", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # -------------------------------------------------------------------------
    # PAGE 1: PORTADA Y PRESENTACIÓN
    # -------------------------------------------------------------------------
    pdf.add_page()
    
    # Cover Decorative Accents
    pdf.set_fill_color(30, 58, 96) # Primary deep blue
    pdf.rect(0, 0, 210, 25, "F")
    pdf.set_fill_color(46, 196, 182) # Secondary teal accent line
    pdf.rect(0, 25, 210, 4, "F")
    
    # Title Text
    pdf.set_y(40)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 10, "INFORME TÉCNICO PEDAGÓGICO", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(100, 110, 120)
    pdf.cell(0, 8, "ANÁLISIS COMPARATIVO DE LOGROS DE APRENDIZAJE 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "EVALUACIÓN DIAGNÓSTICA VS. PRIMER BIMESTRE", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Metadata Block
    pdf.set_fill_color(245, 247, 250)
    pdf.rect(15, 75, 180, 45, "F")
    pdf.set_xy(20, 78)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 58, 96)
    
    metadata = [
        ("ÁREA CURRICULAR:", "Educación para el Trabajo (EPT)"),
        ("COMPETENCIA:", "Gestiona proyectos de emprendimiento económico o social"),
        ("DOCENTE DEL ÁREA:", "Segundo"),
        ("AÑO ACADÉMICO:", "2026"),
        ("FECHA DE EMISIÓN:", "22 de Mayo de 2026")
    ]
    
    for label, value in metadata:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(30, 58, 96)
        pdf.cell(45, 6, label, align="L")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(33, 37, 41)
        pdf.cell(0, 6, value, align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(20)
    
    # Introduction / Presentación Section
    pdf.set_xy(15, 130)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 8, "PRESENTACIÓN", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(15, 138, 30, 1, "F") # Small underline
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(33, 37, 41)
    
    p1 = ("El presente informe técnico-pedagógico ofrece un análisis estadístico y comparativo detallado de "
          "los logros de aprendizaje obtenidos en el área de Educación para el Trabajo (EPT) - especialidad "
          "de Gestión de Proyectos de Emprendimiento. Se contrasta de manera cuantitativa y cualitativa la "
          "Evaluación Diagnóstica inicial (línea de base) con los resultados oficiales de la evaluación del "
          "Primer Bimestre del año escolar 2026, abarcando una población evaluada de 266 estudiantes desde "
          "el primer grado hasta el quinto grado de secundaria.")
    pdf.multi_cell(0, 5.5, p1, align="J")
    pdf.ln(3)
    
    p2 = ("Este estudio tiene como finalidad identificar el impacto real de las intervenciones pedagógicas "
          "aplicadas en cada aula, visibilizar el avance de los estudiantes en relación con el desarrollo de la "
          "competencia, detectar brechas significativas entre diferentes secciones, y establecer recomendaciones "
          "pedagógicas estratégicas y focalizadas para el Segundo Bimestre. Los resultados indican que "
          "se han obtenido mejoras institucionales sumamente significativas, principalmente una reducción "
          "drástica de los niveles de rezago o inicio (nivel C).")
    pdf.multi_cell(0, 5.5, p2, align="J")
    
    # Cover footer decorative banner
    pdf.set_fill_color(30, 58, 96)
    pdf.rect(0, 280, 210, 17, "F")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(0, 277, 210, 3, "F")
    
    # -------------------------------------------------------------------------
    # PAGE 2: ANÁLISIS COMPARATIVO POR GRADOS Y GRÁFICO
    # -------------------------------------------------------------------------
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 8, "1. CUADRO COMPARATIVO GENERAL POR GRADOS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(15, 23, 50, 1, "F")
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(33, 37, 41)
    p_tab1 = ("La siguiente tabla consolida los porcentajes de los niveles de logro (Logro Destacado/Previsto [AD/A], "
              "En Proceso [B] y En Inicio [C]) obtenidos de manera agregada por cada grado académico (1° a 5°). "
              "Se detalla la variación porcentual de cada indicador para medir de forma directa el progreso estudiantil:")
    pdf.multi_cell(0, 5, p_tab1, align="J")
    pdf.ln(4)
    
    # General Table Header (Total Printable Width = 180mm)
    # Widths: Grado (22), Diag_A(26), Bim_A(24), Var_A(20), Diag_B(24), Bim_B(22), Diag_C(24), Bim_C(18)
    col_w = [22, 26, 24, 20, 24, 22, 24, 18]
    
    # Row 1 of header
    pdf.set_fill_color(30, 58, 96)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    
    pdf.cell(22, 10, "GRADO", border=1, align="C", fill=True)
    pdf.cell(70, 5, "LOGRO DESTACADO / PREVISTO (AD/A)", border=1, align="C", fill=True)
    pdf.cell(46, 5, "EN PROCESO (B)", border=1, align="C", fill=True)
    pdf.cell(42, 5, "EN INICIO (C)", border=1, align="C", fill=True)
    pdf.ln(5)
    
    # Row 2 of header (we must adjust the x coordinate back)
    pdf.set_x(15 + 22)
    pdf.cell(26, 5, "E. DIAGNÓSTICA", border=1, align="C", fill=True)
    pdf.cell(24, 5, "I BIMESTRE", border=1, align="C", fill=True)
    pdf.cell(20, 5, "VARIACIÓN", border=1, align="C", fill=True)
    pdf.cell(24, 5, "E. DIAGNÓSTICA", border=1, align="C", fill=True)
    pdf.cell(22, 5, "I BIMESTRE", border=1, align="C", fill=True)
    pdf.cell(24, 5, "E. DIAGNÓSTICA", border=1, align="C", fill=True)
    pdf.cell(18, 5, "I BIMESTRE", border=1, align="C", fill=True)
    pdf.ln(5)
    
    # Table Data
    # Each row: (Grado, [Diag_A, Bim_A, Var_A], [Diag_B, Bim_B], [Diag_C, Bim_C])
    table_data = [
        ("1° Grado", "0.0%", "57.8%", "+57.8%", "25.0%", "42.2%", "75.0%", "0.0%"),
        ("2° Grado", "48.0%", "34.6%", "-13.4%", "52.0%", "60.0%", "0.0%", "5.5%"),
        ("3° Grado", "75.0%", "62.8%", "-12.2%", "25.0%", "34.9%", "0.0%", "2.3%"),
        ("4° Grado", "72.0%", "51.9%", "-20.1%", "28.0%", "46.2%", "0.0%", "1.9%"),
        ("5° Grado", "76.0%", "75.0%", "-1.0%", "24.0%", "25.0%", "0.0%", "0.0%"),
        ("Promedio", "54.2%", "56.0%", "+1.8%", "30.8%", "42.1%", "15.0%", "1.9%")
    ]
    
    for i, row in enumerate(table_data):
        is_total = (row[0] == "Promedio")
        bg = (230, 240, 250) if is_total else ((245, 247, 250) if i % 2 == 0 else (255, 255, 255))
        text_color = (15, 30, 54) if is_total else (33, 37, 41)
        bold = is_total
        
        # Determine color for variation
        var_val = float(row[3].replace("%", ""))
        var_color = (40, 150, 80) if var_val > 0 else ((180, 40, 40) if var_val < 0 else (33, 37, 41))
        
        # C-variation color (reduction in C is good, so negative variation in C is green!)
        c_bim = float(row[7].replace("%", ""))
        c_diag = float(row[6].replace("%", ""))
        c_var = c_bim - c_diag
        c_var_color = (40, 150, 80) if c_var < 0 else ((180, 40, 40) if c_var > 0 else (33, 37, 41))
        
        # Draw cells
        draw_data_cell(pdf, row[0], col_w[0], bg_color=bg, text_color=text_color, is_bold=bold, align="L")
        draw_data_cell(pdf, row[1], col_w[1], bg_color=bg, text_color=text_color, is_bold=bold)
        draw_data_cell(pdf, row[2], col_w[2], bg_color=bg, text_color=text_color, is_bold=bold)
        # Variation cell (col 3)
        draw_data_cell(pdf, row[3], col_w[3], bg_color=bg, text_color=var_color, is_bold=True)
        
        draw_data_cell(pdf, row[4], col_w[4], bg_color=bg, text_color=text_color, is_bold=bold)
        draw_data_cell(pdf, row[5], col_w[5], bg_color=bg, text_color=text_color, is_bold=bold)
        
        draw_data_cell(pdf, row[6], col_w[6], bg_color=bg, text_color=text_color, is_bold=bold)
        
        # C value in I Bimestres (col 7)
        c_text_color = (180, 40, 40) if c_bim > 0 else text_color
        draw_data_cell(pdf, row[7], col_w[7], bg_color=bg, text_color=c_text_color, is_bold=bold or (c_bim > 0))
        pdf.ln()
        
    pdf.ln(4)
    
    # Embed the chart image
    if os.path.exists("comparativa_logros.png"):
        pdf.image("comparativa_logros.png", x=20, y=95, w=170)
        pdf.set_y(198) # Adjust cursor to be below the image
    else:
        pdf.ln(50)
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 5, "[Gráfico de comparativa no encontrado]", align="C", new_x="LMARGIN", new_y="NEXT")
        
    # Analysis Paragraph
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 6, "Análisis del Consolidado General:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(33, 37, 41)
    
    cons_text = ("El análisis consolidado muestra una tendencia institucional sumamente positiva. El indicador "
                 "más sobresaliente es el descenso radical en el nivel de Inicio (C), el cual se redujo en 13.12 "
                 "puntos porcentuales, cayendo de un promedio de 15.0% en la evaluación diagnóstica a solo 1.88% "
                 "al finalizar el primer bimester. Esto evidencia la efectividad de las estrategias pedagógicas "
                 "iniciales aplicadas para nivelar a los alumnos con mayores carencias, rescatándolos de las "
                 "dificultades de inicio de la competencia. De manera paralela, se observa un incremento "
                 "de 11.31% en el nivel de Proceso (B), nutriéndose tanto de la salida de estudiantes del nivel "
                 "Inicio como de un reajuste de estudiantes de alta calificación (AD/A) que pasaron a B. "
                 "El nivel general de logro satisfactorio (AD/A) se mantuvo estable e incremental en 1.82%, "
                 "alcanzando una sólida mayoría del 56.02% de la población estudiantil.")
    pdf.multi_cell(0, 5, cons_text, align="J")
    
    # -------------------------------------------------------------------------
    # PAGE 3: DESGLOSE DETALLADO POR SECCIONES
    # -------------------------------------------------------------------------
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 8, "2. DESGLOSE ESTADÍSTICO DETALLADO POR SECCIONES", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(15, 23, 60, 1, "F")
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(33, 37, 41)
    p_tab2 = ("Para un análisis micro-pedagógico, se presenta a continuación el desglose completo del "
              "Primer Bimestre correspondiente a las 10 secciones del plantel (de 1°A a 5°B). Esta vista tabular "
              "permite detectar brechas significativas e identificar directamente las aulas que requieren "
              "acciones de refuerzo focalizado de manera inmediata:")
    pdf.multi_cell(0, 5, p_tab2, align="J")
    pdf.ln(3)
    
    # Section Table Column Widths: Sección (22), Matriculados (23), Asisten (20), AD/A (40), B (40), C (35)
    # Total = 22 + 23 + 20 + 40 + 40 + 35 = 180mm. Perfect!
    sec_w = [22, 23, 20, 40, 40, 35]
    
    # Header Row
    pdf.set_fill_color(30, 58, 96)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8.5)
    
    headers2 = ["SECCIÓN", "MATRICULADOS", "EVALUADOS", "LOGRO SATISFACTORIO (AD/A)", "EN PROCESO (B)", "EN INICIO (C)"]
    for h, w in zip(headers2, sec_w):
        pdf.cell(w, 8, h, border=1, align="C", fill=True)
    pdf.ln()
    
    # Section Data rows
    sec_data = [
        ("1° A", "39", "35", "18  /  51.4%", "17  /  48.6%", "0  /  0.0%"),
        ("1° B", "33", "29", "19  /  65.5%", "10  /  34.5%", "0  /  0.0%"),
        ("2° A", "30", "27", "4  /  14.8%", "20  /  74.1%", "3  /  11.1%"),
        ("2° B", "30", "28", "15  /  53.6%", "13  /  46.4%", "0  /  0.0%"),
        ("3° A", "24", "21", "14  /  66.7%", "7  /  33.3%", "0  /  0.0%"),
        ("3° B", "24", "22", "13  /  59.1%", "8  /  36.4%", "1  /  4.5%"),
        ("4° A", "28", "25", "11  /  44.0%", "14  /  56.0%", "0  /  0.0%"),
        ("4° B", "29", "27", "16  /  59.3%", "10  /  37.0%", "1  /  3.7%"),
        ("5° A", "28", "26", "19  /  73.1%", "7  /  26.9%", "0  /  0.0%"),
        ("5° B", "28", "26", "20  /  76.9%", "6  /  23.1%", "0  /  0.0%"),
        ("TOTAL", "293", "266", "149  /  56.0%", "112  /  42.1%", "5  /  1.9%")
    ]
    
    for i, row in enumerate(sec_data):
        is_total = (row[0] == "TOTAL")
        bg = (230, 240, 250) if is_total else ((245, 247, 250) if i % 2 == 0 else (255, 255, 255))
        text_color = (15, 30, 54) if is_total else (33, 37, 41)
        bold = is_total
        
        # Highlighting alert sectors: 2°A has 11.1% C and 74% B, and very low AD/A
        # We can make 2°A's text bold or slightly colored if it's the main concern
        is_alert_row = (row[0] == "2° A")
        row_text_color = (180, 40, 40) if is_alert_row else text_color
        
        draw_data_cell(pdf, row[0], sec_w[0], bg_color=bg, text_color=row_text_color, is_bold=bold or is_alert_row, align="C")
        draw_data_cell(pdf, row[1], sec_w[1], bg_color=bg, text_color=text_color, is_bold=bold)
        draw_data_cell(pdf, row[2], sec_w[2], bg_color=bg, text_color=text_color, is_bold=bold)
        
        # AD/A
        draw_data_cell(pdf, row[3], sec_w[3], bg_color=bg, text_color=text_color, is_bold=bold)
        # B
        draw_data_cell(pdf, row[4], sec_w[4], bg_color=bg, text_color=text_color, is_bold=bold)
        
        # C (Highlight if there are students in C)
        c_count = int(row[5].split(" / ")[0].strip())
        c_text_color = (180, 40, 40) if c_count > 0 else text_color
        draw_data_cell(pdf, row[5], sec_w[5], bg_color=bg, text_color=c_text_color, is_bold=bold or (c_count > 0))
        pdf.ln()
        
    pdf.ln(5)
    
    # Specific Section Interpretation
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 6, "Hallazgos y Brechas Inter-Seccionales Críticas:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(33, 37, 41)
    
    # Helper to write structured points
    def write_inline_bullet(bullet_title, bullet_desc):
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(30, 58, 96)
        pdf.write(5, "-  ")
        pdf.write(5, bullet_title)
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(33, 37, 41)
        pdf.write(5, bullet_desc)
        pdf.ln(6)
        
    write_inline_bullet(
        "Alerta Extrema en 2° A: ", 
        "Esta sección registra la brecha más crítica del plantel. Apenas el 14.8% (4 alumnos) se ubica en el nivel de logro satisfactorio (AD/A), en agudo contraste con el 53.6% de su sección gemela (2°B). Adicionalmente, el 74.1% de 2°A está estancado en Proceso (B) y un 11.1% (3 alumnos) se encuentra en Inicio (C). Esta sección demanda intervención pedagógica inmediata."
    )
    
    write_inline_bullet(
        "Rendimiento Excepcional en 5° Grado: ", 
        "Los estudiantes de la promoción muestran un desarrollo de competencia extraordinario y muy homogéneo. Tanto 5°A (73.1% AD/A) como 5°B (76.9% AD/A) presentan un 0% de alumnos en nivel C y porcentajes mínimos en proceso, reflejando solidez en las competencias del ciclo VII."
    )
    
    write_inline_bullet(
        "Éxito Total en Primer Grado: ", 
        "Partiendo de un alarmante 75.0% de alumnos en Inicio (C) según la evaluación diagnóstica, la docente del área logró reducir este porcentaje al 0.0% en ambas secciones (1°A y 1°B). 1°B destaca con un notable 65.5% en nivel AD/A."
    )
    
    write_inline_bullet(
        "Situación Controlada pero con Rezago en 3°B y 4°B: ", 
        "Aunque ambas aulas exhiben un rendimiento satisfactorio (59.1% y 59.3% en AD/A), registran 1 estudiante cada una en el nivel Inicio (C). Son casos de rezago individual que deben ser nivelados antes del cierre del II Bimestre."
    )
    
    # -------------------------------------------------------------------------
    # PAGE 4: CONCLUSIONES Y RECOMENDACIONES
    # -------------------------------------------------------------------------
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 8, "3. CONCLUSIONES PEDAGÓGICAS CLAVE", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(15, 23, 50, 1, "F")
    pdf.ln(4)
    
    # List of Conclusions
    conclusions = [
        ("Eficacia en el Rescate Pedagógico: ", "La reducción global del nivel de Inicio (C) de 15.0% a 1.88% certifica la altísima eficacia de los procesos de nivelación y retroalimentación formativa de la docente en el primer bimester. Se logró revertir las graves deficiencias de entrada."),
        ("El Impacto de la Complejidad Curricular: ", "La caída del nivel superior (AD/A) observada en 2° (-13.4%), 3° (-12.2%) y 4° (-20.1%) no representa un fracaso, sino el efecto esperado de la introducción de los temas curriculares técnicos del año de estudios (metodologías ágiles, validación de modelos, prototipado de alta fidelidad), los cuales presentan una exigencia infinitamente mayor que los temas evaluados en la prueba diagnóstica."),
        ("Heterogeneidad en la Práctica del Aula: ", "La coexistencia de brechas severas entre secciones del mismo grado (como 2°A y 2°B) sugiere factores contextuales, tales como dinámicas de aula, hábitos de estudio específicos o asistencia irregular que impactan los resultados colectivos."),
        ("Consolidación en el Egreso: ", "El rendimiento de 5° grado evidencia que al concluir la educación secundaria, el perfil de egreso del área de EPT se ha consolidado exitosamente en tres cuartas partes del alumnado, capacitándolos con habilidades robustas para la gestión de proyectos de emprendimiento.")
    ]
    
    for title, desc in conclusions:
        write_inline_bullet(title, desc)
        
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 8, "4. RECOMENDACIONES ESTRATÉGICAS Y ACCIONES FOCALIZADAS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(46, 196, 182)
    pdf.rect(15, 126, 75, 1, "F")
    pdf.ln(4)
    
    # Recommendations
    recommendations = [
        ("Plan de Choque Inmediato para 2° A: ", "Se debe diseñar una estrategia diferenciada para esta sección. Priorizar la conformación de grupos de trabajo cooperativo emparejando a los alumnos de nivel Proceso (B) con los alumnos de alto rendimiento (A). Implementar un cuaderno de mentoría estudiantil y sesiones de retroalimentación individuales con la docente para rescatar a los 3 alumnos en Inicio (C)."),
        ("Estrategias Didácticas de Validación Práctica: ", "Para mitigar las caídas en el logro de AD/A y la retención de alumnos en nivel B en los grados 3° y 4°, se recomienda flexibilizar la enseñanza del prototipado y validación métrica. Utilizar herramientas visuales paso a paso (lienzos simplificados, maquetas de baja fidelidad inicial) antes de exigir prototipos complejos o métricas ambientales complejas."),
        ("Estímulo al Trabajo Cooperativo Cohesionado: ", "Para resolver las 'dificultades de trabajo cooperativo y equipo' detectadas en los diagnósticos de 2° y 3° grado, se debe estructurar la co-evaluación y auto-evaluación grupal mediante rúbricas claras de roles y responsabilidades dentro de los proyectos de emprendimiento."),
        ("Consolidación del Emprendimiento Real (5° Grado): ", "En 5° grado, dado que el 75% se encuentra en nivel AD/A, la meta del II Bimestre debe centrarse en la inserción de sus proyectos de emprendimiento en entornos reales. Estimular la experimentación en campo de sus PMV mediante encuestas de tracción y análisis de mercado reales, preparándolos para ferias de emprendimiento y la incubación de sus proyectos.")
    ]
    
    for title, desc in recommendations:
        write_inline_bullet(title, desc)
        
    # Signature Zone
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 58, 96)
    pdf.cell(0, 5, "Segundo", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 4, "Docente del Área de Educación para el Trabajo", align="C")
    
    # Save the PDF file
    output_path = "Reporte_Comparativo_Estadisticas_EPT_2026.pdf"
    pdf.output(output_path)
    print(f"Comparative report generated successfully and saved as: '{output_path}'")

if __name__ == "__main__":
    main()
