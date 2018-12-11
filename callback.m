function callBack(object,eventdata)
    eval('data');
    C = get (gca, 'CurrentPoint');
    angles=modele_inverse(C(1,1),C(1,2),l1,l2,og,od);
    if(size(angles,2)==2)
        representation(C(1,1),C(1,2),angles,l1,og,od);
    end
end

