# wayback-ctf

**wayback-ctf** is a web application developed to store and manage **scoreboards** of **Capture The Flag (CTF)** competitions. This project supports collecting, storing, and displaying CTF competition data, allowing users to track performance, compare scores across events, and preserve results over time.

## Table of Contents
- [wayback-ctf](#wayback-ctf)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
    - [Requirements](#requirements)
    - [Backend Installation](#backend-installation)
    - [Frontend Installation](#frontend-installation)
  - [Usage](#usage)
  - [API](#api)
  - [Contributing](#contributing)

## Features

- **Link Submission**: Allows users to submit the scoreboard link for CTF competitions (supports CTFd and rCTF formats).
- **Data Storage**: Automatically stores scoreboard data, including player rankings and scores.
- **Scoreboard Display**: Re-displays scoreboard data in an organized format, supporting comparison and review of past competition results.
- **CSV Export**: Exports competition data in CSV format for long-term storage and easy sharing.

## Project Structure

```plaintext
wayback-ctf
├── backend                  # Contains backend code
│   ├── app.js               # Main server file
│   ├── routes               # Application routes
│   └── models               # Data schemas
├── frontend                 # Contains frontend code
│   ├── src
│   │   ├── components       # Vue.js components
│   │   ├── App.vue          # Main Vue component
│   │   └── main.js          # Frontend entry point
└── README.md
```

## Installation

### Requirements

- **Node.js** version 14 or above
- **MongoDB** (or MongoDB Atlas for online database access)

### Backend Installation
```bash
cd backend  # Navigate to the backend directory
npm install # Install necessary packages
npm start   # Start the server
```


The backend server will run at `http://localhost:3000`.

### Frontend Installation
```bash
cd ../frontend # Navigate to the frontend directory
npm install    # Install necessary packages
npm run dev    # Start the frontend server
```
The frontend will run at `http://localhost:5173`.

## Usage

1. Access the homepage at `http://localhost:5173`.
2. Enter the URL of the CTF scoreboard you want to store, then press "Submit" to save it.
3. The application will automatically fetch and display the competition scoreboard, storing it within the system and enabling CSV download.

## API

- **GET** `/api/scoreboards` - Retrieve a list of all saved scoreboards.
- **POST** `/api/scoreboard` - Add a new scoreboard from a provided URL.
- **GET** `/api/scoreboard/:id` - View details of a specific scoreboard.

## Contributing

We welcome contributions from the community! To contribute:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request. 
