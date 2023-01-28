import json
import pandas as pd

class StandardNotesJsonParser:

    DEFAULT_DECRYPTED_FILE = 'C:/var/misc/ajokilometrit/tmp/SN-Data-Decrypted.json'
    
    tagToInclude = 'Ajokilometrit2023'

    def ParseNotes(self, filename):

        with open(filename ) as f:
            json_data = json.load(f)

        uuids = []
        for _version in json_data["items"]: 
            if _version["content_type"] == "Tag":
                print('Tag title', _version["content"]["title"])
                if _version["content"]["title"] == self.tagToInclude:
                    for ref in _version["content"]["references"]:
                        uuids.append(ref["uuid"])

        print('uuids', uuids)

        data = []
        for _version in json_data["items"]: 
            if _version["content_type"] == "Note" and _version["uuid"] in uuids:
                c = _version['content']
                print("Note", c["title"], c["preview_plain"])
                data.append(
                    { 
                        'title' : c["title"], 
                        'entry' : c["preview_plain"],
                        'createdAt' : _version['created_at']
                    }
                )

        df = pd.DataFrame(data)
        df['km'] = df.apply(lambda x: self.func(x['entry']), axis=1)
        df['date'] = df.apply(lambda x: self.funcDate(x['title']), axis=1)

        df.sort_values(by=['date', 'title'], inplace=True)

        print('data', df)        
        return df

    def funcDate(self, par):
        import re
        x = re.search(r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))", par)
        if not x:
            return "-"
        return x.group(1)

    def func(self, par):
        import re
        x = re.search(r"(\d{3,5})", par)
        if not x:
            return "-"
        return x.group()

if __name__ == '__main__':
    StandardNotesJsonParser().ParseNotes(StandardNotesJsonParser.DEFAULT_ENCRYPTED_FILE)