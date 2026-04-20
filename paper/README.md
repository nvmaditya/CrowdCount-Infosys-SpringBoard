# Paper Assets

This folder contains small utilities to generate reproducible paper-ready figures and CSV exports from the repository.

## Generate zone + log figures

```bash
python paper/generate_figures.py
```

Outputs:

- `paper/figures/zones_overlay.png`
- `paper/figures/system_architecture.svg`
- `paper/figures/frame_processing_flowchart.svg`
- `paper/data/zone_areas.csv`
- `paper/data/activity_logs_by_action.csv`
- `paper/data/activity_logs_timeseries_hour.csv`
- `paper/data/alerts_history.csv`

If `matplotlib` is installed, the script will also write PNG charts into `paper/figures/`.
