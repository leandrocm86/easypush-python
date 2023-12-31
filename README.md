# easypush
### An easier way to exchange texts between your devices


This is the Python module and CLI (terminal only) client of EasyPush.<br>
EasyPush is a multi-platform and serverless (decentralized) utility to easily exchange text messages between devices through any given UDP port.<br>
No login or any account required! Not even an internet connection is necessary (as long as your devices are on the same local network).<br>
On one end, run EasyPush on the devices you want to receive notifications by just selecting any UDP port to listen to. On the other end, use EasyPush to send messages to the desired recipients by their IPs/hostnames and the port you previously chose, and all listeners of that port will be notified.

#### Use cases:
- Easily share a link between PC and phone:
Tired of copying/pasting (and then copying/pasting again) online notes to share links or texts between your devices?
EasyPush allows you to quickly move texts from one device to another.
Once a message is sent, PCs and Android phones running EasyPush are able to show a notification with the new message, along with the options to quickly copy it or browse it directly. No hassle about account logins or manually switching between apps or sites.

- Server automation:
With EasyPush your server can easily send you warnings even when no internet is available. You can also go the other way around, sending commands for the server to read and start your tasks.
Tired of going through SSH everytime just to start trivial jobs? Program your server to act upon the text it receives through EasyPush. You can probably achieve the same result by using REST APIs or netcat/telnet, but EasyPush makes it more simple because it's focused on only exchanging regular text, without all the overhead and configurations needed on those other solutions. Plus, since it's multi-platform you can easily integrate Linux/Windows/Android devices with barely no configuration needed.

#### Installation:
EasyPush's Python module and client can easily be installed via pip (python3 and pip required) with
```
pip install easypush
```
This way, you can launch it with the *easypush* command, or integrate it directly with your own python scripts by importing the *easypush* module.

#### EasyPush is also available for PCs with Java (Windows/Linux/Mac) and phones with Android.
Java's CLI client and library: https://github.com/leandrocm86/easypush-cli/<br>
Desktop (GUI) client: https://github.com/leandrocm86/easypush/<br>
Android client: Download  the [app on GooglePlay](https://play.google.com/store/apps/details?id=lcm.easypush), or check the [project on github](https://github.com/leandrocm86/easypush-android)<br>
All projects are free, open sourced and open to suggestions.

#### Usage

##### CLI client:
EasyPush's Python CLI client can be used in two ways: sender mode and listener mode.<br>
Sender mode: **easypush send \<IPs\>@\<PORT\> \<message\>** <br>
Example:
```
easypush send 192.168.0.255@1050 'Hello world!'
```
On Sender mode, the client(s) with the IP(s) informed (comma separated) will receive the text if listening on the given port. Consider using a broadcast IP if you have many devices or if you don't know their addresses. <br>

Receiver mode: **easypush listen \<PORT\>  [--timeout MILLISECONDS] [--keep-alive]** <br>
Example:
```
easypush listen 1050
```
On listener mode, EasyPush will wait for the first message on the given UDP port and print it to standard output. Then it will quit, unless the optional *-k/--keep-alive* flag is set, in which case EasyPush will keep printing every text received on that port. You can also set the optional *--timeout* parameter so the listener will terminate after a given time (in milliseconds).<br>

##### Python module:
Instead of using the CLI client, python scripts can directly integrate with EasyPush's module. It has only two functions: *send* and *listen*. Read their docstrings or source for details.  
Example:
```
import easypush

easypush.send(['192.168.0.255'], 1050, 'Hello, world!')
received_message = easypush.listen(1050)
print('Received message:', received_message)
```