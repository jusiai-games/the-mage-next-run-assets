# character color direction

Reference coverage: 2 assets (limited).

Keep the requested character's base hue and material identities. Match the reference lightness contrast and chroma, with discrete pixel-art shade steps.
Use the job's approved palette, matching swatch and pose reference as generation inputs.

- OKLCH lightness targets: p10 0.282, p50 0.528, p90 0.571.
- OKLCH chroma targets: p10 0.043, p50 0.076, p90 0.079.
- Typical visible-pixel lightness span (P90–P10): 0.289.
- About 4 shades in a comparable material ramp, with a shadow-to-highlight OKLCH L span near 0.275.
- Observed shadow hue offset from the base: +3° in OKLCH. Use as a tentative cue on similar materials.
- hood_wizard / robe shade example: #28283F → #393B5B → #454568 → #505276. Use the contrast as a guide.
- meadow_slime / gel shade example: #48643C → #638752 → #86A866 → #BEDD90. Use the contrast as a guide.
