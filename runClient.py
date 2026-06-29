import os, subprocess, sys, shutil, urllib.request, urllib.parse, json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

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

# Helpers for mod management and Modrinth API integration

def is_our_mod(filename):
    fn = filename.lower()
    return "arrow-and-slots" in fn or "arrowandslots" in fn or "arrowmod" in fn or "arrow_and_slots" in fn

def cleanup_own_jars(directory):
    if not os.path.exists(directory):
        return
    for f in os.listdir(directory):
        if f.endswith(".jar") and is_our_mod(f):
            try:
                os.remove(os.path.join(directory, f))
            except:
                pass

def get_external_mods(target_dir):
    if not os.path.exists(target_dir):
        return []
    return [f for f in os.listdir(target_dir) if f.endswith(".jar") and not is_our_mod(f)]

def print_status_message(msg, color=GR):
    os.system("cls")
    w = 44
    bar = "\u2500" * (w - 2)
    print()
    print(f"  {C}\u250C{bar}\u2510{S}")
    print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
    lines_to_print = []
    # split by lines first to preserve original formatting
    for part in msg.split('\n'):
        words = part.split()
        if not words:
            lines_to_print.append("")
            continue
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= 36:
                current_line = (current_line + " " + word).strip()
            else:
                lines_to_print.append(current_line)
                current_line = word
        if current_line:
            lines_to_print.append(current_line)
    for l in lines_to_print:
        print(line("  ", l, color))
    print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
    print(line("  ", "Press any key to continue"))
    print(f"  {C}\u2514{bar}\u2518{S}")
    print()
    msvcrt.getch()

def print_status_no_key(msg, color=GR):
    os.system("cls")
    w = 44
    bar = "\u2500" * (w - 2)
    print()
    print(f"  {C}\u250C{bar}\u2510{S}")
    print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
    lines_to_print = []
    for part in msg.split('\n'):
        words = part.split()
        if not words:
            lines_to_print.append("")
            continue
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= 36:
                current_line = (current_line + " " + word).strip()
            else:
                lines_to_print.append(current_line)
                current_line = word
        if current_line:
            lines_to_print.append(current_line)
    for l in lines_to_print:
        print(line("  ", l, color))
    print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
    print(f"  {C}\u2514{bar}\u2518{S}")
    print()

def search_modrinth(query, loader, mc_version):
    if loader == "paper":
        loader_categories = ["categories:paper", "categories:spigot", "categories:bukkit"]
        project_type = "plugin"
    else:
        loader_categories = [f"categories:{loader}"]
        project_type = "mod"
        
    facets = [
        loader_categories,
        [f"versions:{mc_version}"],
        [f"project_type:{project_type}"]
    ]
    
    facets_str = json.dumps(facets)
    params = {
        "query": query,
        "facets": facets_str,
        "limit": 5
    }
    
    url = "https://api.modrinth.com/v2/search?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ArrowMod-ClientRunner/1.0.0"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("hits", [])
    except Exception as e:
        return []

def get_latest_compatible_version(project_id, loader, mc_version):
    url = f"https://api.modrinth.com/v2/project/{project_id}/version"
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ArrowMod-ClientRunner/1.0.0"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            versions = json.loads(response.read().decode('utf-8'))
            
            for v in versions:
                if mc_version in v.get("game_versions", []):
                    loaders = v.get("loaders", [])
                    if loader in loaders or (loader == "paper" and ("spigot" in loaders or "bukkit" in loaders)):
                        files = v.get("files", [])
                        if files:
                            primary_file = next((f for f in files if f.get("primary")), files[0])
                            return {
                                "version_number": v.get("version_number"),
                                "filename": primary_file.get("filename"),
                                "url": primary_file.get("url")
                            }
    except Exception as e:
        pass
    return None

def view_installed_mods(ext_mods):
    while True:
        os.system("cls")
        w = 44
        bar = "\u2500" * (w - 2)
        print()
        print(f"  {C}\u250C{bar}\u2510{S}")
        print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
        print(line("  ", "Installed External Mods", W))
        print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
        for m in ext_mods:
            display_name = m
            if len(display_name) > 34:
                display_name = display_name[:31] + "..."
            print(line("  - ", display_name, GR))
        print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
        print(line("  ", "Press any key to return"))
        print(f"  {C}\u2514{bar}\u2518{S}")
        print()
        msvcrt.getch()
        break

def remove_mod_menu(target_dir, ext_mods):
    if not ext_mods:
        return
    options = ext_mods + ["Back"]
    sel = pick("Select mod to remove:", options)
    if sel < len(ext_mods):
        mod_to_remove = ext_mods[sel]
        try:
            os.remove(os.path.join(target_dir, mod_to_remove))
            print_status_message(f"Removed:\n{mod_to_remove}")
        except Exception as e:
            print_status_message(f"Error removing file:\n{e}", color=R)

def clear_all_mods(target_dir, ext_mods):
    options = ["No, Keep Them", "Yes, Clear All"]
    sel = pick("Clear all external mods?", options)
    if sel == 1:
        success_count = 0
        for m in ext_mods:
            try:
                os.remove(os.path.join(target_dir, m))
                success_count += 1
            except:
                pass
        print_status_message(f"Cleared {success_count} mods.")

def add_mod_menu(loader, mc_version, target_dir):
    os.system("cls")
    w = 44
    bar = "\u2500" * (w - 2)
    print()
    print(f"  {C}\u250C{bar}\u2510{S}")
    print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
    print(line("  ", "Search Modrinth", W))
    print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
    print(line("  ", "Enter mod/plugin name:", G))
    print(f"  {C}\u2502{' ' * (w - 2)}\u2502{S}")
    print(f"  {C}\u2514{bar}\u2518{S}")
    print()
    
    sys.stdout.write(f"  Search: ")
    sys.stdout.flush()
    try:
        query = input().strip()
    except KeyboardInterrupt:
        return
        
    if not query:
        return
        
    print_status_no_key(f"Searching Modrinth for '{query}'...")
    hits = search_modrinth(query, loader, mc_version)
    if not hits:
        print_status_message("No results found or error occurred.", color=R)
        return
        
    options = [h["title"] for h in hits] + ["Back"]
    sel = pick("Select mod to download:", options)
    if sel >= len(hits):
        return
        
    selected_hit = hits[sel]
    project_id = selected_hit["project_id"]
    title = selected_hit["title"]
    
    print_status_no_key(f"Fetching versions for:\n{title}...")
    version_info = get_latest_compatible_version(project_id, loader, mc_version)
    if not version_info:
        print_status_message(f"No compatible version found\nfor MC {mc_version}.", color=R)
        return
        
    filename = version_info["filename"]
    url = version_info["url"]
    dest_path = os.path.join(target_dir, filename)
    
    print_status_no_key(f"Downloading:\n{filename}...")
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "ArrowMod-ClientRunner/1.0.0"}
        )
        with urllib.request.urlopen(req) as response:
            with open(dest_path, "wb") as f:
                f.write(response.read())
        print_status_message(f"Successfully downloaded:\n{filename}")
    except Exception as e:
        print_status_message(f"Download failed:\n{e}", color=R)

def manage_mods(loader, mc_version, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    while True:
        ext_mods = get_external_mods(target_dir)
        options = ["Proceed to Launch"]
        if ext_mods:
            options.append(f"View installed mods ({len(ext_mods)})")
            options.append("Remove a mod")
            options.append("Clear all external mods")
        options.append("Add a mod from Modrinth")
        options.append("Cancel and exit")
        
        sel = pick(f"External Mods ({loader}):", options)
        opt = options[sel]
        
        if opt == "Proceed to Launch":
            break
        elif opt.startswith("View installed mods"):
            view_installed_mods(ext_mods)
        elif opt == "Remove a mod":
            remove_mod_menu(target_dir, ext_mods)
        elif opt == "Clear all external mods":
            clear_all_mods(target_dir, ext_mods)
        elif opt == "Add a mod from Modrinth":
            add_mod_menu(loader, mc_version, target_dir)
        elif opt == "Cancel and exit":
            sys.exit(0)

# Main Flow

script_dir = os.path.dirname(os.path.abspath(__file__))

vi = pick("Select Minecraft version:", [v["l"] for v in VERSIONS])
ver = VERSIONS[vi]
mi = pick(f"MC {ver['mc']} - select mode:", [m["l"] for m in MODES])
mode = MODES[mi]

# Determine target folder and loader
if "fabric" in mode["r"]:
    loader = "fabric"
    target_dir = os.path.abspath(os.path.join(script_dir, "fabric", "run", "mods"))
elif "neoforge" in mode["r"]:
    loader = "neoforge"
    target_dir = os.path.abspath(os.path.join(script_dir, "neoforge", "run", "mods"))
elif mode["r"] == "paper":
    loader = "paper"
    target_dir = os.path.abspath(os.path.join(script_dir, "paper-server", "plugins"))
else:
    loader = None
    target_dir = None

# Show mod manager if applicable
if loader and target_dir:
    manage_mods(loader, ver["mc"], target_dir)

# Clean up own mod's duplicate jars in the launcher folder to avoid duplicates
if target_dir:
    cleanup_own_jars(target_dir)

# Build command dynamically using wrapper if available
if sys.platform == "win32":
    gradle_cmd = os.path.join(script_dir, "gradlew.bat") if os.path.exists(os.path.join(script_dir, "gradlew.bat")) else "gradle"
else:
    gradle_cmd = os.path.join(script_dir, "gradlew") if os.path.exists(os.path.join(script_dir, "gradlew")) else "gradle"

os.system("cls")
print(f"\n  {C}Building {mode['l']} for MC {ver['mc']} ...{S}\n")
r = subprocess.run([gradle_cmd, mode["b"], "--no-daemon", "--warning-mode", "summary",
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
    
    # Copy plugin
    libs = os.path.join(script_dir, "paper", "build", "libs")
    if os.path.exists(libs):
        jars = sorted([f for f in os.listdir(libs) if f.endswith(".jar") and "sources" not in f],
                      key=lambda f: os.path.getmtime(os.path.join(libs, f)), reverse=True)
        if jars:
            # Make sure we clean up duplicate/old own jars first, then copy the new one
            cleanup_own_jars(os.path.join(sd, "plugins"))
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
    subprocess.run([gradle_cmd, mode["r"], "--no-daemon", "--warning-mode", "summary",
        f"-Pminecraft_version={ver['mc']}", f"-Pfabric_api_version={ver['fa']}",
        f"-Pneoforge_version={ver['nf']}", f"-Ppaper_version={ver['pa']}"])
