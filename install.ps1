[CmdletBinding()]
param([switch]$InstallSystemTools,[switch]$Check)
$ErrorActionPreference = 'Stop'
function Find-Python {
 foreach ($candidate in @('python','py')) {
  $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
  if ($cmd) {
   $result = & $cmd.Source -c "import sys; print(sys.executable if sys.version_info >= (3,10) else '')" 2>$null
   if ($LASTEXITCODE -eq 0 -and $result) { return [string]($result | Select-Object -Last 1) }
  }
 }
 $known = Join-Path $env:LOCALAPPDATA 'Programs/Python/Python312/python.exe'
 if (Test-Path -LiteralPath $known) { return $known }
 return $null
}
$python = Find-Python
$git = Get-Command git -ErrorAction SilentlyContinue
if ((-not $python -or -not $git) -and $InstallSystemTools -and -not $Check) {
 if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'winget missing, install Git and Python 3.10+ first' }
 if (-not $python) {
  & winget install --id Python.Python.3.12 --exact --scope user --accept-package-agreements --accept-source-agreements
  if ($LASTEXITCODE -ne 0) { throw 'Python installation failed' }
 }
 if (-not $git) {
  & winget install --id Git.Git --exact --accept-package-agreements --accept-source-agreements
  if ($LASTEXITCODE -ne 0) { throw 'Git installation failed' }
 }
 $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
 $python = Find-Python
 $git = Get-Command git -ErrorAction SilentlyContinue
}
if (-not $python -or -not $git) { throw 'Git and Python 3.10+ required, or use -InstallSystemTools on Windows with winget' }
$repo = $PSScriptRoot
if (-not $repo -or -not (Test-Path -LiteralPath (Join-Path $repo 'install.py'))) {
 if ($Check) { throw 'Download or clone the repository before using -Check' }
 $repo = Join-Path ([IO.Path]::GetTempPath()) ('story-motion-' + [guid]::NewGuid().ToString('N'))
 & $git.Source clone --depth 1 'https://github.com/yangmuye520-dotcom/story-motion-studio.git' $repo
 if ($LASTEXITCODE -ne 0) {
  $archive = Join-Path ([IO.Path]::GetTempPath()) ('story-motion-' + [guid]::NewGuid().ToString('N') + '.zip')
  $extract = Join-Path ([IO.Path]::GetTempPath()) ('story-motion-archive-' + [guid]::NewGuid().ToString('N'))
  Invoke-WebRequest 'https://codeload.github.com/yangmuye520-dotcom/story-motion-studio/zip/refs/heads/main' -OutFile $archive
  Expand-Archive -LiteralPath $archive -DestinationPath $extract
  $repo = Join-Path $extract 'story-motion-studio-main'
  if (-not (Test-Path -LiteralPath (Join-Path $repo 'install.py'))) { throw 'Repository archive invalid; confirm it has been published' }
 }
}
if ($Check) { & $python -X utf8 (Join-Path $repo 'install.py') --check }
else { & $python -X utf8 (Join-Path $repo 'install.py') }
if ($LASTEXITCODE -ne 0) { throw 'Installer stopped, see the message above' }
