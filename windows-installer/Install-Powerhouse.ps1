[CmdletBinding()]
param(
    [switch]$LaunchAfterInstall
)

$ErrorActionPreference = 'Stop'

function Write-Section {
    param([string]$Message)
    Write-Host "`n=== $Message ===" -ForegroundColor Cyan
}

function Ensure-Winget {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Error "Winget is required. Install it from the Microsoft Store (App Installer) and rerun this installer."}
}

function Ensure-Package {
    param(
        [string]$Id,
        [string]$DisplayName
    )

    $alreadyInstalled = (winget list --id $Id | Select-String $Id)
    if ($alreadyInstalled) {
        Write-Host "$DisplayName already installed." -ForegroundColor Green
        return
    }

    Write-Host "Installing $DisplayName..." -ForegroundColor Yellow
    winget install --id $Id --silent --accept-package-agreements --accept-source-agreements | Out-Null
    Write-Host "$DisplayName installed." -ForegroundColor Green
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "Powerhouse Windows Installer" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host "This guided installer sets up everything with minimal prompts." -ForegroundColor White

Write-Section "Prerequisite check"
Ensure-Winget

Ensure-Package -Id "Git.Git" -DisplayName "Git"
Ensure-Package -Id "Python.Python.3.10" -DisplayName "Python 3.10"
Ensure-Package -Id "OpenJS.NodeJS.LTS" -DisplayName "Node.js (LTS)"

Write-Host "Ensuring Yarn is available..." -ForegroundColor Yellow
if (-not (Get-Command yarn -ErrorAction SilentlyContinue)) {
    npm install -g yarn --silent
    Write-Host "Yarn installed globally." -ForegroundColor Green
} else {
    Write-Host "Yarn already installed." -ForegroundColor Green
}

Write-Section "Backend dependencies"
Push-Location (Join-Path $repoRoot 'backend')
python -m pip install --upgrade pip --quiet
python -m pip install --no-cache-dir -r requirements.txt
Pop-Location

Write-Section "Frontend dependencies"
Push-Location (Join-Path $repoRoot 'frontend/app')
yarn install --ignore-optional
Pop-Location

Write-Section "Environment files"
$backendEnv = Join-Path $repoRoot 'backend/.env'
$backendExample = Join-Path $repoRoot 'backend/.env.example'
if (-not (Test-Path $backendEnv) -and (Test-Path $backendExample)) {
    Copy-Item $backendExample $backendEnv
    Write-Host "Created backend .env (edit with your credentials)." -ForegroundColor Green
} elseif (-not (Test-Path $backendEnv)) {
    Set-Content -Path $backendEnv -Value "PH_DB_URL=postgresql://user:password@localhost:5432/powerhouse"
    Write-Host "Created placeholder backend .env." -ForegroundColor Green
} else {
    Write-Host "Backend .env already present." -ForegroundColor Green
}

$frontendEnv = Join-Path $repoRoot 'frontend/app/.env.local'
if (-not (Test-Path $frontendEnv)) {
    Set-Content -Path $frontendEnv -Value "NEXT_PUBLIC_API_URL=http://localhost:8000"
    Write-Host "Created frontend .env.local." -ForegroundColor Green
} else {
    Write-Host "Frontend .env.local already present." -ForegroundColor Green
}

Write-Section "All set"
Write-Host "Powerhouse is installed." -ForegroundColor Green
Write-Host "Backend will run on http://localhost:8000 and frontend on http://localhost:3001" -ForegroundColor White
Write-Host "To start, double-click START.bat in the project folder." -ForegroundColor White

if ($LaunchAfterInstall) {
    Write-Host "Launching now..." -ForegroundColor Yellow
    Start-Process -FilePath (Join-Path $repoRoot 'START.bat')
}

Write-Host "If you need to rerun, just double-click this installer again." -ForegroundColor White
