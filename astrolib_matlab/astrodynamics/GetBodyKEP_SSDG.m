function [ sma, ecc, inc, nu, argp, raan ] = GetBodyKEP_SSDG ( ...
    planet, jd2k )
%GETBODYKEP_SSDG Get body's orbital elements
%   Returns the classical orbital elements for the given body.
%   Reference is J2000. Simplified perturbations are considered.
%
% Observations:
%   Data resulting from a polynomial fit.
%   Data magnitudes are in [deg] and [AU]
%
% Inputs:
%   planet: name of the target planet [string]
%   jd2k: days from J2000 (1 Jan 2000 T12.0) [days]
%
% Outputs:
%   sma: semi-major axis [km]
%   ecc: eccentricity (0=circle, <1=ellipse, 1=parabola, >1=hyperbola)
%   inc: inclination to the ecliptic [rad]
%   nu: true anomaly [rad]
%   argp: argument of perihelion [rad]
%   raan: right ascension of the ascending node [rad]
%
% Example:
%   [ sma, ecc, inc, nu, argp, raan ] = GetBodyKEP_SSDG ( 'Earth', 7300 );
%
% References:
%   [1] E. M. Standish
%       Keplerian elements for approximate positions of the major planets
%       Solar System Dynamics Group, JPL, Caltech
%       https://ssd.jpl.nasa.gov/?planet_pos
%       https://ssd.jpl.nasa.gov/txt/aprx_pos_planets.pdf
%
%David de la Torre Sangra
%August 2014

% Constants
AU = 149597871; % Astronomical Unit (AU) [km]
d2r = pi/180; % Degrees to Radians

% Find planet
planets = {'MERCURY','VENUS','EARTH','MARS',...
    'JUPITER','SATURN','URANUS','NEPTUNE','PLUTO'}; % Array of planets
i = find(contains(planets,upper(planet))); % Find planet index in array

% If planet not in database, throw error
if isempty(i), error('Planet "%s" not in database',planet); end

% Planet index in database
i = 2 * (i - 1) + 1;

% Compute T reference time (number of centuries past J2000)
T = jd2k / 36525;

% Select table to use for computations, by J2000 century range
kep = zeros(1,6);
hirestable = T > -2 && T < 0.5;
if hirestable % Use [1800,2050] table
    
    % Table of Keplerian Elements and their rates, wrt the mean ecliptic
    % and equinox J2000, valid for the time interval 1800 AD - 2050 AD
    tke1 = [ ...
    ... % sma         ecc           inc             L               w           raan
      0.38709927,  0.20563593,  7.00497902,    252.25032350,  77.45779628,  48.33076593; ...
      0.00000037,  0.00001906, -0.00594749, 149472.67411175,   0.16047689,  -0.12534081; ...
      0.72333566,  0.00677672,  3.39467605,    181.97909950, 131.60246718,  76.67984255; ...
      0.00000390, -0.00004107, -0.00078890,  58517.81538729,   0.00268329,  -0.27769418; ...
      1.00000261,  0.01671123, -0.00001531,    100.46457166, 102.93768193,   0.00000000; ...
      0.00000562, -0.00004392, -0.01294668,  35999.37244981,   0.32327364,   0.00000000; ...
      1.52371034,  0.09339410,  1.84969142,     -4.55343205, -23.94362959,  49.55953891; ...
      0.00001847,  0.00007882, -0.00813131,  19140.30268499,   0.44441088,  -0.29257343; ...
      5.20288700,  0.04838624,  1.30439695,     34.39644051,  14.72847983, 100.47390909; ...
     -0.00011607, -0.00013253, -0.00183714,   3034.74612775,   0.21252668,   0.20469106; ...
      9.53667594,  0.05386179,  2.48599187,     49.95424423,  92.59887831, 113.66242448; ...
     -0.00125060, -0.00050991,  0.00193609,   1222.49362201,  -0.41897216,  -0.28867794; ...
     19.18916464,  0.04725744,  0.77263783,    313.23810451, 170.95427630,  74.01692503; ...
     -0.00196176, -0.00004397, -0.00242939,    428.48202785,   0.40805281,   0.04240589; ...
     30.06992276,  0.00859048,  1.77004347,    -55.12002969,  44.96476227, 131.78422574; ...
      0.00026291,  0.00005105,  0.00035372,    218.45945325,  -0.32241464,  -0.00508664; ...
     39.48211675,  0.24882730, 17.14001206,    238.92903833, 224.06891629, 110.30393684; ...
     -0.00031596,  0.00005170,  0.00004818,    145.20780515,  -0.04062942,  -0.01183482; ...
      ];
    
    % Extract orbital elements from table
    for j=1:6
        kep0 = tke1(i,j); % Keplerian element
        dkep = tke1(i+1,j); % Time-derivative of Keplerian element
        kep(j) = kep0 + dkep * T; % Propagate Keplerian element in time
    end
    
else % Use [-3000,3000] table
    
    % Table of Keplerian Elements and their rates, wrt the mean ecliptic and
    % equinox J2000, valid for the time interval 3000 BC - 3000 AD
    tke2 = [ ...
    ... % sma         ecc           inc             L               w           raan
      0.38709843,  0.20563661,  7.00559432,    252.25166724,  77.45771895,  48.33961819; ...
      0.00000000,  0.00002123, -0.00590158, 149472.67486623,   0.15940013,  -0.12214182; ...
      0.72332102,  0.00676399,  3.39777545,    181.97970850, 131.76755713,  76.67261496; ...
     -0.00000026, -0.00005107,  0.00043494,  58517.81560260,   0.05679648,  -0.27274174; ...
      1.00000018,  0.01673163, -0.00054346,    100.46691572, 102.93005885,  -5.11260389; ...
     -0.00000003, -0.00003661, -0.01337178,  35999.37306329,   0.31795260,  -0.24123856; ...
      1.52371243,  0.09336511,  1.85181869,     -4.56813164, -23.91744784,  49.71320984; ...
      0.00000097,  0.00009149, -0.00724757,  19140.29934243,   0.45223625,  -0.26852431; ...
      5.20248019,  0.04853590,  1.29861416,     34.33479152,  14.27495244, 100.29282654; ...
     -0.00002864,  0.00018026, -0.00322699,   3034.90371757,   0.18199196,   0.13024619; ...
      9.54149883,  0.05550825,  2.49424102,     50.07571329,  92.86136063, 113.63998702; ...
     -0.00003065, -0.00032044,  0.00451969,   1222.11494724,   0.54179478,  -0.25015002; ...
     19.18797948,  0.04685740,  0.77298127,    314.20276625, 172.43404441,  73.96250215; ...
     -0.00020455, -0.00001550, -0.00180155,    428.49512595,   0.09266985,   0.05739699; ...
     30.06952752,  0.00895439,  1.77005520,    304.22289287,  46.68158724, 131.78635853; ...
      0.00006447,  0.00000818,  0.00022400,    218.46515314,   0.01009938,  -0.00606302; ...
     39.48686035,  0.24885238, 17.14104260,    238.96535011, 224.09702598, 110.30167986; ...
      0.00449751,  0.00006016,  0.00000501,    145.18042903,  -0.00968827,  -0.00809981; ...
      ];
    
    % Extract orbital elements from table
    for j=1:6
        kep0 = tke2(i,j); % Keplerian element
        dkep = tke2(i+1,j); % Time-derivative of Keplerian element
        kep(j) = kep0 + dkep * T; % Propagate Keplerian element in time
    end
    
end

% Convert Keplerian elements in proper units
sma = kep(1) * AU;
ecc = kep(2);
inc = kep(3) * d2r;
raan = mod(kep(6)*d2r,2*pi);
argp = mod((kep(5)-kep(6))*d2r,2*pi); % [1] Eq. 8-30
M = mod((kep(4)-kep(5))*d2r,2*pi); % [1] Eq. 8-30

% Fix for mean anomaly, Jupiter through Pluto, -3000,3000 database
if ~hirestable && i>7
    
    % Additional terms which must be added to the computation of M
    % for Jupiter through Pluto, 3000 BC to 3000 AD, as described
    % in the related document.
    tke3 = [ ... 
    ... %  b             c             s            f 
      -0.00012452,  0.06064060, -0.35635438, 38.35125000; ...
       0.00025899, -0.13434469,  0.87320147, 38.35125000; ...
       0.00058331, -0.97731848,  0.17689245,  7.67025000; ...
      -0.00041348,  0.68346318, -0.10162547,  7.67025000; ...
      -0.01262724,  0.00000000,  0.00000000,  0.00000000; ...
      ];
    
    ii = (i-1)/2+1;
    b = tke3(ii-4,1);
    c = tke3(ii-4,2);
    s = tke3(ii-4,3);
    f = tke3(ii-4,4);
    M = M/d2r + b*T^2 + c*cos(f*T) + s*sin(f*T); % [1] Eq. 8-30
    M = mod(M*d2r,2*pi); % From deg to rad
end

% Compute true anomaly (Kepler's equation)
M = mod(M,2*pi); % Range [0,2pi]
nu = M2O(M,ecc,1E-9);

end

