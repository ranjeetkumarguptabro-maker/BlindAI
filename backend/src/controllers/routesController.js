/**
 * Route Planner Controller for Blind AI
 * Module 2: Current Location and Route Planning
 */

const routingService = require("../services/routingService");
const { LOCATIONS } = require("../models/locations");

exports.getRoutes = async (req, res) => {
  const routes = LOCATIONS.map(loc => ({
    id: `route-${loc.id}`,
    name: loc.canonicalName,
    destinationName: loc.subtitle,
    distanceKm: loc.distanceKm,
    estimatedMinutes: loc.estimatedMinutes,
    waypointsCount: loc.waypoints ? loc.waypoints.length : 0,
    pedestrianCrossings: loc.pedestrianCrossings || [],
    publicTransportOptions: loc.transitOptions || [],
    waypoints: loc.waypoints || []
  }));

  return res.json({
    status: "success",
    data: routes
  });
};

exports.planRoute = async (req, res) => {
  try {
    const { origin, destination, originCoords, destinationCoords, preferences } = req.body || {};
    const routePlan = await routingService.calculateRoute({
      origin,
      destination,
      originCoords,
      destinationCoords,
      preferences
    });

    if (!routePlan.isDestinationClear) {
      return res.json({
        status: "clarification_needed",
        data: routePlan
      });
    }

    return res.json({
      status: "success",
      data: routePlan
    });
  } catch (err) {
    console.error("[RoutesController] Error planning route:", err);
    return res.status(500).json({
      status: "error",
      message: err.message
    });
  }
};
