"""SQL and constants for the tourism itinerary app. All user values are bound with qmark (?) params."""

# Interest label -> Overture basic_category values (fixed allowlist).
INTERESTS = {
    "Food": ["restaurant", "casual_eatery", "food_truck_stand", "market"],
    "Coffee & cafes": ["cafe", "coffee_shop"],
    "Nightlife": ["bar", "brewery", "music_venue", "winery"],
    "Culture & history": ["museum", "art_gallery", "historic_site", "monument", "cultural_center", "theatre_venue"],
    "Outdoors": ["park", "beach", "garden", "nature_reserve", "scenic_viewpoint"],
    "Shopping": ["shopping_mall", "second_hand_store", "fashion_and_apparel_store"],
    "Family fun": ["zoo", "aquarium", "amusement_park", "arts_and_entertainment"],
}

# Curated city centers (Overture locality strings are too noisy to geocode reliably).
PRESET_CITIES = {
    "Sydney": (-33.8688, 151.2093),
    "London": (51.5080, -0.1281),
    "Paris": (48.8566, 2.3522),
    "New York City": (40.7580, -73.9855),
    "Tokyo": (35.6762, 139.6503),
    "Berlin": (52.5200, 13.4050),
    "Lisbon": (38.7223, -9.1393),
    "Barcelona": (41.3874, 2.1686),
    "Bangkok": (13.7563, 100.5018),
    "Singapore": (1.2903, 103.8519),
    "Austin": (30.2672, -97.7431),
    "Chicago": (41.8781, -87.6298),
    "Los Angeles": (34.0522, -118.2437),
    "Miami": (25.7617, -80.1918),
    "Sheffield": (53.3811, -1.4701),
    "Varanasi": (25.3176, 82.9739),
    "Taipei": (25.0330, 121.5654),
}

SOCIAL_CITIES_SQL = """
SELECT city, AVG(lat) lat, AVG(lon) lon, COUNT(DISTINCT overture_id) places
FROM TOURISM_APP.CORE.SOCIAL_PLACES_GEOCODED
GROUP BY city ORDER BY places DESC
"""

# Params: lon, lat, radius_m, categories_json
CANDIDATES_SQL = """
WITH params AS (
  SELECT ?::float lon, ?::float lat, ?::float radius_m, PARSE_JSON(?) cats
),
cand AS (
  SELECT p.id, p.names:primary::string name, p.basic_category category,
         ST_Y(p.geometry) lat, ST_X(p.geometry) lon,
         p.addresses[0]:freeform::string address, p.websites[0]::string website, p.confidence,
         ST_DISTANCE(p.geometry, ST_MAKEPOINT(x.lon, x.lat)) / 1000 km,
         ARRAY_SIZE(COALESCE(p.sources, ARRAY_CONSTRUCT())) n_sources,
         IFF(p.socials IS NOT NULL AND ARRAY_SIZE(p.socials) > 0, 1, 0) has_socials,
         s.num_posts, s.total_likes, s.total_comments, s.sentiment_score, s.buzz,
         ARRAY_TO_STRING(s.platforms, ', ') platforms, s.vibe, s.sample_post_url
  FROM OVERTURE_MAPS_PLACES.CARTO.PLACE p
  CROSS JOIN params x
  LEFT JOIN TOURISM_APP.CORE.PLACE_SOCIAL_SCORES s ON s.overture_id = p.id
  WHERE ST_DWITHIN(p.geometry, ST_MAKEPOINT(x.lon, x.lat), x.radius_m)
    AND (s.overture_id IS NOT NULL
         OR (ARRAY_CONTAINS(p.basic_category::variant, x.cats)
             AND p.confidence > 0.85
             AND COALESCE(p.operating_status, 'open') = 'open'))
),
scored AS (
  SELECT *,
    confidence + 0.4 * has_socials + 0.15 * LEAST(n_sources, 4) + IFF(website IS NOT NULL, 0.2, 0)
    + COALESCE(0.6 * buzz + sentiment_score + 2, 0) - 0.15 * km AS score
  FROM cand
)
SELECT name, category, ROUND(km, 2) km, address, website, lat, lon,
       num_posts, total_likes, total_comments, ROUND(sentiment_score, 2) sentiment_score,
       platforms, vibe, sample_post_url, ROUND(score, 2) score
FROM scored
WHERE name IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY category ORDER BY score DESC) <= 6
ORDER BY score DESC
LIMIT 40
"""

# Params: model, prompt
ITINERARY_SQL = """
SELECT AI_COMPLETE(
  model => ?,
  prompt => ?,
  response_format => TYPE OBJECT(
    title STRING,
    summary STRING,
    stops ARRAY(OBJECT(day NUMBER, start_time STRING, name STRING, duration_min NUMBER, why STRING, tip STRING))
  )
) AS itinerary
"""
