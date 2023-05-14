import os.path
import pickle
from datetime import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleSpreadSheetHandler:
    def __init__(self, spreadsheet_id: str, sheet_name: str):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None
        self.service = None

    def init_connection(self) -> None:
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                self.creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('sheets', 'v4', credentials=self.creds)
        if self.service:
            print("Successfully connected to google sheets.")
        else:
            print("Error while connecting to google sheets.")

    def save_users_ids_to_sheets(self, users_ids: dict) -> None:
        last_row = self.__get_last_row()
        data = self.__convert_users_ids_to_data(users_ids, last_row)
        range_name = f'{self.sheet_name}!A{last_row + 1}'
        body = {
            'values': data
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id, range=range_name,
            valueInputOption='RAW', body=body).execute()
        print(f'Added {result.get("updates").get("updatedCells")} cells to the Google Sheet.')

    def __get_last_row(self) -> int:
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.sheet_name).execute()
        values = result.get('values', [])
        last_row = 0
        if values:
            last_row = len(values)
        return last_row

    @staticmethod
    def __convert_users_ids_to_data(users_ids: dict, last_row: int) -> list[list[str]]:
        timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        data = [
            [
                (lambda x: "Private Bot Messages" if x is None else x)(group_name),
                timestamp_now,
                len(users_ids.get(group_name, set()))
            ]
            for group_name in users_ids
        ]
        if last_row == 0:
            data.insert(0, ['TG group', 'Timestamp', 'Unique senders'])

        return data
