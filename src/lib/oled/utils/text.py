def center_text(draw, text, font, bounding_box, y = 0):
    # Obtener el cuadro delimitador del texto
    bbox = draw.textbbox(bounding_box[:2], text, font=font)
    # Calcular la posición x del texto para centrarlo horizontalmente
    x = (bounding_box[0] + bounding_box[2] - bbox[2]) // 2
    # Dibujar el texto centrado horizontalmente
    draw.text((x, y), text, font=font, fill="white")