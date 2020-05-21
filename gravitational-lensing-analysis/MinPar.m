function a = MinPar(x, y, dy)
    u = 0.12:0.001:0.122;
    tau = 50:0.0001:53;
    
    umin = 1;
    taumin = 1;
    minXi = Xi(1,1, x, y, dy);
    
    for i = u
       for j = tau
           xi = Xi(i, j, x, y, dy);
           
           if(xi < minXi)
               minXi= xi;
               umin = i;
               taumin = j;
           end
       end
    end
    a = [umin, taumin];
end

function u = Mu(u, tau, x)
    a = (x)./tau;
    u = (u.^2+a.^2+2)/(sqrt(u.^2+a.^2).*sqrt(u.^2+a.^2+4));
end

function xi = Xi(u, tau, x, y, dy)
    N = length(x);
    xi = 0;
    for i = 1:N
        xi = xi + ((y(i) - Mu(u, tau, x(i)))/(dy(i))).^2;
    end
end

%{
function dMu = dMudumin(u, tau, x)
    a = (x)./tau;
    dMu =  -(u.*(a.^2 + u.^2 + 2))/((a.^2 + u.^2).^(3/2).*sqrt(a.^2 + u.^2 + 4)) + (2.*u)/(sqrt(a.^2 + u.^2).*sqrt(a.^2 + u.^2 + 4)) - (u (a.^2 + u.^2 + 2))/(sqrt(a.^2 + u.^2).*(a.^2 + u.^2 + 4).^(3/2));
end

function dMu = dMudtau(u, tau, x)
    a = (x)./tau;
    dMu = (((x).^2).*((x).^2/a.^2 + u.^2 + 2))/((a.^3).*((x).^2/a.^2 + u.^2).^(3/2).*sqrt((x).^2/a.^2 + u.^2 + 4)) - (2.*(x).^2)/(a.^3.*sqrt((x).^2/a.^2 + u.^2).*sqrt((x).^2/a.^2 + u.^2 + 4)) + ((x).^2.*((x).^2/a.^2 + u.^2 + 2))/(a.^3.*sqrt((x).^2/a.^2 + u.^2).*((x).^2/a.^2 + u.^2 + 4).^(3/2));
end

function dXi = gradXi(u, tau, x, y, dy)
    N = length(x);
    dXi = [0, 0];
    for i = 1:N
        a = (1/dy(i)).*(y(i) - Mu(u, tau, x(i)));
        dXi(1) = dXi(1) + dMudumin(u, tau, x(i)).*a;
        dXi(2) = dXi(2) + dMudtau(u, tau, x(i)).*a;
    end
end
%}