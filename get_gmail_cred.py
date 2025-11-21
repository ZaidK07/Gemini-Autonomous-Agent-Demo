from oauth2client import client, file, tools
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

CRED_DIR = "./gmail_credentials"
CLIENT_SECRET_PATH = os.path.join(CRED_DIR, "client_secret.json")
TOKEN_PATH = os.path.join(CRED_DIR, "gmail_token.json")

def main():
    os.makedirs(CRED_DIR, exist_ok=True)

    storage = file.Storage(TOKEN_PATH)
    creds = storage.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_PATH, SCOPES)
        creds = tools.run_flow(flow, storage)

    print("SimpleGmail-compatible gmail_token.json generated successfully.")

if __name__ == "__main__":
    main()