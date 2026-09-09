# =====================================================
# Test Prediction Data Layer
# Tests saving an ML prediction into the database.
# =====================================================

from predictions import save_prediction


# User ID of the user making the prediction
user_id = 1

# Image used for prediction
image_path = "uploads/corn_image.jpg"

# Prediction result from ML model
crop = "Corn"
disease = "Common Rust"
confidence = 98.45


# Save prediction into the database
save_prediction(
    user_id,
    image_path,
    crop,
    disease,
    confidence
)

print("✅ Prediction Test Completed")