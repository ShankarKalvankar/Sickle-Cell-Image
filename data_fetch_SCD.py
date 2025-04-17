import os
import pandas as pd
from PIL import Image
import random

# Define a function to process images and extract the required features
def process_images(folder_path):
    # Initialize an empty list to store the results
    results = []

    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp')):  # Check for valid image file types
            file_path = os.path.join(folder_path, filename)

            try:
                # Open the image (just to confirm it's valid, no actual processing here)
                image = Image.open(file_path)

                # Generate random values for the features (replace with real logic if available)
                total_rbcs = round(random.uniform(4.0, 6.5), 2)  # Random value for Total RBCs (in millions)
                sickled_cells = round(random.uniform(5.0, 25.0), 2)  # Random value for Sickled Cells (%)
                normocytes = round(random.uniform(60.0, 80.0), 2)  # Random value for Normocytes (%)
                target_cells = round(random.uniform(2.0, 10.0), 2)  # Random value for Target Cells (%)
                anisocytosis_severity = random.choice(["Mild", "Moderate", "Severe"])  # Random severity
                reticulocytes = round(random.uniform(10.0, 20.0), 2)  # Random value for Reticulocytes (%)

                # Append the data as a dictionary to the results list
                results.append({
                    "Filename": filename,
                    "Total RBCs (in millions)": total_rbcs,
                    "Sickled Cells (%)": sickled_cells,
                    "Normocytes (%)": normocytes,
                    "Target Cells (%)": target_cells,
                    "Anisocytosis Severity": anisocytosis_severity,
                    "Reticulocytes (%)": reticulocytes,
                    "Sickle Cell": "YES"  # Default value for Sickle Cell
                })
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    return results

data = {
    "Total RBCs (in millions)": 4.2,  # Normal range is typically 4.1–5.5 million/μL; often lower in sickle cell disease.
    "Sickled Cells (%)": 0.10,  # Sickle cell disease patients might have 20–50% sickled cells.
    "Normocytes (%)": 0.20,  # Normocytes might be reduced in sickle cell anemia.
    "Target Cells (%)": 0.90,  # Target cells are often seen in sickle cell anemia (elevated levels).
    "Anisocytosis Severity": 0.2,  # Scored from 0–4, with 0 being no anisocytosis and 4 being severe anisocytosis.
    "Reticulocytes (%)": 0.3,  # Reticulocyte count is often elevated (normal range is 0.5–2.5%).
}


# Path to the folder containing extracted images
folder_path = "C:/Users/shank/Desktop/ENGG PROJECTS/MAJOR PROJECT MAIN/FINALPROJECT/DATA/Positive/Unlabelled/output"  # Replace with the path to the extracted folder

# Process the images
data = process_images(folder_path)

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
output_csv = "image_features_SCD.csv"
df.to_csv(output_csv, index=False)

print(f"CSV file saved as {output_csv}")
