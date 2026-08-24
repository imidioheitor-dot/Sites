# Burma Superstar — Menu Sync

A delivery-menu control room for Burma Superstar (San Francisco). One screen that
shows every dish across every US delivery platform the restaurant is listed on, so
a mismatch is visible before a customer finds it.

**Deliverable:** `index.html` — one self-contained file (no build step, no framework).

## What it does

The restaurant's own website is treated as the **source of truth**. Every other
platform is compared against it and each listing is graded:

| State | Meaning |
|---|---|
| **In sync** | price, photo and copy all match the source of truth |
| **Drifted** | listed, but the price is more than 30% over base, or the photo/description is stale |
| **Broken** | not listed at all, sold out, or priced *below* the restaurant's own price |

Platforms covered — the four majors are highlighted, the rest are still tracked:

**Direct site** (truth) · **DoorDash** · **Uber Eats** · **Grubhub** · **Caviar** ·
Seamless · Postmates · ChowNow · Toast · Yelp

## Using it

- **Filter** by category, or press **Issues only** to see just what needs attention.
- **Export CSV / JSON** downloads the current table.
- **Import & export** panel: paste a CSV or JSON export and press **Load into table**
  to replace the seed data with the real menu. Edits persist in the browser via
  `localStorage`; nothing is uploaded anywhere. **Reset to seed data** undoes it.

CSV columns:

```
id,name,category,burmese,description,direct,doordash,ubereats,grubhub,caviar,seamless,postmates,chownow,toast,yelp
```

Each platform cell accepts:

| Value | Meaning |
|---|---|
| `21.50` | listed at that price |
| *(empty)* | not listed on that platform |
| `SOLD OUT` | listed but currently unavailable |
| `21.50 -photo` | listed, but no image |
| `21.50 -copy` | listed, but the description is out of date |

## Assets

`index.html` loads its media from a CDN by default so it works the moment you open
it. To make the folder fully self-contained:

```bash
./fetch-assets.sh
```

That downloads the video and stills into `assets/`, compresses them if `ffmpeg` /
ImageMagick are available, and flips `ASSET_LOCAL` in `index.html` to `true`.

## Interaction

Built for the cursor and for phones:

- **Hero** — scroll-driven 15s video of the tea leaf salad turning in 3D, no text baked in.
- **TextPressure** — the `MENU SYNC` headline bends its variable-font weight, width
  and slant toward the cursor.
- **Portal** — a scroll-driven aperture that opens through the dish and swallows the screen.
- **3D product** — the signature dish as a layered volume you can drag to rotate; it
  swings on its own when idle.
- **Object reveal on hover** — hovering a menu row floats its photo under the cursor.
- **Cursor** — a warm spice-ember trail follows the pointer, with a magnetic dot that
  grows over anything interactive.
- **Bento** — spotlight, border glow, 3D tilt, magnetism, particles and a click ripple.

All pointer effects are disabled on touch devices and under
`prefers-reduced-motion`, where the video is replaced by a still.

## A note on the data

The dish names are Burma Superstar's real menu. **The prices are estimates** — the
restaurant's own site and the delivery platforms are blocked by this environment's
network policy, so they could not be read directly. Replace them via the CSV/JSON
import; the structure is already correct.
