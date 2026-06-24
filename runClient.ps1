$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$versions = @(
    @{ L="1.21.1 (min)"; MC="1.21.1"; FA="0.116.12+1.21.1"; NF="21.1.234";          PA="1.21.1-R0.1-SNAPSHOT" },
    @{ L="1.21.2";        MC="1.21.2"; FA="0.102.3+1.21.2";  NF="21.2.89-beta";      PA="1.21.2-R0.1-SNAPSHOT" },
    @{ L="26.1.2 (max)";  MC="26.1.2"; FA="0.145.4+26.1.2";  NF="26.1.2.76";         PA="26.1.2-R0.1-SNAPSHOT" }
)
$modes = @(
    @{ L="Fabric Client";    B=":fabric:remapJar"; R=":fabric:runClient" },
    @{ L="Fabric Server";    B=":fabric:remapJar"; R=":fabric:runServer" },
    @{ L="NeoForge Client";  B=":neoforge:jar";    R=":neoforge:runClient" },
    @{ L="NeoForge Server";  B=":neoforge:jar";    R=":neoforge:runServer" },
    @{ L="Paper Server";     B=":paper:jar";        R="paper" }
)

function Pick($title, $items, $sel=0) {
    while ($true) {
        Clear-Host
        $w = 38
        $bar = "".PadLeft($w - 2, [char]0x2500)

        Write-Host ""
        Write-Host ("  {0}{1}{2}" -f [char]0x250C, $bar, [char]0x2510) -ForegroundColor DarkCyan
        Write-Host ("  {0}{1}{2}" -f [char]0x2502, "".PadLeft($w-2), [char]0x2502) -ForegroundColor DarkCyan

        $header = "  Arrow & Slots"
        Write-Host "  $([char]0x2502)" -ForegroundColor DarkCyan -NoNewline
        Write-Host $header -ForegroundColor White -NoNewline
        Write-Host "".PadLeft($w - 3 - $header.Length) -NoNewline
        Write-Host "$([char]0x2502)" -ForegroundColor DarkCyan

        $sub = "  $title"
        Write-Host "  $([char]0x2502)" -ForegroundColor DarkCyan -NoNewline
        Write-Host $sub -ForegroundColor DarkGray -NoNewline
        Write-Host "".PadLeft($w - 3 - $sub.Length) -NoNewline
        Write-Host "$([char]0x2502)" -ForegroundColor DarkCyan

        Write-Host ("  {0}{1}{2}" -f [char]0x2502, "".PadLeft($w-2), [char]0x2502) -ForegroundColor DarkCyan

        for ($i = 0; $i -lt $items.Count; $i++) {
            Write-Host "  $([char]0x2502)" -ForegroundColor DarkCyan -NoNewline
            if ($i -eq $sel) {
                Write-Host "  $([char]0x25B8) " -ForegroundColor Black -BackgroundColor Green -NoNewline
                Write-Host ("  $($items[$i])").PadRight($w - 6) -ForegroundColor Black -BackgroundColor Green -NoNewline
            } else {
                Write-Host "    $($items[$i])".PadRight($w - 3) -ForegroundColor DarkGray -NoNewline
            }
            Write-Host "$([char]0x2502)" -ForegroundColor DarkCyan
        }

        Write-Host ("  {0}{1}{2}" -f [char]0x2502, "".PadLeft($w-2), [char]0x2502) -ForegroundColor DarkCyan
        $hint = "  [up/down] navigate   [enter] select"
        Write-Host "  $([char]0x2502)" -ForegroundColor DarkCyan -NoNewline
        Write-Host $hint -ForegroundColor DarkGray -NoNewline
        Write-Host "".PadLeft($w - 3 - $hint.Length) -NoNewline
        Write-Host "$([char]0x2502)" -ForegroundColor DarkCyan
        Write-Host ("  {0}{1}{2}" -f [char]0x2514, $bar, [char]0x2518) -ForegroundColor DarkCyan
        Write-Host ""

        $k = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        switch ($k.VirtualKeyCode) {
            38 { if ($sel -gt 0) { $sel-- } }
            40 { if ($sel -lt $items.Count - 1) { $sel++ } }
            13 { return $sel }
            27 { exit 0 }
        }
    }
}

$vi = Pick "Select Minecraft version:" ($versions | % { $_.L })
$ver = $versions[$vi]

$mi = Pick "MC $($ver.MC) — select mode:" ($modes | % { $_.L })
$mod = $modes[$mi]

Clear-Host
Write-Host ""
Write-Host "  Building $($mod.L) for MC $($ver.MC) ..." -ForegroundColor Cyan
Write-Host ""

$ga = @($mod.B, "--no-daemon", "--warning-mode", "summary",
    "-Pminecraft_version=$($ver.MC)",
    "-Pfabric_api_version=$($ver.FA)",
    "-Pneoforge_version=$($ver.NF)",
    "-Ppaper_version=$($ver.PA)")

& gradle @ga
if ($LASTEXITCODE -ne 0) { Write-Host "`n  Build failed." -ForegroundColor Red; exit 1 }

if ($mod.R -eq "paper") {
    $sd = "$PSScriptRoot\paper-server"
    $pj = "$sd\paper.jar"
    New-Item -ItemType Directory -Path "$sd\plugins" -Force | Out-Null
    if (!(Test-Path "$sd\eula.txt")) { "eula=true" | Set-Content "$sd\eula.txt" }

    $jar = Get-ChildItem "$PSScriptRoot\paper\build\libs\*.jar" |
        Where-Object { $_.Name -notmatch 'sources' } | Sort-Object LastWriteTime -Desc | Select -First 1
    Copy-Item $jar.FullName "$sd\plugins\$($jar.Name)" -Force

    if (!(Test-Path $pj)) {
        Write-Host "  Downloading Paper $($ver.MC) ..." -ForegroundColor Yellow
        try {
            $b = (Invoke-RestMethod "https://api.papermc.io/v2/projects/paper/versions/$($ver.MC)/builds").builds[-1]
            Invoke-WebRequest "https://api.papermc.io/v2/projects/paper/versions/$($ver.MC)/builds/$($b.build)/downloads/$($b.downloads.application.name)" -OutFile $pj
        } catch { Write-Host "  Download failed: $_" -ForegroundColor Red; exit 1 }
    }
    if (!(Test-Path "$sd\server.properties")) {
        "online-mode=false","motd=Arrow & Slots Test","level-type=flat","gamemode=creative" | Set-Content "$sd\server.properties"
    }

    Write-Host "  Starting Paper server ..." -ForegroundColor Green
    Push-Location $sd; try { java -Xmx2G -Xms1G -jar paper.jar --nogui } finally { Pop-Location }
} else {
    Write-Host "  Launching $($mod.L) ..." -ForegroundColor Green
    Write-Host ""
    & gradle $mod.R --no-daemon --warning-mode summary
}
