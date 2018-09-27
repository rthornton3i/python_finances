## Roth 401k & IRA

roth401Percent = .05
roth401 = roth401Percent * avgGrossEarnings

rothIRA = 0

## Benefits

# Medical

monthlyHealthPrem = 200

if filing == 1
    healthCont(1:year,1) = monthlyHealthPrem * 12 * 2
elseif filing == 2
    healthCont(1:year,1) = monthlyHealthPrem * 12


# Vision

visPrem = 0

if filing == 1
    visCont(1:year,1) = visPrem * 12 * 2
elseif filing == 2
    visCont(1:year,1) = visPrem * 12


# Dental

denPrem = 0

if filing == 1
    denCont(1:year,1) = denPrem * 12 * 2
elseif filing == 2
    denCont(1:year,1) = denPrem * 12


## Total Posttax

totalWithheld = roth401 + rothIRA + healthCont + visCont + denCont

