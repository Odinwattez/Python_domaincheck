import psutil

def kill_python_script(script_name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python.exe' and script_name in proc.info['cmdline']:
            print(f"Killing process {proc.info['pid']} running {script_name}")
            proc.terminate()
            return True
    return False

if __name__ == "__main__":
    if kill_python_script("domain_check.py"):
        print("Script terminated successfully.")
    else:
        print("No running script found.")