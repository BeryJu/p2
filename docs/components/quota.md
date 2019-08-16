# Quota

Quota allows you to limit he Size of a Volume. You can configure a size threshold and an action which p2 will execute. Currently supported actions are:

-   Do Nothing
    -   Shows warning in UI
    -   No alerts
-   Prevent Further Uploads
    -   Prevents new Uploads to Volume
    -   Existing Blobs can still be updated
    -   Warning in UI is still shown
-   Send E-Mail to uploader and admin
    -   A Warning E-Mail will be sent to the User uploading the Blob and all Admins as well.
    -   Warning in UI is still shown.
