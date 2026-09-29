exports.getRoutes = async (req, res) => {
  const routes = [
    {
      id: "route-rtu-kipsala",
      name: "Riga Technical University (RTU)",
      destinationName: "Ķīpsala Campus, Rīga",
      distanceKm: 2.4,
      estimatedMinutes: 28,
      waypointsCount: 8,
      waypoints: [
        { sequence: 1, instruction: "Walk towards Vanšu tilts", distanceMeters: 320, maneuver: "head_straight", icon: "arrow.up" },
        { sequence: 2, instruction: "Cross Vanšu tilts (bridge)", distanceMeters: 730, maneuver: "cross_bridge", icon: "arrow.turn.up.left" },
        { sequence: 3, instruction: "Turn left towards Ķīpsala", distanceMeters: 610, maneuver: "turn_left", icon: "arrow.turn.up.left" },
        { sequence: 4, instruction: "Continue to RTU main entrance", distanceMeters: 450, maneuver: "head_straight", icon: "arrow.up" }
      ]
    },
    {
      id: "route-central-station",
      name: "Rīga Central Station",
      destinationName: "Stacijas laukums, Rīga",
      distanceKm: 1.8,
      estimatedMinutes: 22,
      waypointsCount: 6
    }
  ];

  return res.json({
    status: "success",
    data: routes
  });
};

exports.planRoute = async (req, res) => {
  const { destination } = req.body || {};
  return res.json({
    status: "success",
    data: {
      destination: destination || "Riga Technical University (RTU)",
      distanceKm: 2.4,
      estimatedMinutes: 28,
      waypoints: [
        { sequence: 1, instruction: "Walk towards Vanšu tilts", distanceMeters: 320, maneuver: "head_straight", icon: "arrow.up" },
        { sequence: 2, instruction: "Cross Vanšu tilts (bridge)", distanceMeters: 730, maneuver: "cross_bridge", icon: "arrow.turn.up.left" },
        { sequence: 3, instruction: "Turn left towards Ķīpsala", distanceMeters: 610, maneuver: "turn_left", icon: "arrow.turn.up.left" },
        { sequence: 4, instruction: "Continue to RTU main entrance", distanceMeters: 450, maneuver: "head_straight", icon: "arrow.up" }
      ]
    }
  });
};
