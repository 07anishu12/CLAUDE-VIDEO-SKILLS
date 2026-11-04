param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$InstallerArgs
)
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& python "$ScriptDir/manage.py" @InstallerArgs --uninstall
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
