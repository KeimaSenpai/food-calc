"""
Aplicación Flask para Food Calculator
Interfaz web para calcular cantidades de comida
"""

import os
import sys
import webbrowser
import threading
import io
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from PIL import Image, ImageDraw, ImageFont
from utils.food_calculator import (
    calcular_cantidades_comida,
    formatear_resultados,
    obtener_producto_especifico,
    listar_productos_disponibles,
    calcular_ingredientes_preparacion,
    formatear_ingredientes_preparacion
)

# Configuración de la aplicación
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Obtener ruta base para recursos
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent


def abrir_navegador():
    """Abre el navegador automáticamente después de que el servidor esté listo"""
    import time
    time.sleep(2)  # Esperar a que el servidor inicie
    webbrowser.open('http://localhost:5000')


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/calcular', methods=['POST'])
def calcular():
    """API para calcular cantidades de comida"""
    try:
        data = request.get_json()
        personas = int(data.get('personas', 1))
        
        if personas < 1:
            return jsonify({'error': 'Número de personas debe ser mayor a 0'}), 400
        
        resultado = calcular_cantidades_comida(personas)
        
        return jsonify({
            'success': True,
            'personas': personas,
            'productos_kg': resultado['productos_kg'],
            'productos_unidades': resultado['productos_unidades']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/formato/<formato_tipo>', methods=['POST'])
def obtener_formato(formato_tipo):
    """API para obtener resultados en diferentes formatos"""
    try:
        data = request.get_json()
        personas = int(data.get('personas', 1))
        
        resultado = calcular_cantidades_comida(personas)
        
        if formato_tipo == 'texto':
            contenido = formatear_resultados(resultado, formato='texto')
        elif formato_tipo == 'markdown':
            contenido = formatear_resultados(resultado, formato='markdown')
        elif formato_tipo == 'lista':
            contenido = formatear_resultados(resultado, formato='lista')
        else:
            return jsonify({'error': 'Formato no válido'}), 400
        
        return jsonify({
            'success': True,
            'contenido': contenido
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/producto', methods=['POST'])
def obtener_producto():
    """API para obtener cantidad de un producto específico"""
    try:
        data = request.get_json()
        personas = int(data.get('personas', 1))
        producto = data.get('producto', '')
        
        if not producto:
            return jsonify({'error': 'Producto no especificado'}), 400
        
        resultado = obtener_producto_especifico(personas, producto)
        
        if resultado:
            return jsonify({'success': True, 'datos': resultado})
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/productos-disponibles', methods=['GET'])
def productos_disponibles():
    """API para listar todos los productos disponibles"""
    try:
        productos = listar_productos_disponibles()
        return jsonify({
            'success': True,
            'productos': productos,
            'total': len(productos)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ingredientes', methods=['POST'])
def obtener_ingredientes():
    """API para calcular ingredientes de preparaciones"""
    try:
        data = request.get_json()
        personas = int(data.get('personas', 1))
        formato = data.get('formato', 'texto')
        
        ingredientes = calcular_ingredientes_preparacion(personas)
        contenido = formatear_ingredientes_preparacion(ingredientes, formato=formato)
        
        return jsonify({
            'success': True,
            'personas': personas,
            'contenido': contenido
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/descargar/pdf', methods=['POST'])
def descargar_pdf():
    """API para descargar resultados en PDF"""
    try:
        data = request.get_json()
        personas = int(data.get('personas', 1))
        
        resultado = calcular_cantidades_comida(personas)
        contenido_texto = formatear_resultados(resultado, formato='texto')
        
        # Crear PDF
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=1
        )
        
        # Título
        story.append(Paragraph(f"🍳 Food Calculator - {personas} personas", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Productos en kg
        productos_kg = resultado['productos_kg']
        if productos_kg:
            story.append(Paragraph("Productos en Kilogramos", styles['Heading2']))
            story.append(Spacer(1, 0.2*inch))
            
            data_table = [['Producto', 'Cantidad (kg)']]
            for producto, cantidad in sorted(productos_kg.items()):
                data_table.append([producto, f'{cantidad}'])
            
            table = Table(data_table, colWidths=[4*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            story.append(Spacer(1, 0.3*inch))
        
        # Productos por unidades
        productos_unidades = resultado['productos_unidades']
        if productos_unidades:
            story.append(Paragraph("Productos por Unidades", styles['Heading2']))
            story.append(Spacer(1, 0.2*inch))
            
            data_table = [['Producto', 'Cantidad (unidades)']]
            for producto, cantidad in sorted(productos_unidades.items()):
                data_table.append([producto, f'{cantidad}'])
            
            table = Table(data_table, colWidths=[4*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
        
        doc.build(story)
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'food-calculator-{personas}-personas.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/descargar/imagen', methods=['POST'])
def descargar_imagen():
    """API para descargar resultados como imagen"""
    try:
        data = request.get_json()
        personas = int(data.get('personas', 1))
        
        resultado = calcular_cantidades_comida(personas)
        contenido_texto = formatear_resultados(resultado, formato='texto')
        
        # Crear imagen
        # Dimensiones base
        width = 1200
        height = 100  # Base
        line_height = 30
        
        # Contar líneas
        lineas = contenido_texto.split('\n')
        height += len(lineas) * line_height + 100
        
        # Crear imagen
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Intentar usar font, si no, usar default
        try:
            titulo_font = ImageFont.truetype("arial.ttf", 32)
            texto_font = ImageFont.truetype("arial.ttf", 20)
        except:
            titulo_font = ImageFont.load_default()
            texto_font = ImageFont.load_default()
        
        y_position = 30
        
        # Título
        draw.text((50, y_position), f"🍳 Food Calculator - {personas} personas", 
                 fill='#1e40af', font=titulo_font)
        y_position += 60
        
        # Contenido
        for linea in lineas:
            if linea.strip():
                draw.text((50, y_position), linea, fill='black', font=texto_font)
            y_position += line_height
        
        # Guardar en buffer
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return send_file(
            img_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'food-calculator-{personas}-personas.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def no_encontrado(error):
    """Manejar errores 404"""
    return jsonify({'error': 'Recurso no encontrado'}), 404


@app.errorhandler(500)
def error_servidor(error):
    """Manejar errores 500"""
    return jsonify({'error': 'Error interno del servidor'}), 500


def main():
    """Función principal"""
    # Abrir navegador en un hilo separado
    thread = threading.Thread(target=abrir_navegador, daemon=True)
    thread.start()
    
    # Iniciar servidor Flask
    print("🍳 Food Calculator iniciado")
    print("🌐 Abriendo navegador en http://localhost:5000...")
    app.run(debug=False, host='localhost', port=5000)


if __name__ == '__main__':
    main()
