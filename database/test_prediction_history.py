# =====================================================
# Test Prediction History
# Tests whether prediction history can be fetched.
# =====================================================

from prediction_history import get_prediction_history


# User ID whose prediction history we want to check
user_id = 1


# Get prediction history from database
history = get_prediction_history(user_id)


# Display the result
print("Prediction History:")

if history:
    for prediction in history:
        print(prediction)
else:
    print("No prediction history found.")