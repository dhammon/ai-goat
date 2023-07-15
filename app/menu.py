
import argparse
from sys import exit
from app.installer import Installer
from app.runner import Runner


def handle_args(inputs):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--install', help="Install", action="store_true")
    parser.add_argument('-r', '--run', help="Start CTFd or a Challenge.", choices=['ctfd', '1', '2', '3'])
    args = parser.parse_args(inputs)
    return args

def banner():
    title = """                                               
                                                                    
        _))
        > *\     _~
        `;'\\__-' \_
    ____  | )  _ \ \\ _____________________
    ____  / / ``  w w ____________________        
    ____ w w ________________AI_Goat______                                                                          
    ______________________________________

    Presented by: rootcauz

    """
    print(title)


def run(inputs):
    banner()
    if inputs is not None:
        args = handle_args(inputs)
        if args.install is True:
            Installer.install()
            exit()
        if args.run == 'ctfd':
            Runner.ctfd()
            exit()
        if args.run == '1':
            Runner.challenge_1()
            exit()
    handle_args(["--help"])