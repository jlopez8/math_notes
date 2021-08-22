# Test_config.py

from math_notes.configs import keys.txt

def ocr_request(filename):
    """Sends an API request to MathPix API to be handled by the OCR .
    
    :param filename: Dictionary with the filename of the image to be sent to the MathPix API for a LaTeX prediction.
    :type filename: dict
 
    :return: Latex-formatted string.
    :rtype: str
    """
    
    dict_request={
            "src": "data:image/png",
            "formats": ["text", "data", "html"],
            "data_options": {
            "include_asciimath": True,
            "include_latex": True
            }
        }

    # Put desired filename from earlier.
    file_path = filename
    image_uri = "data:image/png;base64," + base64.b64encode(open(file_path, "rb").read()).decode()

    # Send the request.
    r = requests.post("https://api.mathpix.com/v3/text",
                      data=json.dumps({'src': image_uri}),
                      headers={"app_id": app_id, 
                               "app_key": app_key,
                               "Content-type": "application/json"})

    print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))
    
    json_return = json.loads(r.text)
    latex_return = json_return.get("latex_styled")
    
    print(latex_return)
    print()
    
    return latex_return

ocr_request("canvas_img_LKNB0E0.png")



