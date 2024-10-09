import json
from pprint import pprint
from datetime import datetime, timedelta
from Requester import Requester
from Parser import Parser
from DatabaseHandler import MySQLDatabaseHandler 
import constants as secrets

NODEFILE_PATH = 'data/node_data.json'
TIMEFILE_PATH = 'data/time_data.json'
API_URL = "https://api.searchneu.com/"

epoch = datetime(1970, 1, 1)
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def format_time(seconds):
    time = str(timedelta(seconds=seconds))  
    return time[:-3]

def format_meetings(meetings):
    classes = {}
    for id, meets in meetings.items():
        for meet in meets:
            class_location = ' '.join(meet[0]["where"].split(" ")[:-1])
            class_number = meet[0]["where"].split(" ")[-1]

            if class_location not in classes:
                classes[class_location] = {}
            if class_number not in classes[class_location]:
                classes[class_location][class_number] = []

            times = meet[0]["times"]
            for day_id, time in times.items():
                for t in time:
                    start_time = format_time(t["start"])
                    end_time = format_time(t["end"])
                    classes[class_location][class_number].append({
                        "id": f"{id}",
                        "start": start_time, 
                        "end": end_time,
                        "day": days[int(day_id)],
                    })
    return classes

def fetch_data_from_api(api_url, initial_request_object, max_pages=10):
    requester = Requester(api_url, request_object=initial_request_object)
    all_nodes = []
    offset = 0
    while True:
        data = requester.request_with_object()
        parser = Parser(data)

        nodes = parser.get_nodes()
        all_nodes.extend(nodes)

        if not parser.has_next_page():
            break

        offset += 10
        requester.update_request_object_variable("offset", offset)

        print(f"Fetched {offset} documents.")

    return all_nodes

def write_data_to_file(filepath, data):
    with open(filepath, 'w') as datafile:
        json.dump(data, datafile)

def read_data_from_file(filepath):
    with open(filepath, 'r') as datafile:
        return json.load(datafile)

def main():
    request_object = {
        "operationName": "searchResults",
        "query": "query searchResults($termId: String!, $query: String, $offset: Int = 0, $first: Int = 10, $subject:[String!], $nupath: [String!], $honors: Boolean, $campus: [String!], $classType: [String!], $classIdRange: IntRange) {\n  search(\n    termId: $termId\n    query: $query\n    offset: $offset\n    first: $first\n    subject: $subject\n    nupath: $nupath\n    honors: $honors\n    campus: $campus\n    classType: $classType\n    classIdRange: $classIdRange\n  ) {\n    pageInfo {\n      hasNextPage\n    }\n    filterOptions {\n      nupath {\n        value\n        count\n        description\n      }\n      subject {\n        value\n        count\n        description\n      }\n      classType {\n        value\n        count\n        description\n      }\n      campus {\n        value\n        count\n        description\n      }\n      honors {\n        value\n        count\n        description\n      }\n    }\n    nodes {\n      type: __typename\n      ... on Employee {\n        email\n        firstName\n        lastName\n        name\n        officeRoom\n        phone\n        primaryDepartment\n        primaryRole\n      }\n      ... on ClassOccurrence {\n        name\n        subject\n        classId\n        termId\n        host\n        desc\n        nupath\n        prereqs\n        coreqs\n        prereqsFor\n        optPrereqsFor\n        maxCredits\n        minCredits\n        classAttributes\n        url\n        prettyUrl\n        lastUpdateTime\n        feeAmount\n        feeDescription\n        sections {\n          campus\n          classId\n          classType\n          crn\n          honors\n          host\n          lastUpdateTime\n          meetings\n          profs\n          seatsCapacity\n          seatsRemaining\n          subject\n          termId\n          url\n          waitCapacity\n          waitRemaining\n        }\n      }\n    }\n  }\n}\n",
        "variables": {
            "offset": 0,
            "query": "",
            "termId": "202510"
        }
    }

    # all_nodes = fetch_data_from_api(API_URL, request_object)

    # write_data_to_file(NODEFILE_PATH, all_nodes)

    # nodes = read_data_from_file(NODEFILE_PATH)

    # parser = Parser(nodes)
    # all_meetings = parser.get_meetings(nodes)
    # formatted_classes = format_meetings(all_meetings)

    # write_data_to_file(TIMEFILE_PATH, formatted_classes)

    db_handler = MySQLDatabaseHandler(
        host=secrets.host,
        user=secrets.username,
        password=secrets.password,
        database=secrets.database,
        port=secrets.port
    )

    with open(TIMEFILE_PATH, 'r') as timefile:
        json_data = json.load(timefile)

    db_handler.transfer_json_data_to_mysql(json_data)
    db_handler.close()

if __name__ == "__main__":
    main()
