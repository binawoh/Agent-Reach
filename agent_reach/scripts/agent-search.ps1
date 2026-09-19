[CmdletBinding()]
param(
    [Parameter(Mandatory, Position = 0)]
    [ValidateNotNullOrEmpty()]
    [string]$Query,

    [ValidateRange(1, 20)]
    [int]$Limit = 5,

    [ValidateSet("auto", "exa", "tavily", "firecrawl", "tinyfish")]
    [string]$Provider = "auto"
)

$ErrorActionPreference = "Stop"
$attempts = [System.Collections.Generic.List[object]]::new()

function Add-SearchFailure {
    param(
        [string]$Name,
        [string]$Message
    )

    $attempts.Add([pscustomobject]@{
        provider = $Name
        error = $Message
    })
}

function Write-SearchResult {
    param(
        [string]$Name,
        [object]$Data
    )

    [pscustomobject]@{
        success = $true
        provider = $Name
        query = $Query
        data = $Data
    } | ConvertTo-Json -Depth 30 -Compress
}

$providers = if ($Provider -eq "auto") {
    @("exa", "tavily", "firecrawl", "tinyfish")
}
else {
    @($Provider)
}

foreach ($currentProvider in $providers) {
    if ($currentProvider -eq "exa") {
        try {
            if (-not (Get-Command mcporter -ErrorAction SilentlyContinue)) {
                throw "mcporter command not found"
            }

            $exaOutput = & mcporter call exa.web_search_exa "query=$Query" "numResults=$Limit" 2>&1
            $exaExitCode = $LASTEXITCODE
            $exaText = ($exaOutput | ForEach-Object { $_.ToString() }) -join "`n"

            if ($exaExitCode -ne 0) {
                throw $exaText
            }

            Write-SearchResult -Name "exa" -Data $exaText
            exit 0
        }
        catch {
            Add-SearchFailure -Name "exa" -Message $_.Exception.Message
        }
    }

    if ($currentProvider -eq "tavily") {
        try {
            $tavilyKey = $env:TAVILY_API_KEY
            if ([string]::IsNullOrWhiteSpace($tavilyKey)) {
                $tavilyKey = [Environment]::GetEnvironmentVariable("TAVILY_API_KEY", "User")
            }
            if ([string]::IsNullOrWhiteSpace($tavilyKey)) {
                throw "TAVILY_API_KEY is not configured"
            }

            $headers = @{ Authorization = "Bearer $tavilyKey" }
            $body = @{
                query = $Query
                search_depth = "basic"
                max_results = $Limit
                include_answer = $false
                include_raw_content = $false
            } | ConvertTo-Json -Compress

            $tavilyResult = Invoke-RestMethod `
                -Method Post `
                -Uri "https://api.tavily.com/search" `
                -Headers $headers `
                -ContentType "application/json" `
                -Body $body `
                -TimeoutSec 45

            Write-SearchResult -Name "tavily" -Data $tavilyResult
            exit 0
        }
        catch {
            Add-SearchFailure -Name "tavily" -Message $_.Exception.Message
        }
        finally {
            Remove-Variable tavilyKey,headers,body,tavilyResult -ErrorAction SilentlyContinue
        }
    }

    if ($currentProvider -eq "firecrawl") {
        try {
            if (-not (Get-Command firecrawl -ErrorAction SilentlyContinue)) {
                throw "firecrawl command not found"
            }

            $firecrawlOutput = & firecrawl search $Query --limit $Limit --json 2>&1
            $firecrawlExitCode = $LASTEXITCODE
            $firecrawlText = ($firecrawlOutput | ForEach-Object { $_.ToString() }) -join "`n"

            if ($firecrawlExitCode -ne 0) {
                throw $firecrawlText
            }

            try {
                $firecrawlData = $firecrawlText | ConvertFrom-Json
            }
            catch {
                $firecrawlData = $firecrawlText
            }

            Write-SearchResult -Name "firecrawl" -Data $firecrawlData
            exit 0
        }
        catch {
            Add-SearchFailure -Name "firecrawl" -Message $_.Exception.Message
        }
    }
    if ($currentProvider -eq "tinyfish") {
        try {
            if (-not (Get-Command tinyfish -ErrorAction SilentlyContinue)) {
                throw "tinyfish command not found"
            }

            $tinyfishOutput = & tinyfish search query $Query 2>&1
            $tinyfishExitCode = $LASTEXITCODE
            $tinyfishText = ($tinyfishOutput | ForEach-Object { $_.ToString() }) -join "`n"

            if ($tinyfishExitCode -ne 0) {
                throw $tinyfishText
            }

            $tinyfishData = $tinyfishText | ConvertFrom-Json
            if ($null -eq $tinyfishData -or $null -eq $tinyfishData.results) {
                throw "TinyFish returned no results field"
            }
            $tinyfishData.results = @($tinyfishData.results | Select-Object -First $Limit)
            Write-SearchResult -Name "tinyfish" -Data $tinyfishData
            exit 0
        }
        catch {
            Add-SearchFailure -Name "tinyfish" -Message ($_.Exception.Message -replace 'sk-(?:tinyfish|mino)-[A-Za-z0-9_-]+', '[REDACTED]')
        }
    }
}

[pscustomobject]@{
    success = $false
    query = $Query
    attempts = $attempts
} | ConvertTo-Json -Depth 10 -Compress
exit 1
