# ScanCodes Overview

**QR Code Redirection and Data Display**

When a user scans a QR code, they should be redirected to a frontend page that displays information associated with that specific QR code. This information is provided by the QR code owner (a business or individual) during the QR code creation process.

**QR Code Creation Process:**
- User Interaction: A user (business or individual) visits the website.

- Template Selection: The user chooses a pre-defined template.

- Data Input: The user fills in the required data fields based on the selected template.

- QR Code Generation: Upon submission, the backend generates a QR code containing a unique URL.

- QR Code Delivery: The generated QR code is sent back to the user for sharing.



**QR Code URL Structure:**

The URL embedded within the generated QR code will follow this pattern:

`https://scancodes.net/<short_code>/<template>/<uuid>`

- `<short_code>`: A unique string automatically generated for each registered user.

- `<template>`: An identifier representing the template chosen by the user during creation.

- `<uuid>`: A unique identifier that the frontend will use to fetch the corresponding QR code details from the backend for display.

This setup ensures that when a QR code is scanned, the frontend can use the `uuid` to retrieve and present the specific data the owner provided when creating the code.

## DJ & Club QR Codes, Requests, and Notifications

**DJ QR Code Types:**
- **Club DJ:** QR code is associated with a club (shows club logo, DJ name, request/tip UI).
- **Personal DJ:** QR code is for the DJ alone (shows DJ logo, DJ name, request/tip/shoutout UI).

**Scan Experience:**
- When a DJ QR code is scanned, the page shows:
  - Club logo (if club DJ) or DJ logo (if personal DJ)
  - DJ name
  - UI for:
    - Music request (song title, tip amount, etc.)
    - Shoutout (message, tip, etc.)

**Endpoints:**
- **POST /api/requests**: Submit a music request or shoutout (fields: qr_code_id, type, message, song title, tip amount, etc.).
- **GET /api/notifications**: DJs can poll for new requests/shoutouts (notifications).

**Notifications:**
- When a request/shoutout is made, a notification is created for the DJ.
- DJs see notifications in their portal (API for now, websocket-ready for future).

**Data Model Additions:**
- **Club** and **DJ** models, with relationships to QR codes and requests.
- **MusicRequest** model for requests/shoutouts (linked to QR code, user, DJ, club).
- **Notification** model for DJ notifications.

**Flow:**
1. QR code is scanned (club or personal DJ).
2. Frontend fetches DJ/club info and displays request/shoutout UI.
3. User submits a request/shoutout (not anonymous).
4. DJ receives notification (API polling for now).
5. DJ can view and act on requests/shoutouts in their portal.

This setup supports both club and personal DJs, music requests, shoutouts, and a scalable notification system.