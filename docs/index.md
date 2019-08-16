# Welcome

Welcome to the p2 Documentation. p2 is an open-source Object Storage Server, focused on simple and quick
sharing. It allows you to quickly share files with people. It also offers an S3-Compatible API, which
allows you to easily integrate other software with p2.

p2 uses the following Terminology:

### Storage

A Storage represents a way p2 stores data. For example, this might be a LocalStorageController instance,
which saves data on a locally mounted drive. There is for example also a S3StorageController class,
which allows you to use S3 or an S3-compatible backend to store data.

### Volume

Logical Groupings of data, can be compared with an S3 Bucket

### Component

Single Features which can be enabled on a per-Volume basis.

### tier0

tier0 is the component which accelerates serving of your Blobs. It also allows to match custom URLs based on Regular Expressions and caches Blobs.
