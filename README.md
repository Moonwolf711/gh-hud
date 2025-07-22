# gh-hud

This repository hosts a small demo that combines a VS Code extension with a
Node.js server and a Flutter mobile application. The goal is to present a
heads‑up display (HUD) that reflects events occurring inside the editor in real
time. The server acts as the communication hub while the extension and mobile
app provide the user interfaces.

## Prerequisites

Before setting up the project you will need the following software installed:

- **Node.js** (version 16 or later)
- **Flutter SDK** (any stable channel release)
- **Visual Studio Code** with the ability to load extensions from this
  repository

## Node server setup

1. Navigate to the `server` directory:
   ```bash
   cd server
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   npm start
   ```
   The server exposes endpoints and WebSocket channels used by both the VS Code
   extension and the Flutter application.

## Flutter application setup

1. Navigate to the `flutter_app` directory:
   ```bash
   cd flutter_app
   ```
2. Fetch packages:
   ```bash
   flutter pub get
   ```
3. Run the application on an emulator or device:
   ```bash
   flutter run
   ```
   The app will connect to the running Node server to display HUD information.

## How the extension and server work together

The VS Code extension monitors your workspace for events (such as file changes
or test runs). It sends these events to the Node server using a lightweight
protocol. The server aggregates and streams the data to any connected Flutter
clients, allowing the mobile HUD to stay in sync with your editor. Make sure the
server is running before launching the extension and the Flutter app.

## Contributing

Contributions are welcome! To propose a change:

1. Fork this repository and create a feature branch.
2. Follow existing code style conventions (`prettier` for JavaScript, `flutter
   format` for Dart).
3. Commit your changes and open a pull request describing your work.
4. Please ensure any major design decisions are discussed in an issue first.

This project is released under the MIT License. By contributing you agree that
any code submitted may be distributed under that license.
