% 第二题：显式迎风格式与隐式迎风格式
% 求解初边值问题：
%   u_t + u_x = 0, x > 0, t > 0
%   u(x,0) = |x-1|
%   u(0,t) = 1
%
% 方程的传播速度 a = 1，波从左向右传播，所以入流边界在 x = 0。
% 因此迎风差分要使用左侧网格点。
%
% 第一问：显式迎风差分格式，tau = h = 0.5
%   u_j^{k+1} = u_j^k - (tau/h)*(u_j^k - u_{j-1}^k)
%
% 第二问：隐式迎风差分格式，tau = 1, h = 0.5
%   (1+tau/h)u_j^{k+1} - (tau/h)u_{j-1}^{k+1} = u_j^k

clear; clc; close all;

% 题目没有单独给出右端边界，这里取 x 从 0 到 5。
% 由于最大计算时间为 t = 5，且波速为 1，这个区间刚好覆盖边界影响范围。
x_left = 0;
x_right = 5;
h = 0.5;
x = x_left:h:x_right;
N = length(x) - 1;              % 未知点为 x = 0.5,1.0,...,5.0

% 设置需要输出的时间
t_targets = 1:5;

% 计算显式迎风格式
tau_explicit = 0.5;
result_explicit = solve_explicit_upwind(x, h, tau_explicit, t_targets);

% 计算隐式迎风格式
tau_implicit = 1;
result_implicit = solve_implicit_upwind(x, h, tau_implicit, t_targets);

% 计算精确解，便于检查数值结果
result_exact = zeros(length(t_targets), length(x));
for m = 1:length(t_targets)
    result_exact(m, :) = exact_solution_problem2(x, t_targets(m));
end

% 输出显式迎风格式结果
fprintf('\n===== 显式迎风格式：tau = %.1f, h = %.1f =====\n', tau_explicit, h);
for m = 1:length(t_targets)
    fprintf('\n--- t = %d ---\n', t_targets(m));
    result_table = table( ...
        x.', ...
        result_explicit(m, :).', ...
        result_exact(m, :).', ...
        'VariableNames', {'x', 'Explicit', 'Exact'} ...
    );
    disp(result_table);
end

% 输出隐式迎风格式结果
fprintf('\n===== 隐式迎风格式：tau = %.1f, h = %.1f =====\n', tau_implicit, h);
for m = 1:length(t_targets)
    fprintf('\n--- t = %d ---\n', t_targets(m));
    result_table = table( ...
        x.', ...
        result_implicit(m, :).', ...
        result_exact(m, :).', ...
        'VariableNames', {'x', 'Implicit', 'Exact'} ...
    );
    disp(result_table);
end

% 绘制显式格式和隐式格式的结果对比
figure('Name', 'Upwind problem 2');
for m = 1:length(t_targets)
    subplot(2, 3, m);
    plot(x, result_exact(m, :), 'k-', 'LineWidth', 1.5); hold on;
    plot(x, result_explicit(m, :), 'ro--', 'LineWidth', 1.2);
    plot(x, result_implicit(m, :), 'bs--', 'LineWidth', 1.2);
    grid on;
    xlabel('x');
    ylabel('u');
    title(sprintf('t = %d', t_targets(m)));
    legend('Exact', 'Explicit', 'Implicit', 'Location', 'best');
end

function result = solve_explicit_upwind(x, h, tau, t_targets)
    % 使用显式迎风格式求解
    r = tau / h;
    k_targets = round(t_targets / tau);
    k_max = max(k_targets);

    u = abs(x - 1);             % 初值条件
    u(1) = 1;                   % 左边界条件 u(0,t)=1

    result = zeros(length(t_targets), length(x));
    for k = 1:k_max
        u_old = u;
        u(2:end) = u_old(2:end) - r * (u_old(2:end) - u_old(1:end - 1));
        u(1) = 1;

        target_index = find(k_targets == k, 1);
        if ~isempty(target_index)
            result(target_index, :) = u;
        end
    end
end

function result = solve_implicit_upwind(x, h, tau, t_targets)
    % 使用隐式迎风格式求解
    r = tau / h;
    k_targets = round(t_targets / tau);
    k_max = max(k_targets);
    N = length(x) - 1;

    u = abs(x - 1);             % 初值条件
    u(1) = 1;                   % 左边界条件 u(0,t)=1

    % 隐式格式的系数矩阵：
    % (1+r)u_j^{k+1} - r*u_{j-1}^{k+1} = u_j^k
    A = (1 + r) * eye(N) - r * diag(ones(N - 1, 1), -1);

    result = zeros(length(t_targets), length(x));
    for k = 1:k_max
        b = u(2:end).';
        b(1) = b(1) + r * 1;    % 将左边界条件加入右端项
        u_new_inner = A \ b;
        u(2:end) = u_new_inner.';
        u(1) = 1;

        target_index = find(k_targets == k, 1);
        if ~isempty(target_index)
            result(target_index, :) = u;
        end
    end
end

function u = exact_solution_problem2(x, t)
    % 精确解由特征线 x - t = 常数给出
    % 当 x >= t 时，特征线回到初始线 t = 0；
    % 当 x < t 时，特征线回到左边界 x = 0。
    u = ones(size(x));
    inside_initial = (x >= t);
    u(inside_initial) = abs(x(inside_initial) - t - 1);
end
