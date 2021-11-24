import requests
import json

import config as cfg

app_id = cfg.APP_ID
app_key = cfg.APP_KEY


def ocr_request(image):
    """Sends an API request to MathPix API to be handled by the OCR.

    :param filename: Dictionary with the filename of the image to be sent to the MathPix API for a LaTeX prediction.
    :type filename: dict

    :return: Latex-formatted string.
    :rtype: str
    """

    # Send the request.
    r = requests.post(
        "https://api.mathpix.com/v3/text",
        data=json.dumps({"src": image}),
        headers={
            "app_id": app_id,
            "app_key": app_key,
            "Content-type": "application/json",
        },
    )

    json_return = json.loads(r.text)
    latex_return = json_return.get("latex_styled")

    return latex_return


def predict(images):
    """Receives images to send to the prediction service.

    :param images: List with base64 enconded images as pngs.
    :type images: [bytes]

    :return: List of Latex-formatted strings.
    :rtype: [str]
    """

    latex_results = []
    for image in images:
        # Any image pre-processing necessary is done here.
        latex_return = ocr_request(image)
        latex_results.append(latex_return)

    return latex_results
