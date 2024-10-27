# Email Service

- Email Service, der Emails über IMAP abrufen kann und diese dann in die Wissensdatenbank einspielt.
- Dabei wird der Inhalt von einem Large Language Model (LLM) analysiert, aufbereitet und kategorisiert.
- Funktioniert in einem Polling-Modus, bei dem in regelmäßigen Abständen die Emails abgerufen werden.

# Env Variables
|Env Variable| Beschreibung                              |
|---|-------------------------------------------|
|`BACKEND_BASE_URL`| URL des Backends                          |
|`EMAIL_USER`| Email-Adresse des E-Mail-Accounts für IMAP |
|`EMAIL_PASSWORD`| Passwort des E-Mail-Accounts für IMAP |
|`EMAIL_IMAP`| IMAP-Server des E-Mail-Accounts |
|`OLLAMA_BASE_URL`| URL des OLLAMA-Service |
|`OLLAMA_MODEL`| Name des OLLAMA-Modells |