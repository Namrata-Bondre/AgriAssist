from database.prediction_history import get_prediction_history

def test_prediction_history():
    print("Testing prediction history...")

    history = get_prediction_history(1)

    for record in history:
        print(record)


if __name__ == "__main__":
    test_prediction_history()