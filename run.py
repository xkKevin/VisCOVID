from handleData.analyze import analyze
from handleData.prepare import prepare 
from handleData.validation import valid_dirs
from handleData.components.element import AppendOthers
from handleData.parser.parser import Parser, get_parser
from handleData.compiler import Compiler
from pymongo import MongoClient
from handleData.utils import load_config
import json
from handleData.components.element import AppendOthers
from handleData.descriptions.default import get_default_descriptions

if __name__ == "__main__":
    db = MongoClient()['coronavirus_analysis']
    config = load_config()
    desc = {
        "name": "AppendOthers",
        "args": {
            "f": "lambda x: x"
        }
    }

    parser = get_parser()
    a = parser.jsonify_component_classes()
    descriptions = get_default_descriptions()
    with open("./main/static/json/componentClasses.json", "w") as fp:
        json.dump(a, fp)
    print(a)
    compiler = Compiler(db, config)   

    # with open("./handleData/parser/sample.json", "r") as fp:
    #     obj = json.load(fp)
    #     obj = parser.parse_file(obj)
    #     d = compiler.compile(obj['descriptions'][0])
    #     print(d)
    # component = AppendOthers({"f": "lambda x: x"})
    
    # component.run()
    # prepare()
    # analyze(export_dir="./main/static/export/run")
    # valid_dirs("./main/static/export/rxjeljbw", "./main/static/export/run")
