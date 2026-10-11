from database.prediction_history import get_prediction_history


def test_prediction_history():
    print("Testing prediction history...")

    history = get_prediction_history(user_id=2)

    print("Prediction History:")

    for record in history:
        print(record)

    if not history:
        print("No prediction history found.")


if __name__ == "__main__":
    test_prediction_history()