import psutil

def get_zoom_process():
  process_pid_list = psutil.pids()
  for process_pid in process_pid_list:
    process = psutil.Process(process_pid)
    process_name = str(process.name())
    if 'zoom' in process_name:
      print(process)
      return process
  return None

def kill_zoom_process():
  try:
    process = get_zoom_process()
    if process != None:
      process.kill()
      return 1
  except:
    return 0
  return 0
