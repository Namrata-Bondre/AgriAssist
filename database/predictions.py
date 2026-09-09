# =====================================================
# Prediction Data Layer
# Handles saving ML prediction results
# into the Predictions table.
# =====================================================

from connection import connection


# =====================================================
# Save Prediction
# Saves one ML prediction into the database.
# =====================================================

def save_prediction(user_id, image_path, crop, disease, confidence):
    """
    Saves one ML prediction into the Predictions table.
    """

    # Create a cursor to execute SQL commands
    cursor = connection.cursor()

    # SQL query to insert prediction data
    query = """
        INSERT INTO Predictions
        (user_id, image_path, crop, disease, confidence)
        VALUES (?, ?, ?, ?, ?)
    """

    # Execute query with prediction values
    cursor.execute(
        query,
        user_id,
        image_path,
        crop,
        disease,
        confidence
    )

    # Save changes permanently in the database
    connection.commit()

    # Close the cursor
    cursor.close()

    print("✅ Prediction Saved Successfully")