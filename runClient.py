import os, subprocess, sys, shutil, urllib.request, json

os.system('')
import msvcrt

VERSIONS = [
    {"l":"1.21.1",  "mc":"1.21.1",  "fa":"0.116.12+1.21.1", "nf":"21.1.234",      "pa":"1.21.1-R0.1-SNAPSHOT"},
    {"l":"1.21.2",  "mc":"1.21.2",  "fa":"0.102.3+1.21.2",  "nf":"21.2.89-beta",  "pa":"1.21.2-R0.1-SNAPSHOT"},
    {"l":"1.21.3",  "mc":"1.21.3",  "fa":"0.114.1+1.21.3",  "nf":"21.3.95",       "pa":"1.21.3-R0.1-SNAPSHOT"},
    {"l":"1.21.4",  "mc":"1.21.4",  "fa":"0.119.4+1.21.4",  "nf":"21.4.156",      "pa":"1.21.4-R0.1-SNAPSHOT"},
    {"l":"1.21.5",  "mc":"1.21.5",  "fa":"0.128.2+1.21.5",  "nf":"21.5.96",       "pa":"1.21.5-R0.1-SNAPSHOT"},
    {"l":"1.21.6",  "mc":"1.21.6",  "fa":"0.128.2+1.21.6",  "nf":"21.6.20-beta",  "pa":"1.21.6-R0.1-SNAPSHOT"},
    {"l":"1.21.7",  "mc":"1.21.7",  "fa":"0.129.0+1.21.7",  "nf":"21.7.25-beta",  "pa":"1.21.7-R0.1-SNAPSHOT"},
    {"l":"1.21.8",  "mc":"1.21.8",  "fa":"0.136.1+1.21.8",  "nf":"21.8.52",       "pa":"1.21.8-R0.1-SNAPSHOT"},
    {"l":"1.21.9",  "mc":"1.21.9",  "fa":"0.134.1+1.21.9",  "nf":"21.9.16-beta",  "pa":"1.21.9-R0.1-SNAPSHOT"},
    {"l":"1.21.10", "mc":"1.21.10", "fa":"0.138.4+1.21.10", "nf":"21.10.64",      "pa":"1.21.10-R0.1-SNAPSHOT"},
    {"l":"1.21.11", "mc":"1.21.11", "fa":"0.139.4+1.21.11", "nf":"21.11.8-beta",  "pa":"1.21.11-R0.1-SNAPSHOT"},
]
MODES = [
    {"l":"Fabric Client",   "b":":fabric:remapJar","r":":fabric:runClient"},
    {"l":"Fabric Server",   "b":":fabric:remapJar","r":":fabric:runServer"},
    {"l":"NeoForge Client", "b":":neoforge:jar",   "r":":neoforge:runClient"},
    {"l":"NeoForge Server", "b":":neoforge:jar",   "r":":neoforge:runServer"},
    {"l":"Paper Server",    "b":":paper:jar",       "r":"paper"},
]

C  = "\033[36m"
W  = "\033[37m"
G  = "\033[90m"
R  = "\033[31m"
Y  = "\033[33m"
GR = "\033[32m"
S  = "\033[0m"
n  = "\033[30;42m"

def line(pre, text, color=G):
    pad = max(0, 44 - 3 - len(pre + text))
    return f"  {C}\u2502{color}{pre}{text}{' ' * pad}{C}\u2502{S}"

def pick(title, items, sel=0):
    while True:
        os.system("cls")
        w = 44
        bar = "\u2500" * (w - 2)
        print()
        print(f"  {C}\u250C{bar}\u2510{S}")
        print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
        print(line("  ", "Arrow & Slots", W))
        print(line("  ", title))
        print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
        for i, item in enumerate(items):
            if i == sel:
                l = f"  \u25b8   {item}"
                pad = max(0, w - 3 - len(l))
                print(f"  {C}\u2502{n}{l}{' ' * pad}{S}{C}\u2502{S}")
            else:
                l = f"      {item}"
                pad = max(0, w - 3 - len(l))
                print(f"  {C}\u2502{G}{l}{' ' * pad}{C}\u2502{S}")
        print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
        print(line("  ", "\u2191\u2193 navigate   \u21a9 select"))
        print(f"  {C}\u2514{bar}\u2518{S}")
        print()
        k = msvcrt.getch()
        if k == b'\xe0':
            k = msvcrt.getch()
            if k == b'H' and sel > 0: sel -= 1
            elif k == b'P' and sel < len(items) - 1: sel += 1
        elif k == b'\r': return sel
        elif k == b'\x1b': sys.exit(0)

script_dir = os.path.dirname(os.path.abspath(__file__))

vi = pick("Select Minecraft version:", [v["l"] for v in VERSIONS])
ver = VERSIONS[vi]
mi = pick(f"MC {ver['mc']} - select mode:", [m["l"] for m in MODES])
mode = MODES[mi]

os.system("cls")
print(f"\n  {C}Building {mode['l']} for MC {ver['mc']} ...{S}\n")
r = subprocess.run(["gradle", mode["b"], "--no-daemon", "--warning-mode", "summary",
    f"-Pminecraft_version={ver['mc']}", f"-Pfabric_api_version={ver['fa']}",
    f"-Pneoforge_version={ver['nf']}", f"-Ppaper_version={ver['pa']}"])
if r.returncode != 0:
    print(f"\n  {R}Build failed.{S}")
    sys.exit(1)

if mode["r"] == "paper":
    sd = os.path.join(script_dir, "paper-server")
    pj = os.path.join(sd, "paper.jar")
    os.makedirs(os.path.join(sd, "plugins"), exist_ok=True)
    if not os.path.exists(os.path.join(sd, "eula.txt")):
        open(os.path.join(sd, "eula.txt"), "w").write("eula=true")
    libs = os.path.join(script_dir, "paper", "build", "libs")
    jars = sorted([f for f in os.listdir(libs) if f.endswith(".jar") and "sources" not in f],
                  key=lambda f: os.path.getmtime(os.path.join(libs, f)), reverse=True)
    shutil.copy2(os.path.join(libs, jars[0]), os.path.join(sd, "plugins", jars[0]))
    if not os.path.exists(pj):
        print(f"  {Y}Downloading Paper {ver['mc']} ...{S}")
        try:
            data = json.loads(urllib.request.urlopen(f"https://api.papermc.io/v2/projects/paper/versions/{ver['mc']}/builds").read())
            b = data["builds"][-1]
            urllib.request.urlretrieve(f"https://api.papermc.io/v2/projects/paper/versions/{ver['mc']}/builds/{b['build']}/downloads/{b['downloads']['application']['name']}", pj)
        except Exception as e:
            print(f"  {R}Download failed: {e}{S}")
            sys.exit(1)
    sp = os.path.join(sd, "server.properties")
    if not os.path.exists(sp):
        open(sp, "w").write("online-mode=false\nmotd=Arrow and Slots Test\nlevel-type=flat\ngamemode=creative\n")
    print(f"  {GR}Starting Paper server ...{S}")
    subprocess.run(["java", "-Xmx2G", "-Xms1G", "-jar", "paper.jar", "--nogui"], cwd=sd)
else:
    print(f"  {GR}Launching {mode['l']} ...{S}\n")
    subprocess.run(["gradle", mode["r"], "--no-daemon", "--warning-mode", "summary",
        f"-Pminecraft_version={ver['mc']}", f"-Pfabric_api_version={ver['fa']}",
        f"-Pneoforge_version={ver['nf']}", f"-Ppaper_version={ver['pa']}"])
