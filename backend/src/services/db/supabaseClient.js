const env = require("../../config/env");

/**
 * Lightweight, dependency-free Supabase REST Client
 * Interacts with Supabase PostgREST API using standard fetch
 * Keeps keys strictly on backend and never exposed to client/iOS
 */
class SupabaseClient {
  constructor() {
    this.key = env.supabaseKey;
    this.url = env.supabaseUrl;
    this.isConfigured = !!(this.key && this.url && !this.url.includes("your-project-id"));
  }

  /**
   * Helper to make authenticated requests to Supabase PostgREST
   */
  async request(endpoint, options = {}) {
    if (!this.isConfigured) {
      console.log(`[Supabase Mock] ${options.method || "GET"} ${endpoint} (Local mode - Supabase not fully connected)`);
      return { success: true, local: true };
    }

    const headers = {
      "apikey": this.key,
      "Authorization": `Bearer ${this.key}`,
      "Content-Type": "application/json",
      ...(options.headers || {})
    };

    const targetUrl = `${this.url.replace(/\/$/, "")}/rest/v1/${endpoint.replace(/^\//, "")}`;
    const response = await fetch(targetUrl, {
      ...options,
      headers
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Supabase API error (${response.status}): ${errText}`);
    }

    return await response.json();
  }

  /**
   * Logs an obstacle detection event to Supabase obstacle_events table
   */
  async recordObstacleEvent(eventData) {
    return this.request("obstacle_events", {
      method: "POST",
      body: JSON.stringify({
        obstacle_type: eventData.obstacle_type,
        lane: eventData.lane || "center",
        height_zone: eventData.height_zone || "torso",
        distance_meters: eventData.distance_meters,
        confidence: eventData.confidence || 0.95,
        severity: eventData.severity || "warning",
        action_taken: eventData.action_taken || "none",
        detected_at: eventData.detected_at || new Date().toISOString()
      })
    });
  }

  /**
   * Logs an environment query to Supabase environment_queries table
   */
  async recordEnvironmentQuery(queryData) {
    return this.request("environment_queries", {
      method: "POST",
      body: JSON.stringify({
        query_type: queryData.query_type,
        query_text: queryData.query_text,
        response_text: queryData.response_text,
        processing_mode: "cloud",
        created_at: new Date().toISOString()
      })
    });
  }
}

module.exports = new SupabaseClient();
