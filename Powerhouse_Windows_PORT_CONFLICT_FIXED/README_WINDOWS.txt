
╔══════════════════════════════════════════════════════════════╗
║     POWERHOUSE B2B PLATFORM - WINDOWS INSTALLATION           ║
║              COMPLETE SETUP GUIDE                            ║
╚══════════════════════════════════════════════════════════════╝

WHAT YOU NEED:
--------------
1. Python 3.11+ (https://www.python.org/downloads/)
2. Node.js 18+ (https://nodejs.org/)
3. PostgreSQL 15+ (https://www.postgresql.org/download/windows/)

═══════════════════════════════════════════════════════════════

QUICK START (5 SIMPLE STEPS):
------------------------------

1. INSTALL DEPENDENCIES
   → Double-click: INSTALL.bat
   → Wait 10-15 minutes for installation
   → You'll see "INSTALLATION COMPLETE!"

2. INSTALL POSTGRESQL DATABASE
   → Double-click: DATABASE_SETUP_WINDOWS.bat
   → Follow the instructions on screen
   → Download and install PostgreSQL
   → Use password: "default" (or remember your own)

3. SETUP DATABASE TABLES
   → Double-click: SETUP_DATABASE.bat
   → Wait for "DATABASE SETUP COMPLETE!"

4. START POWERHOUSE
   → Double-click: START.bat
   → Browser opens automatically
   → Platform loads at http://localhost:3000

5. LOGIN
   → Username: test@test.com
   → Password: test123
   → Start using your 19 AI agents!

═══════════════════════════════════════════════════════════════

IF YOU SEE ERRORS:
------------------

Error: "@prisma/client did not initialize yet"
Fix: Read WINDOWS_DATABASE_GUIDE.txt and run SETUP_DATABASE.bat

Error: "Can't reach database server at localhost:5432"
Fix: Install PostgreSQL using DATABASE_SETUP_WINDOWS.bat

Error: "FieldInfo object has no attribute 'in_'"
Fix: Delete backend\venv folder, run INSTALL.bat again

Error: "Failed to fetch agents"
Fix: Make sure backend is running (check backend window)

Error: "Port 5432 already in use"
Fix: Another database is running. Stop it or contact support.

Error: "White screen" or "Server Error"
Fix: Run SETUP_DATABASE.bat to initialize the database

═══════════════════════════════════════════════════════════════

WHAT EACH FILE DOES:
--------------------

INSTALL.bat
  → Installs all Python and Node.js dependencies
  → Creates virtual environment for backend
  → Run this FIRST, only once

DATABASE_SETUP_WINDOWS.bat
  → Guides you through PostgreSQL installation
  → Shows download link and instructions
  → Run this if PostgreSQL is not installed

SETUP_DATABASE.bat
  → Creates database tables for Powerhouse
  → Generates Prisma client
  → Run this ONCE after PostgreSQL is installed

START.bat
  → Starts both backend and frontend
  → Opens browser automatically
  → Run this every time you want to use Powerhouse

STOP.bat
  → Stops all Powerhouse processes
  → Closes backend and frontend servers

REINSTALL.bat
  → Deletes all dependencies and reinstalls
  → Use if you have version conflicts
  → This fixes compatibility issues

═══════════════════════════════════════════════════════════════

TROUBLESHOOTING GUIDE:
----------------------

Problem: Installation fails
Solution:
  1. Make sure Python and Node.js are installed
  2. Right-click INSTALL.bat → Run as Administrator
  3. Check internet connection
  4. Try REINSTALL.bat

Problem: Backend won't start
Solution:
  1. Delete backend\venv folder
  2. Run INSTALL.bat
  3. Check no other app is using port 8001

Problem: Frontend shows white screen or Prisma error
Solution:
  1. Check PostgreSQL is running (services.msc)
  2. Run SETUP_DATABASE.bat
  3. Check .env file has correct password
  4. See WINDOWS_DATABASE_GUIDE.txt

Problem: Agents show 0% or "Failed to fetch"
Solution:
  1. Make sure backend window is still open
  2. Check backend window for errors
  3. Backend might still be starting (wait 30 seconds)

Problem: Browser doesn't open
Solution:
  1. Manually open: http://localhost:3000
  2. Make sure frontend is running (check windows)

═══════════════════════════════════════════════════════════════

SYSTEM REQUIREMENTS:
--------------------
- Windows 10 or 11
- 8GB RAM minimum (16GB recommended)
- 5GB free disk space
- Internet connection for installation

PORTS USED:
-----------
- 3000: Frontend (Next.js)
- 8001: Backend (FastAPI)
- 5432: PostgreSQL Database

═══════════════════════════════════════════════════════════════

FEATURES:
---------
✓ 19 Advanced AI Agent Architectures
✓ Budget Control & Rate Limiting
✓ Real-time Dashboard & Analytics
✓ Multi-tenant B2B Platform
✓ Modern UX/UI
✓ Comprehensive Documentation

═══════════════════════════════════════════════════════════════

DAILY USE:
----------
After initial setup, just:
1. Double-click START.bat
2. Login with test@test.com / test123
3. Use your AI agents!

To stop:
1. Double-click STOP.bat
OR
2. Close the terminal windows

═══════════════════════════════════════════════════════════════

NEED MORE HELP?
---------------
See these files:
- WINDOWS_DATABASE_GUIDE.txt (Database setup)
- QUICK_START_GUIDE.pdf (Visual guide with screenshots)
- TROUBLESHOOTING.txt (Common problems)

═══════════════════════════════════════════════════════════════
