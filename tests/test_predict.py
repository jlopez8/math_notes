import base64

from math_notes.predict import predict

def test_prediction_service():

    filename = "tests/integral_to_transform.png"
    
    image_uri = []
    image_uri.append("data:image/png;base64," + base64.b64encode(open(filename, "rb").read()).decode())
    
    latex_return = predict(image_uri)
    true_latex_string = "f(x)=\\int_{a}^{x} t^{3}+1 d t"
    
    assert latex_return[0] == true_latex_string
    
# maybe test an array of images


# if you send a blank image what happens and send this

