# Dashboards

Once Metabase is connected to your database, you can build dashboards to visualize your baseball statistics. Below are some suggested dashboards and the queries behind them.

## Team Overview Dashboard

A high-level view of team performance.

### Win/Loss Record

- **Type:** Number
- **Table:** `team_stats`
- **Display:** Show `wins` and `losses` as a formatted record

### Runs Scored vs. Runs Allowed

- **Type:** Bar chart
- **Table:** `team_stats`
- **Columns:** `team_runs_scored`, `team_runs_allowed`
- **Group by:** `team_name`

### Division Ranking

- **Type:** Number
- **Table:** `team_stats`
- **Column:** `division_rank`
- **Filter:** Current season year

## Player Leaderboards

### Home Run Leaders

- **Type:** Row chart or table
- **Table:** `players`
- **Sort by:** `home_runs` descending
- **Limit:** Top 10

### Batting Average Leaders

- **Type:** Table
- **Table:** `players`
- **Sort by:** `batting_average` descending
- **Filter:** Minimum at-bats (if tracked)

### RBI Leaders

- **Type:** Row chart
- **Table:** `season_stats` joined with `players`
- **Sort by:** `runs_batted_in` descending

## Game Results

### Recent Games Timeline

- **Type:** Table
- **Table:** `games`
- **Sort by:** `date` descending
- **Columns:** `date`, `away_team`, `away_team_score`, `home_team`, `home_team_score`

### Home vs. Away Performance

- **Type:** Pie chart or bar chart
- **Query:** Count wins when team is `home_team` vs. `away_team`

## Pitching Dashboard

### Team ERA Comparison

- **Type:** Bar chart
- **Table:** `team_stats`
- **Column:** `team_era`
- **Group by:** `team_name`

### Strikeouts and WHIP

- **Type:** Combo chart
- **Table:** `team_stats`
- **Columns:** `team_strikeouts`, `team_whip`

## Creating Custom Dashboards

1. In Metabase, click **New** > **Dashboard**.
2. Click **+** to add questions (visualizations).
3. Use the **Simple question** builder to select tables and columns.
4. For advanced queries, switch to **Native query** and write SQL directly:

```sql
SELECT p.name, p.position, s.batting_average, s.home_runs, s.runs_batted_in
FROM players p
JOIN season_stats s ON p.id = s.player_id
WHERE s.year = 2025
ORDER BY s.home_runs DESC;
```

5. Save and arrange cards on your dashboard.
