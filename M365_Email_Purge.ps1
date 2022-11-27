

## Azure M365 Log On Run section 
## Modify to be an email address with M365 admin access
$upn = admin@example.com

#H3HVAC M354 Admin - RUN ONCE
Connect-IPPSSession -userprincipalname $upn

## Run Section 2: Repeat from here:

$contentMatchQueries = @(
'Subject: Email Subject 1', 
'Subject: Email Subject 2', 
'Subject: Email Subject 3',
'Subject: Email Subject 4'
)

foreach ($contentMatchQuery in $contentMatchQueries){
	echo "Attempting to Purge " + $contentMatchQuery
	$date= Get-Date -Format "dddd-MM-dd-yyyy-HH-mm-ss"

	$compSearchName = $upn + "_maliciousEmail_" + $date  #change name

	# Date/ Senders search
	#New-ComplianceSearch -Name $compSearchName -ExchangeLocation all -ContentMatchQuery 'sent>=04/18/2018 AND From:"baduser@baddomain.com"' # Can also do something like Subject:"Bad Subject"



	# subject search
	New-ComplianceSearch -Name $compSearchName -ExchangeLocation all -ContentMatchQuery $contentMatchQuery

	Start-ComplianceSearch -Identity $compSearchName

	$i = 0
	$isCompleted = $false
	DO {
		echo "Search Results Run" + $i
		Start-Sleep -Seconds 20
		$searchResult = Get-ComplianceSearch -Identity $compSearchName # Run this till it shows Completed -- TODO: Do-while loop with 20 second sleep
		echo $searchResult.Status
		$isCompleted = $searchResult.Status -like '*Completed*'
		$i++
		} WHILE ((-not $isCompleted))


	## Run Section 3 - Verify
	$searchResultCount = Get-ComplianceSearch -Identity $compSearchName | Select Items # Show count of matching emails
	#Get-ComplianceSearch -Identity $compSearchName | fl # Show list of matching mailboxes


	IF($searchResultCount.Items -gt 0){
		echo "found results:"$searchResultCount.Items.ToString()

		## Run Section 4 - soft delete
		New-ComplianceSearchAction -SearchName $compSearchName -Purge -PurgeType SoftDelete -Confirm:$False # Purge from mailboxes
		
		## Check if the purge has completed
		$i = 0
		$isCompleted = $false
		DO {
			echo "Purge Check" + $i
			Start-Sleep -Seconds 20
			$purgeResult = Get-ComplianceSearchAction -Identity "$($compSearchName)_Purge" # Make sure it all purged fine - TODO repeat until complete
			echo "Purge" + $purgeResult.Status
			$isCompleted = $purgeResult.Status -like '*Completed*'
			$i++
			} WHILE ((-not $isCompleted))
		echo "Purge Completed for " + $contentMatchQuery
		}
	ELSE {
	 echo "no results found for "+ $contentMatchQuery
	 }
}
