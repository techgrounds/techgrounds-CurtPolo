<powershell>
# Install OpenSSH
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start the sshd service
Start-Service sshd

# Set the sshd service to start automatically
Set-Service -Name sshd -StartupType Automatic

# Confirm that the firewall rule is configured
Get-NetFirewallRule -Name *ssh*

# If the firewall rule is not configured, run the following command
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22

# Disable IE ESC for Administrators
$AdminKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A7-37EF-4b3f-8CFC-4F3A74704073}"
$AdminValueName = "IsInstalled"
Set-ItemProperty -Path $AdminKey -Name $AdminValueName -Value 0

# Disable IE ESC for Users
$UserKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A8-37EF-4b3f-8CFC-4F3A74704073}"
$UserValueName = "IsInstalled"
Set-ItemProperty -Path $UserKey -Name $UserValueName -Value 0

# Restart Windows Explorer to apply the changes
Stop-Process -Name explorer -Force
Start-Sleep -Seconds 3
Start-Process -FilePath explorer


# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Update the package list
choco upgrade chocolatey -y

# Install MySQL Workbench
choco install mysql.workbench -y

# Re-enable IE ESC for Administrators
$AdminKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A7-37EF-4b3f-8CFC-4F3A74704073}"
$AdminValueName = "IsInstalled"
Set-ItemProperty -Path $AdminKey -Name $AdminValueName -Value 1

# Re-enable IE ESC for Users
$UserKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A8-37EF-4b3f-8CFC-4F3A74704073}"
$UserValueName = "IsInstalled"
Set-ItemProperty -Path $UserKey -Name $UserValueName -Value 1

# Restart Windows Explorer to apply the changes
Stop-Process -Name explorer -Force
Start-Sleep -Seconds 3
Start-Process -FilePath explorer
</powershell>