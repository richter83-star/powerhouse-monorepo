# Powerhouse Windows Installer (Click-to-Install)

This folder contains a single PowerShell script that sets up Powerhouse on Windows with minimal steps—ideal for non-technical users.

## Quick start (CEO-friendly)
1. **Download or clone** the Powerhouse folder onto your Windows PC.
2. Open the `windows-installer` folder.
3. **Right-click** `Install-Powerhouse.ps1` and select **Run with PowerShell**.
4. Wait for the installer to finish. It will:
   - Install Git, Python 3.10, Node.js (LTS), and Yarn (via Winget + npm) if missing.
   - Install backend and frontend dependencies.
   - Create the `.env` files with sensible defaults if they are missing.
5. Double-click `START.bat` (in the project root) to launch Powerhouse.

If you see messages like `python is not recognized` or `node is not recognized`, **close PowerShell**, reopen it, and rerun `Install-Powerhouse.ps1`. This refreshes your PATH after winget installs new tools. Yarn is enabled via Corepack when possible and falls back to a silent npm install if needed.

## Optional: auto-launch after install
If you prefer the installer to start Powerhouse immediately, run it from PowerShell with:

```powershell
./Install-Powerhouse.ps1 -LaunchAfterInstall
```

## Notes
- The script requires **Winget** (App Installer) to fetch dependencies silently. If Winget is not available, install it from the Microsoft Store first.
- You can re-run the installer anytime; it will skip items that are already installed.
