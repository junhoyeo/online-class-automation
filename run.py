import datetime
import json

import schedule
import webbrowser
from rich.console import Console
from rich.table import Column, Table

def load_json_file(filename: str) -> dict:
  with open(filename) as file_stream:
    data = json.load(file_stream)
  return data

console = Console()

timetable = load_json_file('./timetable.json')
classrooms = load_json_file('./classrooms.json')
periods = load_json_file('./periods.json')
period_names, period_list = map(list, [periods.keys(), periods.values()])

def get_classroom_from_subject_name(subject_name: str) -> dict:
  for classroom in classrooms:
    if subject_name == classroom['name']:
      return classroom

def get_homeroom() -> dict:
  for classroom in classrooms:
    if 'homeroom' in classroom and classroom['homeroom']:
      return classroom

def print_classroom(classroom: dict) -> None:
  table = Table(show_header=True, header_style='bold light_sky_blue1')
  table.add_column('시간', style='dim', width=5)
  table.add_column('과목명', style='bold')
  table.add_column('선생님', justify='right')

  for classroom_index, classroom in enumerate(timetable_for_today):
    classroom['start_time'] = period_list[classroom_index]
    table.add_row(
      period_names[classroom_index],
      classroom['name'],
      classroom['teacher'],
    )

  console.print(table)

def open_classroom(classroom: dict) -> None:
  name = classroom['name']
  code = classroom['code']
  webbrowser.open_new_tab(f'zoommtg://zoom.us/join?action=join&pwd=dimigo&confno={code}')
  console.print(f'✔ {name} 수업 접속 완료', style='dim')

weekday = datetime.datetime.today().weekday()
timetable_for_today = [
  get_classroom_from_subject_name(subject_name)
  for subject_name in timetable[weekday]
]

homeroom = get_homeroom()
timetable_for_today.insert(0, homeroom)
timetable_for_today.append(homeroom)

print_classroom(timetable_for_today)

for classroom in timetable_for_today:
  schedule.every().day.at(classroom['start_time']).do(open_classroom, classroom=classroom)

console.print('수업이 끝나길 기다리는 중...', style='dim')
while True:
  schedule.run_pending()
