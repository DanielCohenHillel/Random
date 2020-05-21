%This code solves the heat equation given the parameters below.

%The initial condition of the heat distrabution is 
%U(x, 0) = 2x + sin(2?x) + 1 (This is controlled by the function U0 below)

%On the left(x=0) we have the Dirichlet boundary condition(U(x = 0, t) = 1 
%is constant for all t)

%On the right(x=l) we have the Neumann boundary condition
%(dU(x = l, t)/dx = 2)

%We should expect that U(x, t) = 2x + 1 as t ? ? from those boundary
%conditions and initial conditions


b = 0.00001; %Betta paramater in the heat equaion
l = 1; %Length of the rod
Tt = 500000; %Time interval for the simulation (0 < t < T)
n = 40; %Amount of space steps
m = 6000; %Amount of time steps

dx = l/n; %Space step
dt = Tt/m; %Time step
s = b*(dt/(dx^2));

X = 0:dx:l;
T = 0:dt:Tt;

U = zeros(n+1, m); %Makes an empty matrix where the firstt coordinate represnts space and the second coordinate represnts time
U(:,1) = U0(X);

Error = b*dt/(dx^2);
%if(Error > 0.5)
%  error("Explicit numerical exsplotion") 
%end

%Takes care of the inside of the rod not including the end points(see chapter 2.2)
A = sparse(n-1, n-1);
b = zeros(n-1,1);


%Sets A
for i = 1:(n-1)
   A(i,i) = 1+2*s;
   if(i ~= 1)
     A(i,i -1) = -s;
     A(i-1, i) = -s;
   end
end

%Calculates the heat distribution in time assuming initial conditions
for k = 1:m
    U(1,k) = 1;
    U(n+1,k) = dx*2 + U(n,k);
    
    b(1) = s.*U(1,k);
    b(n-1) = s.*U(n+1,k);
    
    U(2:n, k+1) = A\(U(2:n,k)+b); %Equation 2.7
end


y = trapz(X, U0(X));
t = linspace(0, 1.5*T(end));

plot(T, trapz(X, U(:,:)), t ,y*(t./t), '--');
title('Avarage U over Time');


%{
%Loop that animates the heat distribution over time
for i=1:m
    plot(X,U(:,i));
    axis([0 1 1 3]);
    pause(0.03);
end
%}


%This is the initial condition heat distribution
function u = U0(x)
    u = 2*x + sin(2*3.141*x) + 1; %Some random initial condition, you can change itt as you like
end