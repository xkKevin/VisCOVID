from handleData.analyze import analyze
from handleData.prepare import prepare 
from handleData.validation import valid_dirs

if __name__ == "__main__":
    prepare()
    analyze(export_dir="./main/static/export/run")
    valid_dirs("./main/static/export/rxjeljbw", "./main/static/export/run")
