import cv2
import os
import numpy as np
input_folder = 'carpeta'  
output_folder = 'carpeta'  

os.makedirs(output_folder, exist_ok=True)

def filtrar_ruido(mask):
    # Paso 1: Filtro de mediana para suavizar el ruido de sal y pimienta
    filtered_mask = cv2.medianBlur(mask, 5)
    
    # Paso 2: Operaciones morfológicas para eliminar ruido y pequeñas partículas
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    morph_open = cv2.morphologyEx(filtered_mask, cv2.MORPH_OPEN, kernel)  # Elimina pequeños puntos
    morph_close = cv2.morphologyEx(morph_open, cv2.MORPH_CLOSE, kernel)   # Rellena pequeños huecos

    # Paso 3: Eliminar componentes conectados pequeños
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(morph_close, connectivity=8)
    # Mantener solo componentes grandes (puedes ajustar el umbral)
    min_size = 500  # Ajusta este valor según el tamaño del ruido
    filtered_mask = np.zeros_like(labels, dtype=np.uint8)
    for i in range(1, num_labels):  # Ignorar el fondo
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            filtered_mask[labels == i] = 255
    
    return filtered_mask

# Procesar cada imagen en la carpeta de entrada
for filename in os.listdir(input_folder):
    if filename.endswith(".png"):  # Asegurarse de procesar solo archivos de imagen
        # Leer la imagen en escala de grises
        image_path = os.path.join(input_folder, filename)
        mask = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # Aplicar el filtro avanzado
        processed_mask = filtrar_ruido(mask)
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, processed_mask)

print("Proceso de filtrado completado. Las imágenes filtradas se han guardado en 'truchas GTv2'.")