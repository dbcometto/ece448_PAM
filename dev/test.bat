@echo off
:loop
  type "C:\workspace\ece448_PAM\test_output.bin"
  rem Wait for 500 milliseconds using ping to a non-routable IP address
  ping -n 1 -w 500 192.0.2.1 >nul
  goto loop
