*** Settings ***
Resource    ../../Common/Resources/common.resource
Resource    ../Resources/RPA_resources.resource
Library      ../../Common/Resources/GmailClient.py     ${GmailCredentialFile}
Force Tags  rpa

*** Tasks ***
Login to Gmail and download Standard Notes backup
    Open session to Gmail
    Download latest export      ${encryptedFilePath}
