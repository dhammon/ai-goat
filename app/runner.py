
import subprocess
from time import sleep
from sys import exit


class Runner:

    def run(os_command:list, happy_msg:str, sad_msg:str):
        try:
            process = subprocess.Popen(os_command, stdout=subprocess.PIPE, universal_newlines=True)
            while True:
                output = process.stdout.readline()
                print("    > ", output.strip())
                return_code = process.poll()
                if return_code is not None:
                    for output in process.stdout.readlines():
                        print("    > ", output.strip())
                    break
            print(happy_msg)
            return True
        except:
            print(sad_msg)
            exit()


    def restart_container(container_name):
        print("[!] Checking if Challenge is already running.")
        status = subprocess.run(["docker", "container", "ps",], capture_output=True, text=True)
        if container_name in status.stdout:
            print("[!] Challenge is already running, rebooting it now.")
            subprocess.run(["docker", "stop", container_name ], capture_output=True, text=True)
        else:
            print("[+] Challenge not already started, starting now")


    def ctfd():
        print("[+] Starting CTFd")
        os_command = ['docker', 'compose', 'up', 'ctfd', '-d']
        happy_msg = "[+] CTFd Started! Open browser to http://127.0.0.1:8000"
        sad_msg = "[-] CTFd startup failed!"
        Runner.run(os_command, happy_msg, sad_msg)
    
    #Basic Prompt Injection
    def challenge_1():
        print("[!] Starting Challenge 1!")
        Runner.restart_container("challenge1")
        os_command = ['docker', 'compose', 'up', 'challenge1', '-d']
        happy_msg = "[!] Challenge 1 pending..."
        sad_msg = "[-] Challenge 1 startup failed!"
        Runner.run(os_command, happy_msg, sad_msg)
        print("[!] Waiting for LLM to load, this may take a few minutes...")
        try:
            test = False
            while test == False:
                result = subprocess.run(["docker", "exec", "challenge1", "cat", "log.txt" ], capture_output=True, text=True)
                if "LLM loaded!" in result.stdout:
                    print("[+] LLM Loaded!")
                    print("[+] Netcat to port 9001 to start the challenge.  Good luck!")
                    test = True
                else:
                    sleep(5)
        except Exception as e:
            print(sad_msg, e)
            exit()
