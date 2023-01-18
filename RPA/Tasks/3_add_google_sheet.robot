*** Settings ***
Resource    ../Resources/RPA_resources.resource
Library     ../../Common/Resources/StandardNotesJsonParser.py
Library     ../../Common/Resources/GoogleSheetClient.py     ${GoogleSheetCredentialFile}
Force Tags  rpa

*** Tasks ***
Login to Google and add sheet
    ${df} =     Parse notes         ${decryptedFilePath}
    Populate sheet      ${sheetName}    ${df}
