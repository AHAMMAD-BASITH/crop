# import os
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import load_img, img_to_array

# # Load the trained model (Ensure this path is correct)
# MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xception_leaf_disease_model.h5")
# model = tf.keras.models.load_model(MODEL_PATH)

# # Load class labels from training folder
# CLASS_NAMES = sorted(os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "indian crop", "Train")))

# def predict_leaf_disease(image_path):
#     """
#     Predict the disease of a leaf image.
    
#     Parameters:
#     - image_path: str, path to the image file

#     Returns:
#     - predicted_class: str, name of the predicted disease
#     - confidence: float, confidence of the prediction
#     """

#     # Load and preprocess the image
#     img = load_img(image_path, target_size=(299, 299))  # Resize to match Xception input size
#     img_array = img_to_array(img) / 255.0  # Normalize pixel values
#     img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions for model input

#     # Predict using the trained Xception model
#     prediction = model.predict(img_array)
#     predicted_class = CLASS_NAMES[np.argmax(prediction)]  # Get the highest confidence class
#     confidence = np.max(prediction)  # Get confidence score

#     return predicted_class, confidence


# import os
# import numpy as np
# from PIL import Image
# from keras.models import load_model
# from keras.preprocessing.image import img_to_array


# # Define paths to the training data directory and the saved model
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Move up to project root
# train_data_dir = sorted(os.listdir(os.path.join(PROJECT_ROOT, "train")))  # ✅ Now correctly points to root "train"
# model_path = os.path.join(PROJECT_ROOT, "disclass.h5")  # ✅ Now correctly points to project root

# # Load the trained model
# model = load_model(model_path)

# # Define a function to preprocess the uploaded image
# def preprocess_image(image_path):
#     img = Image.open(image_path)
#     img = img.resize((224, 224))  # Resize to match the input size of the model
#     img = img_to_array(img) / 255.0  # Convert to numpy array and normalize pixel values
#     img = np.expand_dims(img, axis=0)  # Add batch dimension
#     return img

# # Define the function to automatically populate class labels
# def get_class_labels(data_dir):
#     class_labels = sorted(os.listdir(data_dir))
#     return class_labels

# # Get class labels from training data folders
# class_labels = get_class_labels(train_data_dir)

# # Define the predict_disease function
# def predict_disease(image_path):
#     try:
#         # Preprocess the uploaded image
#         processed_image = preprocess_image(image_path)

#         # Make predictions using the model
#         predictions = model.predict(processed_image)

#         # Get the predicted class label
#         predicted_class_index = np.argmax(predictions)
#         prediction_label = class_labels[predicted_class_index]

#         return prediction_label

#     except Exception as e:
#         print("Error:", e)
#         return "Error"

import os
import numpy as np
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import img_to_array

# Define paths to the training data directory and the saved model
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
train_data_dir = os.path.join(PROJECT_ROOT, "train")  # ✅ Correct path as a string
model_path = os.path.join(PROJECT_ROOT, "disclass.h5")  

# Check if model file exists before loading
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

# Load the trained model
model = load_model(model_path)
DISEASE_FERTILIZER_MAPPING = {
    # Apple
    "Apple___Black_rot": "Use a fungicide containing Mancozeb. Supplement with Nitrogen-rich fertilizers.",
    "Apple___Scab": "Apply Potassium and Phosphorus-based fertilizers. Captan fungicide also helps.",
    "Apple___healthy": "Maintain regular NPK balance (10-10-10) and organic compost.",
    
    # Corn
    "Corn___Cercospora_leaf_spot Gray_leaf_spot": "Apply Nitrogen-rich fertilizers. Tebuconazole fungicide recommended.",
    "Corn___Common_rust": "Use Sulfur-based sprays and boost with Phosphorus fertilizers.",
    "Corn___Northern_Leaf_Blight": "Use Potassium-rich fertilizers. Consider Azoxystrobin fungicide.",
    "Corn___healthy": "Balanced NPK (20-20-20) and proper irrigation is key.",
    
    # Grape
    "Grape___Black_rot": "Apply balanced NPK (12-24-12) and fungicides like Myclobutanil.",
    "Grape___Esca_(Black_Measles)": "Use low-Nitrogen, high-Phosphorus fertilizers. Copper fungicide also helps.",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Phosphorus and Potassium help resist the disease.",
    "Grape___healthy": "Maintain good Nitrogen and trace elements like Zinc and Iron.",
    
    # Tomato
    "Tomato___Late_blight": "Use potassium nitrate and copper-based fungicides.",
    "Tomato___Leaf_Mold": "Spray sulfur and ensure calcium-rich fertilizer is used.",
    "Tomato___Septoria_leaf_spot": "Use a foliar spray with high phosphorus. Avoid nitrogen overload.",
    "Tomato___healthy": "Balanced 5-10-10 fertilizer every 2 weeks.",
    
    # Peach
    "Peach___Bacterial_spot": "Use copper-based sprays and increase Calcium and Potassium levels.",
    "Peach___healthy": "Balanced fertilizers with Nitrogen, Phosphorus, and Potassium, and organic compost.",
    
    # Pepper (bell)
    "Pepper,_bell___Bacterial_spot": "Apply copper-based bactericides, and increase calcium and potassium.",
    "Pepper,_bell___healthy": "Fertilize with calcium nitrate and potassium sulfate.",
    
    # Potato
    "Potato___Early_blight": "Use potassium and calcium-rich fertilizer. Foliar fungicides are recommended.",
    "Potato___healthy": "NPK (15-15-15) and consistent watering.",
    "Potato___Late_blight": "Copper oxychloride, potassium phosphite foliar sprays.",
    
    # Strawberry
    "Strawberry___healthy": "Use NPK (12-12-17) with micronutrients.",
    "Strawberry___Leaf_scorch": "Use compost-based fertilizer, avoid over-watering.",
    
    # Soybean
    "Soybean___healthy": "Inoculated Rhizobium-based fertilizers (biofertilizers), phosphate boosters.",
    
    # Squash
    "Squash___Powdery_mildew": "Sulfur fungicides, boost potassium and magnesium.",
    
    # Raspberry
    "Raspberry___healthy": "Balanced NPK (10-10-10), and composted manure.",
    
    # Apple (continued)
    "Apple___Cedar_apple_rust": "Avoid high nitrogen; use fungicides (e.g., Myclobutanil).",
    
    # Cherry (including sour)
    "Cherry_(including_sour)___healthy": "Use balanced fertilizers (10-15-10).",
    "Cherry_(including_sour)___Powdery_mildew": "Use sulfur-based fungicides; ensure good potassium levels.",
    
    # Blueberry
    "Blueberry___healthy": "Acidic fertilizer (e.g., ammonium sulfate or urea), pH ~4.5–5.5.",
    
    # Orange
    "Orange___Haunglongbing_(Citrus_greening)": "Foliar sprays with zinc, manganese, magnesium; chelated micronutrients.",
    
    # Tomato (continued)
    "Tomato___Tomato_mosaic_virus": "No cure, but apply micronutrient mix to strengthen plant resistance.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Use chelated micronutrients (Fe, Mn, Zn), and neem-based sprays.",
    
    # Grape (continued)
    "Grape___Esca_(Black_Measles)": "Use low-Nitrogen, high-Phosphorus fertilizers. Copper fungicide also helps.",
    
    # Squash (continued)
    "Squash___Powdery_mildew": "Sulfur fungicides, boost potassium and magnesium."
}



# Define a function to preprocess the uploaded image
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))  # Resize to match the input size of the model
    img = img_to_array(img) / 255.0  # Convert to numpy array and normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Define the function to automatically populate class labels
def get_class_labels(data_dir):
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Training data directory not found: {data_dir}")
    
    class_labels = sorted(os.listdir(data_dir))
    return class_labels

# Get class labels from training data folders
class_labels = get_class_labels(train_data_dir)

#
def predict_disease(image_path):
    try:
        # Preprocess the uploaded image
        processed_image = preprocess_image(image_path)

        # Make predictions using the model
        predictions = model.predict(processed_image)

        # Get the predicted class label
        predicted_class_index = np.argmax(predictions)
        prediction_label = class_labels[predicted_class_index]

        # Split the label and get the last part (disease name)
        disease_name = prediction_label
        return disease_name

    except Exception as e:
        print("Error:", e)
        return "Error"
