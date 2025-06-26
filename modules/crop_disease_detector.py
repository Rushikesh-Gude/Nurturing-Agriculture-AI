from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import random
import requests

# Load the model and class labels
# model = load_model(r"assets/new-model-with-wheat/keras_model.h5", compile=False)
# Define the raw URL to download the model
model_url = "https://github.com/nurturingagriculture/agri-app/raw/main/modules/keras_model.h5"
model_path = "keras_model.h5"

# Download the model if it doesn't exist
if not os.path.exists(model_path):
    response = requests.get(model_url)
    with open(model_path, "wb") as file:
        file.write(response.content)

# Load the model
model = load_model(model_path, compile=False)
class_names = open(r"assets/new-model-with-wheat/labels.txt", "r").readlines()

# Define remedy pairs: (remedy in English, remedy translation in Marathi)
remedy_pairs = [
    (
       "Enhance air circulation by spacing plants adequately and pruning dense foliage. This practice minimizes lingering moisture on leaves, ensuring rapid drying and reducing the favorable conditions for fungal pathogens.",
       "वनस्पतींमध्ये योग्य अंतर राखून आणि घनपड्या पानांची छाटणी करून हवेचा प्रवाह सुधारावा. या पद्धतीने पानांवरील ओलावा कमी होतो, ज्यामुळे फफूंदीजन्य रोगांच्या अनुकूल वातावरणात लवकर कोरडे होतात."
    ),
    (
       "Apply a broad-spectrum fungicide, preferably copper or sulfur-based, at the first sign of infection. Follow label recommendations, and reapply after heavy rains to consistently suppress fungal growth.",
       "पहिल्या लक्षणा दिसताच कॉपर किंवा सल्फर-आधारित व्यापक स्पेक्ट्रम फंगिसाइड लावा. लेबलवरील सूचना पाळा आणि पावसामुळे ओलावा वाढल्यास पुन्हा लावा जेणेकरून फंगसचा वाढ रोखता येईल."
    ),
    (
       "Implement a strategic crop rotation plan by avoiding the planting of similar crops in the same location each season. This disrupts the buildup of soil pathogens and minimizes recurring disease outbreaks.",
       "दर वर्षी सारखे पीक एका ठिकाणी न लावता पीकांची फेरबदल योजनेची अंमलबजावणी करा. या पद्धतीने मातीतील रोगाणूंचा संचय थांबतो आणि रोग पुनरावृत्ती कमी होते."
    ),
    (
       "Regularly inspect your plants for early signs of disease and promptly remove any infected leaves, stems, or fruits. Dispose of the affected material properly to prevent the spread of spores to healthy parts.",
       "पिकांवरील रोगाच्या लक्षणांची नियमित तपासणी करा आणि संक्रमित पानं, डाळिंब किंवा फळं लगेच काढून टाका. संक्रमित साहित्य योग्यरित्या नष्ट करा जेणेकरून रोगाणू निरोगी भागांमध्ये पसरू नयेत."
    ),
    (
       "Adopt targeted watering practices by using drip irrigation or soaker hoses to deliver water directly to the soil. This method keeps the foliage dry, thereby deterring the moisture-dependent spread of fungal infections.",
       "ड्रिप इरिगेशन किंवा सोकर होसेस वापरून पाण्याची योग्य पद्धतीने मातीमध्ये थेट पूरवठा करा. या पद्धतीने पानं कोरडी राहतात, ज्यामुळे फंगसचा ओलावावर अवलंबून प्रसार थांबतो."
    ),
    (
       "Focus on building healthy soil by incorporating organic compost and ensuring excellent drainage. A well-nourished and well-drained soil environment boosts the plant’s natural defenses against infections.",
       "जैविक कंपोस्ट मिसळून आणि उत्तम ड्रेनेज सुनिश्चित करून मातीची गुणवत्ता सुधारावी. चांगल्या पोषणयुक्त आणि व्यवस्थित निचरा असलेल्या मातीमुळे पिकांची नैसर्गिक रोगप्रतिकारक क्षमता वाढते."
    ),
    (
       "When available, choose plant varieties known for their resistance to fungal pathogens. Resistant cultivars can substantially reduce the impact of diseases, making overall plant care more effective.",
       "उपलब्ध असल्यास, फफूंदीजन्य रोगांपासून प्रतिकारक्षम असे पीक प्रकार निवडा. रोगप्रतिकारक किस्मांमुळे रोगांचा परिणाम कमी होतो आणि एकूणच पिकांची काळजी घेणे सोपे जाते."
    ),
    (
       "Use a layer of organic mulch around the base of your plants to curb soil splashing during rain. Mulching helps maintain a stable moisture level in the soil and minimizes the transfer of soil-borne pathogens to foliage.",
       "पिकांच्या तळाशी जैविक मल्च लावा ज्यामुळे पावसामुळे मातीचा उड्या पडण्याचा त्रास कमी होईल. मल्चिंगमुळे मातीतील ओलावा स्थिर राहतो आणि मातीतील रोगाणूंचा प्रसार पानांपर्यंत मर्यादित राहतो."
    ),
    (
       "Sanitize all gardening tools regularly by cleaning and disinfecting them between uses. This routine is essential to stop the inadvertent spread of pathogens from one plant to another during routine care.",
       "सर्व बागकामाच्या उपकरणांची नियमितपणे स्वच्छता आणि निर्जंतुकीकरण करा. या प्रक्रियेने एका वनस्पतीवरून दुसऱ्या वनस्पतीपर्यंत रोगाणूंचा अनपेक्षित प्रसार थांबतो."
    )
]

def preprocess_image(image):
    """Preprocess the input image to the format required by the model."""
    size = (224, 224)
    # Convert image to RGB to handle images with an alpha channel (e.g. RGBA)
    image = image.convert("RGB")
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1  # Normalize between -1 and 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    return data

def predict_crop_disease(image):
    """
    Predict the disease of the given crop image.
    
    Parameters:
        image (PIL.Image): The crop image to analyze.
    
    Returns:
        dict: Contains the predicted disease, confidence score, alternative predictions,
              and treatment recommendations if applicable.
    """
    # Preprocess the image
    data = preprocess_image(image)

    # Make a prediction
    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]
    
    # Prepare the result
    result = {
        "disease": class_names[index].strip(),
        "confidence": confidence_score,
        "alternatives": []
    }
    
    # Find alternative predictions with lower confidence
    for i, score in enumerate(prediction[0]):
        if i != index and score > 0.1:  # Only include alternatives with confidence > 10%
            result["alternatives"].append({"disease": class_names[i].strip(), "confidence": score})
    
    # Define indices corresponding to infected diseases (non-healthy)
    # Healthy indices: 0, 2, 4 (Apple Healthy Leaf, Potato Healthy Leaf, Tomato Healthy Leaf)
    # Infected indices: 1, 3, 5 (Apple Rust Leaf, Potato Late Blight Leaf, Tomato Late Blight Leaf)
    infected_indices = [0,3,5,6]
    
    # If the detected disease is infected, add a treatment recommendation
    if index in infected_indices:
        remedy, remedy_translation = random.choice(remedy_pairs)
        result["remedy"] = remedy
        result["remedy_translation"] = remedy_translation
    
    return result
