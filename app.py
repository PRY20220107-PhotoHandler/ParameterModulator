import os
from flask import Flask, jsonify, request
import spacy
import classy_classification

app = Flask(__name__)

@app.route('/')
def world():
    return 'Hello World from Photo Handler Api!'

data = {
    "specific": ["a face with a bowlcut",
                 "a face with a curly hair",
                 "hair with bangs",
                 "a face with pink hair",
                 "a face with blue hair",
                 "a face with blonde hair",
                 "a face with short hair",
                 "a face with long hair",
                 "a face without hair",
                 "a face with blue eyes",
                 "a face with green eyes",
                 "a face with brown eyes",
                 "a face with big nose",
                 "a face with big eyes",
                 "a face with big mouth",
                 "a face with big eyebrows",
                 "a face with a small mouth",
                 "a face with a big forehead",
                 "a bearded face",
                 "a face with a mustache"],
    "medium": ["a freckled face",
               "a pimpled face",
               "a face full of pimples",
               "a face with many moles",
               "a face with some moles",
               "freckled face",
               "a happy face",
               "an annoying face",
               "an upset face",
               "an angry face",
               "a sad face",
               "an unhappy face",
               "a disappointed face",
               "a melancholy face",
               "a smiling face",
               "cheerful face",
               "a disgusted face",
               "an irritating face",
               "a surprised face",
               "a tired face"],
    "entangled": ["an old face",
                  "an elderly face",
                  "a kid face",
                  "a baby face",
                  "an adult face",
                  "a teen face",
                  "a male face",
                  "a female face",
                  "a young face",
                  "a wrinkled face",
                  "a face with botox",
                  "a made up face",
                  "grimacing face",
                  "a beauty face",
                  "an ugly face",
                  "a beautiful face",
                  "a handsome face",
                  "a misshapen face",
                  "a nasty face",
                  "an aged face"]
}

@app.route('/classifier', methods=['POST'])
def classifier():
    request_json = request.get_json()
    if request_json and 'text' in request_json:
        text = request.json['text']
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("text_categorizer", 
            config={
                "data": data,
                "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                "device": "cpu"
            }
        )
        result = nlp(text)._.cats
        category = max(result.keys(), key = lambda k: result[k])
        return jsonify({"category": category})
    else:
        return jsonify({"result": "No hay atributo text en el json"})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))