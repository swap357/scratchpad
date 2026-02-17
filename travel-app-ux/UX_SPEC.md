# Voyager: UX Design Specification

## 1. Design Philosophy

Most travel apps optimize for **booking conversion**. This app optimizes for
**decision quality**. The core insight: travel planning is a multi-objective
optimization problem under uncertainty, and the UX should make that explicit
rather than burying it under pretty photos.

### Design Principles

1. **Tradeoffs are first-class citizens** -- never show an option without its cost
2. **Time is the scarce resource** -- every view anchors on hours, not dollars
3. **Comparison over curation** -- side-by-side beats "recommended for you"
4. **Progressive disclosure of complexity** -- simple by default, analytical on demand
5. **Simulate before you commit** -- preview the lived experience, not just the plan

---

## 2. Information Architecture

```
App
 |-- Trip Dashboard           (all trips, upcoming/past)
 |-- Trip Workspace           (single trip, the core experience)
 |    |-- Day Planner         (the main view -- map + timeline + tradeoff panel)
 |    |-- Pareto Explorer     (multi-day optimization across the trip)
 |    |-- Simulation Mode     (animated walkthrough of the planned itinerary)
 |    +-- Share/Export
 |-- Explore                  (inspiration, seeded by preferences)
 +-- Settings / Profile
```

---

## 3. Core View: The Day Planner (Split-Panel Layout)

This is where 80% of the interaction happens. Three synchronized panels:

```
+---------------------------------------------+---------------------------+
|                                              |                           |
|              MAP PANEL (60%)                 |   TIMELINE PANEL (25%)    |
|                                              |                           |
|   [Numbered pins on map]                     |   08:00  Hotel            |
|   [Colored route lines between pins]         |     |  15 min walk        |
|   [Heat zones for crowding/wait times]       |   08:30  Tsukiji Market   |
|   [Isochrone rings from current position]    |     |  ** 2.5h experience  |
|                                              |   11:00  --               |
|   [Drag pins to reorder]                     |     |  40 min train       |
|   [Click empty area to add candidate POI]    |   11:40  Senso-ji Temple  |
|                                              |     |  ** 1.5h experience  |
|                                              |   13:00  --               |
|                                              |     ...                   |
+---------------------------------------------+---------------------------+
|                                              |                           |
|         TRADEOFF PANEL (bottom, collapsible)                             |
|                                              |                           |
|  [Time budget bar]  Experience: 6.5h | Transit: 2.3h | Buffer: 1.2h     |
|  [Fatigue curve]    Energy ████████░░░░ declining after 14:00            |
|  [Opportunity cost]  "Dropping Meiji Shrine saves 1.5h, costs 4.7★"     |
|                                              |                           |
+--------------------------------------------------------------+-----------+
```

### 3.1 Map Panel

- **Numbered pins** corresponding to timeline entries, connected by colored
  polylines (walk=green, transit=blue, taxi=yellow, flight=red arc)
- **Drag-to-reorder** pins directly on the map; timeline auto-updates with
  new transit calculations
- **Isochrone overlay**: tap any pin to see "what else is reachable in 15/30/60
  min from here" as shaded rings -- this is how you discover nearby alternatives
- **Crowd heatmap toggle**: time-of-day-aware density overlay (sourced from
  Google Popular Times or similar) so you can avoid peak hours
- **Transit layer toggle**: show metro lines, bus routes, train stations
  contextually

### 3.2 Timeline Panel

A vertical **Gantt-style strip** for the day:

- **Experience blocks** (solid, colored by category: culture, food, nature,
  nightlife) with a star rating and duration
- **Transit blocks** (hatched/striped, gray) with mode icon and duration
- **Buffer/free blocks** (dotted outline) -- unallocated time you can fill
- **Drag edges** of blocks to adjust time allocation
- **Tap a block** to expand inline: see photos, hours, cost, notes, reviews
  summary
- **Pain indicators**: small icons on transit blocks (crowded, transfers,
  long walk) and experience blocks (queue, weather-sensitive)

The timeline and map are **bidirectionally linked**: selecting on one highlights
on the other. Reordering on either side propagates.

### 3.3 Tradeoff Panel (Bottom Drawer)

The analytical core. Collapsed by default to a single summary bar, expandable
to full analysis.

**Collapsed state -- the Time Budget Bar:**
```
[===EXPERIENCE 6.5h===|--TRANSIT 2.3h--|..BUFFER 1.2h..]  Total: 10h
```
Color-coded stacked bar. Immediately tells you: "Am I spending my day
experiencing or commuting?"

**Expanded state -- four sub-views:**

#### a) Time Allocation Donut
- Donut chart: experience / transit / meals / buffer
- Compare against your "ideal day" profile (set in preferences)
- Deviation highlighted in red/green

#### b) Gain vs. Pain Scatter
- Each POI plotted: X = time cost (transit + experience), Y = expected value
  (composite of rating, uniqueness, personal interest score)
- Items above the efficiency frontier are "obviously good"
- Items below are candidates for cutting
- Interactive: click a point to see its name, drag it off the chart to remove

#### c) Opportunity Cost Ticker
- For each item in your itinerary, show: "If you drop X, you could add Y or Z"
- Sorted by net value gain
- One-tap swap: replace the item directly

#### d) What-If Slider
- "What if I wake up 1 hour earlier / later?"
- "What if I skip lunch out and grab convenience store food?"
- Slide to see how the itinerary reshuffles and what becomes possible/impossible

---

## 4. Pareto Explorer (Multi-Objective Optimization View)

This is the power-user analytical view for optimizing across the full trip.

### 4.1 The Pareto Frontier Chart

```
    Value (composite score)
     ^
     |        * Plan A (culture-heavy)
     |      *   * Plan B (balanced)
     |    *
     |  *           * Plan C (food-focused)
     | *          *
     +----------------------------> Cost (time + money + fatigue)
```

- **Each dot is a complete itinerary variant** auto-generated by the optimizer
- **Pareto frontier** drawn as a curve connecting non-dominated solutions
- **Click any dot** to load that itinerary into the Day Planner for inspection
- **Filter axes**: toggle what "cost" and "value" mean:
  - Cost: total transit time, total spend, walking distance, fatigue score
  - Value: unique experiences, rating sum, cuisine variety, cultural depth

### 4.2 Dimension Controls

A row of **weighted sliders** at the top:

```
Culture:     [====|======]  60%
Food:        [========|==]  80%
Nature:      [==|========]  20%
Nightlife:   [=|=========]  10%
Budget:      [=====|=====]  50%  ($ constraint)
Pace:        [===|=======]  30%  (relaxed <-> packed)
```

Moving any slider **recomputes the Pareto frontier in real-time** and
re-ranks the candidate itineraries. The animation of dots shifting on the
chart makes the impact of each preference tangible.

### 4.3 Comparison Table

Below the chart, a **structured comparison table** for up to 4 pinned
itinerary variants:

```
                     | Plan A       | Plan B       | Plan C       |
---------------------------------------------------------------------
Unique experiences   |     8        |     6        |     5        |
Total transit time   |  3.2h        |  2.1h        |  1.8h        |
Walking distance     |  9.4 km      |  6.1 km      |  4.2 km      |
Meals                |  2 sit-down  |  3 sit-down  |  4 sit-down  |
Estimated cost       |  $145        |  $182        |  $210        |
Fatigue score        |  High        |  Medium      |  Low         |
Weather risk         |  2 outdoor   |  1 outdoor   |  0 outdoor   |
```

Cells are **color-coded** (green = best in column, red = worst) so you can
instantly see which plan dominates on which dimensions.

---

## 5. Simulation Mode

The "wow" feature. After planning, you experience the day before living it.

### 5.1 Animated Path Playback

- **Camera follows the route** on a 3D map (Mapbox GL / Google Earth-style)
- **Speed control**: 1x, 5x, 20x, or jump-to-next-stop
- **Mode transitions**: smooth animation changes between walking (street
  level), train (elevated tracking shot), flight (globe arc zoom-out/in)
- **Time-of-day lighting**: the map lighting shifts as simulated time
  progresses (morning golden hour, harsh midday, sunset, night)
- **POI preview cards**: as the camera arrives at each stop, a card slides
  in with: photo, name, why it's in the plan, scheduled duration, and what
  you'll see at that hour specifically (e.g., "Tsukiji outer market -- tuna
  auction ends at 9am, arrive by 8:30")

### 5.2 Street-Level Preview

At each stop, option to drop into:
- **Street View** of the entrance/area
- **Photo carousel** from recent visitors at the same time of day
- **"Vibe check"**: a 2-sentence AI-generated description of what it feels
  like at that hour ("Quiet morning, few tourists, vendors still setting up.
  Best for photography.")

### 5.3 Transit Simulation

For each transit segment:
- **Route rendered on map** with real transit lines
- **Info overlay**: departure time, platform, number of stops, transfers
- **Walking segments highlighted** with distance and terrain (stairs, hills)
- For flights: animated great-circle arc with duration overlay

### 5.4 Simulation Controls

```
[|<] [<<] [ > PLAY ] [>>] [>|]     Speed: [1x] [5x] [20x]

08:00 ====|========================= 22:00
          ^ current: 09:15 -- Tsukiji Market

[Toggle: Street View] [Toggle: Transit Detail] [Toggle: Time Lapse Photos]
```

---

## 6. Sharing & Export

### 6.1 Share as Animated Story

- **Auto-generate a 30-60 second animation** of the simulation path
- Rendered as a short video (MP4) or animated image sequence
- Overlay: day title, stop names, transit modes, timestamps
- Optimized aspect ratios for: Instagram Stories (9:16), Twitter/X (16:9),
  TikTok (9:16), square (1:1)
- **One-tap share** to platform with pre-filled caption:
  "Day 3 in Tokyo: 8 stops, 14km walked, zero regrets. Planned with Voyager."

### 6.2 Share as Interactive Link

- **Web viewer** (no login required) where recipients can:
  - Scrub through the timeline
  - Click pins on the map
  - See the itinerary details
  - Fork the trip into their own account
- Shareable URL with optional expiry and privacy controls

### 6.3 Export Formats

- **PDF itinerary**: clean printable schedule with map snapshots, addresses,
  transit directions, reservation confirmation numbers
- **Google Maps list**: export all POIs as a saved list in Google Maps
- **Calendar events**: .ics file or direct Google/Apple Calendar sync, with
  transit time blocked as travel events
- **Offline package**: downloadable bundle with cached maps, directions, and
  POI info for areas with poor connectivity

### 6.4 Collaborative Planning

- **Shared trip workspace**: invite travel companions by link
- **Voting on alternatives**: when the Pareto explorer surfaces options,
  companions can upvote/downvote preferences
- **Split view**: "Your picks vs. their picks" with Pareto frontier showing
  compromise solutions
- **Activity log**: who added/removed what, with optional notifications

---

## 7. Interaction Patterns

### 7.1 Adding a POI to the Day

1. **Search / browse** in a side panel or tap the map
2. POI appears as a **candidate pin** (ghost/dashed outline) on the map
3. The tradeoff panel immediately shows: "Adding X costs Y transit time,
   pushes Z to later, reduces buffer by W"
4. **Confirm** to lock it into the itinerary, or **dismiss**
5. System auto-suggests optimal insertion point (minimizes added transit)

### 7.2 Removing / Swapping a POI

1. Long-press or swipe on timeline block
2. **"Remove"** shows what opens up: "Frees 2.1h, enables: A, B, or C"
3. **"Swap"** shows alternatives ranked by value-for-time at that slot
4. One-tap to execute the swap

### 7.3 Reordering

- **Drag on timeline** or **drag pins on map**
- Real-time transit recalculation as you drag (debounced)
- If a new order creates a conflict (e.g., museum closed by then), the
  conflicting block turns red with an explanation tooltip

### 7.4 Undo / History

- **Full undo stack** with named checkpoints
- "Revert to version from 10 minutes ago" in a history sidebar
- Named snapshots: "Save this as 'ambitious plan'" to compare later

---

## 8. Data Model (Conceptual)

```
Trip
 +-- id, name, dates, destination, collaborators[]
 +-- days[]
      +-- Day
           +-- date, start_time, end_time
           +-- items[]
           |    +-- Item
           |         +-- poi_id, type (experience|meal|transit|buffer)
           |         +-- scheduled_start, scheduled_end
           |         +-- transit_to_next { mode, duration, distance, route }
           |         +-- scores { rating, uniqueness, personal_interest }
           |         +-- pain_factors { queue_time, crowd_level, walk_dist }
           +-- constraints { budget, pace_preference, must_include[], avoid[] }
           +-- generated_alternatives[]  (Pareto set)
```

---

## 9. Visual Design Direction

### Color System
- **Experience time**: deep teal (#0D7377)
- **Transit time**: warm gray (#9E9E9E)
- **Buffer/free time**: light dotted (#E0E0E0)
- **Pain indicators**: muted red (#C0392B at 60% opacity)
- **Gain indicators**: muted green (#27AE60 at 60% opacity)
- **Pareto frontier line**: gold (#F39C12)

### Typography
- **Primary**: Inter or DM Sans (clean, high legibility at small sizes for
  dense data views)
- **Monospace accent**: JetBrains Mono for time values and metrics

### Map Style
- **Custom Mapbox style**: muted base map (desaturated) so POI pins and route
  lines pop. No visual competition between the map and the data overlays.
- **3D buildings** enabled for simulation mode only

### Motion
- **Route drawing**: polylines animate along the path (like drawing a line)
- **Mode transitions**: smooth 1-2s camera moves between walking/transit/flight
- **Data transitions**: when changing sliders in Pareto explorer, dots animate
  to new positions (not jump-cut)

---

## 10. Key Screens Summary

| Screen | Purpose | Key Interaction |
|---|---|---|
| Day Planner | Plan a single day | Drag-reorder, add/remove POIs, inspect tradeoffs |
| Tradeoff Panel | Analyze time/value allocation | Time budget bar, gain-vs-pain scatter, what-if sliders |
| Pareto Explorer | Optimize across trip | Weighted sliders, frontier chart, compare table |
| Simulation | Preview the lived experience | Animated path playback, street-level previews |
| Share | Export and distribute | Animated story, interactive link, PDF, calendar sync |
| Collab | Plan with others | Voting, split preferences, compromise frontier |

---

## 11. Technical Considerations

- **Routing engine**: OSRM or Valhalla for walking/driving, GTFS feeds for
  transit, great-circle + airline schedule data for flights
- **Optimization backend**: multi-objective optimization (NSGA-II or similar)
  for generating Pareto-optimal itinerary sets; runs server-side, streams
  results to the client as they're found
- **Map rendering**: Mapbox GL JS (web) / MapLibre (cross-platform) for the
  custom-styled interactive map and 3D simulation
- **Offline support**: pre-cache map tiles, POI data, and transit schedules
  for downloaded trips
- **Real-time data**: crowd levels, transit delays, weather -- pulled on
  refresh and surfaced as alerts if they affect the plan
