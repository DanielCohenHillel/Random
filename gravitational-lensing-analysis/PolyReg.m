function a = PolyReg(x, y, dy, n)

if (length(x) ~= length(y)) || (length(x) ~= length(dy)) || (length(y) ~= length(dy))
    error('Inputs do not match in size.');
end

N = length(x); %Num of data points

%The sums in the matrices
Sx = zeros(1, 2*n + 1);
Sy = zeros(1, n+1);

for i = 1:N %Calculate sums in the matrices
    for j = 1:(2*n + 1)
        Sx(j) = Sx(j) + (x(i)^(j-1))/(dy(i)^2);
    end
    
    for j = 1:(n+1)
        Sy(j) = Sy(j) + (x(i)^(j-1))*y(i)/(dy(i)^2);
    end
end

%Matrices discribing the linear system of equations
A = zeros(n+1);
B = zeros(n+1, 1);

%Place the sums in the right place in the matrices
for i = 1:(n+1)
    for j = 1:(n+1)
        A(i, j) = Sx(i + j - 1);
    end 
    B(i) = Sy(i);
end

%Solve the linear system of equations using Cramer's rule
Ai = A;
detA = determinant(A);
disp(detA);
a = zeros(1, n+1);
for i = 1:(n+1)
   Ai(:,i) = B;
   a(i) = determinant(Ai)/detA;
   Ai = A;
end
disp(detA/det(A));

%a = [det(Ax) , det(Ay) , det(Az)]./det(A);
%a = B\A; 
end