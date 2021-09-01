import base64

from math_notes.predict import predict

# def test_prediction_single():

#     filename = "tests/integral_to_transform_1.png"
#     true_latex_string = "f(x)=\\int_{a}^{x} t^{3}+1 d t"

#     image_uri = []
#     image_uri.append("data:image/png;base64," + base64.b64encode(open(filename, "rb").read()).decode())

#     latex_return = predict(image_uri)

#     assert latex_return[0] == true_latex_string


def test_prediction_multiple():
    filenames = [
        "tests/integral_to_transform_1.png",
        "tests/integral_to_transform_2.png",
        "tests/integral_to_transform_3.png",
    ]

    true_latex_strings = ["f(x)=\\int_{a}^{x} t^{3}+1 d t", "x^{2}+1=0", "a x+b=y"]

    image_uri = []
    for file in filenames:
        image_uri.append(
            "data:image/png;base64,"
            + base64.b64encode(open(file, "rb").read()).decode()
        )
    latex_returns = predict(image_uri)

    assert latex_returns == true_latex_strings
