# Moving p2 to a different host

All the uploads are saved in the `media/` folder (full path on debian-based systems: `/usr/share/p2/media/`). To migrate all your data, simply install p2 as described in [Install](/install/package/). Afterwards, copy all files in the media folder from the old system to the new one. Make sure filles within the folder have correct permissions (owner p2, group p2, chown 755). Afterwards run `/usr/share/p2/p2.sh reindex`. This will re-add all files to the database.
