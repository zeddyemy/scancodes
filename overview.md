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