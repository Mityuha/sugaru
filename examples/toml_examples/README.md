# Toml servers' configuration
Let's suppose that you have some servers with fixed ip-address and some domain controller.   
Also, let's suppose that writing configuration file the hundredth time you have to specify all server's attributes there.   
Is it worth it? I don't think so. If you don't either let's come up with some declarative syntax for it.    
Let's say that all we need to do is just specify if server enabled or not.    
Such an approach has at least two benefits:
- You shouldn't change loads of configuration files every time the server's ip-address/dns-name changed
- You shouldn't remove/append the whole server's section on demand. All you need to do is just switch from false to true or vice-versa

Let's see how it works.
## Expected input
Let's say that we have configuration file, where we can switch on/off `alpha` and `beta` servers.   
```toml
title = "TOML Example"

[database]
server = "192.168.1.1"
ports = [ 8000, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]
alpha = true
beta = false
hosts = ["alpha", "omega"]
```
## Expected output
In the case above we have an alpha-server enabled and beta-server not. That how the output will look like:
```toml
title = "TOML Example"

[database]
server = "192.168.1.1"
ports = [ 8000, 8001, 8002,]
connection_max = 5000
enabled = true

[servers]
hosts = [ "alpha", "omega",]

[servers."servers.alpha"]
ip = "10.0.0.1"
dc = "eqdc10"
```
## Run it
First, if your python version is less that 3.11, you have to install toml package by typing (e.g.):
```bash
$ pip install toml
```
Second, `sugaru` does not support toml format out-of-box. So if you simply type
```bash
$ python3 -m sugaru my.toml --plugin servers
```
You'll get the warning: `Cannot find plugin loader by extension '.toml'`.     
That's why we have to specify toml-file loader and toml-file writer.
```bash
$ python3 -m sugaru my.toml --plugin servers --file-loader toml_utils --file-writer toml_utils
```
