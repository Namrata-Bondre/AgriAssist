from database.connection import get_connection


def save_prediction(
    user_id,
    image_path,
    crop=None,
    disease=None,
    confidence=None,
    status="SUPPORTED",
    condition_text=None,
    severity=None,
    recommendation=None
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO Predictions
            (
                user_id,
                image_path,
                crop,
                disease,
                confidence,
                status,
                [condition],
                severity,
                recommendation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                user_id,
                image_path,
                crop,
                disease,
                confidence,
                status,
                condition_text,
                severity,
                recommendation
            )
        )

        connection.commit()
        print("Prediction saved successfully!")

    except Exception:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()