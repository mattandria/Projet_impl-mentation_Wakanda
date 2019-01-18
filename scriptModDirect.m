alphag = pi/2;
alphad = pi/3;
l1 = 60;
l2 = 80;
og = [-12.5,0];
od = [12.5,0];

% Coordonnees de Ig
ig(1) = og(1) + l1*cos(alphag);
ig(2) = og(2) + l1*sin(alphag);
% Coordonnees de Id
id(1) = od(1) + l1*cos(alphad);
id(2) = od(2) + l1*sin(alphad);

h = model_geom(alphag,alphad,l1,l2,og,od);

%on verifie qu'on retrouve l1
IgOg = sqrt((ig(1)-og(1))^2+(ig(2)-og(2))^2)
IdOd = sqrt((id(1)-od(1))^2+(id(2)-od(2))^2)

%on verifie qu'on retrouve l2
IgH = sqrt((ig(1)-h(1))^2+(ig(2)-h(2))^2)
IdH = sqrt((id(1)-h(1))^2+(id(2)-h(2))^2)

figure
hold on

%Position des points
plot(og(1),og(2), 'r--o');
plot(od(1),od(2), 'r--o');
plot(ig(1),ig(2), 'y--o');
plot(id(1),id(2), 'y--o');
plot(h(1),h(2), 'g--o');

%Modelisation des bras
plot([og(1),ig(1)], [og(2),ig(2)], 'b--x');
plot([od(1),id(1)], [od(2),id(2)], 'b--x');
plot([ig(1),h(1)], [ig(2),h(2)], 'b--x');
plot([id(1),h(1)], [id(2),h(2)], 'b--x');
axis([-inf, inf, -inf, inf])
