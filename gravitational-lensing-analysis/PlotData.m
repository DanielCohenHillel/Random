% Load data and insert it into variables
DATA = 'C:\MatlabProjects\GravitationalLensingData\phot.dat';
FULL_DATA = load(DATA);

T = FULL_DATA(:, 1); 
I = FULL_DATA(:,2);
dI = FULL_DATA(:,3);

Bottom = 470;
Top = 30;
T([1:Bottom,574-Top:574])=[];
I([1:Bottom,574-Top:574])=[];
dI([1:Bottom,574-Top:574])=[];

t = T-T(1);
I0=20.479;
FF0 = 10.^(0.4.*(I0-I));
FF0E = FF0.*0.4.*log(10).*dI;

%Draws daa with error bars
errorbar(t, FF0, FF0E,'.');

n = 6;
a = PolyReg(t, FF0, FF0E, n);
x = 0:t(end);
y = 0;
disp(a);
for i = 1:(n+1)
    y = y + a(i)*x.^(i-1);
end

plot(x, y, '-', t, FF0,'.');