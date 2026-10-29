param([Parameter(Mandatory=$true)][string]$Project,[int]$Port=8793)
$ErrorActionPreference='Stop'
$adapter=Join-Path $PSScriptRoot 'hyperframes.py'
python $adapter --project $Project preview --background --port $Port
if ($LASTEXITCODE -ne 0) { throw 'Chinese preview failed; inspect configured runtime and port' }
Write-Host "中文界面已应用，请打开输出的实际地址；旧标签页请按 Ctrl+F5 刷新"
