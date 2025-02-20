Get-Content -Path "C:\Users\EpicPichu\AppData\Roaming\.minecraft\logs\latest.log" -Tail 0 -Wait |
Select-String -Pattern "\[CHAT\]" |
ForEach-Object {
    # Extract the chat message by removing everything before [CHAT]
    $line = $_.Line -replace '.*\[CHAT\] ', ''

    # Tab check
    if (
        (($line -split ' ').Count - 1) -eq (($line -split ',').Count - 1) -and 
        ($line -match "^[a-zA-Z0-9 _,]*$")
    )   {
        if ($line -match ".*,.*,.+") {
            Write-Output "TAB: $line"
        }
    }
    # Join check
    elseif ($line -match "^BedWars .* ([a-zA-Z0-9_]+) has joined! \s?(.*)") {
        Write-Output "JOIN: $($matches[1])"
        Write-Output "PLAYERCOUNT: $($matches[2])"
    }
    # Leave check
    elseif ($line -match "^BedWars .* ([a-zA-Z0-9_]+) has quit! \s?(.*)") {
        Write-Output "LEAVE: $($matches[1])"
        Write-Output "PLAYERCOUNT: $($matches[2])"
    }
}
