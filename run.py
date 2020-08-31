import datetime
import json

from rich.console import Console
from rich.table import Column, Table

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

def print_classroom(classroom: dict) -> None:
  console = Console()

  table = Table(show_header=True, header_style='bold magenta')
  table.add_column('시간', style='dim', width=5)
  table.add_column('과목명')
  table.add_column('선생님', justify='right')

  for classroom_index, classroom in enumerate(timetable_for_today):
    table.add_row(f'{classroom_index + 1}교시', classroom['name'], classroom['teacher'])

  console.print(table)

weekday = datetime.datetime.today().weekday()
timetable_for_today = [
  get_classroom_from_subject_name(subject_name)
  for subject_name in timetable[weekday]
]
print_classroom(timetable_for_today)
