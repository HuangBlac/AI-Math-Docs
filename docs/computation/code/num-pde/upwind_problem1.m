% 第一题：迎风差分格式
% 求解初边值问题：
%   u_t - 2 u_x = 0, 0 < x < 1, t > 0
%   u(x,0) = 1 + sin(2*pi*x)
%   u(1,t) = 1
%
% 因为方程可以写成 u_t + a u_x = 0，其中 a = -2，
% 波从右向左传播，所以入流边界在 x = 1。
% 因此迎风差分要使用右侧网格点：
%   显式格式：u_j^{k+1} = u_j^k + (2*tau/h)*(u_{j+1}^k - u_j^k)
%   隐式格式：u_j^k - u_j^{k-1} = (2*tau/h)*(u_{j+1}^k - u_j^k)

clear; clc; close all;

% 设置空间步长、时间步长和网格比
h = 0.1;
tau = 0.02;
lambda = 2 * tau / h;

% 建立空间网格
x = 0:h:1;
N = length(x) - 1;              % 未知点为 x = 0,0.1,...,0.9

% 设置需要输出的时间层
t_targets = [0.1, 0.5];
k_targets = round(t_targets / tau);
k_max = max(k_targets);

% 初值条件
u_explicit = 1 + sin(2 * pi * x);
u_implicit = u_explicit;
u_explicit(end) = 1;            % 右边界条件 u(1,t)=1
u_implicit(end) = 1;

% 保存指定时刻的数值解和精确解
result_explicit = zeros(length(t_targets), length(x));
result_implicit = zeros(length(t_targets), length(x));
result_exact = zeros(length(t_targets), length(x));

% 隐式格式的系数矩阵：
% (1+lambda)u_j^k - lambda*u_{j+1}^k = u_j^{k-1}
A = (1 + lambda) * eye(N) - lambda * diag(ones(N - 1, 1), 1);

for k = 1:k_max
    % 显式迎风格式
    u_old = u_explicit;
    u_explicit(1:N) = u_old(1:N) + lambda * (u_old(2:N + 1) - u_old(1:N));
    u_explicit(end) = 1;

    % 隐式迎风格式
    b = u_implicit(1:N).';
    b(end) = b(end) + lambda * 1;        % 将右边界条件加入右端项
    u_new_inner = A \ b;
    u_implicit(1:N) = u_new_inner.';
    u_implicit(end) = 1;

    % 如果当前时间层是目标时间层，则记录结果
    target_index = find(k_targets == k, 1);
    if ~isempty(target_index)
        t_now = k * tau;
        result_explicit(target_index, :) = u_explicit;
        result_implicit(target_index, :) = u_implicit;
        result_exact(target_index, :) = exact_solution_problem1(x, t_now);
    end
end

% 在命令行输出表格
for m = 1:length(t_targets)
    fprintf('\n===== t = %.2f =====\n', t_targets(m));
    result_table = table( ...
        x.', ...
        result_explicit(m, :).', ...
        result_implicit(m, :).', ...
        result_exact(m, :).', ...
        'VariableNames', {'x', 'Explicit', 'Implicit', 'Exact'} ...
    );
    disp(result_table);
end

% 绘制数值解和精确解的对比图
figure('Name', 'Upwind problem 1');
for m = 1:length(t_targets)
    subplot(1, length(t_targets), m);
    plot(x, result_exact(m, :), 'k-', 'LineWidth', 1.5); hold on;
    plot(x, result_explicit(m, :), 'ro--', 'LineWidth', 1.2);
    plot(x, result_implicit(m, :), 'bs--', 'LineWidth', 1.2);
    grid on;
    xlabel('x');
    ylabel('u');
    title(sprintf('t = %.2f', t_targets(m)));
    legend('Exact', 'Explicit upwind', 'Implicit upwind', 'Location', 'best');
end

function u = exact_solution_problem1(x, t)
    % 精确解由特征线 x + 2t = 常数给出
    y = x + 2 * t;
    u = ones(size(x));
    inside_initial = (y <= 1);
    u(inside_initial) = 1 + sin(2 * pi * y(inside_initial));
end
