%% Deductions

%% Standard

if filing == 1
    stdDed(1:year,1) = 24000;
elseif filing == 2
    stdDed(1:year,1) = 12000;
end

%% Itemized
% State, Local, & Property

slDed = zeros(year,1);
if exist('stateTaxes','var')
    slDed = stateTaxes;
end

propDed = zeros(year,1);
if exist('houseProp','var')
    propDed = houseProp;
end

slpDed = slDed + propDed;

for n = 1:year
    if slpDed(n) > 10000
        slpDed(n) = 10000;
    end
end

% Mortgage & Loan Interest

loanDed = zeros(year,1);
if exist('houseInt','var')
    loanDed = houseInt;
end

% [slDed propDed loanDed];

% Charitable Donations

charDed = zeros(year,1);
if exist('charExpense','var')
    charDed = -charExpense(:,10);
end

%% Traditional 401k & IRA

trad401 = 0;

tradIRA = 0;

%% HSA & FSA

hsaCont = 0;

fsaCont = 0;

%% Total Pretax

itemDed = slpDed + loanDed + charDed;

% [slpDed loanDed charDed];

totalDed = zeros(year,1);

for n = 1:year
    if itemDed(n) > stdDed(n)
        totalDed(n) = itemDed(n);
    else
        totalDed(n) = stdDed(n);
    end
end

totalDed = totalDed + trad401 + tradIRA + hsaCont + fsaCont;