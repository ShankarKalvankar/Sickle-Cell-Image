import streamlit as st
import base64
from PIL import Image
import os

# Function to convert image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set page configuration
st.set_page_config(
    page_title="Sickle Cell Prediction App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title Section
st.markdown(
    "<div style='text-align: center;'><h1 style='color:Lime;'>SICKLE CELL PREDICTION APP</h1></div>",
    unsafe_allow_html=True,
)

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

    chatbot_icon_path = "chatbot_icon.png"  # Update with your actual chatbot icon image path
    if os.path.exists(chatbot_icon_path):
        st.image(chatbot_icon_path, width=50)  # Adjust the width to decrease the size of the icon
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

# Main Content
with st.container():
    st.markdown("<h2 style='color:Olive;'>Introduction</h2>", unsafe_allow_html=True)
    st.write(
        """
        Sickle Cell Disease (SCD) is a group of inherited red blood cell disorders that affect millions of people worldwide.
        In individuals with SCD, red blood cells, which are typically round and flexible, become rigid and shaped like a crescent or "sickle." 
        These abnormally shaped cells can block blood flow, leading to pain, organ damage, and increased risk of infection. 
        SCD is a lifelong condition that requires ongoing management and care.
        """
    )

    col1, col2 = st.columns(2)
    imwidth = 800
    image_height = 400
    with col1:
        img1 = Image.open("SCP.jpg")  # Adjust path as needed
        img1 = img1.resize((imwidth, image_height))
        st.image(img1, caption="Sickle Cell")

    with col2:
        img2 = Image.open("RBC.jpg")  # Adjust path as needed
        img2 = img2.resize((imwidth, image_height))
        st.image(img2, caption="Regular Blood Cell")

# Additional content
with st.container():
    st.markdown("<h2 style='color:Beige;'>How Sickle Cell Forms ?</h2>", unsafe_allow_html=True)
    st.video(
        "What is Sickle Cell Anemia - American Society of Hematology (720p, h264).mp4", 
        "rb"
    )

# News Section
with st.container():
    st.markdown("<h2 style='color:Turquoise;'>News</h2>", unsafe_allow_html=True)
    st.image("NEWSs.png", use_column_width=True)
    st.image("NEWS3.png", use_column_width=True)
    st.image("NEWS2.png", caption="Recent Research", use_column_width=True)

# Background and Animation
image_path = "blood.jpg"  # Replace with your actual image path
base64_image = get_base64_image(image_path)

# Apply custom CSS to add a background image and animate all images
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    img {{
        transition: transform 0.3s ease; /* Smooth animation */
    }}
    img:hover {{
        transform: scale(1.1); /* Zoom effect on hover */
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3); /* Optional shadow effect */
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# How to Predict Sickle Cell Section
with st.container():
    st.markdown("<h2 style='color:Orange;'>How Predict Sickle Cell ?</h2>", unsafe_allow_html=True)
    st.write(
        """
        Our app leverages advanced machine learning models to predict the likelihood of Sickle Cell Disease from microscopic blood smear images. Follow these steps to use the prediction tool:
        1. Upload a high-quality image of the blood smear.
        2. Click the "Predict" button to analyze the image.
        3. View the results, which include the likelihood of Sickle Cell Disease and recommendations for further testing.
        
        **Note:** Ensure the image is clear and well-lit for accurate predictions. 
        """
    )
    