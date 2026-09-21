% 1D 抛物方程差分格式
% 原方程:
%   u_t = u_xx + sin(t), 0 < x < 1, t > 0
% 初值:
%   u(0,x) = cos(pi*x)
% Neumann 边界:
%   u_x(t,0) = u_x(t,1) = 0
%
% 精确解:
%   u(x,t) = exp(-pi^2*t)*cos(pi*x) + 1 - cos(t)
%
% 计算目标:
%   输出 x_j = j/4, j = 0,1,2,3,4 处的数值结果。
%   内部按 MATLAB double 精度计算，表格输出保留六位小数。

clear; clc; close all;

sample_x = (0:4)' / 4;
output_dir = fullfile(fileparts(mfilename('fullpath')), 'Parabolic_1D_output');

if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

%% 向前显式格式
explicit_cases = struct( ...
    'name', {'a', 'b', 'c'}, ...
    'N', {40, 80, 80}, ...
    'T', {3200, 12800, 3200}, ...
    'report_steps', {[3200], [12800], [20, 40]} ...
);

for case_id = 1:numel(explicit_cases)
    cfg = explicit_cases(case_id);
    h = 1 / cfg.N;
    tau = 1 / cfg.T;
    r = tau / h^2;

    [x, snapshots] = forward_difference(cfg.N, cfg.T, cfg.report_steps);

    fprintf('\n显式格式 方案 %s: h = 1/%d, tau = 1/%d, r = %.6g\n', ...
        cfg.name, cfg.N, cfg.T, r);

    show_case_results(output_dir, 'explicit', '显式格式', cfg, tau, sample_x, snapshots);
    save_case_plot(output_dir, 'explicit', '显式格式', cfg, x, tau, r, snapshots);
end

%% 向后隐式格式
% 两组网格:
%   h = 1/40, r = 1  -> tau = 1/1600, T = 1600
%   h = 1/80, r = 2  -> tau = 1/3200, T = 3200
implicit_cases = struct( ...
    'name', {'a', 'b'}, ...
    'N', {40, 80}, ...
    'r', {1, 2}, ...
    'report_time', {1, 1} ...
);

for case_id = 1:numel(implicit_cases)
    cfg = make_r_case(implicit_cases(case_id));
    [x, snapshots] = backward_difference(cfg.N, cfg.T, cfg.report_steps);

    fprintf('\n隐式格式 方案 %s: h = 1/%d, tau = 1/%d, r = %.6g\n', ...
        cfg.name, cfg.N, cfg.T, cfg.r);

    show_case_results(output_dir, 'implicit', '隐式格式', cfg, cfg.tau, sample_x, snapshots);
    save_case_plot(output_dir, 'implicit', '隐式格式', cfg, x, cfg.tau, cfg.r, snapshots);
end

%% 六点对称格式，也就是 Crank-Nicolson 格式
cn_cases = struct( ...
    'name', {'a', 'b'}, ...
    'N', {40, 80}, ...
    'r', {1, 2}, ...
    'report_time', {1, 1} ...
);

for case_id = 1:numel(cn_cases)
    cfg = make_r_case(cn_cases(case_id));
    [x, snapshots] = crank_nicolson_difference(cfg.N, cfg.T, cfg.report_steps);

    fprintf('\n六点对称格式(CN) 方案 %s: h = 1/%d, tau = 1/%d, r = %.6g\n', ...
        cfg.name, cfg.N, cfg.T, cfg.r);

    show_case_results(output_dir, 'cn', '六点对称格式', cfg, cfg.tau, sample_x, snapshots);
    save_case_plot(output_dir, 'cn', '六点对称格式', cfg, x, cfg.tau, cfg.r, snapshots);
end

fprintf('\n结果表格和图片已保存到:\n%s\n', output_dir);

function cfg = make_r_case(raw_cfg)
    h = 1 / raw_cfg.N;
    tau = raw_cfg.r * h^2;
    T = round(raw_cfg.report_time / tau);

    cfg = raw_cfg;
    cfg.tau = tau;
    cfg.T = T;
    cfg.report_steps = T;
end

function show_case_results(output_dir, scheme_tag, scheme_label, cfg, tau, sample_x, snapshots)
    sample_index = round(sample_x * cfg.N) + 1;

    for k = 1:numel(cfg.report_steps)
        n = cfg.report_steps(k);
        t_now = n * tau;

        numerical = snapshots{k}(sample_index);
        exact = exact_solution(sample_x, t_now);
        err = abs(numerical - exact);

        fprintf('n = %d, t = %.10g\n', n, t_now);
        print_fixed_table(sample_x, numerical, exact, err);

        table_file = fullfile(output_dir, ...
            sprintf('%s_case_%s_n_%d_table.csv', scheme_tag, cfg.name, n));
        write_fixed_csv(table_file, sample_x, numerical, exact, err);
    end
end

function print_fixed_table(sample_x, numerical, exact, err)
    fprintf('%10s  %14s  %14s  %14s\n', ...
        'x_j', '数值解', '精确解', '绝对误差');
    fprintf('%10s  %14s  %14s  %14s\n', ...
        '----------', '--------------', '--------------', '--------------');

    for i = 1:numel(sample_x)
        fprintf('%10.6f  %14.6f  %14.6f  %14.6f\n', ...
            sample_x(i), numerical(i), exact(i), err(i));
    end
end

function write_fixed_csv(file_name, sample_x, numerical, exact, err)
    fid = fopen(file_name, 'w');
    if fid < 0
        error('无法写入结果文件: %s', file_name);
    end

    cleanup = onCleanup(@() fclose(fid));
    fprintf(fid, 'x_j,数值解,精确解,绝对误差\n');

    for i = 1:numel(sample_x)
        fprintf(fid, '%.6f,%.6f,%.6f,%.6f\n', ...
            sample_x(i), numerical(i), exact(i), err(i));
    end
end

function save_case_plot(output_dir, scheme_tag, scheme_label, cfg, x, tau, r, snapshots)
    figure('Name', [scheme_label, ' 方案 ', cfg.name]);
    hold on;
    grid on;

    for k = 1:numel(cfg.report_steps)
        n = cfg.report_steps(k);
        t_now = n * tau;
        plot(x, snapshots{k}, 'LineWidth', 1.4, ...
            'DisplayName', sprintf('n=%d, t=%.5g', n, t_now));
    end

    xlabel('x');
    ylabel('u(x,t)');
    title(sprintf('%s 方案 %s, r = %.6g', scheme_label, cfg.name, r));
    legend('Location', 'best');
    ax = gca;
    ax.Toolbar.Visible = 'off';

    figure_file = fullfile(output_dir, sprintf('%s_case_%s_plot.png', scheme_tag, cfg.name));
    exportgraphics(gcf, figure_file, 'Resolution', 200);
end

function [x, snapshots] = forward_difference(N, T, report_steps)
    h = 1 / N;
    tau = 1 / T;
    r = tau / h^2;
    max_step = max(report_steps);

    x = linspace(0, 1, N + 1)';
    u = cos(pi * x);
    snapshots = cell(numel(report_steps), 1);
    report_id = 1;

    for n = 1:max_step
        old = u;
        t_now = n * tau;

        u(1) = old(1) + tau * ...
            (2 * (old(2) - old(1)) / h^2 + sin(t_now));
        u(N + 1) = old(N + 1) + tau * ...
            (2 * (old(N) - old(N + 1)) / h^2 + sin(t_now));

        for j = 2:N
            u(j) = old(j) + r * (old(j - 1) + old(j + 1) - 2 * old(j)) ...
                + tau * sin(t_now);
        end

        if report_id <= numel(report_steps) && n == report_steps(report_id)
            snapshots{report_id} = u;
            report_id = report_id + 1;
        end
    end
end

function [x, snapshots] = backward_difference(N, T, report_steps)
    h = 1 / N;
    tau = 1 / T;
    r = tau / h^2;
    max_step = max(report_steps);

    x = linspace(0, 1, N + 1)';
    u = cos(pi * x);
    A = backward_matrix(N, r);
    snapshots = cell(numel(report_steps), 1);
    report_id = 1;

    for n = 1:max_step
        t_now = n * tau;
        rhs = u + tau * sin(t_now) * ones(N + 1, 1);
        u = A \ rhs;

        if report_id <= numel(report_steps) && n == report_steps(report_id)
            snapshots{report_id} = u;
            report_id = report_id + 1;
        end
    end
end

function A = backward_matrix(N, r)
    A = zeros(N + 1, N + 1);

    A(1, 1) = 1 + 2 * r;
    A(1, 2) = -2 * r;
    A(N + 1, N) = -2 * r;
    A(N + 1, N + 1) = 1 + 2 * r;

    for j = 2:N
        A(j, j - 1) = -r;
        A(j, j) = 1 + 2 * r;
        A(j, j + 1) = -r;
    end
end

function [x, snapshots] = crank_nicolson_difference(N, T, report_steps)
    h = 1 / N;
    tau = 1 / T;
    r = tau / h^2;
    max_step = max(report_steps);

    x = linspace(0, 1, N + 1)';
    u = cos(pi * x);
    [left_matrix, right_matrix] = crank_nicolson_matrices(N, r);
    snapshots = cell(numel(report_steps), 1);
    report_id = 1;

    for n = 1:max_step
        t_old = (n - 1) * tau;
        t_now = n * tau;
        source = tau * 0.5 * (sin(t_old) + sin(t_now)) * ones(N + 1, 1);
        rhs = right_matrix * u + source;
        u = left_matrix \ rhs;

        if report_id <= numel(report_steps) && n == report_steps(report_id)
            snapshots{report_id} = u;
            report_id = report_id + 1;
        end
    end
end

function [left_matrix, right_matrix] = crank_nicolson_matrices(N, r)
    left_matrix = zeros(N + 1, N + 1);
    right_matrix = zeros(N + 1, N + 1);

    left_matrix(1, 1) = 1 + r;
    left_matrix(1, 2) = -r;
    left_matrix(N + 1, N) = -r;
    left_matrix(N + 1, N + 1) = 1 + r;

    right_matrix(1, 1) = 1 - r;
    right_matrix(1, 2) = r;
    right_matrix(N + 1, N) = r;
    right_matrix(N + 1, N + 1) = 1 - r;

    for j = 2:N
        left_matrix(j, j - 1) = -r / 2;
        left_matrix(j, j) = 1 + r;
        left_matrix(j, j + 1) = -r / 2;

        right_matrix(j, j - 1) = r / 2;
        right_matrix(j, j) = 1 - r;
        right_matrix(j, j + 1) = r / 2;
    end
end

function u = exact_solution(x, t)
    u = exp(-pi^2 * t) .* cos(pi * x) + 1 - cos(t);
end
