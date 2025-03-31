# Bathroom Renovation Quote System

A comprehensive web application for generating bathroom renovation quotes. This system is designed to collect detailed information about bathroom renovation projects and generate accurate quotes.

## Features

- Detailed form collection for personal details
- Property information gathering
- Appliance requirements assessment
- Interior fitting specifications
- Tile and painting requirements
- Additional notes and special requirements
- Quote generation (coming in future phases)

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

- Windows:

```bash
venv\Scripts\activate
```

- Unix/MacOS:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

## Development

The application is built using:

- Flask (Backend)
- Bootstrap 5 (Frontend)
- WTForms (Form handling)
- JavaScript (Client-side validation and dynamic behavior)

## Project Structure

```
├── app.py              # Main application file
├── forms/             # Form definitions
├── static/            # Static files (CSS, JS)
├── templates/         # HTML templates
└── requirements.txt   # Project dependencies
```

## License

This project is licensed under the MIT License.
