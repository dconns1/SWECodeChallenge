# Security Innovation's Code Challenge for Software Engineer II

## Challenge Description

A Python program that parses /var/lib/dpkg/status (and/or any other needed files) and displays a list of packages explicitly installed by the user (the equivalent of Gentoo selected set https://wiki.gentoo.org/wiki/Selected_set_(Portage)).

## Guidelines

- Write a program in Python 3. The code should be readable and easy to follow, please include comments.
- Target the program to run on Debian 12.
- Create a Debian package from the solution.

## Installation

### Git

```bash
- git clone git@github.com:dconns1/SWECodeChallenge.git
- cd SWECodeChallenge
```

#### Utilizing Docker

- Make sure you install docker desktop for your operating system
  - https://www.docker.com/get-started/
- To bring up docker, after the installation, navigate to the project directory and use the below command use the command:
  - `docker-compose up -d --build`
- To login to docker use the command from the project directory:
  - `docker compose exec -u testUser app bash`
  - If you are in the project directory and using a bash terminal you can just use the below command to login:
    - `./bin/bash`
- Navigate to the folder /swe-code-challenge and you can use the below command to run it:
  - `python3 -m my_module.SWECodeChallenge`
- When you are finished utilizing docker run the below command to bring the container down while you are in the project directory:
  - `docker compose down`

### Local

- Place swe-code-challenge_0.0-0_all.deb onto your debian machine and run the below command from the directory you placed it in
  - `sudo dpkg -i swe-code-challenge_0.0-0_all.deb`
- To confirm installation run the below command
  - `dpkg -l | grep swe-code-challenge`
- Once you have confirmed it is installed you can run the below command and it will execute it
  - `swe-code-challenge`

## Solution Thought Process

### Utilization of Data Objects and Collections

#### Data Objects

- I decided to use objects to store the data because utilizing the properties and setters makes it easier to cleanly store the data for access later. I also feel the properties and setters add to the readability as well as usability for other engineers.

#### Collections

- I decided to use collections since they allow me to encapsulate methods used for comparing as well as parsing the lists. I have learned over the years this makes access to data less frustrating when trying to keep your code base clean and organized.

### Utilization of Injection Dependency and Interfaces

#### Injection Dependency

- I decided to inject the parsers in the runtime rather than implicitly declaration because in a scenario like this we do not always know if the format of the file could change. In this scenario it is not as likely but I always like to account for these scenarios if possible.

#### Interfaces

- I decided to use interfaces since it allows me to ensure the important methods for the parsers are always present. When it comes to code a rewrite is not always out of the question depending on how much the requirements change (Ex: a file format). In the instance where we change the format we want to make sure that the data is still being returned to us for use in the same way. The ability to specify the methods and those return types allows us to just inject the new parsers with little to no issues since the methods called and return type will still be present.

## Additional Enhancements

If I had more time below is a list of additional enhancements I would have pursued:

- Command Line Interface
  - Since I stored requested by in the history.log object I would have added the parameter `userId` and used that value to pluck the matching objects from the HistoryFileSection Collection.
  - Since I stored the start date in the history.log object I would have added a parameter `startDate` and used that value to pluck the objects equaling a specific start date or pluck all objects installed since a specific start date.
- Pytest
  - Normally I would create unit tests for the parsers and objects but with the time constraint and the fact that I did not have experience with the status file and referencing it I decided to create a docker environment and test manually as I progressed.
