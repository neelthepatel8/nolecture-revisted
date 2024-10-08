from pprint import pprint as print 

class Parser:
    def __init__(self, data: dict):
        self.data = data

    def has_next_page(self) -> bool:
        return self.data["data"]["search"]["pageInfo"]["hasNextPage"]

    def get_meetings(self) -> dict[str, list]:
        all_meetings = {}
        nodes = self.data["data"]["search"]["nodes"]

        for node in nodes:
            id = node["classId"]
            subject = node["subject"]
            sections = node["sections"]
            meetings = [section.get("meetings") for section in sections]
            all_meetings[f"{subject}{id}"] = meetings

        return all_meetings


