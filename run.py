from handleData.analyze import analyze
from handleData.prepare import prepare 
from handleData.validation import valid_dirs
from handleData.interface.component import AppendOthers
if __name__ == "__main__":
    desc = {
        "name": "AppendOthers",
        "args": {
            "f": "lambda x: x"
        }
    }
    component = AppendOthers()
    # prepare()
    # analyze(export_dir="./main/static/export/run")
    # valid_dirs("./main/static/export/rxjeljbw", "./main/static/export/run")
