# Image References for PowerPoint Presentation

**Created:** January 4, 2026  
**Purpose:** Guide for inserting thesis figures into PowerPoint slides

---

## IMAGE FILE LOCATIONS

All images are located in: `/Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo/docs/thesis/figures/`

### Available PNG Files (Ready to Insert):

1. **cultural_authenticity_comparison.png** (141 KB)
   - Bar/box chart showing cultural authenticity scores
   - Shows Raw GPT-4 (0.568), Traditional RAG (0.584), OG-RAG (0.627)

2. **translation_fidelity_comparison.png** (130 KB)
   - Bar/box chart showing translation fidelity scores
   - Shows improvement from 0.308 → 0.369

3. **overall_quality_comparison.png** (128 KB)
   - Bar/box chart showing composite quality metric
   - Shows improvement from 0.335 → 0.380

4. **score_distributions.png** (116 KB)
   - Box plots showing distributions across all 3 metrics
   - Demonstrates tighter IQR for OG-RAG (consistency)

5. **og_rag_improvements.png** (130 KB)
   - Summary bar chart showing percentage improvements
   - Three bars: 10.5%, 19.8%, 13.5%

### TikZ Diagrams (Need Manual Recreation or Screenshot):

6. **system-architecture.tex** → Need to convert to image
   - 5-layer architecture diagram (Knowledge Graph → Evaluation)
   - Color-coded layers with feedback loop
   - **Alternative:** Screenshot from compiled thesis PDF (page with Figure 4.1)

7. **methodology-flowchart.tex** → Need to convert to image
   - CRISP-DM 6-phase workflow
   - Shows iteration loops
   - **Alternative:** Screenshot from compiled thesis PDF (page with Figure 3.1)

---

## SLIDE-BY-SLIDE IMAGE INSERTION GUIDE

### SLIDE 8: OG-RAG System Architecture

**Image to Insert:** `system-architecture.png` (or screenshot from thesis)
- **Location in Thesis:** Figure 4.1 (Chapter 4: Design & Implementation)
- **Size Recommendation:** Full width of slide
- **Placement:** Above the layer descriptions
- **Caption:** "Five-layer OG-RAG architecture with feedback loop"

**If rendering TikZ not possible:**
1. Open `docs/thesis/thiLLMo_Thesis_Revised_Dec2025.pdf`
2. Navigate to Chapter 4, Figure 4.1
3. Take screenshot of system architecture diagram
4. Crop and save as `system-architecture.png`
5. Insert into slide

---

### SLIDE 10: CRISP-DM Research Methodology

**Image to Insert:** `methodology-flowchart.png` (or screenshot from thesis)
- **Location in Thesis:** Figure 3.1 (Chapter 3: Methodology)
- **Size Recommendation:** Full width of slide
- **Placement:** Above the 6-phase description
- **Caption:** "CRISP-DM framework adapted for cultural AI with iteration loops"

**If rendering TikZ not possible:**
1. Open `docs/thesis/thiLLMo_Thesis_Revised_Dec2025.pdf`
2. Navigate to Chapter 3, Figure 3.1
3. Take screenshot of methodology flowchart
4. Crop and save as `methodology-flowchart.png`
5. Insert into slide

---

### SLIDE 13: Quantitative Results - Cultural Fidelity

**Image to Insert:** `cultural_authenticity_comparison.png` ✅ **READY**
- **Full Path:** `docs/thesis/figures/cultural_authenticity_comparison.png`
- **Size Recommendation:** Half-width (left side) or full-width above table
- **Placement:** Above or beside the statistical table
- **Caption:** "Cultural Authenticity comparison across three translation systems (n=100)"

**PowerPoint Steps:**
1. Insert → Pictures → Browse
2. Navigate to `docs/thesis/figures/`
3. Select `cultural_authenticity_comparison.png`
4. Resize to ~50-60% slide width
5. Position top-center or left-aligned

---

### SLIDE 16: Interpreting Low Absolute Scores

**Image to Insert:** `score_distributions.png` ✅ **READY**
- **Full Path:** `docs/thesis/figures/score_distributions.png`
- **Size Recommendation:** Full width of slide
- **Placement:** Top of slide, above score range table
- **Caption:** "Score distributions across all three metrics and translation systems"

**PowerPoint Steps:**
1. Insert → Pictures
2. Select `score_distributions.png`
3. Resize to 80-90% slide width
4. Position at top, centered
5. Move table below the figure

**Key Point to Emphasize:**
Point to the box plots during presentation and say: "Notice OG-RAG has tighter boxes (smaller IQR) - that's more consistent performance"

---

### SLIDE 17: Core Research Contributions

**Image to Insert:** `og_rag_improvements.png` ✅ **READY**
- **Full Path:** `docs/thesis/figures/og_rag_improvements.png`
- **Size Recommendation:** Half-width (right side) or centered above text
- **Placement:** Right side or top-center
- **Caption:** "OG-RAG Performance Improvements Over Raw GPT-4 Baseline"

**PowerPoint Steps:**
1. Insert → Pictures
2. Select `og_rag_improvements.png`
3. Resize to ~40-50% slide width
4. Position on right side of slide
5. List contributions on left side

**Presentation Tip:**
Gesture to the three bars (10.5%, 19.8%, 13.5%) when stating "Empirical Evidence" contribution

---

## POWERPOINT FORMATTING RECOMMENDATIONS

### Image Quality Settings:
- **Resolution:** Keep at original (already 300 DPI from thesis)
- **Compression:** Minimal (High Quality 330 PPI in PowerPoint)
- **Format:** Keep as PNG (supports transparency)

### Sizing Guidelines:
- **Full-width figures:** 10-11 inches wide
- **Half-width figures:** 5-6 inches wide
- **Maintain aspect ratio:** Always lock aspect ratio when resizing

### Positioning:
- **Alignment:** Use PowerPoint's alignment guides
- **White space:** Leave 0.5-inch margins on all sides
- **Text wrapping:** Avoid overlapping text on images

### Captions:
- **Font:** Same as slide body text (typically 18-20pt)
- **Style:** Italic for figure captions
- **Format:** "Figure: [Description]" or "Reference: Thesis Figure X.X"

---

## ALTERNATIVE: SCREENSHOT EXTRACTION METHOD

If you cannot render TikZ diagrams to PNG, use this method:

### Steps:
1. Open `docs/thesis/thiLLMo_Thesis_Revised_Dec2025.pdf` in Preview/Acrobat
2. Navigate to the page with the desired figure:
   - Figure 3.1 (Methodology) → Chapter 3
   - Figure 4.1 (Architecture) → Chapter 4
3. Use macOS Screenshot tool:
   - Press `Cmd + Shift + 4`
   - Drag to select the figure area
   - Screenshot saved to Desktop
4. Crop and clean:
   - Open in Preview
   - Crop to remove extra white space
   - Save as PNG with descriptive name
5. Move to `docs/thesis/figures/` folder
6. Insert into PowerPoint

### Screenshot Naming Convention:
- `system-architecture-screenshot.png`
- `methodology-flowchart-screenshot.png`

---

## COLOR SCHEME CONSISTENCY

### Ensure figures match presentation theme:

**System Architecture Colors:**
- 🟢 Green = Knowledge Graph layer
- 🔵 Cyan/Blue = Retrieval layer
- 🟡 Yellow = Context Builder
- 🟠 Orange = LLM Integration
- 🟣 Purple = Evaluation

**Result Charts:**
- OG-RAG typically in blue or green (highlighted)
- Raw GPT-4 in gray (baseline)
- Traditional RAG in orange (intermediate)

**Methodology Flowchart:**
- 🔵 Blue = CRISP-DM phases
- 🟢 Green = Activities
- 🟠 Orange = Deliverables
- 🔴 Red dashed = Iteration loops

---

## PRESENTATION SOFTWARE COMPATIBILITY

### PowerPoint (.pptx):
✅ PNG files work perfectly
✅ Supports transparency
✅ High-quality rendering

### Keynote (.key):
✅ PNG files compatible
✅ Drag-and-drop from Finder
✅ Maintains quality

### Google Slides:
✅ Upload PNG files
✅ Insert → Image → Upload from computer
⚠️ May compress on upload (check quality)

### Gamma.app:
✅ Upload to media library
✅ Reference via Markdown syntax
✅ Supports PNG embedding

---

## QUICK CHECKLIST

Before finalizing presentation:

- [ ] All 5 PNG charts copied to presentation folder
- [ ] System architecture figure obtained (TikZ render or screenshot)
- [ ] Methodology flowchart figure obtained (TikZ render or screenshot)
- [ ] Images inserted into correct slides
- [ ] Captions match thesis figure numbers
- [ ] Image quality verified (no pixelation)
- [ ] Aspect ratios maintained (not distorted)
- [ ] Color schemes consistent with thesis
- [ ] File sizes reasonable (<500 KB per image)
- [ ] Test presentation on projector
- [ ] Backup copy of all images saved

---

## TROUBLESHOOTING

### Issue: Image appears pixelated
**Solution:** Use original PNG from `docs/thesis/figures/` - already high resolution

### Issue: Colors look different on projector
**Solution:** Test with actual defense venue projector, adjust brightness if needed

### Issue: File size too large
**Solution:** Original PNGs are already optimized (116-141 KB), no compression needed

### Issue: TikZ diagrams not available as PNG
**Solution:** Use screenshot method from thesis PDF (detailed above)

---

## CONTACT & BACKUP

**Image Source Repository:** `/Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo/docs/thesis/figures/`

**Backup Location:** Save copies to:
- Desktop/Defense_Presentation_Backup/
- Cloud storage (Google Drive/Dropbox)
- USB drive for defense day

**Emergency Fallback:** If any image fails to load during defense, reference the thesis document:
"As shown in Figure X.X of the thesis document, the architecture demonstrates..."

---

**Last Updated:** January 4, 2026  
**Defense Date:** January 14, 2026  
**Status:** Images ready for insertion
