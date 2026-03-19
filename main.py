# -*- coding: utf-8 -*-
"""Web app para CEM A3 Mercados - Railway deployment."""

import os
from flask import Flask, render_template, request, send_file
from procesador import cargar_archivo, procesar_dataframe, guardar_excel

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-cambiar-en-produccion")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/procesar", methods=["POST"])
def procesar():
    if "archivo" not in request.files:
        return "No se subió ningún archivo.", 400

    file = request.files["archivo"]
    if not file or file.filename == "":
        return "No se seleccionó archivo.", 400

    try:
        df = cargar_archivo(file)
        df_proc = procesar_dataframe(df)
        buffer = guardar_excel(df_proc)

        nombre_base = os.path.splitext(file.filename)[0]
        nombre_salida = f"{nombre_base}_procesado.xlsx"

        return send_file(
            buffer,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=nombre_salida,
        )
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return f"Error al procesar: {e}", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
