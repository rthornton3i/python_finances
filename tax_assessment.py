%% Miscellaneous Taxes

socialSecurity = .062;
medicare = .0145;
medicareAdditional = .009;

maxTaxSS = 127200;
minTaxAM = 250000;

% Social Security
ssTax = zeros(year,1);

for n = 1:year
    if avgGrossEarnings(n) < maxTaxSS   
        ssTax(n) = avgGrossEarnings(n) * socialSecurity; 
    else                
        ssTax(n) = maxTaxSS * socialSecurity;
    end
end

% Medicare
mTax = zeros(year,1);

for n = 1:year  
    mTax(n) = avgGrossEarnings(n) * medicare;
end

% Additional Medicare
amTax = zeros(year,1);

for n = 1:year
    if avgGrossEarnings(n) > minTaxAM   
        amTax(n) = avgGrossEarnings(n) * medicareAdditional; 
    end
end

miscTaxes = ssTax + mTax + amTax;

%miscTaxCheck = [avgGrossEarnings ssTax mTax amTax miscTaxes]

%% State Taxes

stateTaxPercent = zeros(year,1);
stateTaxOwed = zeros(year,1);
bracketState = zeros(year,1);

bracketState1 = 17000;

for n = 1:year
    if avgGrossEarnings(n) < bracketState1
        stateTaxPercent(n) = 0;
        stateTaxOwed(n) = 0;
        bracketState(n) = 0;
    elseif avgGrossEarnings(n) > bracketState1
        stateTaxPercent(n) = .0575;
        stateTaxOwed(n) = 720;
        bracketState(n) = bracketState1;
    end
end

stateTaxes = zeros(year,1);

for n = 1:year              
    stateTaxes(n) = stateTaxOwed(n) + (stateTaxPercent(n) * (avgGrossEarnings(n) - bracketState(n)));
    if stateTaxes(n) < 0
        stateTaxes(n) = 0;
    end
end

stateTaxes;

%% Federal Taxes

grossDedEarnings = avgGrossEarnings - totalDed;

fedTaxPercent = zeros(year,1);
fedTaxOwed = zeros(year,1);
bracketFed = zeros(year,1);

if filing == 1
    bracketFed1 = 77400;
    bracketFed2 = 165000;
    bracketFed3 = 315000;
    bracketFed4 = 400000;
    bracketFed5 = 600000;

    for n = 1:year
        if grossDedEarnings(n) < bracketFed1
            fedTaxPercent(n) = 0;
            fedTaxOwed(n) = 0;
            bracketFed(n) = 0;
        elseif (grossDedEarnings(n) > bracketFed1) && (grossDedEarnings(n) < bracketFed2)
            fedTaxPercent(n) = .22;
            fedTaxOwed(n) = 10452.5;
            bracketFed(n) = bracketFed1;
        elseif (grossDedEarnings(n) > bracketFed2) && (grossDedEarnings(n) < bracketFed3)
            fedTaxPercent(n) = .24;
            fedTaxOwed(n) = 29752.5;
            bracketFed(n) = bracketFed2;
        elseif (grossDedEarnings(n) > bracketFed3) && (grossDedEarnings(n) < bracketFed4)
            fedTaxPercent(n) = .32;
            fedTaxOwed(n) = 52222.5;
            bracketFed(n) = bracketFed3;
        elseif (grossDedEarnings(n) > bracketFed4) && (grossDedEarnings(n) < bracketFed5)
            fedTaxPercent(n) = .35;
            fedTaxOwed(n) = 112728;
            bracketFed(n) = bracketFed4;
        elseif grossDedEarnings(n) > bracketFed5
            fedTaxPercent(n) = .37;
            fedTaxOwed(n) = 131628;
            bracketFed(n) = bracketFed5;
        end
    end
    
elseif filing ==2
    bracketFed1 = 38700;
    bracketFed2 = 82500;

    for n = 1:year
        if grossDedEarnings(n) < bracketFed1
            fedTaxPercent(n) = 0;
            fedTaxOwed(n) = 0;
            bracketFed(n) = 0;
        elseif (grossDedEarnings(n) > bracketFed1) && (grossDedEarnings(n) < bracketFed2)
            fedTaxPercent(n) = .22;
            fedTaxOwed(n) = 4453.5;
            bracketFed(n) = bracketFed1;
        elseif grossDedEarnings(n) > bracketFed2
            fedTaxPercent(n) = .24;
            fedTaxOwed(n) = 14090;
            bracketFed(n) = bracketFed2;
        end
    end
end

fedTaxes = zeros(year,1);

for n = 1:year
    fedTaxes(n) = fedTaxOwed(n) + (fedTaxPercent(n) * (grossDedEarnings(n) - bracketFed(n)));
    if fedTaxes(n) < 0
        fedTaxes(n) = 0;
    end
end

fedTaxes;
