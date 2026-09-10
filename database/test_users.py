from users import add_user


def test_add_user():
    print("Testing add_user function...")

    add_user(
        "Test User",
        "testuser@example.com",
        "9876543210"
    )


if __name__ == "__main__":
    test_add_user()