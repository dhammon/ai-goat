
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
    

    def check_llm_status(container_name, happy_msg, sad_msg):
        subprocess.run(["docker", "exec", container_name, "touch", "/challenge/log.txt"])
        print("[!] Waiting for LLM to load, this may take a few minutes...")
        try:
            test = False
            while test == False:
                result = subprocess.run(["docker", "exec", container_name, "cat", "/challenge/log.txt" ], capture_output=True, text=True)
                if result.returncode > 0:
                    print("[-] Docker launch failed!", result)
                    exit()
                if "LLM loaded!" in result.stdout:
                    print("[+] LLM Loaded!")
                    print(happy_msg)
                    test = True
                else:
                    sleep(5)
        except Exception as e:
            print(sad_msg, e)
            exit()
    
    #TODO kill other containers when launching a new container
    #TODO starter()  

    #Basic Prompt Injection
    def challenge_1():
        container_name = "challenge1"
        print("[+] Starting Challenge 1!")
        os_command = ['docker', 'compose', 'up', container_name, '-d']
        run_happy_msg = "[!] Challenge 1 pending..."
        run_sad_msg = "[-] Challenge 1 startup failed!"
        llm_happy_msg = "[+] Netcat to port 9001 to start the challenge.  Good luck!"
        llm_sad_msg = run_sad_msg
        Runner.restart_container(container_name)
        Runner.run(os_command, run_happy_msg, run_sad_msg)
        Runner.check_llm_status(container_name, llm_happy_msg, llm_sad_msg)


    #Title Requestor
    def challenge_2():
        container_name = "challenge2"
        print("[+] Starting Challenge 2!")
        os_command = ['docker', 'compose', 'up', container_name, '-d']
        run_happy_msg = "[!] Challenge 2 pending..."
        run_sad_msg = "[-] Challenge 2 startup failed!"
        llm_happy_msg = "[+] Netcat to port 9002 to start the challenge.  Good luck!"
        llm_sad_msg = run_sad_msg
        Runner.restart_container(container_name)
        Runner.run(os_command, run_happy_msg, run_sad_msg)
        Runner.check_llm_status(container_name, llm_happy_msg, llm_sad_msg)