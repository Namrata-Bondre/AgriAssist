
from database.predictions import save_prediction

save_prediction(
    user_id=1,
    image_path="test_images/corn_leaf.jpg",
    crop="Corn",
    disease="Corn_Common_rust",
    confidence=95.50,
    status="SUPPORTED",
    condition_text="Disease detected",
    severity="Moderate",
    recommendation="Remove affected leaves and monitor crop health."
)
