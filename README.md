
# README

## Table of Contents
1. [About](#about)
2. [Repository](#repository)
3. [Name Change Note](#name-change-note)
4. [Prerequisites](#prerequisites)
5. [Build Docker Image](#build-docker-image)
6. [Running Tests with PowerShell](#running-tests-with-powershell)
   - [API Tests](#api-tests-pwsh)
   - [UI Tests](#ui-tests-pwsh)
   - [Running Both API and UI Tests](#both-tests-pwsh)
7. [Running Tests with Linux](#running-tests-with-linux)
   - [API Tests](#api-tests-linux)
   - [UI Tests](#ui-tests-linux)
8. [Reports & Screenshots](#reports-and-screenshots)
9. [Run Git hub Actions CI](#reports-and-screenshots)

---

## About

This repository contains automated test suites (API, UI and Github Actions CI) for the **droneS** project.

---

## Repository
You can access the public repo here: 
https://github.com/KenClemson/droneS

To get the code, you can clone this repository from GitHub via HTTPS or SSH:

```bash
# HTTPS
git clone https://github.com/KenClemson/droneS.git

# SSH
git clone git@github.com:KenClemson/droneS.git
```

---

## Name Change Note

Ken Clemson is my name before I was married; I changed my last name to King, this is why the repo has KenClemson.

---

## Prerequisites

- Install Docker on your system.
- (Optional) Install Git if you want to clone the repository.

---

## Build Docker Image

Navigate (cd) into the cloned repository folder:

```bash
cd droneS
```

Build the Docker image:

```bash
docker build -t tests1 .
```

---

## Running Tests with PowerShell

Open PowerShell and navigate to your local droneS directory. Below are example commands to run the tests.

### API Tests (PowerShell) <a name="api-tests-pwsh"></a>

```powershell
docker run --rm `
  -v "${PWD}:/app" `
  -v "${PWD}/reports:/app/reports" `
  -v "${PWD}/screenshots:/app/screenshots" `
  -e "PYTHONPATH=/app" `
  tests1 `
  pytest tests/API --gherkin-terminal-reporter --html=/app/reports/report.html --self-contained-html --cucumberjson=/app/reports/report.json --log-cli-level=INFO --color=yes
```

### UI Tests (PowerShell) <a name="ui-tests-pwsh"></a>

```powershell
docker run --rm `
  -v "${PWD}:/app" `
  -v "${PWD}/reports:/app/reports" `
  -v "${PWD}/screenshots:/app/screenshots" `
  -e "PYTHONPATH=/app" `
  tests1 `
  pytest tests/UI --gherkin-terminal-reporter --html=/app/reports/report.html --self-contained-html --cucumberjson=/app/reports/report.json --log-cli-level=INFO --color=yes
```

### Running Both API and UI Tests (PowerShell) <a name="both-tests-pwsh"></a>

```powershell
docker run --rm `
  -v "${PWD}:/app" `
  -v "${PWD}/reports:/app/reports" `
  -v "${PWD}/screenshots:/app/screenshots" `
  -e "PYTHONPATH=/app" `
  tests1 `
  pytest --gherkin-terminal-reporter --html=/app/reports/report.html --self-contained-html --cucumberjson=/app/reports/report.json --log-cli-level=INFO --color=yes
```

---

## Running Tests with Linux Terminal

Open a terminal in your droneS directory. Below are example commands to run the tests on Linux.

### API Tests (Linux) <a name="api-tests-linux"></a>

```bash
docker run --rm   -v "${PWD}:/app"   -v "${PWD}/reports:/app/reports"   -v "${PWD}/screenshots:/app/screenshots"   -e "PYTHONPATH=/app"   tests1   pytest tests/API --gherkin-terminal-reporter --html=/app/reports/report.html --self-contained-html --cucumberjson=/app/reports/report.json --log-cli-level=INFO --color=yes
```

### UI Tests (Linux) <a name="ui-tests-linux"></a>

```bash
docker run --rm   -v "${PWD}:/app"   -v "${PWD}/reports:/app/reports"   -v "${PWD}/screenshots:/app/screenshots"   -e "PYTHONPATH=/app"   tests1   pytest tests/UI --gherkin-terminal-reporter --html=/app/reports/report.html --self-contained-html --cucumberjson=/app/reports/report.json --log-cli-level=INFO --color=yes
```

---

## Reports and Screenshots <a name="reports-and-screenshots"></a>

Once the tests have run, you can view:

- **HTML Report(s)** in the `reports` folder.
- **Screenshots** (for UI tests) in the `screenshots` folder.


## Run Git hub Actions CI


You can access the public repo here 

https://github.com/KenClemson/droneS
If you go to Actions you can see the test runs but you can run a test or see the logs unless you are logged in as my user account.
You can see the workflow Actions file in droneS/.github/workflows/main.yaml.



