function [] = representation(x,y,angles,l1,og,od)
    clf;
    ig=zeros(1,2);
    id=zeros(1,2);
    ig(1)=og(1)+l1*cos(angles(1));
    ig(2)=l1*sin(angles(1));
    id(1)=od(1)+l1*cos(angles(2));
    id(2)=l1*sin(angles(2));
    hold on
    plot(og(1),og(2),'ok');
    plot(od(1),od(2),'ok');
    plot(ig(1),ig(2),'ok');
    plot(id(1),id(2),'ok');
    plot(x,y,'ok');
    plot([og(1) ig(1)],[og(2) ig(2)],'-r');
    plot([od(1) id(1)],[od(2) id(2)],'-r');
    plot([ig(1) x],[ig(2) y],'-b');
    plot([id(1) x],[id(2) y],'-b');
    xlim([-50;50])
    ylim([-50;50])
    l1g=sqrt((og(1)-ig(1))^2+(og(2)-ig(2))^2)
    l1d=sqrt((od(1)-id(1))^2+(od(2)-id(2))^2)
    l2g=sqrt((x-ig(1))^2+(y-ig(2))^2)
    l2d=sqrt((x-id(1))^2+(y-id(2))^2)
end

