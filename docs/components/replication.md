# Replication

The replication Component replicates Blobs from one Volume to another. This happens in a push-method, rather than pull.

**This feature is under development and might not behave as you imagine it.**

You can optionally specify an offset by which Operations will be delayed, making it possible to use this as a backup.

You can also ignore Blobs matching a certain pattern, for example only replicate files matching not .iso
