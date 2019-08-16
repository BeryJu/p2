# Expiry

The Expiry component allows you to create Blobs which are automatically deleted at a certain date/time.

To use expiry on a Blob, enable the Component on your Volume and tag the Blob with the Following tag:

`component.p2.io/expiry/date`

The value is a Unix-Timestamp. The Blob will be deleted as soon as the time has been reached.
