function [h] = model_geom(alphag,alphad,l1,l2,og,od)
	close all
	%Initialisations
	ig = zeros(2, 1);
	milieu = zeros(2, 1);
	h = zeros(2, 1);
    
	% Coordonnees de Ig
	ig(1) = og(1) + l1*cos(alphag);
	ig(2) = og(2) + l1*sin(alphag);
    
	% Coordonnees de Id
	id(1) = od(1) + l1*cos(alphad);
	id(2) = od(2) + l1*sin(alphad);
    
	% Coordonnees du milieu de IgId
	milieu(1) = ( ig(1)+id(1) )/2;
	milieu(2) = ( ig(2)+id(2) )/2;
    
	%calcul des coordonnées du point H
	u = [ig(1)-id(1) ig(2)-id(2)];
    
    A = 1 + u(1)^2/u(2)^2;
	B = -2*ig(1) - 2*milieu(1)*u(1)^2/u(2)^2 - 2*u(1)/u(2)*milieu(2) + 2*ig(2)*u(1)/u(2);
	C = ig(1)^2 + ig(2)^2 - 2*ig(2)*u(1)/u(2)*milieu(1) - 2*ig(2)*milieu(2) - l2^2 + u(1)^2/u(2)^2*milieu(1)^2 + milieu(2)^2 + 2*u(1)/u(2)*milieu(2)*milieu(1);
    
	delta = B^2 - 4*A*C
    
    
	if delta < 0
    	Display('Position inatteignable');
	else if delta > 0
    	xh1 = (-B - sqrt(delta))/2/A
    	xh2 = (-B + sqrt(delta))/2/A
   	 
    	end
	end
    
	yh1 = u(1)/u(2)*(milieu(1)-xh1) + milieu(2)
	yh2 = u(1)/u(2)*(milieu(1)-xh2) + milieu(2)
    
	% Coordonnes de H
	%le point H se trouve en haut du point M
	if yh1 < milieu(2)
    	h(1) = xh2;
    	h(2) = yh2;
	else
    	h(1) = xh1;
    	h(2) = yh1;
   
	%on verifie qu'on retrouve l2
	sqrt((ig(1)-h(1))^2+(ig(2)-h(2))^2)
	sqrt((id(1)-h(1))^2+(id(2)-h(2))^2)
    
end
