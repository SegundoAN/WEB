import os
import json
import re
from flask import Flask, jsonify, request, send_file, render_template
from werkzeug.utils import secure_filename

from chart_engine import generate_comparative_chart
from pdf_engine import generate_pdf_report
from excel_importer import import_bimester_excel, import_section_excel, consolidate_bimester, get_upload_status

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs('uploads', exist_ok=True)

def resolve_year_context(req):
    year_val = None
    if req.method == "POST":
        data = req.get_json(silent=True) or {}
        year_val = data.get("year") or req.form.get("year")
    if not year_val:
        year_val = req.args.get("year")
    if not year_val:
        year_val = 2026

    try:
        year_int = int(year_val)
    except (ValueError, TypeError):
        year_int = 2026

    json_filename = f"evaluaciones_{year_int}.json"
    pdf_filename = f"Reporte_Comparativo_Estadisticas_EPT_{year_int}.pdf"
    chart_filename = f"comparativa_logros_{year_int}.png"

    if not os.path.exists(json_filename):
        init_json_for_year(json_filename, year_int)

    return json_filename, pdf_filename, chart_filename, year_int

def init_json_for_year(json_filename, year_int):
    default_data = {
        "meta": {
            "institucion": "I.E. 2026",
            "area": "Educación para el Trabajo (EPT)",
            "especialidad": "Gestión de Proyectos de Emprendimiento Económico o Social",
            "docente": "Segundo Antonio Guanilo Cacho",
            "ano_academico": year_int,
            "periodos_disponibles": ["Diagnóstica", "I Bimestre"],
            "periodos_totales": ["Diagnóstica", "I Bimestre", "II Bimestre", "III Bimestre", "IV Bimestre"]
        },
        "grados": {
            "1° Grado": {},
            "2° Grado": {},
            "3° Grado": {},
            "4° Grado": {},
            "5° Grado": {},
            "Promedio General": {}
        },
        "secciones": {},
        "secciones_bimestres": {}
    }
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(default_data, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def get_data():
    json_path, pdf_path, chart_path, year = resolve_year_context(request)
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify({"success": True, "data": data, "year": year})
    return jsonify({"success": False, "error": f"No data found for year {year}"}), 404

@app.route("/api/upload-status", methods=["GET"])
def api_upload_status():
    """Returns which sections have been uploaded per bimester for the requested year."""
    json_path, pdf_path, chart_path, year = resolve_year_context(request)
    status = get_upload_status(json_path=json_path)
    return jsonify({"success": True, "status": status, "year": year})

@app.route("/api/generate-pdf", methods=["GET", "POST"])
def api_generate_pdf():
    json_path, pdf_path, chart_path, year = resolve_year_context(request)
    
    if request.method == "POST":
        req = request.get_json(silent=True) or {}
        periods = req.get("periods", None)
    else:
        periods_str = request.args.get("periods", "")
        periods = [p.strip() for p in periods_str.split(",") if p.strip()] if periods_str else None
    
    success = generate_pdf_report(json_path=json_path, output_pdf=pdf_path, periods=periods)
    if success and os.path.exists(pdf_path):
        as_attach = request.args.get("view", "download") != "preview"
        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=as_attach,
            download_name=f"Reporte_Comparativo_Estadisticas_EPT_{year}.pdf"
        )
    return jsonify({"success": False, "error": "Error al generar el PDF"}), 500

@app.route("/api/upload-sections", methods=["POST"])
def api_upload_sections():
    """Upload multiple section files at once for a selected year and bimester."""
    json_path, pdf_path, chart_path, year = resolve_year_context(request)
    bimester_name = request.form.get("bimester_name", "II Bimestre")
    
    sections_data = []
    
    for field_name, file in request.files.items():
        if file.filename == '':
            continue
            
        grado = None
        seccion = None
        
        if field_name.startswith("file_"):
            parts = field_name.split("_")
            if len(parts) >= 3:
                grade_num = parts[1]
                sec_letter = parts[2]
                grado = f"{grade_num}° Grado"
                seccion = f"{grade_num}° {sec_letter}"
                
        if not grado or not seccion:
            match = re.search(r'\d+', field_name)
            if match:
                idx = match.group()
                form_grado = request.form.get(f"grado_{idx}")
                form_seccion = request.form.get(f"seccion_{idx}")
                if form_grado and form_seccion:
                    grado = form_grado
                    seccion = form_seccion
                    
        if grado and seccion:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{year}_{bimester_name}_{seccion}_{filename}")
            file.save(filepath)
            
            sec_result = import_section_excel(filepath, grado, seccion)
            if sec_result:
                sections_data.append(sec_result)
                
    if not sections_data:
        return jsonify({"success": False, "error": "No se procesaron archivos validos."}), 400
        
    ok, msg, details = consolidate_bimester(sections_data, bimester_name, json_path=json_path)
    
    if ok:
        generate_comparative_chart(json_path=json_path, output_image=chart_path)
        generate_pdf_report(json_path=json_path, output_pdf=pdf_path)
        
        with open(json_path, "r", encoding="utf-8") as f:
            updated_data = json.load(f)
        
        upload_status = get_upload_status(json_path=json_path)
            
        return jsonify({
            "success": True, 
            "message": msg, 
            "data": updated_data,
            "upload_status": upload_status,
            "consolidation_details": details,
            "year": year
        })
    else:
        return jsonify({"success": False, "error": msg}), 500

@app.route("/comparativa_logros.png")
def get_chart_image():
    json_path, pdf_path, chart_path, year = resolve_year_context(request)
    if not os.path.exists(chart_path):
        generate_comparative_chart(json_path=json_path, output_image=chart_path)
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype="image/png")
    return jsonify({"error": "Image not generated yet"}), 404

if __name__ == "__main__":
    print("Iniciando Servidor Web de Analisis Estadistico Multianual (2026-2035) en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
