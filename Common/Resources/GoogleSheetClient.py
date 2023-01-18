import gspread
from gspread_dataframe import set_with_dataframe
import gspread_dataframe as gd
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd


class GoogleSheetClient:

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
        ]

    _tokenFileName = 'gooogleSheetToken.json'

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1yknVXAKMrdzLUHfghkTMiMSk89aoJjVtNABjk6uKhNA'
    
    def __init__(self, credentialsFile="credentials.json"):
        self._credentialsFile = credentialsFile
        print(f'init using credentials file: {credentialsFile}')
        self._credentials = Credentials.from_service_account_file(credentialsFile, scopes=self.SCOPES)

    def PopulateSheet(self, sheetTitle, df):

        gc = gspread.authorize(self._credentials)

        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)

        # open a google sheet
        gs = gc.open_by_key(self.SAMPLE_SPREADSHEET_ID)
        # select a work sheet from its name

        #worksheet1 = gs.add_worksheet(title="Ajokilometrit (20)", rows=100, cols=20)

        worksheet1 = gs.worksheet(sheetTitle)

        if True:
            worksheet1.clear()
            #df.drop(columns=['B', 'C'])
            df['entry'] = df['entry'].astype(str)
            df['title'] = df['title'].astype(str)
            import dateutil.parser
            df['createdAt'] = df.apply(lambda x: dateutil.parser.isoparse(x['createdAt']), axis=1)
            df['createdAt'] = df.apply(lambda x: x['createdAt'].strftime('%Y-%m-%d %H:%M'), axis=1)
            df.rename(columns={"date": "pvm", "km": "km lopussa"}, inplace=True)
            df['ajo km'] = 0
            df = df[['pvm', 'km lopussa', 'ajo km', 'title', 'entry', 'createdAt']]
            set_with_dataframe(worksheet=worksheet1, dataframe=df, include_index=False, include_column_header=True, resize=True)
            #worksheet1.add_rows(1)
            #worksheet1.append_row([''] , insert_data_option="INSERT_ROWS")
            #worksheet1.append_row(['Total', "=B2+B3", "=SUM(C2:C3)" ], value_input_option="USER_ENTERED", insert_data_option="INSERT_ROWS")
            from datetime import datetime
            pvm = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            worksheet1.append_row( [ 'Tulostettu:', pvm ], value_input_option="RAW", insert_data_option="INSERT_ROWS") # USER_ENTERED
            worksheet1.add_cols(1)

        else:
            print('df',df)
            df_values = df.values.tolist()
            #df_values.extend([ 'Yhteensä', '', '', '=SUM(D3:D4)'])
            print(f'Add {df.shape[0]} rows', df_values)
            gs.values_append(sheetTitle, {'valueInputOption': 'RAW'}, {'values': df_values})        
            #existing = gd.get_as_dataframe(worksheet1)
            #updated = existing.append(df)
            #gd.set_with_dataframe(worksheet1, updated)            
            formula = '=SUM(D3:D4)'
            worksheet1.update_acell('D30', formula)

    def main(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        d = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(data=d)
        self.PopulateSheet('Ajokilometrit 2023', df)

if __name__ == '__main__':
    GoogleSheetClient(r"C:\Users\olli_\Downloads\essaimgauth-c9a81bccd845.json").main()
