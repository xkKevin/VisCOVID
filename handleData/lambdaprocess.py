from .compiler import Compiler
from .parser.parser import get_parser
from pymongo import MongoClient, DESCENDING
from .utils import save_data, load_config, find_population_by_chinese_name, save_world_map, build_time_range
from .format import format_data
import json
class LambdaProcess:
    def __init__(self):
        client = MongoClient()
        db = client['coronavirus_analysis']
        self.db = db
        self.config = load_config()
        self.compiler = Compiler(self.db, self.config)
        self.parser = get_parser()
        self.descriptions = []
    
    def compile_description(self, description_str):
        description = json.loads(description_str)
        description = self.parser.parse_description(description)
        data = self.compiler.compile(description)
        return format_data( data['id'], data['data'])[0]

    def create_description(self, description_str):
        description = json.loads(description_str)
        # description = self.parser.parse_description(description)
        description['seq'] = self.db.descriptions.count()
        self.db.descriptions.insert_one(description) 


def lambda_api_compile():
    description = json.loads(description_str)
    config = load_config()
    compiler = Compiler()
    parser = get_parser()
    compiler
    data = []
    data.to_csv("./tmp/compiled.csv", index=False, quoting=csv.QUOTE_NONE)
    with open('stockitems_misuper.csv') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stockitems_misuper.csv'
    return response

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
