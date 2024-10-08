from pprint import pprint as print 

class Parser:
    def __init__(self, data: dict):
        self.data = data

    def has_next_page(self) -> bool:
        if not self.data: return False
        return self.data["data"]["search"]["pageInfo"]["hasNextPage"]
    
    def get_nodes(self) -> list:
        return self.data["data"]["search"]["nodes"]
        
    def get_meetings(self, nodes: list) -> dict[str, list]:
        all_meetings = {}

        for node in nodes:
            id = node["classId"]
            subject = node["subject"]
            sections = node["sections"]
            meetings = [section.get("meetings") for section in sections]
            all_meetings[f"{subject}{id}"] = meetings

        return all_meetings



