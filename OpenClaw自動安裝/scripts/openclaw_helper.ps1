param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('status', 'install-prerequisites', 'install-openclaw', 'uninstall-openclaw', 'stop-gateway')]
    [string]$Action
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding

function Invoke-CommandAndCapture {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [string[]]$Arguments = @()
    )

    $originalPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $output = & $FilePath @Arguments 2>&1
        $exitCode = if ($null -ne $LASTEXITCODE) { $LASTEXITCODE } else { 0 }
        return [pscustomobject]@{
            Output = ($output | Out-String).Trim()
            ExitCode = $exitCode
        }
    }
    finally {
        $ErrorActionPreference = $originalPreference
    }
}

function Get-VersionInfo {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CommandName,
        [string[]]$Arguments = @('--version')
    )

    $command = Get-Command $CommandName -ErrorAction SilentlyContinue
    if (-not $command) {
        return [ordered]@{
            installed = $false
            version = $null
            path = $null
        }
    }

    $result = Invoke-CommandAndCapture -FilePath $command.Source -Arguments $Arguments
    return [ordered]@{
        installed = $true
        version = $result.Output
        path = $command.Source
    }
}

function Get-NpmGlobalPrefix {
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npm) {
        return $null
    }

    $result = Invoke-CommandAndCapture -FilePath $npm.Source -Arguments @('prefix', '-g')
    if ($result.ExitCode -ne 0) {
        return $null
    }

    return $result.Output.Trim()
}

function Resolve-OpenClawPath {
    $prefix = Get-NpmGlobalPrefix
    if ($prefix) {
        $cmdPath = Join-Path $prefix 'openclaw.cmd'
        if (Test-Path $cmdPath) {
            return $cmdPath
        }
    }

    $command = Get-Command openclaw -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    return $null
}

function Convert-VersionSafely {
    param([string]$Value)

    if (-not $Value) {
        return $null
    }

    if ($Value -match '(\d+\.\d+\.\d+)') {
        return [version]$Matches[1]
    }

    return $null
}

function Test-VersionAtLeast {
    param(
        [string]$Actual,
        [string]$Minimum
    )

    $actualVersion = Convert-VersionSafely $Actual
    if (-not $actualVersion) {
        return $false
    }

    return $actualVersion -ge ([version]$Minimum)
}

function Get-GatewayProcesses {
    $processes = Get-CimInstance Win32_Process | Where-Object {
        $_.CommandLine -and (
            $_.CommandLine -match 'openclaw(\.cmd|\.mjs)?\s+gateway' -or
            $_.CommandLine -match 'node(.exe)? .*openclaw.*gateway'
        )
    }

    return $processes
}

function Test-WingetInstalled {
    return [bool](Get-Command winget -ErrorAction SilentlyContinue)
}

function Test-WingetNoApplicableUpgrade {
    param(
        [Parameter(Mandatory = $true)]
        [int]$ExitCode,
        [string]$Output = ''
    )

    if ($ExitCode -eq -1978335189) {
        return $true
    }

    return $false
}

function Invoke-WingetPackage {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PackageId,
        [Parameter(Mandatory = $true)]
        [string]$DisplayName
    )

    if (-not (Test-WingetInstalled)) {
        throw 'winget is required to install dependencies automatically.'
    }

    Write-Host "=== $DisplayName ($PackageId) ==="
    $listResult = Invoke-CommandAndCapture -FilePath 'winget' -Arguments @('list', '--id', $PackageId, '--exact', '--accept-source-agreements')
    $isInstalled = $listResult.ExitCode -eq 0 -and $listResult.Output -match [regex]::Escape($PackageId)

    if ($isInstalled) {
        $upgradeResult = Invoke-CommandAndCapture -FilePath 'winget' -Arguments @('upgrade', '--id', $PackageId, '--exact', '--accept-package-agreements', '--accept-source-agreements', '--disable-interactivity')
        if ($upgradeResult.Output) {
            Write-Host $upgradeResult.Output
        }
        if ($upgradeResult.ExitCode -ne 0 -and -not (Test-WingetNoApplicableUpgrade -ExitCode $upgradeResult.ExitCode -Output $upgradeResult.Output)) {
            throw "winget upgrade $PackageId failed."
        }
        return
    }

    & winget install --id $PackageId --exact --accept-package-agreements --accept-source-agreements --disable-interactivity
    if ($LASTEXITCODE -ne 0) {
        throw "winget install $PackageId failed."
    }
}

function Get-Status {
    $pwsh = Get-VersionInfo -CommandName 'pwsh'
    $node = Get-VersionInfo -CommandName 'node'
    $npm = Get-VersionInfo -CommandName 'npm'
    $git = Get-VersionInfo -CommandName 'git'
    $python = Get-VersionInfo -CommandName 'python'
    $py = Get-VersionInfo -CommandName 'py' -Arguments @('-3', '--version')
    $openClawPath = Resolve-OpenClawPath

    $openclaw = if ($openClawPath) {
        $versionResult = Invoke-CommandAndCapture -FilePath $openClawPath -Arguments @('--version')
        [ordered]@{
            installed = $true
            version = $versionResult.Output
            path = $openClawPath
        }
    }
    else {
        [ordered]@{
            installed = $false
            version = $null
            path = $null
        }
    }

    $gatewayProcesses = @(Get-GatewayProcesses)
    $npmPrefix = Get-NpmGlobalPrefix

    [ordered]@{
        tools = [ordered]@{
            pwsh = $pwsh
            node = $node
            npm = $npm
            git = $git
            python = $python
            py = $py
            openclaw = $openclaw
            npmGlobalPrefix = $npmPrefix
            openclawResolvedPath = $openClawPath
        }
        requirements = [ordered]@{
            wingetAvailable = (Test-WingetInstalled)
            pwsh7Installed = ($pwsh.installed -and (Test-VersionAtLeast -Actual $pwsh.version -Minimum '7.0.0'))
            nodeSatisfiesMinimum = ($node.installed -and (Test-VersionAtLeast -Actual $node.version -Minimum '22.16.0'))
            nodeRecommended = ($node.installed -and (Test-VersionAtLeast -Actual $node.version -Minimum '24.0.0'))
        }
        gateway = [ordered]@{
            running = ($gatewayProcesses.Count -gt 0)
            pids = @($gatewayProcesses | ForEach-Object { $_.ProcessId })
        }
    }
}

function Install-Prerequisites {
    Invoke-WingetPackage -PackageId 'Microsoft.PowerShell' -DisplayName 'PowerShell 7'
    Invoke-WingetPackage -PackageId 'OpenJS.NodeJS.LTS' -DisplayName 'Node.js LTS'
    Invoke-WingetPackage -PackageId 'Git.Git' -DisplayName 'Git'
    Invoke-WingetPackage -PackageId 'Python.Python.3.12' -DisplayName 'Python 3.12'
}

function Install-OpenClaw {
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npm) {
        throw 'npm was not found. Install Node.js first.'
    }

    $status = Get-Status
    if (-not $status.requirements.nodeSatisfiesMinimum) {
        throw 'Node.js version is too old. Update to 22.16.0 or newer.'
    }

    & $npm.Source install -g openclaw@latest
    if ($LASTEXITCODE -ne 0) {
        throw 'npm install -g openclaw@latest failed.'
    }
}

function Uninstall-OpenClaw {
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npm) {
        throw 'npm was not found. Cannot uninstall OpenClaw.'
    }

    & $npm.Source uninstall -g openclaw
    if ($LASTEXITCODE -ne 0) {
        throw 'npm uninstall -g openclaw failed.'
    }
}

function Stop-Gateway {
    $processes = @(Get-GatewayProcesses)
    if (-not $processes.Count) {
        Write-Host 'No running OpenClaw Gateway processes were detected.'
        return
    }

    $processes | ForEach-Object {
        Write-Host "Stopping PID $($_.ProcessId): $($_.CommandLine)"
        Stop-Process -Id $_.ProcessId -Force
    }
}

switch ($Action) {
    'status' {
        Get-Status | ConvertTo-Json -Depth 6
    }
    'install-prerequisites' {
        Install-Prerequisites
    }
    'install-openclaw' {
        Install-OpenClaw
    }
    'uninstall-openclaw' {
        Uninstall-OpenClaw
    }
    'stop-gateway' {
        Stop-Gateway
    }
}