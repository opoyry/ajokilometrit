*** Settings ***
Variables   commonvariables.py
Resource    locators.resource

*** Variables ***
${encryptedFileName}        SN-Data-Encrypted.txt
${decryptedFileName}        decrypted-sn-data.txt
${encryptedFilePath}        ${EXECDIR}${/}tmp${/}${encryptedFileName}
${decryptedFilePath}        ${EXECDIR}${/}tmp${/}SN-Data-Decrypted.json
${GmailCredentialFile}      C:/users/olli_/Downloads/gmail-credentials.json
${GoogleSheetCredentialFile}    C:/Users/olli_/Downloads/essaimgauth-c9a81bccd845.json
${browserPageToDecrypt}     https://crmprodsa02.blob.core.windows.net/carelocationpub/decrypt.html
${sheetName}       Ajokilometrit data

*** Keywords ***

Initiate Automation Run
    [Documentation] Starts the automation by opening the browser and logging in
    Open Browser    ${pmurl}    chrome
    Maximize Browser Window

End Automation Run
    [Documentation]    Ends the automation execution.

    #Delete All Cookies
    Close Browser

Use browser page to decrypt file
	Wait Until Element Is Enabled   id=chooser
	Choose File    id=chooser    ${encryptedFilePath}
    click    id=password
    type    id=password    Talvi2022!
    clickAndWait    id=download-import-file
    BuiltIn.Sleep   5
    Move downloaded file        ${decryptedFileName}        ${decryptedFilePath}
