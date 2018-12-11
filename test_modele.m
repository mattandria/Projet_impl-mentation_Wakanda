close all
figure('WindowButtonMotionFcn',@callBack);
eval('data');
hold on
plot(og(1),og(2),'ok');
plot(od(1),od(2),'ok');
xlim([-150;150])
ylim([-150;150])
