% This is just meant to test the functions I made to make sure that they
% work




subplot(1,3, 1)
alt = 1:1:(80000); 
temp = zeros(1, 80000);
for i = 1:1:80000
    temp(i) = getTemperature(i);
end
plot(temp, alt / 1000)
xlabel("Temperature (K)")
ylabel("Altitude (m)");
title("Temperature")

subplot(1, 3, 2)
density = zeros(1, 80000);
for i = 1:1:80000
    density(i) = getAirDensity(i);
end
plot(density, alt / 1000)
xlabel("Density (kg/m^3)")
ylabel("Altitude (m)");
title("Density")

subplot(1, 3, 3)
pressure = zeros(1, 80000);
for i = 1:1:80000
    pressure(i) = getPressure(i);
end
plot(pressure / 1000, alt / 1000)
xlabel("Pressure (kPa)")
ylabel("Altitude (m)");
title("Pressure")





%% Functions

% We want to use the geopotential altitude instead of the normal altitude
% because it works a bit better with our density and pressure calculations
function geoAlt = getGeopotentialAlt(alt)
 
    earthRadius = 20902211; % feet
    geoAlt = (alt * earthRadius)/(alt + earthRadius);
    

end
% Same but for metric so alt is in meters
function geoAlt = getMetricGeopotentialAlt(alt)
 
    earthRadius = 6369000; % meters
    geoAlt = (alt * earthRadius)/(alt + earthRadius);
    
end


% A function to get the temperature at any point 
% This takes in meters
function temp = getTemperature(alt)

    alt = getMetricGeopotentialAlt(alt);

    if alt < 11000
        temp = 288.15 - 6.5 / 1000 * alt;
    elseif alt < 20000
        temp = 216.65;
    elseif alt < 32000
        temp = 216.65 + 1 / 1000 * (alt - getMetricGeopotentialAlt(20000));
    elseif alt < 47000
        temp = 228.65 + 2.8 / 1000 * (alt - getMetricGeopotentialAlt(32000));
    elseif alt < 51000
        temp = 270.65;
    elseif alt < 71000
        temp = 270.65 - 2.8 / 1000 * (alt - getMetricGeopotentialAlt(51000));
    elseif alt < 84850
        temp = 214.65 - 2 / 1000 * (alt - getMetricGeopotentialAlt(71000));
    else 
        temp = 186.95;
    end


end

% A function to get the atmopheric density at a certain altitude in meters 
function den = getAirDensity(alt) 

    % We need the pressure at this altitude and temperature, so 
    pressure = getPressure(alt); % Pa
    temp = getTemperature(alt); % K

    % The specific gas constant for dry air
    gasConstant = 8.31446261815324 / 0.0289652; % J/(K kg)

    den = (pressure)/(gasConstant * temp);
    

end

% A function to get the pressure at a certain altitude in METERS
function pressure = getPressure(alt)

    alt = getMetricGeopotentialAlt(alt);

    standardSeaLevelPressure = 101325; % Pa
    seaLevelStandardTemp = 288.15; % K
    g = 9.80665; % m/ss
    molarMassOfDryAir = 0.02896968; % kg/mol
    gasConstant = 8.314462618; % J/(molK)
    
    % This gets close, but is aparently only in the troposphere, so I have
    % to change it
    pressure = standardSeaLevelPressure*exp(-(g*alt*molarMassOfDryAir)/(seaLevelStandardTemp*gasConstant)); 

    


end

% A function to get the burst height
function altitude = getBurstAltitude(burstDiameter, k, basePressure) 

    % We can find the volume because of math (check the paper)
    % volume = k*temperature/pressure

    % I am going to incremement the altitude until we hit the altitude
    % where it will pop
    % Thie is horribly inefficient, so if it takes too long then I might
    % have to optimize
    altitude = 0;

    while (2 * power((3 * k * getTemperature(altitude))/(4 * getPressure(altitude, basePressure)), 1/3) < burstDiameter)

        altitude = altitude + 100;

    end

    altitude = altitude - 100;

    % Now that it has hit I will be doing it again but with a smaller step
    while (2 * power((3 * k * getTemperature(altitude))/(4 * getPressure(altitude, basePressure)), 1/3) < burstDiameter)

        altitude = altitude + 1;

    end

    % And finally even smaller (tho I probably don't need to)
    altitude = altitude - 1;
    while (2 * power((3 * k * getTemperature(altitude))/(4 * getPressure(altitude, basePressure )), 1/3) < burstDiameter)

        altitude = altitude + 0.1;

    end
end