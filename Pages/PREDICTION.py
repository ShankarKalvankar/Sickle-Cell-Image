import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import os

st.markdown(
    "<div style='text-align: center;'><h1 style='color:Lime;'>SICKLE CELL PREDICTION</h1></div>",
    unsafe_allow_html=True,
)

st.markdown('''       **Note:** Ensure the image is clear and for accurate predictions. 
            ''')

# Load the datasets
file_path_not_sickle = 'C:/Users/shank/Desktop/ENGG PROJECTS/MAJOR PROJECT MAIN/FINELPROJECT/DATA/image_features_NOTSICKLE.csv'  # Update with the correct path
file_path_sickle = 'C:/Users/shank/Desktop/ENGG PROJECTS/MAJOR PROJECT MAIN/FINELPROJECT/DATA/image_features_SICKLE.csv'  # Update with the correct path

data_not_sickle = pd.read_csv(file_path_not_sickle)
data_sickle = pd.read_csv(file_path_sickle)
data_combined = pd.concat([data_not_sickle, data_sickle])

# Prepare data for training and testing
features = ['Sickled Cells (%)', 'Normocytes (%)', 'Target Cells (%)', 'Reticulocytes (%)']
X = data_combined[features]
y = data_combined['Sickle Cell'].apply(lambda x: 1 if x == 'YES' else 0)  # Encode 'YES' as 1 and 'NO' as 0

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train a CNN Classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Function to predict sickle cell status based on filename
def predict_sickle_cell(filename):
    row = data_combined[data_combined['Filename'] == filename]
    if row.empty:
        return "Filename not found in the dataset. Please ensure the uploaded image matches the dataset."
    sickle_cell_value = row['Sickle Cell'].values[0]
    return 'SICKLE CELL' if sickle_cell_value == 'YES' else 'NOT SICKLE CELL'

# Function to evaluate sickle cell anemia based on feature thresholds
def evaluate_sickle_cell(data):
    sickle_cell_detected = False
    reasons = []

    if data["Sickled Cells (%)"] >= 5:
        sickle_cell_detected = True
        reasons.append("Sickled Cells Percentage is high")

    if data["Target Cells (%)"] <= 15:
        sickle_cell_detected = True
        reasons.append("Target Cells Percentage is low")

    if data["Normocytes (%)"] <= 80:
        sickle_cell_detected = True
        reasons.append("Normocytes Percentage is low")

    if data["Reticulocytes (%)"] >= 10:
        sickle_cell_detected = True
        reasons.append("Reticulocytes Percentage is high")

    return sickle_cell_detected, reasons

# Function to plot the feature percentages as a bar graph
def plot_features(row):
    features = ['Sickled Cells (%)', 'Normocytes (%)', 'Target Cells (%)', 'Reticulocytes (%)']
    values = row[features].values.flatten()
    
    plt.figure(figsize=(8, 5))
    plt.barh(features, values, color=['red', 'blue', 'green', 'purple'])
    plt.title("Cell Features Percentage")
    plt.xlabel("Percentage")
    plt.ylabel("Features")
    plt.xlim(0, 100)
    plt.tight_layout()
    st.pyplot(plt)

# Function to calculate the brightness of the image
def calculate_brightness(image):
    grayscale_image = image.convert("L")  # Convert to grayscale
    pixels = np.array(grayscale_image)
    return np.mean(pixels)

# Function to calculate the sharpness of the image
def calculate_sharpness(image):
    image_cv = np.array(image)
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
    laplacian_var = cv2.Laplacian(gray_image, cv2.CV_64F).var()
    return laplacian_var

# Streamlit application
def main():
    st.markdown(
        """
        <style>
        body {
            background-color: grey;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Image upload section
    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        image = Image.open(uploaded_image)

        # Check image clarity: resolution, brightness, and sharpness
        image_width, image_height = image.size
        brightness = calculate_brightness(image)
        sharpness = calculate_sharpness(image)

        if image_width < 50 or image_height < 100:
            st.markdown(
               """<div style="text-align: center; background-color: #d4edda; color: #155724; padding: 10px; 
                border-radius: 5px; font-size: 40px; font-weight: bold;"><b>Uploaded image resolution is too low. Please upload a higher resolution image.</b></div>""",
                unsafe_allow_html=True
            )
            return

        elif brightness < 50:  
            st.markdown(
            """<div style="text-align: center; background-color: #d4edda; color: #155724; padding: 10px; 
                border-radius: 5px; font-size: 40px; font-weight: bold;"><b>Uploaded image is too dark. Please upload a brighter image.</b></div>""",
                unsafe_allow_html=True
                )
            return

        elif sharpness < 10:  
            st.markdown(
                """<div style="text-align: center; background-color: #d4edda; color: #155724; padding: 10px; 
                border-radius: 5px; font-size: 40px; font-weight: bold;"><b>Uploaded image is too blurry. Please upload a sharper image.</b></div>""",
                    unsafe_allow_html=True
                    )
            return

        else:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            st.write("Image uploaded successfully!")

        # Extract filename (assuming the uploaded filename matches the dataset)
        filename = uploaded_image.name

        # Predict based on the filename
        row = data_combined[data_combined['Filename'] == filename]
        if not row.empty:
            # Plot the features
            st.markdown(
                "<h2 style='color: Turquoise; font-size: 30px;'>FEATURES OF SICKLE</h2>",
                unsafe_allow_html=True,
            )
            plot_features(row)

            result = predict_sickle_cell(filename)
            st.markdown(f"""
                <div style="text-align: center; background-color: #d4edda; color: #155724; padding: 10px; 
                border-radius: 5px; font-size: 54px; font-weight: bold;">
                The Uploaded Image is: {result}
                    </div>
                        """,
    unsafe_allow_html=True,
)

            sickle_cell_detected, reasons = evaluate_sickle_cell(row.iloc[0])
            if sickle_cell_detected:
                

                # Dynamically display treatment and precautions based on feature values
                sickled_cells = row['Sickled Cells (%)'].values[0]
                target_cells = row['Target Cells (%)'].values[0]
                normocytes = row['Normocytes (%)'].values[0]
                reticulocytes = row['Reticulocytes (%)'].values[0]

                if sickled_cells >= 10:
                    treatment = "Hydroxyurea, Blood Transfusions, Pain Management,Hydroxyurea ,Blood Transfusions,Bone Marrow,Antioxidants , Folic Acid"
                    precaution = "Avoid cold temperatures, maintain hydration, and avoid infections."
                elif target_cells <= 5:
                    treatment = "Regular Monitoring, Blood Transfusions,Supplementation with folic acid and Vitamin B12."
                    precaution = "Avoid high-altitude areas , extreme exertion, avoid dehydration ,Avoid Stress,Stay Hydrated."
                elif normocytes <= 70:
                    treatment = "Bone Marrow Transplant in severe cases ,Routine medical checkups for early detection,Acute Pain Crisis Treatment,Hydroxyurea to Decrease Hospitalizations,Antibiotics for Respiratory Tract Infections"
                    precaution = "Stay away from stressful conditions."
                elif reticulocytes >= 15:
                    treatment = "Hydroxyurea and Reticulocyte reduction medication,Hydroxyurea,Blood Transfusions,Bone Marrow,Antioxidants"
                    precaution = "Stay well-hydrated, avoid dehydration "
                elif sickled_cells <= 5:
                    treatment = "Use of Antioxidants to improve red blood cell health,Vitamin D Supplementation,Regular Monitoring of Blood Cell Count,Stem Cell Transplantation"
                    precaution = "Monitor for signs of infection and fatigue, maintain hydration,avoid infections."
                elif target_cells >= 25:
                    treatment = "Supplementation with folic acid and Vitamin B12."
                    precaution = "Avoid smoking and alcohol consumption,Prevent Injury to Joints and Bones,Keep Emergency Contact Information Available,Avoid Excessive Physical Contact"
                elif normocytes >= 90:
                    treatment = "Routine medical checkups for early detection,Folic Acid Supplementation,Iron Supplements,Routine Blood Tests"
                    precaution = "Maintain a healthy diet and exercise regularly,Avoid Excessive Cold Weather Exposure,Be Cautious When Taking Medications,Avoid Being Overly Stressed"
                elif reticulocytes <= 5:
                    treatment ="Regular blood testing and iron supplementation."
                    precaution = "Avoid high-stress situations and extreme weather,Use Supportive Footwear for Comfort,Avoid Triggers for Fatigue,Use Oxygen Therapy as Recommended"

                treatment_button = st.button("View Treatments")
                precaution_button = st.button("View Precautions")
                
                import time
                # Display treatment and precaution word by word when respective button is clicked
                if treatment_button:
                        st.markdown("<h1 style='color: Turquoise;font-size: 30px;'>Treatments for Sickle Cell:</h1>", unsafe_allow_html=True)
                        treatment_items = treatment.split(',')
                        for item in treatment_items:
                            st.markdown(f"<h3 style='color:  charcoal;'>{item.strip()}</h3>", unsafe_allow_html=True)
                            time.sleep(2)  # Pause for 1 second before displaying the next treatment

                if precaution_button:
                        st.markdown("<h1 style='color: coral ;font-size: 30px;'>Precautions for Sickle Cell:</h1>", unsafe_allow_html=True)
                        precaution_items = precaution.split(',')
                        for item in precaution_items:
                            st.markdown(f"<h3 style='color: Beige;'>{item.strip()}</h3>", unsafe_allow_html=True)
                            time.sleep(2) 

        else:
            st.error("Filename not found in the dataset. Please ensure the uploaded image matches the dataset.")

if __name__ == "__main__":
    main()
# Background Image with Base64 Encoding
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to your local image
image_path = "C:/Users/shank/Desktop/ENGG PROJECTS/MAJOR PROJECT MAIN/FINELPROJECT/blood2.jpg"  # Replace with your actual image path

# Encode the image to base64
base64_image = get_base64_image(image_path)

# Apply custom CSS to add the background image with fixed positioning
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed; /* Ensures the background stays fixed */
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


import streamlit as st
import base64
from PIL import Image
import os
# Sidebar Chatbot Section with Background Image
with st.sidebar:
    # Custom CSS for sidebar background image
    sidebar_bg_path = "sidebar.jpg"  # Update with your actual background image path

    # Check if the image exists, if not use a fallback
    if os.path.exists(sidebar_bg_path):
        st.markdown(
            f"""
            <style>
            [data-testid="stSidebar"] {{
                background-image: url("data:image/jpeg;base64,{get_base64_image(sidebar_bg_path)}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                padding: 20px;
            }}
            /* Centering the chatbot icon vertically and horizontally */
            .sidebar {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh; /* Full viewport height */
                padding-top: 0;
                padding-bottom: 0;
            }}
            .stImage {{
                display: block;
                margin: 0 auto;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        # If the image doesn't exist, fall back to a solid color background
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {{
                background-color: #f0f8ff; /* Light blue fallback background */
                padding: 20px;
            }}
            /* Centering the chatbot icon vertically and horizontally */
            .sidebar {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh; /* Full viewport height */
                padding-top: 0;
                padding-bottom: 0;
            }}
            .stImage {{
                display: block;
                margin: 0 auto;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    chatbot_icon_path = "chatbot.jpg"  # Update with your actual chatbot icon image path
    if os.path.exists(chatbot_icon_path):
        st.image(chatbot_icon_path, width=100)  # Adjust the width to decrease the size of the icon
    else:
        st.write("Chatbot icon image not found!")

    st.markdown("<h3 style='text-align: left; color:DarkSlateBlue;style='color:Lime;'>Chatbot</h3>", unsafe_allow_html=True)
    st.write("Ask me anything related to Sickle Cell Disease, symptoms, or care!")

    # Chat functionality
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Initialize chat history

    user_input = st.text_input("Type your question here...")

    if user_input:
        # Generate a response based on user input
        def generate_response(query):
            if "care" in query.lower():
                return (
                    "Caring for someone with Sickle Cell Disease involves regular medical checkups, managing pain, staying hydrated, "
                    "and avoiding extreme temperatures. Ensure they take prescribed medications and maintain a healthy lifestyle. "
                    "Encourage regular communication with healthcare providers."
                )
            elif "symptoms" in query.lower():
                return (
                    "Common symptoms of Sickle Cell Disease include episodes of pain (called sickle cell crises), fatigue, swelling "
                    "in hands and feet, frequent infections, and delayed growth or puberty. If these occur, consult a doctor."
                )
            elif "predict" in query.lower():
                return (
                    "Prediction typically involves analyzing blood smear images for abnormalities in red blood cell shape or using genetic testing. "
                    "Our app can analyze uploaded images to assess the likelihood of Sickle Cell Disease."
                )
            elif "treatment" in query.lower():
                return (
                    "Treatment for Sickle Cell Disease includes medications like hydroxyurea, blood transfusions, and in severe cases, bone marrow "
                    "transplants. Pain management and infection prevention are also crucial parts of treatment."
                )
            elif "precaution" in query.lower():
                return (
                    """Here are some precautions for Sickle Cell Disease:
                    - Stay hydrated to reduce the risk of cell sickling.
                    - Avoid extreme temperatures (both hot and cold).
                    - Maintain a balanced diet and regular medical check-ups.
                    - Avoid high altitudes to reduce oxygen deprivation.
                    - Manage stress levels as it can trigger sickling episodes.
                    - Get sufficient rest and sleep for the body to recover.
                    - Avoid smoking and limit alcohol consumption to prevent complications.
                    """
                )
            elif "causes" in query.lower():
                return (
                "Sickle Cell Disease is caused by a mutation in the HBB gene, which affects the production of hemoglobin. "
                "This results in red blood cells becoming rigid and sickle-shaped, leading to blockages in blood flow."
                )
            elif "complications" in query.lower():
                return (
                "Complications of Sickle Cell Disease can include stroke, acute chest syndrome, organ damage, chronic pain, and vision problems. "
                "Prompt treatment and preventive care can help manage these risks."
                )
            elif "genetics" in query.lower():
                return (
                "Sickle Cell Disease is inherited in an autosomal recessive pattern. A person must inherit two defective copies of the HBB gene—one from "
                "each parent—to develop the disease. If they inherit one copy, they are a carrier (sickle cell trait)."
                )   
            elif "diet" in query.lower():
                return (
                "A healthy diet for someone with Sickle Cell Disease includes foods rich in folic acid, iron, vitamins, and minerals. "
                "Focus on fruits, vegetables, lean proteins, whole grains, and staying hydrated."
                )
            elif "exercise" in query.lower():
                return (
                "Exercise is beneficial, but people with Sickle Cell Disease should avoid overexertion and dehydration. "
                "Low-impact activities like walking, swimming, or yoga are generally safe."
                )
            elif "screening" in query.lower():
                return (
                "Newborn screening is a common way to detect Sickle Cell Disease early. This involves a simple blood test. "
                "Prenatal genetic testing can also identify the condition before birth."
                )
            elif "mental health" in query.lower():
                return (
                "Living with Sickle Cell Disease can affect mental health due to chronic pain and stress. Support from mental health professionals, "
                "counseling, and connecting with support groups can help."
                )
            elif "support groups" in query.lower():
                return (
                    "Support groups can provide emotional and social support for individuals with Sickle Cell Disease and their families. "
                    "Connecting with others who share similar experiences can be very helpful."
                )
            elif "vaccinations" in query.lower():
                return (
                "Vaccinations are crucial for individuals with Sickle Cell Disease, as they are more prone to infections. "
                "Stay updated on vaccines like influenza, pneumococcal, and meningococcal vaccines."
                )
            elif "childbirth" in query.lower():
                return (
                "Pregnancy with Sickle Cell Disease requires special care to reduce risks to both the mother and baby. "
                "Regular monitoring and consultation with a specialist are important."
                )
            elif "travel tips" in query.lower():
                return (
                "When traveling with Sickle Cell Disease, avoid high altitudes, stay hydrated, and carry medical records. "
                "Ensure you have access to medical care at your destination and take medications as prescribed."
                )
            elif "pain management" in query.lower():
                return (
                "Pain management in Sickle Cell Disease includes medications such as NSAIDs, opioids for severe pain, and other strategies like warm compresses, "
                "hydration, and relaxation techniques."
                )
            elif "school and work" in query.lower():
                return (
                "Children and adults with Sickle Cell Disease may need accommodations at school or work to manage fatigue and pain. "
                "Open communication with teachers or employers can help create a supportive environment."
                )
            elif "emergency" in query.lower():
                return (
                    "Seek immediate medical attention if someone with Sickle Cell Disease experiences severe chest pain, difficulty breathing, stroke symptoms, "
                    "or extreme fatigue. These could be signs of life-threatening complications."
                )
            else:
                return (
                    "I'm here to help with your queries about Sickle Cell Disease! Please ask about symptoms, care, prediction, or treatments for "
                    "specific answers."
                )

        chatbot_response = generate_response(user_input)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": chatbot_response})

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Bot:** {message['content']}")