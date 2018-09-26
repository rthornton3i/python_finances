%% Projected Salary

%salaryPrompt = 'Please enter current salary.\n';
%salary = input(salaryPrompt);
salary = 145000;

%yearsPrompt = 'Please enter the number of years.\n';
%years = input(yearsPrompt);
year = 40;

%growthString1 = 'Please enter the corresponding number for the desired means of salary growth.';
%growthString2 = '  1) Logistic \n  2) Linear \n  3) Exponential Growth \n  4) Exponential CDF';
%growthPrompt = strcat(growthString1,'\n',growthString2,'\n','SELECTION:');
%growth = input(growthPrompt);
growth = 1;

%filingString1 = 'Please enter the corresponding number based on your filing status.';
%filingString2 = '  1) Married Filing Jointly \n  2) Single';
%filingPrompt = strcat(filingString1,'\n',filingString2,'\n','SELECTION:');
%filing = input(filingPrompt);
filing = 1;

%% Children

%numChild = [# of Kids, Yr @ Kid1, Yr @ Kid2,...]
numChild = [2, 7, 9];
ageChild = zeros(year,numChild(1,1) + 1);

ageChild(1:year,1) = 1:40;

for n = 1:year
    for m = 2:size(ageChild,2)
        if (n >= numChild(1,m)) && (n <= numChild(1,m) + 21)
            ageChild(n,m) = n - numChild(1,m);
        end
    end
end

%% Salary

salaryGrowthPercent = .028;
salaryMax = salary * (1 + salaryGrowthPercent) ^ (year);

grossEarnings = zeros(year,1);

for n = 1:year
    for m = 1:100
        rMin = .85;
        rMax = 1.15;
        r = rMin + (rMax - rMin) * rand;

        if growth == 1
            initialValueFactor = (salaryMax / salary) * (year / 5);
            growthFactor = log(((1 / .95) - 1) / initialValueFactor) / (-(7/8) * year);

            rMin = rMin * growthFactor;
            rMax = rMax * growthFactor;
            rLog = rMin + (rMax - rMin) * rand;

            grossEarnings(n,m) = (((salaryMax - salary) / (1 + (initialValueFactor * exp(-rLog * n)))) + salary) - (((year - n) / year) * 0.1 * salary);
        elseif growth == 2
            grossEarnings(n,m) = ((((salaryMax - salary) / year) * r) * n) + salary;
        elseif growth == 3
            grossEarnings(n,m) = salary * (1 + r * salaryGrowthPercent) ^ n;
        elseif growth == 4
            grossEarnings(n,m) = (salary + (1 - exp(-n * r * salaryGrowthPercent)) * salaryMax) - (((year - n) / year) * 0.1 * salary);
        end
    end
end

avgGrossEarnings = mean(grossEarnings,2);