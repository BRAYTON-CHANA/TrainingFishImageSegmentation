import os
import cv2
import numpy as np

# Directorios de entrada y salida
input_folder = 'carpeta'  # Carpeta con las máscaras a procesar
output_folder = 'carpeta'  # Carpeta para guardar las máscaras con contornos unificados

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Función para obtener contornos de una máscara
def get_contours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# Función para aplicar dilatación y cierre morfológico
def apply_filters(mask):
    # Dilatación para unir contornos cercanos
    kernel_dilate = np.ones((20, 20), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel_dilate, iterations=1)
    
    # Cierre morfológico para rellenar huecos
    kernel_close = np.ones((10, 10), np.uint8)
    unified_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, kernel_close)
    
    return unified_mask

# Procesar cada archivo de máscara en la carpeta de entrada
for img_name in os.listdir(input_folder):
    mask_path = os.path.join(input_folder, img_name)
    
    # Verificar que el archivo sea una imagen
    if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    
    # Leer la máscara en escala de grises
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        print(f"Error al cargar la máscara: {mask_path}")
        continue

    # Crear una máscara en blanco para llenar los contornos
    filled_mask = np.zeros_like(mask)
    
    # Encontrar y llenar los contornos
    contours = get_contours(mask)
    cv2.drawContours(filled_mask, contours, -1, 255, thickness=cv2.FILLED)
    
    # Verificar si hay más de un contorno, y aplicar filtros si es necesario
    while True:
        # Obtener los contornos después de llenar la máscara
        contours = get_contours(filled_mask)
        print(f"Contornos encontrados en    {img_name}: {len(contours)}")
        
        # Si solo hay un contorno, guardar y pasar a la siguiente imagen
        if len(contours) == 1:
            break
        else:
            # Aplicar filtros de dilatación y cierre morfológico si hay más de un contorno
            filled_mask = apply_filters(filled_mask)

    # Guardar la máscara unificada en la carpeta de salida
    output_path = os.path.join(output_folder, img_name)
    cv2.imwrite(output_path, filled_mask)
    print(f"Máscara unificada guardada en: {output_path}")

print("Las imágenes con contornos unificados se han guardado en 'truchas GTv4'.")
