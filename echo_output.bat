@echo off
setlocal enabledelayedexpansion

:loop
  rem Clear the variable so old data doesn't persist
  set "lastline="

  rem Read through the file and set lastline to the last nonblank line read
  for /f "usebackq delims=" %%a in ("C:\workspace\ece448_PAM\test_output.txt") do (
    set "lastline=%%a"
  )

  rem Check if lastline was set; if not, output a message
  if defined lastline (
      echo Last line: !lastline!
  ) else (
      echo no line found
  )

  rem Wait for 500 milliseconds (using ping to a non-routable IP)
  ping -n 1 -w 500 192.0.2.1 >nul

  goto loop
