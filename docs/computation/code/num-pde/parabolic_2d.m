% 2D 抛物方程差分格式
% 原方程:
%   u_t = (1/16) * (u_xx + u_yy), (x,y) in (0,1) x (0,1), t > 0
%
% 边界条件:
%   u(0,y,t) = u(1,y,t) = 0
%   u_j,0^n = u_j,1^n, u_j,K^n = u_j,K-1^n
%
% 初值:
%   u(x,y,0) = sin(pi*x) * cos(pi*y)
%
% 精确解:
%   u(x,y,t) = sin(pi*x) * cos(pi*y) * exp(-pi^2*t/8)
%
% 需要比较:
%   六点对称格式(Crank-Nicolson)、ADI、预校法、LOD 法。
%   t = 1, 采样点 (x_j,y_k) = (j/4,k/4), j,k = 1,2,3。
%   表格中数值保留六位小数；内部按 MATLAB double 精度计算。

clear; clc; close all;

alpha = 1 / 16;
t_final = 1;
sample_points = [ ...
    1/4, 1/4;
    1/4, 1/2;
    1/4, 3/4;
    1/2, 1/4;
    1/2, 1/2;
    1/2, 3/4;
    3/4, 1/4;
    3/4, 1/2;
    3/4, 3/4 ...
];

output_dir = fullfile(fileparts(mfilename('fullpath')), 'Parabolic_2D_output');
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

methods = { ...
    struct('tag', 'cn', 'label', '六点对称格式(CN)', 'solver', @solve_cn), ...
    struct('tag', 'adi', 'label', 'ADI格式', 'solver', @solve_adi), ...
    struct('tag', 'predictor_corrector', 'label', '预校法', 'solver', @solve_predictor_corrector), ...
    struct('tag', 'lod', 'label', 'LOD法', 'solver', @solve_lod) ...
};

%% 指定网格下的采样点对比
N = 40;
h = 1 / N;
tau = h^2;
r = tau / h^2;
T = round(t_final / tau);

fprintf('采样点对比: h = 1/%d, tau = 1/%d, r = %.6g, t = %g\n', ...
    N, T, r, t_final);
fprintf('y方向边界按 u_j,0^n = u_j,1^n, u_j,K^n = u_j,K-1^n 处理。\n');

comparison_rows = [];
comparison_labels = {};

for method_id = 1:numel(methods)
    method = methods{method_id};
    [x, y, U] = method.solver(N, T, alpha);
    U_exact = exact_solution_2d(x, y, t_final);
    E = abs(U - U_exact);

    fprintf('\n%s\n', method.label);
    rows = sample_result_rows(N, sample_points, U, U_exact);
    print_sample_table(rows);
    write_sample_csv(fullfile(output_dir, [method.tag, '_sample_table.csv']), rows);
    save_error_heatmap(output_dir, method.tag, method.label, x, y, E);

    comparison_rows = [comparison_rows; rows]; %#ok<AGROW>
    comparison_labels = [comparison_labels; repmat({method.label}, size(rows, 1), 1)]; %#ok<AGROW>
end

write_all_sample_csv(fullfile(output_dir, 'all_methods_sample_table.csv'), ...
    comparison_labels, comparison_rows);

%% 误差阶计算
% 取 h = 1/20, 1/40, 1/80，并保持 r = tau/h^2 = 1。
N_list = [20, 40, 80];
error_table = zeros(numel(methods), numel(N_list));
order_table = nan(numel(methods), numel(N_list) - 1);

fprintf('\n无穷范数误差与误差阶，r = 1, t = 1\n');

for method_id = 1:numel(methods)
    method = methods{method_id};

    for grid_id = 1:numel(N_list)
        N_now = N_list(grid_id);
        tau_now = (1 / N_now)^2;
        T_now = round(t_final / tau_now);

        [x, y, U] = method.solver(N_now, T_now, alpha);
        U_exact = exact_solution_2d(x, y, t_final);
        error_table(method_id, grid_id) = max(abs(U(:) - U_exact(:)));
    end

    for grid_id = 2:numel(N_list)
        order_table(method_id, grid_id - 1) = ...
            log(error_table(method_id, grid_id - 1) / error_table(method_id, grid_id)) / log(2);
    end
end

print_convergence_table(methods, N_list, error_table, order_table);
write_convergence_csv(fullfile(output_dir, 'convergence_order_table.csv'), ...
    methods, N_list, error_table, order_table);

fprintf('\n结果表格和图片已保存到:\n%s\n', output_dir);

function rows = sample_result_rows(N, sample_points, U, U_exact)
    rows = zeros(size(sample_points, 1), 5);

    for i = 1:size(sample_points, 1)
        x0 = sample_points(i, 1);
        y0 = sample_points(i, 2);
        ix = round(x0 * N) + 1;
        iy = round(y0 * N) + 1;
        numerical = U(ix, iy);
        exact = U_exact(ix, iy);

        rows(i, :) = [x0, y0, numerical, exact, abs(numerical - exact)];
    end
end

function print_sample_table(rows)
    fprintf('%10s  %10s  %14s  %14s  %14s\n', ...
        'x_j', 'y_k', '数值解', '真解', '绝对误差');
    fprintf('%10s  %10s  %14s  %14s  %14s\n', ...
        '----------', '----------', '--------------', '--------------', '--------------');

    for i = 1:size(rows, 1)
        fprintf('%10.6f  %10.6f  %14.6f  %14.6f  %14.6f\n', rows(i, :));
    end
end

function write_sample_csv(file_name, rows)
    fid = fopen(file_name, 'w');
    if fid < 0
        error('无法写入文件: %s', file_name);
    end

    cleanup = onCleanup(@() fclose(fid));
    fprintf(fid, 'x_j,y_k,数值解,真解,绝对误差\n');

    for i = 1:size(rows, 1)
        fprintf(fid, '%.6f,%.6f,%.6f,%.6f,%.6f\n', rows(i, :));
    end
end

function write_all_sample_csv(file_name, labels, rows)
    fid = fopen(file_name, 'w');
    if fid < 0
        error('无法写入文件: %s', file_name);
    end

    cleanup = onCleanup(@() fclose(fid));
    fprintf(fid, '格式,x_j,y_k,数值解,真解,绝对误差\n');

    for i = 1:size(rows, 1)
        fprintf(fid, '%s,%.6f,%.6f,%.6f,%.6f,%.6f\n', labels{i}, rows(i, :));
    end
end

function print_convergence_table(methods, N_list, error_table, order_table)
    fprintf('%20s', '格式');
    for i = 1:numel(N_list)
        fprintf('  %14s', sprintf('E_1/%d', N_list(i)));
        if i < numel(N_list)
            fprintf('  %14s', sprintf('阶%d-%d', N_list(i), N_list(i + 1)));
        end
    end
    fprintf('\n');

    for method_id = 1:numel(methods)
        fprintf('%20s', methods{method_id}.label);

        for grid_id = 1:numel(N_list)
            fprintf('  %14.6e', error_table(method_id, grid_id));
            if grid_id < numel(N_list)
                fprintf('  %14.6f', order_table(method_id, grid_id));
            end
        end
        fprintf('\n');
    end
end

function write_convergence_csv(file_name, methods, N_list, error_table, order_table)
    fid = fopen(file_name, 'w');
    if fid < 0
        error('无法写入文件: %s', file_name);
    end

    cleanup = onCleanup(@() fclose(fid));
    fprintf(fid, '格式');
    for i = 1:numel(N_list)
        fprintf(fid, ',E_1/%d', N_list(i));
        if i < numel(N_list)
            fprintf(fid, ',阶_%d_to_%d', N_list(i), N_list(i + 1));
        end
    end
    fprintf(fid, '\n');

    for method_id = 1:numel(methods)
        fprintf(fid, '%s', methods{method_id}.label);

        for grid_id = 1:numel(N_list)
            fprintf(fid, ',%.15e', error_table(method_id, grid_id));
            if grid_id < numel(N_list)
                fprintf(fid, ',%.6f', order_table(method_id, grid_id));
            end
        end
        fprintf(fid, '\n');
    end
end

function save_error_heatmap(output_dir, tag, label, x, y, E)
    figure('Name', [label, ' 误差热力图']);
    imagesc(y, x, E);
    set(gca, 'YDir', 'normal');
    colorbar;
    xlabel('y');
    ylabel('x');
    title([label, ' 在 t=1 的绝对误差']);
    ax = gca;
    ax.Toolbar.Visible = 'off';

    exportgraphics(gcf, fullfile(output_dir, [tag, '_error_heatmap.png']), ...
        'Resolution', 200);
end

function [x, y, U] = solve_cn(N, T, alpha)
    [x, y, V, Dx, Dy, mu] = setup_problem(N, T, alpha);
    nx = N - 1;
    ny = N - 1;
    I = speye(nx * ny);
    L = kron(speye(ny), Dx) + kron(Dy, speye(nx));
    A = I - 0.5 * mu * L;
    B = I + 0.5 * mu * L;

    u_vec = V(:);

    for n = 1:T
        u_vec = A \ (B * u_vec);
    end

    V = reshape(u_vec, nx, ny);
    U = expand_with_boundary(N, V);
end

function [x, y, U] = solve_adi(N, T, alpha)
    [x, y, V, Dx, Dy, mu] = setup_problem(N, T, alpha);
    nx = N - 1;
    ny = N - 1;

    Ix = speye(nx);
    Iy = speye(ny);
    Ax = Ix - 0.5 * mu * Dx;
    Bx = Ix + 0.5 * mu * Dx;
    Ay = Iy - 0.5 * mu * Dy;
    By = Iy + 0.5 * mu * Dy;

    for n = 1:T
        half_step = Ax \ (V * By');
        V = (Ay \ (Bx * half_step)')';
    end

    U = expand_with_boundary(N, V);
end

function [x, y, U] = solve_predictor_corrector(N, T, alpha)
    [x, y, V, Dx, Dy, mu] = setup_problem(N, T, alpha);

    for n = 1:T
        L_old = apply_laplacian(V, Dx, Dy);
        V_predict = V + mu * L_old;
        L_predict = apply_laplacian(V_predict, Dx, Dy);
        V = V + 0.5 * mu * (L_old + L_predict);
    end

    U = expand_with_boundary(N, V);
end

function [x, y, U] = solve_lod(N, T, alpha)
    [x, y, V, Dx, Dy, mu] = setup_problem(N, T, alpha);
    nx = N - 1;
    ny = N - 1;

    Ix = speye(nx);
    Iy = speye(ny);
    Ax = Ix - mu * Dx;
    Ay = Iy - mu * Dy;

    for n = 1:T
        half_step = Ax \ V;
        V = (Ay \ half_step')';
    end

    U = expand_with_boundary(N, V);
end

function [x, y, V, Dx, Dy, mu] = setup_problem(N, T, alpha)
    h = 1 / N;
    tau = 1 / T;
    mu = alpha * tau / h^2;

    x = linspace(0, 1, N + 1)';
    y = linspace(0, 1, N + 1)';
    V = initial_solution_2d(x(2:N), y(2:N));

    Dx = second_diff_x_dirichlet_matrix(N);
    Dy = second_diff_y_copy_boundary_matrix(N);
end

function L = apply_laplacian(V, Dx, Dy)
    L = Dx * V + V * Dy';
end

function Dx = second_diff_x_dirichlet_matrix(N)
    n = N - 1;
    e = ones(n, 1);
    Dx = spdiags([e, -2 * e, e], -1:1, n, n);
end

function Dy = second_diff_y_copy_boundary_matrix(N)
    n = N - 1;
    e = ones(n, 1);
    Dy = spdiags([e, -2 * e, e], -1:1, n, n);

    % u_j,0 = u_j,1, u_j,K = u_j,K-1
    % 所以靠近边界的二阶差商分别变成 u_j,2-u_j,1 与 u_j,K-2-u_j,K-1。
    Dy(1, 1) = -1;
    Dy(n, n) = -1;
end

function U = expand_with_boundary(N, V)
    U = zeros(N + 1, N + 1);
    U(2:N, 2:N) = V;

    % x=0 和 x=1 是第一类齐次边界，保持为 0。
    % y=0 和 y=1 使用教材给出的边界层复制。
    U(2:N, 1) = U(2:N, 2);
    U(2:N, N + 1) = U(2:N, N);
end

function U = initial_solution_2d(x, y)
    U = sin(pi * x) * cos(pi * y)';
end

function U = exact_solution_2d(x, y, t)
    U = sin(pi * x) * cos(pi * y)' * exp(-pi^2 * t / 8);
end
