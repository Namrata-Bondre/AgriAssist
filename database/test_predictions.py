from predictions import save_prediction


def test_save_prediction():
    print("Testing save_prediction function...")

    save_prediction(
        1,
        "test_images/corn.jpg",
        "Corn",
        "Common Rust",
        98.45
    )


if __name__ == "__main__":
    test_save_prediction()