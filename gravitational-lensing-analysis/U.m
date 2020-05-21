
function u = U(j, k)
    get = getGlobal();
    s = get(8);
    X = get(9);
    T = get(10);
    
    if j == 1
         u = 0;
    end
    if j == length(X)
        u = 0;
    end
    if k == 1
        disp(j);
        u = U0(X(j));
        
    end
    u = s*(U(j+1, k-1) + U(j-1, k-1)) + (1-2*s)*U(j, k-1);
    plot(X, u);
end

function u = U0(x)
    a = -1;
    u = a*x^2 - a*l*x;
end

function output = getGlobal()
b = 1; %Betta paramater in the heat equaion
l = 1; %Length of the rod
Tt = 10; %Time interval for the simulation (0 < t < T)
n = 100; %Amount of space steps
m = 100; %Amount of time steps

dx = l/(n+1); %Space step
dt = Tt/m; %Time step
s = b*(dt/(dx^2));

X = 0:dx:l;
T = 0:dt:Tt;

output = [b,l,Tt,n,m,dx,dt,s,X,T];
end
