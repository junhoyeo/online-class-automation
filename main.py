import os
import json
import typing
import datetime

import schedule
import webbrowser
from rich.console import Console
from rich.table import Column, Table

from process import kill_zoom_process

console = Console()

def load_json_file(filename: str) -> typing.Dict:
  with open(filename) as file_stream:
    data = json.load(file_stream)
  return data

def run_self_check():
    os.system('cd ./self-check-automation;\
            yarn start')

def get_classroom_from_subject_name(classrooms: typing.Dict, subject_name: str) -> typing.Dict:
  for classroom in classrooms:
    if subject_name == classroom['name']:
      return classroom

def get_homeroom(classrooms: typing.Dict) -> typing.Dict:
  for classroom in classrooms:
    if 'homeroom' in classroom and classroom['homeroom']:
      return classroom

def print_classroom(period_names: typing.List, timetable_for_today: typing.List) -> None:
  table = Table(show_header=True, header_style='bold light_sky_blue1')
  table.add_column('시간', style='dim', width=5)
  table.add_column('과목명', style='bold')
  table.add_column('선생님', justify='right')

  for classroom_index, classroom in enumerate(timetable_for_today):
    table.add_row(
      period_names[classroom_index],
      classroom['name'],
      classroom['teacher'] or '-',
    )

  console.print(table)

def attach_time_to_classroom(period_list: typing.List, timetable_for_today: typing.List):
  for index, classroom in enumerate(timetable_for_today):
    start_time, end_time = period_list[index]
    classroom['start_time'] = start_time
    classroom['end_time'] = end_time

def open_classroom(classroom: typing.Dict) -> None:
  name = classroom['name']
  code = classroom['code']
  password = classroom['password']
  webbrowser.open_new_tab(f'zoommtg://zoom.us/join?action=join&pwd={password}&confno={code}')
  console.print(f'✔ {name} 수업 접속 완료', style='dim')

def close_classroom() -> None:
  if kill_zoom_process():
    console.print(f'✘ 수업 나가기 완료', style='dim')
  else:
    console.print(f'✘ 수업 나가기 실패', style='dim')

def main():
  timetable = load_json_file('./timetable.json')
  classrooms = load_json_file('./classrooms.json')
  periods = load_json_file('./periods.json')
  period_names, period_list = map(list, [periods.keys(), periods.values()])

  weekday = datetime.datetime.today().weekday()
  timetable_for_today = [
    get_classroom_from_subject_name(classrooms, subject_name)
    for subject_name in timetable[weekday]
  ]

  homeroom = get_homeroom(classrooms)
  timetable_for_today.insert(0, homeroom)
  timetable_for_today.append(homeroom)

  print_classroom(period_names, timetable_for_today)
  attach_time_to_classroom(period_list, timetable_for_today)

  for classroom in timetable_for_today:
    schedule.every().day.at(classroom['start_time']).do(open_classroom, classroom=classroom)
    schedule.every().day.at(classroom['end_time']).do(close_classroom)

  console.print('수업이 끝나길 기다리는 중...', style='dim')

  while True:
    schedule.run_pending()

main()