%% Long-Term Personal Finances App

% Created By: Richard Thornton
% Version: 0.0.1
% Date: 1/27/2018

% DISCLAIMER: The following is designed to simulate current and projected
% market data and personal equity. All results are based on historical data
% gathered from Bloomberg and other financial institutes and are not
% designed to be construed as exact measures for the purposes of purchasing
% stocks, ETFs, options, etc.

clear all;
clc;

%% Initial Taxes
Projected_Salary

for n = 1:2
    Pretax_Withholdings
    Tax_Assessment
end

Posttax_Withholdings

%% Initial Net Earnings

netTax = miscTaxes + stateTaxes + fedTaxes;
netPostTax = totalWithheld;
netEarnings = avgGrossEarnings - netTax - netPostTax;

%% Final Taxes, Earnings, & Expenses

Scheduled_Expenses

for n = 1:2
    Pretax_Withholdings
    Tax_Assessment
    
    netTax = miscTaxes + stateTaxes + fedTaxes;
    netPostTax = totalWithheld;
    netEarnings = avgGrossEarnings - netTax - netPostTax;
    
    Mortgage

    Major_Costs
end

%% Net Savings
    
netSavings = netEarnings - totalExpenses - totalMortgage;
percSavings = netSavings ./ avgGrossEarnings;
earnings = [avgGrossEarnings netTax netPostTax netEarnings netSavings];

Savings_Investments_Allocation
Savings_Investments_Totals

%% Net Worth

savingsTotals;

savingsTable = array2table(savingsTotals);
savingsTable.Properties.VariableNames = {'High_Div','LT_Low_Vol','Large_Cap','ST_Low_Vol','Ret_Roth401k','College_529','Emerg_Fund','MT_Savings','ST_Savings','Excess_Spend'};
savingsTable;

% netWorth = zeros(year,2);
% netWorth(1:year,1) = [1e6:1e6:40e6];
% netWorth(1:year,2) = sum(savingsTotals,2);

netWorth = sum(savingsTotals(40,1:10),2) + house(1,4,x) - houseBal(year,1);

% check = [majorExpenses(1:year,10), savingsTotals(1:year,10)];

%% Graphing

yearRange = 1:year;
% 
% figure('Name','Projected Earnings','NumberTitle','off')
% subplot(3,1,1)
subplot(3,1,1)
yyaxis left
plot(yearRange,avgGrossEarnings,yearRange,netEarnings,yearRange,netSavings,'LineWidth',2)
axis([0 year 0 salaryMax])
grid on
xlabel('Year')
ylabel('Amount ($)')

yyaxis right
plot(yearRange,percMort,yearRange,percSavings,'LineWidth',2)
axis([0 year 0 .5])
ylabel('Allocation (%)')

title('Projected Earnings')
legend('Gross Earnings','Net Earnings','Net Savings/Investments','Mortgage Allocation','Savings Allocation','Location','northwest')
% 
% subplot(3,1,2)
% plot(yearRange,savingsAlloc(1:year,1:6),'LineWidth',1)
% grid on
% xlabel('Year')
% ylabel('Savings ($)')
% title('Investments Contributions')
% legend('High Dividend Yield','Long-Term, Low Volatility','Large Cap Growth','Short-Term, Low Volatility','Retirement (Roth 401k)','College Savings (529)','Location','northwest')
% 
% subplot(3,1,3)
% plot(yearRange,savingsAlloc(1:year,7:10),'LineWidth',1)
% grid on
% xlabel('Year')
% ylabel('Investments ($)')
% title('Savings Contributions')
% legend('Emergency Fund','Medium-Term Savings','Short-Term Savings','Excessive Spending','Location','northwest')
% 
% figure('Name','Projected Worth','NumberTitle','off')
% subplot(3,2,1)
% plot(yearRange,percEarnings(1:year,1:6))
% grid on
% xlabel('Year')
% ylabel('Earnings (%)')
% title('Projected Earnings - Investments')
% legend('High Dividend Yield','Long-Term, Low Volatility','Large Cap Growth','Short-Term, Low Volatility','Retirement (Roth 401k)','College Savings (529)','Location','northwest')
% 
% subplot(3,2,2)
% plot(yearRange,percEarnings(1:year,7:10),'LineWidth',2)
% grid on
% xlabel('Year')
% ylabel('Earnings (%)')
% title('Projected Earnings - Savings')
% legend('Emergency Fund','Medium-Term Savings','Short-Term Savings','Excessive Spending','Location','northwest')
% 
% subplot(3,2,[3 4])
subplot(3,1,2)
plot(yearRange,savingsTotals(1:year,1:3),yearRange,savingsTotals(1:year,4) / 5,yearRange,savingsTotals(1:year,5:6))
grid on
xlabel('Year')
ylabel('Earnings (%)')
title('Projected Worth - Investments')
legend('High Dividend Yield','Long-Term, Low Volatility','Large Cap Growth','Short-Term, Low Volatility (5x)','Retirement - Roth 401k','College Savings - 529','Location','northwest')

% subplot(3,2,[5 6])
subplot(3,1,3)
plot(yearRange,savingsTotals(1:year,7:10))
grid on
xlabel('Year')
ylabel('Earnings (%)')
title('Projected Worth - Savings')
legend('Emergency Fund','Medium-Term Savings','Short-Term Savings','Excessive Spending','Location','northwest')