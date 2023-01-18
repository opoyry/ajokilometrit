*** Settings ***
Resource    ../Resources/TA_resources.resource
Resource    ../../Common/Resources/common.resource
Library      ../../Common/Resources/GmailClient.py     ${GmailCredentialFile}
Force Tags  test

*** Variables ***
${XXencryptedFilePath}      ${CURDIR}${/}${encryptedFileName}

*** Test Cases ***
Login to Gmail and download Standard Notes backup
    Open session to Gmail
    Download latest export      ${encryptedFilePath}
