
import functools
import pathlib
import shutil
import requests
import subprocess
from sys import path
path.insert(0, '../app')
from tqdm.auto import tqdm
from os.path import isfile
from sys import exit
from app.config import Config


class Installer:

    def install():
        print("[+] Starting Installation...")
        print("[!] Checking model presence.")
        if Installer.check_model() is False:
            print("[!] Downloading model, this may take 15 minutes...")
            Installer.download_model()
        print("[!] Pulling docker images.")
        Installer.pull_docker_images()
        print("[+] Installation finished!")


    def check_model():
        if isfile(Config.MODEL_PATH):
            print("[+] Model found!")
            return True
        else:
            print("[-] Model missing!")
            return False

    def download_model():
        try:
            r = requests.get(Config.MODEL_URL, stream=True, allow_redirects=True)
            if r.status_code != 200:
                r.raise_for_status()  # Will only raise for 4xx codes, so...
                raise RuntimeError(f"Request to {Config.MODEL_URL} returned status code {r.status_code}")
            file_size = int(r.headers.get('Content-Length', 0))
            path = pathlib.Path(Config.MODEL_PATH).expanduser().resolve()
            path.parent.mkdir(parents=True, exist_ok=True)
            desc = "(Unknown total file size)" if file_size == 0 else ""
            r.raw.read = functools.partial(r.raw.read, decode_content=True)
            with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
                with path.open("wb") as f:
                    shutil.copyfileobj(r_raw, f)
            print("[+] Model downloaded!")
            return True
        except:
            print("[-] Model download failed!")
            exit()
    
    def pull_docker_images():
        try:
            for image in Config.AI_IMAGES:
                process = subprocess.Popen(['docker', 'pull', image], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                while True:
                    output = process.stdout.readline()
                    print("    > ", output.strip())
                    return_code = process.poll()
                    if return_code is not None:
                        for output in process.stdout.readlines():
                            print("    > ", output.strip())
                        for error in process.stderr.readlines():
                            print("    > ", error.strip())
                            if "permission denied" in error.strip():
                                process.stdout.close()
                                print("[!] Docker image pull failed! Check user permissions (add to docker group)")
                                exit()
                        break
                process.stdout.close()
                process.stderr.close()
            print("[+] Docker images pulled!")
            return True
        except Exception as e:
            print("[-] Docker pull failed! Are docker and docker-compose installed?", e)


