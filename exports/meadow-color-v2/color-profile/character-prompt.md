# character color direction

Reference coverage: 2 assets (limited).

Keep the requested character's base hue and material identities. Match the reference lightness contrast and chroma, with discrete pixel-art shade steps.
Use the job's approved palette, matching swatch and pose reference as generation inputs.

- OKLCH lightness targets: p10 0.295, p50 0.525, p90 0.567.
- OKLCH chroma targets: p10 0.039, p50 0.073, p90 0.080.
- Typical visible-pixel lightness span (P90–P10): 0.273.
- About 4 shades in a comparable material ramp, with a shadow-to-highlight OKLCH L span near 0.275.
- Observed shadow hue offset from the base: +3° in OKLCH. Use as a tentative cue on similar materials.
- hood_wizard / robe shade example: #303251 → #40466F → #4D507C → #585D8A. Use the contrast as a guide.
- meadow_slime / gel shade example: #2C5843 → #407B5F → #5D9D76 → #91D3A1. Use the contrast as a guide.
