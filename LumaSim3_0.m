
% Idk if I actually need this, tho I mnight
% balloonVolume = 2.5; %2.2-2.8% m^3


% We have to recalculate the volume each time we do a time step using the
% ideal gas law PV = nRT and some magic 
% (explanation at https://northstar-www.dartmouth.edu/~klynch/pmwiki-gc/uploads/BalloonCalulations.pdf)

% Sample inputs (also I'm absolutely dying because everything is in imperial)
balloonDiameter = 7.4; % Feet
balloonVolume = 212; % Cubic Feet
nozzleLift = 11.02; % Pounds
peakAltitude = 94;% KILO FEET WHAT WHY
ascentSpeed = 1010; % Feet per Minute
timeToBurst = 1.5 ; % Hours
freeLift = 4.02; % Pounds
basePressure = 14.7; % Pounds per square Inch

% I think technically this is all you need because you can put it into an
% online calculator
burstDiameter = 28.3; % feet

simulationTime = 3; % Hours

% Constants
densityOfHelium = 0.01024; % Pounds per Cubic 
deltaTime = 1; % s
timeSteps = simulationTime * 3600 / deltaTime;
coefficientOfDrag = 0.47; % Just a sphere
k = 0.73; % We are in feet so it's weird
burstAltitude = getBurstAltitude(burstDiameter, k, basePressure);

% Working Variables
workingAltitude = 0; % The altitude will be in feet
altitudeVector = 0:0;
altitudeVector(1) = workingAltitude; % Saving the intial altitiude
hasBurst = false;


size(timeVector)

%% Main loop
for i = 1:timeSteps

    % Finding Velocity
    underRadical = (4 * balloonDiameter * (densityOfHelium - getAirDensity(workingAltitude, basePressure)) * -9.81) / (3 * coefficientOfDrag * getAirDensity(workingAltitude, basePressure));

    % Checking to see if the balloon burst
    % We are using a burst altitude calculator and then checking the
    % altitude
    

    % Going about it normally if the balloon hasn't burst yet
    if hasBurst == false

        % Making sure that the balloon is going up 
        if underRadical < 0
            fprintf("Balloon is going down now, but never burst, after %d minutes", i * deltaTime / 60);
            break
        end
    
        % Finding the velocity
        workingVelocity = sqrt(underRadical);
    
        % Applying the velocity
        workingAltitude = workingAltitude + deltaTime * workingVelocity;
    
        % Saving the altitude
        altitudeVector(i) = workingAltitude;

    end

end

% Actually showing the thing
length = size(altitudeVector);
timeVector = (0:1:length(2) - 1) * deltaTime / 3600;
plot(timeVector, altitudeVector / 1000);
xlabel("Time (hours)")
ylabel("Altitude (kft)");
title("The Best LUMA Simulation Ever");



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
% A function to get the atmopheric density at a certain altitude in feet 
function den = getAirDensity(alt, basePressure) 
    metricAlt = getGeopotentialAlt(alt) * 0.3048;

    % We can find a ratio to use using the pressure ratio stuff
    if metricAlt < 11000
        ratio=basePressure*power((288.15/getTemperature(alt)),(34.163195/(-6.5/1000)));
    elseif metricAlt < 20000
        ratio=basePressure*exp(-34.163195*(metricAlt - 20000)/216.65);
    elseif metricAlt < 32000
        ratio=basePressure*power((216.65/getTemperature(alt)),(34.163195/(1/1000)));
    elseif metricAlt < 47000
        ratio=basePressure*power((228.65/getTemperature(alt)),(34.163195/(2.8/1000)));
    elseif metricAlt < 51000
        ratio=basePressure*exp(-34.163195*(metricAlt - 51000)/270.65);
    elseif metricAlt < 71000
        ratio=basePressure*power((270.65/getTemperature(alt)),(34.163195/(-2.8/1000)));
    elseif metricAlt < 84850
        ratio=basePressure*power((214.65/getTemperature(alt)),(34.163195/(-2/1000)));
    else 
        ratio=basePressure*exp(-34.163195*(metricAlt - 84850)/186.95);
    end

    % Then we just do this to adjust it for density
    % We can probably get better results if we save the starting
    % temperature and use that instead
    ratio = ratio / (getTemperature(alt)/getTemperature(0));

    % Another generalization we can adjust with better data
    startingDensity = 0.0765;

    den = startingDensity * ratio;

end

% A function to get the pressure at a certain altitude (in feet)
function pressure = getPressure(alt, basePressure)

    % Figuring out the metric stuff
    metricAlt = alt * 0.3048;

    % THE DELTAH MIGHT SHOULD BE IN GEOPORENTIAL ALTITUDE
    % If this doesn't work, check the units, weird things are happening
    % Everything should be in kelvin or meters (tho I think I got that)
    % There is also a chance that the base pressure should be the baseline
    % pressure for the altitude zone

    if metricAlt < 11000
        ratio=basePressure*power((288.15/getTemperature(alt)),(34.163195/(-6.5/1000)));
    elseif metricAlt < 20000
        ratio=basePressure*exp(-34.163195*(metricAlt - 20000)/216.65);
    elseif metricAlt < 32000
        ratio=basePressure*power((216.65/getTemperature(alt)),(34.163195/(1/1000)));
    elseif metricAlt < 47000
        ratio=basePressure*power((228.65/getTemperature(alt)),(34.163195/(2.8/1000)));
    elseif metricAlt < 51000
        ratio=basePressure*exp(-34.163195*(metricAlt - 51000)/270.65);
    elseif metricAlt < 71000
        ratio=basePressure*power((270.65/getTemperature(alt)),(34.163195/(-2.8/1000)));
    elseif metricAlt < 84850
        ratio=basePressure*power((214.65/getTemperature(alt)),(34.163195/(-2/1000)));
    else 
        ratio=basePressure*exp(-34.163195*(metricAlt - 84850)/186.95);
    end

    pressure = ratio*basePressure;

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