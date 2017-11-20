function [ num_apoptosis, p_on_lethalstates ] = apoptosis_bn( network, num_nodes, removed_edges, num_iters )
% This function takes the network as the input (a nX3 matrix with each row
% i representing the ith edge (u, v, 1) for activating, (u, v, i) for 
% cooperative activating (i>1) and (u, v, -1) for inhibiting. num_nodes 
% represents the number of nodes in the boolean network. removed_edges is 
% a row vector containing the edge numbers of edges removed for this 
% analysis instance. num_iters is the number of random initial states 
% considered in this analysis (10,000 is a good number according to the 
% paper). [Note that node numberings are the same as in the given paper.]
% network = (innode, outnode, +/-, 1/0, contribution)
    adj_matrix = cell(num_nodes,num_nodes,2);
    num_edges = size(network,1);
    num_removed_edges = length(removed_edges);
    for i=1:num_removed_edges
        network(removed_edges(i),3) = 0;
    end
    for i=1:num_edges
        tuple = network(i,:);
        adj_matrix{tuple(1),tuple(2),2-tuple(4)} = cat(2,adj_matrix{tuple(1),tuple(2),2-tuple(4)},[tuple(3);tuple(5)]);
    end
    num_apoptosis = [0,0,0,0];
    p_on_lethalstates = zeros(1,num_nodes);
    num_lethalstates = 0;
    for i=1:num_iters
        init_state = zeros(1,num_nodes);
        for j=1:num_nodes-2
            if (rand<0.5)
                init_state(j) = 0;
            else
                init_state(j) = 1;
            end
        end
        d00 = simulate_bn(adj_matrix, init_state, 0, 0);
        d01 = simulate_bn(adj_matrix, init_state, 0, 1);
        d10 = simulate_bn(adj_matrix, init_state, 1, 0);
        d11 = simulate_bn(adj_matrix, init_state, 1, 1);
        num_apoptosis(1) = num_apoptosis(1) + d00;
        num_apoptosis(2) = num_apoptosis(2) + d01;
        num_apoptosis(3) = num_apoptosis(3) + d10;
        num_apoptosis(4) = num_apoptosis(4) + d11;
        if and(and(d00==1,d01==1),and(d10==1,d11==1))
            num_lethalstates = num_lethalstates + 1;
            for k=1:num_nodes
                if (init_state(k)==1)
                    p_on_lethalstates(k) = p_on_lethalstates(k) + 1;
                end
            end
        end
    end
    num_apoptosis = (num_apoptosis*100)/num_iters;
    p_on_lethalstates = p_on_lethalstates/num_lethalstates;
end

