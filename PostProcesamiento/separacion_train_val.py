import os
import random
import shutil

# Ruta de la carpeta principal
current_dir = os.path.dirname(os.path.abspath(__file__))

# Directorios de imágenes y etiquetas
images_dir = os.path.join(current_dir, 'images')
labels_dir = os.path.join(current_dir, 'labels')

# Crear carpetas de salida para train y val
output_dirs = {
    'train': {
        'images': os.path.join(current_dir, 'train', 'images'),
        'labels': os.path.join(current_dir, 'train', 'labels')
    },
    'val': {
        'images': os.path.join(current_dir, 'val', 'images'),
        'labels': os.path.join(current_dir, 'val', 'labels')
    }
}

# Crear las carpetas si no existen
for dir_type, paths in output_dirs.items():
    os.makedirs(paths['images'], exist_ok=True)
    os.makedirs(paths['labels'], exist_ok=True)

# Obtener todos los nombres de archivos de imágenes (sin extensión)
image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png'))]
image_basenames = [os.path.splitext(f)[0] for f in image_files]

# Definir el porcentaje de datos para validación
val_split = 0.2  # 20% para validación

# Particionar al azar
random.shuffle(image_basenames)
val_size = int(len(image_basenames) * val_split)
val_files = image_basenames[:val_size]
train_files = image_basenames[val_size:]

# Función para copiar archivos
def copy_files(files, dataset_type):
    for basename in files:
        # Copiar imagen
        for ext in ['.jpg', '.png']:
            image_path = os.path.join(images_dir, f"{basename}{ext}")
            if os.path.exists(image_path):
                shutil.copy(image_path, output_dirs[dataset_type]['images'])
                break

        # Copiar etiqueta
        label_path = os.path.join(labels_dir, f"{basename}.txt")
        if os.path.exists(label_path):
            shutil.copy(label_path, output_dirs[dataset_type]['labels'])

# Copiar archivos a las carpetas correspondientes
copy_files(train_files, 'train')
copy_files(val_files, 'val')

print("Partición completada: archivos copiados a 'train' y 'val'")
