from math_notes import predict


def test_prediction_service():git 
    filename = "integral_to_transform.png"
    latex_return = predict.predict(filename)
    true_latex_string = "f(x)=\int_{a}^{x} t^{3}+1 d t"
    
    print("latex return", latex_return)
    print("true_latex_string", true_latex_string)
    
    assert latex_return == true_latex_string
