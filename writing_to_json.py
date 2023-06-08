import json



def writing_to_json_file(name_of_presentation:str, slides_explanations:list):
    """
     Writes slide explanations to a JSON file.

     :param name_of_presentation: The name of the presentation.
     :param slides_explanations: The list of slide explanations.
     :returns: None
     """
    with open(name_of_presentation + ".json", "w") as file:
        json.dump({"Slides": [{"Explaination": slide} for slide in slides_explanations if slide!=None]}, file,indent=4)
        print('a JSON file has saved in this directory.')
