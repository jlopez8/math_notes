from math_notes import predict


def test_prediction_service():
    filename = "integral_to_transform.png"
    latex_return = predict(filename)
    
    print("latex return", latex_return)
    print("true_latex_string", true_latex_string)
    
    assert latex_return == true_latex_string
    
# maybe test an array of images


# if you send a blank image what happens and send this
