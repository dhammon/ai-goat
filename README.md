
```                                                        
        _))
        > *\     _~
        `;'\__-' \_
    ____  | )  _ \ \ _____________________
    ____  / / ``  w w ____________________        
    ____ w w ________________AI_Goat______                                                                          
    ______________________________________

    Presented by: rootcauz
```

Learn AI security through a series of vulnerable LLM CTF challenges.  No sign ups, no cloud fees, run everything locally on your system.

# About
Many companies have started to build software that integrates with AI large language models (LLMs) due to the release of ChatGPT and other engines.  This explosion of interest has led to the rapid development systems that reintroduce old vulnerabilities and impose new classes of less understood threats.  Many company security teams may not be fully equipped do deal with LLM security as the field is still maturing with tools and learning resources.

I've developed AI Goat to learn about LLM development and the security risks companies face that use it.  The CTF format is a great way for security researchers to gain practical experience and learn about how these systems are vulnerable and can be exploited.  Thank you for your interest in this project and I hope you have fun!


## About AI/LLM Security Risks
The [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-2023-v05.pdf) is a great place to start learning about LLM security threats and mitigations.  I recommend you read through the document thoroughly as many of the concepts are explored in AI Goat and it provides an awesome summary of what you will face in the challenges.

Remember, an LLM engine wrapped in a web application hosted in a cloud environment is going to be subject to the same traditional cloud and web application security threats.  In addition to these traditional threats, LLM projects will also be subject to the following noncomprehensive list of threats:
1. Prompt Injection
2. Insecure Output Handling
3. Training Data Poisoning
4. Denial of Service
5. Supply Chain
6. Permission Issues
7. Data Leakage
8. Excessive Agency
9. Overreliance
10. Insecure Plugins

## How AI Goat Works
AI Goat uses the Vicuna LLM which derived from Meta's LLaMA and coupled with ChatGPT's response data.  When installing AI Goat the LLM binary is downloaded from HuggingFace locally on your computer.  This roughly 8GB binary is the AI engine that the challenges are built around.  The LLM binary essentially takes an input "prompt" and gives an output, "response".  The prompt consists of three elements concatenated together in a string.  These elements are: 1. Instructions; 2. Question; and 3. Response.  The Instructions element consists of the described rules for the LLM.  They are meant to describe to the LLM how it is supposed to behave.  The Question element is where most systems allow user input.  For instance, the comment entered into a chat engine would be placed in the Question element.  Lastly, the Response section prescribes that the LLM give a response to the question.

A prebuilt Docker image, ai-base, has all the libraries needed to run the LLM and challenges.  This container is downloaded during the installation process along with the LLM binary.  A docker compose that launches each challenge attaches the LLM binary, specific challenge files, and exposes TCP ports needed to complete each challenge.  See the installation and setup sections for instructions on getting started.

An optional CTFd container has been prepared that includes each challenge description, hints, category, and flag submission.  The container image is hosted in our dockerhub and is call ai-ctfd alongside the ai-base image.  The ai-ctfd container can be launched from the ai-goat.py and accessed using your browser.


# Installation
## Requirements
- git
  - `sudo apt install git -y`
- python3
- pip3
  - `sudo apt install python3-pip -y`
- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)
- User in docker group
  - `sudo usermod -aG docker $USER`
  - `reboot`
- 8GBs of drive space
- Minimum 16GB system memory with at least 8GB dedicated to the challenge; otherwise LLM responses take too long
- A love for cybersecurity!

## Directions
```
git clone https://github.com/dhammon/ai-goat
cd ai-goat
pip3 install -r requirements.txt
chmod +x ai-goat.py
./ai-goat.py --install
```

# Use
This section expects that you have already followed the `Installation` steps.

## Step 1 - Start ai-ctfd (optional)
Using ai-ctfd provides you with a listing of all the challenges and flag submission.  It is a great tool to use by yourself or when hosting a CTF.  Using it as an individual provides you with a map of the challenges and helps you track which challenges you've completed.  It offers flag submission to confirm challenge completion and can provide hints that nudge you in the right direction.  The container can also be launched and hosted on a internal server where you can host your own CTF to a group of security enthusiasts.  The following command launches ai-ctfd in the background and can be accessed on port 8000:
```
./ai-goat.py --run ctfd
```
> Important: Once launched, you must create a user registering a user account.  This registration stays local on the container and does not require a real email address.


## Step 2 - Run a Challenge
See the `Challenges` section for a description of each challenge or refer to the ai-ctfd web page from `Step 1`.  The following command launches the first challenge:
```
./ai-goat.py --run 1
```
The challenge container will launch in the background and provide instructions on how to interact with the challenge.  Each challenge has a flag, which is a string surrounded by curly braces.  For example: `{eXampl3F!ag}`.  You verify the flag through submission to the subject challenge in the ai-ctfd page.
> Important: Sometimes LLMs make up the flag value, so make sure you verify the flag in ai-ctfd ;)

> Important: The LLM response can take 30 seconds or so


## Troubleshooting
1. Challenges can be restarted by rerunning the challenge.  Example: `./ai-goat.py --run <CHALLENGE NUMBER>`.  This command will restart the container if it is already running.
2. You might inadvertently pollute or break a challenge container.  Use docker commands to stop containers if needed.  To list containers: `docker container ps`.  To stop a container: `docker stop <CONTAINER NAME>`.


## Upgrade
The main branch will always contain the latest release.  Historical versions will be maintained in respective branches.  Upgrade instructions:
```
cd ai-goat
git pull
pip3 install -r requirements.txt
chmod +x ai-goat.py
./ai-goat.py --install
```
> Important: ai-ctfd will effectively start from scratch so make sure to create a new user and resubmit/redo any previous challenges if desired.


# Challenges
## Challenge 1 - Basic Prompt Injection
Successful prompt injection attacks influence the LLM to respond with information they are not intended to divulge. In this challenge, an AI chatbot running on port 9001 is storing the flag as a secret and has been prompted to not give it up.  Can you convince or trick the bot into giving you the flag?
```
./ai-goat.py -r 1
```
[LLM01: Prompt Injections](#LLM01) | [LLM07: Data Leakage](#LLM07)

## Challenge 2 - Title Requestor
LLM system output shouldn't be trusted, especially when that output is used in downstream operations such as OS commands or network calls.  This challenge has another AI chatbot running on port 9002 that takes a user question and returns a website's title.  The user input is converted into a URL by the chatbot where it is used to request that site's source while ripping the the title.  What else could this chatbot have network access to?
```
./ai-goat.py -r 2
```
[LLM02: Insecure Output Handling](#LLM02)

# Versioning
Latest version is main branch.  You can find the version in the `CHANGELOG.md` file.  Branches are created for each respective version.


# Credits
CTF engine: [CTFD](https://github.com/CTFd/CTFd)

Art by: ejm97 on ascii.co.uk

AI container technology:
1. Library: [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
2. Large Language Model: [Vicuna LLM](https://lmsys.org/blog/2023-03-30-vicuna/)