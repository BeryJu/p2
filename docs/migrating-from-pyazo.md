# Migrating from pyazo

To migrate from pyazo to p2, we're going to use the S3-API to mass-import Blobs and copy a matching tier0 Policy.

## Prerequisites

* A pyazo install (any version)
* A full-configured p2 install (0.1.16+)
* Enough free Space to store all of pyazo's Blobs
    * Check with the following command on the Server pyazo is running on
        * `du -sh /usr/share/pyazo/media`
* Administrative shell access on the pyazo Server
* An API Key in p2

Recommended, but not required:

*   A dedicated volume to import these Blobs into

## Preparation

To migrate the data, we need the the AWS-CLI Client ([https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)), so install it on the pyazo host as follows:

`sudo pip install awscli`

If that doesn't work for some reason, try the bundled installer: [https://docs.aws.amazon.com/cli/latest/userguide/install-bundle.html](https://docs.aws.amazon.com/cli/latest/userguide/install-bundle.html)

To make sure it is working correctly, execute the following command to configure your account.

`aws configure`

In the prompt asking you for an AWS Access Key, input your p2 Access Key. Same goes for the Secret Access Key. When asked for a region, you can input anything, since p2 doesn't use this field currently.

Now that your AWS-CLI is setup correctly, let's make sure it can interact with p2 correctly. Execute the following command, substituting p2-URL with the URL to your install.

`aws --endpoint-url https://<p2-URL> s3 ls`

The result should look something like this:

2006-02-03 16:45:09 pyazo-import-test
2006-02-03 16:45:09 some-other-volume

## Migrating the data

To actually migrate the data, we use AWS-CLI's `cp` Command, which recursively copies all files.

Run the following in `/usr/share/pyazo/media` to start the copy process:

`aws --endpoint-url https://<p2-URL> s3 cp . s3://<volume-name> --recursive --exclude thumbnails/`

This will import all of your data into p2. You can run this command multiple times without creating duplicate objects. 

## Migrating the URLs

p2 uses a new System to allow you to use URLs of pretty much any format. By default, files will be accessible by their absolute path, e.g.

`https://<p2 URL>/<volume>/<blob path>`

This will obviously only return the file if the current user has Permissions to read the Blob.

To preserve the old URLs, which match based on File Hash, you need to create one or more tier0 Policies. A tier0 Policy consists of two parts:

*   Tags, which are used to match against the current Request, and determine when the tier0 Policy is triggered.
*   A Blob Query, which is used to lookup a Blob from the Database based on the Request.

Depending on which setting you used for `default_return_view`, you can create a tier0 Policy based on the table below.

| Setting in pyazo | Tags | Blob Query |
|---|---|---|
|`view_md5` | `serve.p2.io/match/path/relative: ([A-Fa-f0-9]{32})(\.?[a-zA-Z0-9]*)` | `attributes__blob.p2.io/hash/md5={path_relative}&volume__name=images` |
| `view_sha512_short` | `serve.p2.io/match/path/relative: ([A-Fa-f0-9]{16})(\.?[a-zA-Z0-9]*)` | `attributes__blob.p2.io/hash/sha512__startswith={path_relative}&volume__name=images` |
| `view_sha256` | `serve.p2.io/match/path/relative: ([A-Fa-f0-9]{64})(\.?[a-zA-Z0-9]*)` | `attributes__blob.p2.io/hash/sha256={path_relative}&volume__name=images` |
| `view_sha512` | `serve.p2.io/match/path/relative: ([A-Fa-f0-9]{128})(\.?[a-zA-Z0-9]*)` | `attributes__blob.p2.io/hash/sha512={path_relative}&volume__name=images` |

Final Steps
-----------

To finalise the migration to p2, you should take a look at the following optional components:

 - [Public Access](components/public-access.md)
 - [Image-attribute Scanning](components/image-attribute-scanning.md)
