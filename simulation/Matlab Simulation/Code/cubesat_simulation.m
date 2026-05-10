%% CubeSat Re-entry Burn Simulation
% This script simulates the orbit propagation, deorbit, and burn-up of a CubeSat.

%% 1. Parameters
R_E = 6371;             % Earth radius in km
h_orbit = 700;          % Initial orbit altitude in km
r_orbit = R_E + h_orbit; % Initial orbit radius
incl = 97;              % Inclination in degrees
num_orbits = 3;         % Number of orbits to simulate
total_steps = 1000;     % Total simulation steps

earth_rot_speed = 0.5;  % Earth rotation speed factor

deorbit_start = 200;    % Step where deorbit starts
burn_start = 400;       % Step where burn-up starts

%% 2. Orbit propagation (with deorbit effect)
theta = linspace(0, 2*pi * num_orbits, total_steps);
r_sat = zeros(3, total_steps);

for k = 1:total_steps
    
    altitude = r_orbit;
    
    % Deorbit phase: altitude decreases
    if k > deorbit_start
        t = (k - deorbit_start) / (burn_start - deorbit_start);
        t = min(t, 1);
        altitude = r_orbit - t * (r_orbit - (R_E + 80));
    end
    
    % Burn phase: altitude stays at atmospheric entry level
    if k > burn_start
        altitude = R_E + 80;
    end
    
    % Local position in orbital plane
    r_local = altitude * [cos(theta(k)); sin(theta(k)); 0];
    
    % Rotation matrix for inclination
    R_incl = [1 0 0;
              0 cosd(incl) -sind(incl);
              0 sind(incl) cosd(incl)];
          
    % Final position in 3D space
    r_sat(:,k) = R_incl * r_local;
end

%% 3. Figure Setup
figure('Color', 'w', 'Name', 'CubeSat Re-entry Burn Simulation');
hold on; grid on; axis equal; view(3);

xlabel('X [km]'); ylabel('Y [km]'); zlabel('Z [km]');
title('CubeSat Re-entry and Burn-up (Disappearance)');

limit = r_orbit + 2000;
axis([-limit limit -limit limit -limit limit]);

%% Earth Visualization
[xs, ys, zs] = sphere(60);
% Note: topo.mat is a built-in MATLAB dataset
load('topo.mat', 'topo', 'topomap1');

earth_group = hgtransform('Parent', gca);

surf(R_E*xs, R_E*ys, R_E*zs, ...
    'FaceColor', 'texturemap', ...
    'CData', topo, ...
    'EdgeColor', 'none', ...
    'Parent', earth_group);

colormap(topomap1);

camlight headlight;
camlight right;
lighting gouraud;

%% Orbit path
plot3(r_sat(1,:), r_sat(2,:), r_sat(3,:), 'y:', 'LineWidth', 0.5);

%% 4. Satellite Model
sat_size = 1200; % Scale for visibility
axis_len = 3000;

% Cube vertices
v = [-0.5 -0.5 -0.5; 0.5 -0.5 -0.5; 0.5 0.5 -0.5; -0.5 0.5 -0.5; ...
     -0.5 -0.5 0.5; 0.5 -0.5 0.5; 0.5 0.5 0.5; -0.5 0.5 0.5] * sat_size;

% Cube faces
f = [1 2 6 5; 2 3 7 6; 3 4 8 7; 4 1 5 8; 1 2 3 4; 5 6 7 8];

sat_group = hgtransform('Parent', gca);

hSat = patch('Faces', f, 'Vertices', v, ...
    'FaceColor', 'r', ...
    'EdgeColor', 'k', ...
    'Parent', sat_group);

%% 5. Animation Loop
fprintf('Animation starting...\n');

for k = 1:total_steps
    
    % Earth rotation
    T_earth = makehgtform('zrotate', deg2rad(earth_rot_speed * k));
    set(earth_group, 'Matrix', T_earth);
    
    % Deorbit + burn + disappearance
    if k > burn_start
        
        % Calculate burn progress (disappearance effect)
        burn_progress = (k - burn_start) / 120;
        burn_progress = min(burn_progress, 1);
        
        scale_factor = 1 - burn_progress;
        
        % Apply translation and scaling (shrinking)
        T_sat = makehgtform('translate', r_sat(:,k)) * makehgtform('scale', scale_factor);
        set(sat_group, 'Matrix', T_sat);
        
        % Hide satellite when fully burned
        if burn_progress >= 1
            set(sat_group, 'Visible', 'off');
        end
        
    else
        % Normal translation along orbit
        T_sat = makehgtform('translate', r_sat(:,k));
        set(sat_group, 'Matrix', T_sat);
    end
    
    drawnow;
    pause(0.01);
end

fprintf('Satellite fully burned and disappeared.\n');
