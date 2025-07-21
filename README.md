# Hotel Management System

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![License](https://img.shields.io/badge/license-MIT-blue)](#)

This project is a small demonstration of a modular hotel management backend
implemented with **Flask** and **SQLite**. It is intended for offline use and
showcases common hotel operations such as bookings, housekeeping and dynamic
room pricing.

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
export FLASK_APP=app
flask --app app run --debug
```

Example health check:

```bash
curl http://localhost:5000/health
```

## Features

- Room and booking management
- Housekeeping task tracking
- Dynamic pricing service
- Session based authentication

## Contributing

Pull requests are welcome. Please open an issue first to discuss changes.

[![Lint](https://github.com/<ORG_OR_USER>/<REPO>/actions/workflows/lint.yml/badge.svg)](https://github.com/<ORG_OR_USER>/<REPO>/actions/workflows/lint.yml)
