function [angles] = modele_inverse(x,y,l1,l2,og,od)
    dg=sqrt((x-og(1))^2+y^2);
    dd=sqrt((x-od(1))^2+y^2);
    thetad=atan2(y/dd,(x-od(1))/dd);
    thetag=atan2(y/dg,(x-og(1))/dg);
    betad=acos(((x-od(1))^2+y^2-l1^2-l2^2)/(2*l1*l2));
    betag=acos(((x-og(1))^2+y^2-l1^2-l2^2)/(2*l1*l2));
    phid=acos((l1+l2*cos(betad))/dd);
    phig=acos((l1+l2*cos(betag))/dg);
    angles(1)=thetag+phig;
    angles(2)=thetad-phid;
end