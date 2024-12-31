import os
import shutil
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
from typing import List, Set
import logging
import imagehash
from concurrent.futures import ThreadPoolExecutor

# Configurazione logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ImageDuplicateRemover")

def check_dependencies() -> bool:
    """Verifica che tutte le dipendenze necessarie siano installate."""
    try:
        import skimage
        import PIL
        import numpy
        import imagehash
        return True
    except ImportError as e:
        logger.error(f"Dipendenza mancante: {str(e)}")
        return False

def calculate_similarity(image1: Image.Image, image2: Image.Image) -> float:
    """Calcola la similarità tra due immagini usando SSIM."""
    try:
        # Convert images to grayscale for SSIM
        image1_gray = image1.convert("L")
        image2_gray = image2.convert("L")

        # Resize images to the same dimensions
        size = (256, 256)
        image1_resized = image1_gray.resize(size)
        image2_resized = image2_gray.resize(size)

        # Convert images to numpy arrays
        array1 = np.array(image1_resized)
        array2 = np.array(image2_resized)

        # Calculate SSIM
        score, _ = ssim(array1, array2, full=True)
        return score
    except Exception as e:
        logger.error(f"Errore nel calcolo della similarità: {str(e)}")
        return 0.0

def calculate_hash(image_path: str) -> str:
    """Calcola l'hash dell'immagine usando phash."""
    try:
        with Image.open(image_path) as img:
            return str(imagehash.phash(img))
    except Exception as e:
        logger.error(f"Errore nel calcolo dell'hash per {image_path}: {str(e)}")
        return ""

def move_representative_images(output_folder: str) -> None:
    """Estrae un'immagine da ciascuna cartella group_ e la sposta in non_similar_images."""
    non_similar_folder = os.path.join(output_folder, "non_similar_images")
    group_folders = [
        os.path.join(output_folder, folder) for folder in os.listdir(output_folder) if folder.startswith("group_")
    ]

    for group_folder in group_folders:
        try:
            images = [
                os.path.join(group_folder, file) for file in os.listdir(group_folder)
                if os.path.isfile(os.path.join(group_folder, file))
            ]
            if images:
                representative_image = images[0]
                destination_path = os.path.join(non_similar_folder, os.path.basename(representative_image))

                # Gestisce conflitti di nomi
                counter = 1
                while os.path.exists(destination_path):
                    name, ext = os.path.splitext(os.path.basename(representative_image))
                    destination_path = os.path.join(non_similar_folder, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.move(representative_image, destination_path)
                logger.debug(f"Spostata immagine {representative_image} in {destination_path}")

            # Rimuove la cartella group_
            shutil.rmtree(group_folder)
            logger.debug(f"Rimossa cartella {group_folder}")
        except Exception as e:
            logger.error(f"Errore durante l'elaborazione della cartella {group_folder}: {str(e)}")

def group_and_separate_images(input_folder: str, output_folder: str, similarity_threshold: float = 0.9) -> None:
    """Raggruppa le immagini simili in cartelle separate."""
    if not check_dependencies():
        logger.error("Dipendenze mancanti. Installare tutte le dipendenze necessarie.")
        return

    # Create output folders
    os.makedirs(output_folder, exist_ok=True)
    non_similar_folder = os.path.join(output_folder, "non_similar_images")
    os.makedirs(non_similar_folder, exist_ok=True)

    # Get list of valid images
    valid_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}
    images = [
        os.path.join(input_folder, file) 
        for file in os.listdir(input_folder) 
        if os.path.splitext(file.lower())[1] in valid_extensions
    ]

    if not images:
        logger.warning("Nessuna immagine valida trovata nella cartella di input.")
        return

    logger.debug(f"Trovate {len(images)} immagini valide.")

    # Calculate hashes for all images
    image_hashes = {}
    for image_path in images:
        logger.debug(f"Calcolando hash per {image_path}")
        image_hashes[image_path] = calculate_hash(image_path)

    grouped: List[List[str]] = []
    processed_images: Set[str] = set()

    for i, image_path1 in enumerate(images):
        if image_path1 in processed_images:
            continue

        try:
            with Image.open(image_path1) as image1:
                logger.debug(f"Elaborando immagine principale {image_path1}")
                group = [image_path1]
                processed_images.add(image_path1)

                for image_path2 in images[i+1:]:
                    if image_path2 in processed_images:
                        continue

                    try:
                        logger.debug(f"Confrontando {image_path1} con {image_path2}")
                        # Compare hashes first
                        if image_hashes[image_path1] != image_hashes[image_path2]:
                            logger.debug(f"Hash diversi, saltando {image_path2}")
                            continue

                        with Image.open(image_path2) as image2:
                            similarity = calculate_similarity(image1, image2)
                            logger.info(f"Similarità tra {image_path1} e {image_path2}: {similarity:.2f}")
                            if similarity >= similarity_threshold:
                                group.append(image_path2)
                                processed_images.add(image_path2)
                    except Exception as e:
                        logger.error(f"Errore nell'elaborazione dell'immagine {image_path2}: {str(e)}")
                        continue

                if len(group) > 1:
                    # Create group folder and copy images
                    group_folder = os.path.join(output_folder, f"group_{len(grouped) + 1}")
                    os.makedirs(group_folder, exist_ok=True)
                    for idx, img_path in enumerate(group):
                        try:
                            logger.debug(f"Copiando {img_path} in {group_folder}")
                            shutil.copy(img_path, os.path.join(group_folder, f"image_{idx + 1}{os.path.splitext(img_path)[1]}"))
                        except Exception as e:
                            logger.error(f"Errore nella copia dell'immagine {img_path}: {str(e)}")
                    grouped.append(group)
                else:
                    # Copy single image to non_similar folder
                    try:
                        logger.debug(f"Copiando immagine non simile {image_path1} in {non_similar_folder}")
                        shutil.copy(image_path1, os.path.join(non_similar_folder, os.path.basename(image_path1)))
                    except Exception as e:
                        logger.error(f"Errore nella copia dell'immagine {image_path1}: {str(e)}")

        except Exception as e:
            logger.error(f"Errore nell'elaborazione dell'immagine {image_path1}: {str(e)}")
            continue

    logger.info(f"Elaborazione completata. Gruppi creati: {len(grouped)}")
    
    # Sposta le immagini rappresentative e rimuove le cartelle group_
    move_representative_images(output_folder)

if __name__ == "__main__":
    try:
        script_folder = os.path.dirname(os.path.abspath(__file__))
        input_folder = os.path.join(script_folder, "input_images")
        output_folder = os.path.join(script_folder, "grouped_images")

        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
            print(f"La cartella di input è stata creata: {input_folder}")
            print("Inserisci le immagini nella cartella e riesegui lo script.")
            input("Premi Invio per chiudere...")
            exit()

        logger.debug(f"Cartella di input: {input_folder}, Cartella di output: {output_folder}")
        group_and_separate_images(input_folder, output_folder)
        input("Elaborazione completata. Premi Invio per chiudere...")
    except Exception as e:
        logger.critical(f"Errore critico: {str(e)}")
        input("Si è verificato un errore critico. Premi Invio per chiudere...")
