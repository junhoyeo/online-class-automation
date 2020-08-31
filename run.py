import datetime
import json

def load_json_file(filename: str) -> dict:
  with open(filename) as file_stream:
    data = json.load(file_stream)
  return data

timetable = load_json_file('./timetable.json')
classrooms = load_json_file('./classrooms.json')

def get_classroom_from_subject_name(subject_name: str) -> dict:
  for classroom in classrooms:
    if subject_name == classroom['name']:
      return classroom

weekday = datetime.datetime.today().weekday()
timetable_for_today = [
  get_classroom_from_subject_name(subject_name)
  for subject_name in timetable[weekday]
]

print(timetable_for_today)
