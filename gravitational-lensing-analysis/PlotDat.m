DATA = 'C:\MatlabProjects\GravitationalLensingData\phot.dat';
FULL_DATA = load(DATA);

T = FULL_DATA(:, 1); 
I = FULL_DATA(:,2);
dI = FULL_DATA(:,3);

I0=20.479;
FF0 = 10.^(0.4.*(I0-I));
FF0E = FF0.*0.4.*log(10).*dI;

T0 = 2454476.072;

t = T-T0;
a = MinPar(t, FF0, FF0E);

disp(a);

t = (T-T0)./a(2);
tt = t(1):0.001:t(end);

u = sqrt(a(1).^2 + tt.^2);
Mu = (2 + u.^2)./(u.*sqrt(4 + u.^2));

plot(tt, Mu, '-', t, FF0,'.');



