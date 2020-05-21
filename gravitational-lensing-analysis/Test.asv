[x,y] = meshgrid(-10:1:10,-10:1:10);
u = -x;
v = y;
quiver(x,y,u,v)
for i= 1:1000
    
    u = u.*cos(i);
    v = v.*cos(i);
    drawnow limitrate;
    pause(0.1);
      
end