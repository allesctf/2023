# Solution
Bug should be pretty obvious: Race condition in plugin verification and plugin loading/execution and write permissions to the plugin folder.

The race window is pretty small, but it can be extended: The plugin loader will skip invalid plugins when the type in the plugin namespace is not found. The namespace is taken from the DLL name. Thus, an attacker can create multiple copies of verified plugins and they will be verified, but not loaded/executed properly.

Steps:

1. Create 1000 copies of verified DLLs (see `gen_files.py`)
2. Create evil plugin that reads the flag and stores it into `/tmp` (see `bad_plugin.cs`). Has to be moved to the server.
3. Hit the reliable race window with `race.c`. Has to be build statically and moved to the server.

Not sure of the `setuid, seteuid` in the plugin is nessecary. But it does not hurt.

To build the DLL, the `mono:latest` container can be used: `docker run -v $(pwd):/stuff -t -i mono:latest /bin/bash`