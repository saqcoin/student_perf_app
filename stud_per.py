import streamlit as st
import pandas as pd
# import numpy as np
import pickle
# from sklearn.preprocessing import LabelEncoder

# Load model
def load_model():
    with open("student_lr_final_model.pkl", 'rb') as model_file:
        model, scaler, le = pickle.load(model_file)
    return model, scaler, le

def preprocessing_input_data(data, scaler, le):
    data['Extracurricular Activities Encoded'] = le.fit_transform([data['Extracurricular Activities']])
    df = pd.DataFrame([data])
    # drop column not used during model generation
    df = df.drop('Extracurricular Activities', axis='columns')
    # reorder the columns
    df = df.iloc[:, [0, 1, 4, 2, 3]]
    df_transformed = scaler.transform(df)
    return df_transformed

def predict_data(data):
    model, scaler, le = load_model()
    processed_data = preprocessing_input_data(data, scaler, le)
    prediction = model.predict(processed_data)
    return prediction

def main():
    st.title("Student Perfomance Prediction")
    st.write("Enter your data to get prediction for your performance")

    # make input fields
    hours_studied = st.number_input("Hours Studied", min_value = 1, max_value = 10, value = 5)
    prev_score = st.number_input("Previous Scores", min_value = 40, max_value = 100, value = 70)
    extra = st.selectbox("Extracurricular Activities", ["Yes", "No"])
    sleep_hours = st.number_input("Sleep Hours", min_value = 1, max_value = 20, value = 7)
    no_paper_solved = st.number_input("Sample Question Papers Practiced", min_value = 0, max_value = 10, value = 5) 

    # action button
    if st.button("Predict Your Score!"):
        user_data = {
            "Hours Studied" : hours_studied,
            "Previous Scores" : prev_score,
            "Extracurricular Activities" : extra,
            "Sleep Hours" : sleep_hours,
            "Sample Question Papers Practiced" : no_paper_solved
        }
        prediction = predict_data(user_data)
        st.success(f"Your predicted score in {prediction}")


if __name__ == "__main__":
    main()

