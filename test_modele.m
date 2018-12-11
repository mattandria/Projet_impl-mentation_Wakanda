close all
figure('WindowButtonMotionFcn',@callBack);
og=[-5;0];
od=[5;0];
hold on
plot(og(1),og(2),'ok');
plot(od(1),od(2),'ok');
xlim([-50;50])
ylim([-50;50])
function callBack(object,eventdata)
    C = get (gca, 'CurrentPoint');
    l1=15;
    l2=18;
    og=[-5;0];
    od=[5;0];
    angles=modele_inverse(C(1,1),C(1,2),l1,l2,og,od);
    representation(C(1,1),C(1,2),angles,l1,og,od);
end