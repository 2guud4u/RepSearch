import yaml
import re
import os


class MetafileParser:
    def __init__(self, filename):
        self.filename = filename
        self.metafile = None

    def parse(self):
        with open(self.filename, 'r') as f:
            self.metafile = yaml.safe_load(f)
        return self.metafile

    def validate(self):
        if not self.metafile.get('Collections'):
            raise ValueError("Error: Collections field is missing or empty.")
        if not self.metafile.get('Models'):
            raise ValueError("Error: Models field is missing or empty.")
        collections = self.metafile.get('Collections')
        for collection in collections:
            if not collection.get('Name'):
                raise ValueError("Error: Collections Name field is missing or empty.")
            if not collection.get('License'):
                raise ValueError("Error: Collections License field is missing or empty.")
            if not collection.get('Code'):
                raise ValueError("Error: Collections Code field is missing or empty.")
            if not collection.get('Code')['URL']:
                raise ValueError("Error: Collections Code URL field is missing or empty.")
        models = self.metafile.get('Models')
        for model in models:
            if not model.get('Name'):
                raise ValueError("Error: Models Name field is missing or empty.")
            if not model.get('Results'):
                raise ValueError("Error: Models Results field is missing or empty.")
            results = model.get('Results')
            for result in results:
                if not result.get('Task'):
                    raise ValueError("Error: Models Results Task field is missing or empty.")
                if not result.get('Task'):
                    raise ValueError("Error: Models Results Dataset field is missing or empty.")
            if not model.get('Weights'):
                raise ValueError("Error: Models Weights field is missing or empty.")
        # Add more validation rules as needed

    def parse_and_validate(self) -> dict:
        self.parse()
        self.validate()
        print(f"parse metafile data:{self.metafile}")
        return self.metafile


def get_filename_from_url(url):
    if url.startswith("http://") or url.startswith("https://"):
        raise ValueError(f'Weights must be local path file')
    url.replace('\\', '/')
    url_array = url.split('/')
    if len(url_array) == 1:
        return url_array[0]
    else:
        return url_array[len(url_array) - 1]


def get_meta_payload(repository, private, meta_data):
    _name = repository
    _nickname = repository
    _collection = meta_data['Collections'][0]
    _license = _collection['License']
    _github = _collection['Code']['URL']
    _public_status = 0 if private else 1
    _models = [{"name": m['Name'], "weightName": get_filename_from_url(m['Weights']),
                "evaluations": [{"task": e['Task'], "dataset": e['Dataset']} for e in m['Results']]} for m in
               meta_data['Models']]

    payload = {"name": _name, "nickname": _nickname, "license": _license,
               "github": _github, "publicStatus": _public_status, "models": _models}

    print(f"convert to payload:{payload}")
    return payload
