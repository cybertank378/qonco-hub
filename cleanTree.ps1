function Get-CleanTree {
    param (
        [string]$Path = ".",
        [string[]]$Exclude = @(".venv", ".git", ".idea"),
        [int]$Depth = 10,
        [string]$Indent = "",
        [string]$BasePath = $Path
    )

    $items = Get-ChildItem -Path $Path -Force

    foreach ($item in $items) {
        $relativePath = $item.FullName.Substring((Resolve-Path $BasePath).Path.Length).TrimStart('\', '/')

        if ($Exclude -contains $relativePath) {
            continue
        }

        Write-Output "$Indent├── $($item.Name)"

        if ($item.PSIsContainer -and $Depth -gt 0) {
            Get-CleanTree -Path $item.FullName -Exclude $Exclude -Depth ($Depth - 1) -Indent "$Indent│   " -BasePath $BasePath
        }
    }
}

Get-CleanTree | Out-File clean-tree.txt
