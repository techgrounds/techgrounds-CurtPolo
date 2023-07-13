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

# Install SMS
# https://en.wikiversity.org/wiki/PowerShell/Examples/Install-SQLServerManagementStudio
# This script installs SQL Server Management Studio.
function Install-SQLServerManagementStudio {
    Write-Host "Downloading SQL Server Management Studio..."
    $Path = $env:TEMP
    $Installer = "SSMS-Setup-ENU.exe"
    $URL = "https://aka.ms/ssmsfullsetup"
    Invoke-WebRequest $URL -OutFile $Path\$Installer

    Write-Host "Installing SQL Server Management Studio..."
    Start-Process -FilePath $Path\$Installer -Args "/install /quiet" -Verb RunAs -Wait
    Remove-Item $Path\$Installer
}

Install-SQLServerManagementStudio

</powershell>