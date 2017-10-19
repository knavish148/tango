
--[[
 function which takes plane's IDassigns it a random parking slot [1-99]
 if it doesn't have one
]]

-- get program arguments: plane id and parking slot id (if it exists)
local planeId = ARGV[1]
local parkingSlotId = ARGV[2]

planeId = tonumber(planeId)
parkingSlotId = tonumber(parkingSlotId)

--[[
if conversion to num fails, it means that plane doesn't have a valid
parking slot id and needs it assigned
]]
if parkingSlotId == nil then
  parkingSlotId = 0
end

-- prepare ground before generating random number
local t = redis.call('TIME')
local tnum = tonumber(t[1]) + tonumber(t[2])
math.randomseed(tnum)

-- assign slot id only if plane doesn't have one already
if (parkingSlotId < 1) or (parkingSlotId > 99) then
  return math.random(1, 99)
end
