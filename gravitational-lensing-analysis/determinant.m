function detA = determinant(A)
if(size(A, 1) ~= size(A, 2))
   error('Not a square matrix'); 
end
if(length(A) == 1)
   detA = A(1, 1); 
end
if(length(A) == 2)
    detA = A(1,1)*A(2,2) - A(1,2)*A(2,1);
else
    
    dettA = 0;
    for i = 1:length(A)
        j = 1:length(A);
        j(i) = [];
        Ai = A(j, 2:end);
        dettA = dettA - (-1)^i*A(i)*determinant(Ai);
    end
    detA = dettA;
end
end