from database.connection import get_connection

def save_prediction(user_id, image_path, crop, disease, confidence):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Predictions
        (user_id, image_path, crop, disease, confidence)
        VALUES (?, ?, ?, ?, ?)
    """

    cursor.execute(
        query,
        (user_id, image_path, crop, disease, confidence)
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("Prediction saved successfully!")