function [ d ] = simulate_bn( adj_matrix, init_state, tnf, gf )
%This function takes the adjacency matrix of a network as input, along with
%the initial state condition of all nodes, and the OFF/ON (0/1) value of
%input signals tnf and gf.
%   cas3 = #22
%   dna damage = #38
%   tnf = #39
%   gf = #40
    num_nodes = length(init_state);
    init_state(39) = tnf;
    init_state(40) = gf;
    last_cas3 = 0;
    dna_damage_run = 0;
    if (init_state(38)==1)
        dna_damage_run = 1;
    end
    new_state = zeros(1,num_nodes);
    t = 0;
    d = 0;
    while t<200
        for j=1:num_nodes
            curr_node_on = adj_matrix(j,:,1);
            curr_node_off = adj_matrix(j,:,2);
            dict = containers.Map(double(1), [1,2]); %(key) -> [key;contribution;on/off]
            remove(dict,1);
            for k=1:num_nodes
                curr_regulation_on = curr_node_on{k};
                for p=1:size(curr_regulation_on,2)
                    key = curr_regulation_on(:,p);
                    if (isKey(dict,key(1)))
                        dict(key(1)) = cat(1,dict(key(1)),cat(1,key,init_state(k),1));
                    else
                        dict(key(1)) = cat(1,key,init_state(k),1);
                    end
                end
                curr_regulation_off = curr_node_off{k};
                for p=1:size(curr_regulation_off,2)
                    key = curr_regulation_off(:,p);
                    if (isKey(dict,key(1)))
                        dict(key(1)) = cat(1,dict(key(1)),cat(1,key,init_state(k),0));
                    else
                        dict(key(1)) = cat(1,key,init_state(k),0);
                    end
                end
            end
            pos = 0;
            neg = 0;
            ks = keys(dict);
            for k=1:length(ks)
                key = ks{k};
                check_for = dict(key);
                if(key>0)
                    flag = true;
                    for p=1:size(check_for,2)
                        if (bitxor(check_for(3,p),check_for(4,p))==1)
                            flag = false;
                        end
                    end
                    if (flag)
                        pos = pos + check_for(2,1);
                    end                        
                else
                    if(key<0)
                        flag = true;
                        for p=1:size(check_for,2)
                            if (bitxor(check_for(3,p),check_for(4,p))==1)
                                flag = false;
                            end
                        end
                        if (flag)
                            neg = neg + check_for(2,1);
                        end             
                    end
                end
            end
            if pos==neg
                new_state(j) = init_state(j);
            else
                if pos>neg
                    new_state(j) = 1;
                else
                    new_state(j) = 0;
                end
            end
        end
        if and(last_cas3==1,init_state(22)==1)
            new_state(38) = 1;
            dna_damage_run = dna_damage_run + 1;
        else
            new_state(38) = 0;
            dna_damage_run = 0;
        end
        last_cas3 = init_state(22);
        init_state = new_state;
        new_state = zeros(1,num_nodes);
        if (dna_damage_run >=20)
            d = 1;
            break
        end
        t = t + 1;
    end 
end

