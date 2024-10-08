from parser import Parser
import json
from pprint import pprint
from datetime import datetime, timedelta

epoch = datetime(1970, 1, 1)
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def format_time(seconds):
    time = str(timedelta(seconds=seconds))  
    return time[:-3]

def format_meetings(meetings: dict[str, list]):
    classes = {}

    for id, meets in meetings.items():
        assert type(meets) == list
        for meet in meets:
            class_location = ' '.join(meet[0]["where"].split(" ")[:-1])

            if class_location not in classes:
                classes[class_location] = {}


            class_number = meet[0]["where"].split(" ")[-1]

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
            

            pprint(classes)

def main():
    mock_file = open('mock.json')
    data = json.load(mock_file)

    parser = Parser(data)
    all_meetings = parser.get_meetings()
    format_meetings(all_meetings)
    # print(all_meetings)

if __name__ == "__main__":
    main()