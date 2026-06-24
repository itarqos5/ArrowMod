$ErrorActionPreference = "Stop"

$props = Get-Content "$PSScriptRoot\gradle.properties" -Raw
$mcVersion = ($props | Select-String -Pattern '(?m)^minecraft_version=(.+)$').Matches[0].Groups[1].Value.Trim()

$modes = @(
    @{ Label = "Fabric Client";   Build = ":fabric:remapJar"; Run = ":fabric:runClient" },
    @{ Label = "Fabric Server";   Build = ":fabric:remapJar"; Run = ":fabric:runServer" },
    @{ Label = "NeoForge Client"; Build = ":neoforge:jar";    Run = ":neoforge:runClient" },
    @{ Label = "NeoForge Server"; Build = ":neoforge:jar";    Run = ":neoforge:runServer" },
    @{ Label = "Paper Server";    Build = ":paper:jar";       Run = "paper" }
)

Write-Host ""
Write-Host "  Arrow & Slots - Launcher"
Write-Host "  ========================"
Write-Host "  Minecraft $mcVersion"
Write-Host ""
for ($i = 0; $i -lt $modes.Count; $i++) {
    Write-Host "    [$($i + 1)] $($modes[$i].Label)"
}
Write-Host ""
$choice = Read-Host "  Select (1-$($modes.Count))"

$idx = [int]$choice - 1
if ($idx -lt 0 -or $idx -ge $modes.Count) {
    Write-Host "Invalid choice."
    exit 1
}

$selected = $modes[$idx]

Write-Host ""
Write-Host "  Building $($selected.Build)..."
gradle $selected.Build --no-daemon --warning-mode summary
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed."
    exit 1
}

if ($selected.Run -eq "paper") {
    # ---- Paper / Folia server ----
    $serverDir = "$PSScriptRoot\paper-server"
    $pluginsDir = "$serverDir\plugins"
    $serverJar = "$serverDir\paper.jar"
    $eulaFile = "$serverDir\eula.txt"

    New-Item -ItemType Directory -Path $pluginsDir -Force | Out-Null

    if (-not (Test-Path $eulaFile)) {
        "eula=true" | Set-Content $eulaFile
    }

    # Copy the plugin jar
    $jar = Get-ChildItem "$PSScriptRoot\paper\build\libs\*.jar" |
        Where-Object { $_.Name -notmatch '-sources' } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    Copy-Item $jar.FullName "$pluginsDir\$($jar.Name)" -Force
    Write-Host "  Plugin: $($jar.Name)"

    # Download Paper server if missing
    if (-not (Test-Path $serverJar)) {
        Write-Host "  Downloading Paper $mcVersion (latest build)..."
        try {
            $builds = Invoke-RestMethod "https://api.papermc.io/v2/projects/paper/versions/$mcVersion/builds"
            $latest = $builds.builds[-1]
            $dlName = $latest.downloads.application.name
            $url = "https://api.papermc.io/v2/projects/paper/versions/$mcVersion/builds/$($latest.build)/downloads/$dlName"
            Invoke-WebRequest $url -OutFile $serverJar
            Write-Host "  Downloaded build $($latest.build)"
        }
        catch {
            Write-Host "  ERROR: Could not download Paper $mcVersion - $_"
            Write-Host "  Place paper.jar manually in $serverDir\ and re-run."
            exit 1
        }
    }

    # Create minimal server.properties for local testing
    $sp = "$serverDir\server.properties"
    if (-not (Test-Path $sp)) {
        @(
            "online-mode=false"
            "motd=Arrow & Slots Test Server"
            "level-type=flat"
            "gamemode=creative"
        ) | Set-Content $sp
    }

    Write-Host "  Starting Paper server..."
    Write-Host "  (stop with Ctrl+C or type 'stop' in the console)"
    Write-Host ""
    Push-Location $serverDir
    try {
        java -Xmx2G -Xms1G -jar paper.jar --nogui
    }
    finally {
        Pop-Location
    }
}
else {
    # ---- Fabric / NeoForge ----
    Write-Host "  Launching $($selected.Label)..."
    Write-Host ""
    gradle $selected.Run --no-daemon --warning-mode summary
}
