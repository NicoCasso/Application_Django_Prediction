from predictor import Predictor

if __name__ == "__main__" :
    predictor = Predictor("serialized_model.pkl")

    prediction = predictor.predict(
        age=30, 
        sex="male", 
        bmi=29.0,
        children=2,
        smoker="yes", 
        region="southwest")
    
    print(prediction)