$modes = @(
    @{ Label="Fabric Client";  Task=":fabric:runClient" },
    @{ Label="Fabric Server";  Task=":fabric:runServer" },
    @{ Label="NeoForge Client"; Task=":neoforge:runClient" },
    @{ Label="NeoForge Server"; Task=":neoforge:runServer" },
    @{ Label="Paper Server";   Task=":paper:runServer" }
)

Write-Host ""
Write-Host "Arrow & Slots - Launcher"
Write-Host "========================"
Write-Host ""
for ($i = 0; $i -lt $modes.Count; $i++) {
    Write-Host "  [$($i+1)] $($modes[$i].Label)"
}
Write-Host ""
$choice = Read-Host "Select mode (1-$($modes.Count))"

$idx = [int]$choice - 1
if ($idx -lt 0 -or $idx -ge $modes.Count) {
    Write-Host "Invalid choice."
    exit 1
}

$selected = $modes[$idx]
Write-Host ""
Write-Host "Launching: $($selected.Label)"
Write-Host ""

gradle $selected.Task --no-daemon --warning-mode summary
