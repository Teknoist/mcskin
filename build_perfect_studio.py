# -*- coding: utf-8 -*-
# Otomatik uretilen MC Skin 3D Studio & Palette Hub Pro Derleyici
import base64
import json
import sys
import palettes_data

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("skin.png", "rb") as f:
    skin_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open("capes_cache.js", "r", encoding="utf-8") as f:
    capes_js = f.read().strip()

palettes_json = json.dumps(palettes_data.PALETTES, ensure_ascii=False)

html_content = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minecraft Skin 3D Studio & Palette Hub Pro</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <style>
    :root {
      --bg: #090d16;
      --panel: #131d2e;
      --panel-hover: #1b283d;
      --border: #23354d;
      --border-focus: #3b82f6;
      --text: #f1f5f9;
      --muted: #94a3b8;
      --accent: #3b82f6;
      --accent-hover: #2563eb;
      --success: #10b981;
      --purple: #8b5cf6;
      --gold: #f59e0b;
      --danger: #ef4444;
      --input-bg: #0b121f;
      --card-shadow: 0 8px 24px rgba(0,0,0,0.35);
      --viewer-grad: radial-gradient(circle at center, #1b263b 0%, #0a0f1d 100%);
      --sub-panel: rgba(10, 15, 29, 0.65);
      --chip-bg: #0d1524;
      --chip-text: #94a3b8;
      --chip-hover: #1b283d;
      --chip-active-bg: rgba(59, 130, 246, 0.25);
      --chip-active-text: #ffffff;
      --badge-bg: rgba(15, 23, 42, 0.82);
      --badge-text: #94a3b8;
      --badge-border: rgba(255,255,255,0.08);
      --slider-track: #1e293b;
      --scroll-thumb: #23354d;
      --canvas-bg: repeating-conic-gradient(#1e293b 0% 25%, #0f172a 0% 50%) 50% / 8px 8px;
    }

    body.light-theme {
      --bg: #f8fafc;
      --panel: #ffffff;
      --panel-hover: #f8fafc;
      --border: #e2e8f0;
      --border-focus: #2563eb;
      --text: #0f172a;
      --muted: #475569;
      --accent: #2563eb;
      --accent-hover: #1d4ed8;
      --success: #059669;
      --purple: #7c3aed;
      --gold: #d97706;
      --danger: #dc2626;
      --input-bg: #ffffff;
      --card-shadow: 0 1px 3px rgba(15, 23, 42, 0.05), 0 6px 16px rgba(15, 23, 42, 0.03);
      --viewer-grad: radial-gradient(circle at center, #ffffff 0%, #f1f5f9 100%);
      --sub-panel: #f8fafc;
      --chip-bg: #ffffff;
      --chip-text: #1e293b;
      --chip-hover: #f1f5f9;
      --chip-active-bg: #2563eb;
      --chip-active-text: #ffffff;
      --badge-bg: rgba(255, 255, 255, 0.95);
      --badge-text: #334155;
      --badge-border: #e2e8f0;
      --slider-track: #e2e8f0;
      --scroll-thumb: #cbd5e1;
      --canvas-bg: repeating-conic-gradient(#f1f5f9 0% 25%, #ffffff 0% 50%) 50% / 8px 8px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      height: 100vh;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.4;
      transition: background-color 0.25s cubic-bezier(0.16, 1, 0.3, 1), color 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* TOP HEADER */
    .top-header {
      height: 44px;
      max-width: 100%;
      padding: 0 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
      background: var(--panel);
      transition: background 0.25s, border-color 0.25s;
    }
    .brand-title {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .brand-title h1 {
      font-size: 0.96rem;
      font-weight: 700;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 6px;
      letter-spacing: -0.2px;
    }
    .version-tag {
      font-size: 0.65rem;
      font-weight: 600;
      background: rgba(59, 130, 246, 0.12);
      color: var(--accent);
      padding: 2px 7px;
      border-radius: 12px;
      border: 1px solid rgba(59, 130, 246, 0.25);
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .theme-toggle-btn {
      background: var(--chip-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 5px 11px;
      border-radius: 7px;
      font-size: 0.74rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .theme-toggle-btn:hover {
      border-color: var(--accent);
      background: var(--panel-hover);
      transform: translateY(-1px);
    }
    .theme-toggle-btn:active { transform: scale(0.96); }

    /* 3-COLUMN STUDIO LAYOUT */
    .studio-layout {
      display: grid;
      grid-template-columns: 350px 330px 1fr;
      gap: 10px;
      height: calc(100vh - 44px);
      max-width: 100%;
      padding: 8px 12px 8px 12px;
    }
    @media (max-width: 1200px) {
      .studio-layout { grid-template-columns: 320px 310px 1fr; gap: 8px; }
    }
    @media (max-width: 980px) {
      .studio-layout {
        grid-template-columns: 320px 300px 400px;
        overflow-x: auto;
      }
    }

    .studio-card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      height: 100%;
      overflow: hidden;
      box-shadow: var(--card-shadow);
      transition: background-color 0.25s, border-color 0.25s;
    }

    .inner-scroll {
      flex: 1;
      overflow-y: auto;
      padding-right: 3px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .inner-scroll::-webkit-scrollbar { width: 4px; }
    .inner-scroll::-webkit-scrollbar-thumb { background: var(--scroll-thumb); border-radius: 4px; }
    .inner-scroll::-webkit-scrollbar-thumb:hover { filter: brightness(1.2); }

    /* 3D VIEWER */
    #viewer3d {
      width: 100%;
      height: clamp(230px, 34vh, 290px);
      background: var(--viewer-grad);
      border: 1px solid var(--border);
      border-radius: 8px;
      position: relative;
      overflow: hidden;
      cursor: grab;
      transition: background 0.3s ease;
      flex-shrink: 0;
    }
    #viewer3d:active { cursor: grabbing; }
    .viewer-mode-badge {
      position: absolute;
      bottom: 8px; right: 8px;
      background: rgba(16, 185, 129, 0.15);
      color: var(--success);
      border: 1px solid rgba(16, 185, 129, 0.4);
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 0.65rem;
      font-weight: 600;
      pointer-events: none;
      backdrop-filter: blur(4px);
    }
    .viewer-badge {
      position: absolute;
      top: 6px; left: 6px;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      padding: 3px 7px;
      border-radius: 5px;
      font-size: 0.64rem;
      color: var(--badge-text);
      pointer-events: none;
      backdrop-filter: blur(6px);
    }

    /* 3D ALTINDAKİ İNDİR / YÜKLE BARI */
    .tex-preview-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--sub-panel);
      padding: 6px 8px;
      border-radius: 7px;
      border: 1px solid var(--border);
      margin-top: 6px;
      margin-bottom: 2px;
      flex-shrink: 0;
    }
    #skinCanvas {
      width: 44px; height: 44px;
      image-rendering: pixelated;
      background: var(--canvas-bg);
      border: 1px solid var(--border);
      border-radius: 5px;
      flex-shrink: 0;
    }
    .tex-actions {
      flex: 1;
      display: flex;
      gap: 6px;
    }
    .btn-download {
      flex: 1.4;
      background: var(--success);
      color: #ffffff;
      border: none;
      padding: 7px 10px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.76rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      transition: all 0.15s ease;
      box-shadow: 0 2px 6px rgba(16, 185, 129, 0.25);
    }
    .btn-download:hover { filter: brightness(1.1); transform: translateY(-1px); }
    .btn-download:active { transform: scale(0.97); }
    .btn-upload {
      flex: 1;
      background: var(--chip-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 7px 8px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.72rem;
      cursor: pointer;
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.15s ease;
    }
    .btn-upload:hover { border-color: var(--accent); background: var(--panel-hover); transform: translateY(-1px); }
    .btn-upload:active { transform: scale(0.97); }

    /* CHIP BUTTONS */
    .btn-group { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; }
    .btn-group-layers { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; }
    
    .chip-btn {
      background: var(--chip-bg);
      border: 1px solid var(--border);
      color: var(--chip-text);
      padding: 5px 4px;
      border-radius: 5px;
      font-size: 0.68rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.15s ease;
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
      user-select: none;
    }
    .chip-btn:hover { background: var(--chip-hover); color: var(--text); border-color: var(--border-focus); transform: translateY(-1px); }
    .chip-btn.active {
      background: var(--chip-active-bg);
      border-color: var(--accent);
      color: var(--chip-active-text);
      font-weight: 600;
    }
    .chip-btn.green.active {
      background: var(--success);
      border-color: var(--success);
      color: #ffffff;
    }
    .chip-btn:active { transform: scale(0.96); }

    /* SLIDERS */
    .slider-row { margin-bottom: 2px; }
    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.66rem;
      margin-bottom: 2px;
      color: var(--muted);
      font-weight: 500;
    }
    input[type="range"] {
      width: 100%;
      height: 4px;
      background: var(--slider-track);
      border-radius: 4px;
      accent-color: var(--accent);
      cursor: pointer;
      display: block;
    }

    /* CHECKBOXES (2x2 GRID) */
    .checks-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
      background: var(--sub-panel);
      padding: 6px 8px;
      border-radius: 6px;
      border: 1px solid var(--border);
    }
    .checks-grid label {
      display: flex;
      align-items: center;
      gap: 5px;
      cursor: pointer;
      color: var(--text);
      font-size: 0.70rem;
      font-weight: 500;
      user-select: none;
    }
    .checks-grid input[type="checkbox"] {
      accent-color: var(--accent);
      width: 13px; height: 13px;
      cursor: pointer;
    }

    /* COLOR GRID (2 COLUMNS) */
    .color-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
    }
    .color-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--sub-panel);
      padding: 4px 6px;
      border-radius: 5px;
      border: 1px solid var(--border);
    }
    .color-item label {
      font-size: 0.68rem;
      font-weight: 500;
      color: var(--text);
      white-space: nowrap;
    }
    .color-inputs { display: flex; align-items: center; gap: 4px; }
    input[type="color"] {
      -webkit-appearance: none;
      border: none;
      width: 22px; height: 22px;
      border-radius: 4px;
      cursor: pointer;
      background: none;
    }
    input[type="color"]::-webkit-color-swatch-wrapper { padding: 0; }
    input[type="color"]::-webkit-color-swatch { border: 1px solid var(--border); border-radius: 4px; }
    .hex-input {
      width: 60px;
      background: var(--input-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 3px 4px;
      border-radius: 4px;
      font-family: ui-monospace, SFMono-Regular, monospace;
      font-size: 0.68rem;
      text-transform: uppercase;
      text-align: center;
    }
    .hex-input:focus { border-color: var(--accent); outline: none; }

    /* HAIR ACCENT ITEM */
    .hair-item {
      background: var(--sub-panel);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 5px 6px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .hair-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .hair-top label {
      font-size: 0.68rem;
      font-weight: 600;
      color: var(--text);
    }
    .hair-presets { display: flex; gap: 4px; flex-wrap: wrap; }
    .hair-dot {
      width: 17px; height: 17px;
      border-radius: 50%;
      border: 1px solid var(--border);
      cursor: pointer;
      transition: transform 0.15s, border-color 0.15s;
    }
    .hair-dot:hover { transform: scale(1.22); border-color: var(--accent); }

    /* COLOR-PALETTE MCP SHADE SCALE INSPECTOR */
    .shade-box {
      background: var(--sub-panel);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 6px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .shade-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.68rem;
      font-weight: 600;
      color: var(--text);
    }
    .wcag-badge {
      font-size: 0.62rem;
      padding: 1px 5px;
      border-radius: 3px;
      font-weight: 600;
      background: rgba(16, 185, 129, 0.15);
      color: var(--success);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .shade-scale-strip {
      display: flex;
      height: 18px;
      border-radius: 4px;
      overflow: hidden;
      border: 1px solid var(--border);
    }
    .shade-step {
      flex: 1;
      position: relative;
      cursor: pointer;
      transition: transform 0.1s;
    }
    .shade-step:hover {
      transform: scaleY(1.25);
      z-index: 5;
    }
    .shade-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 6px;
    }
    .shade-legend {
      font-size: 0.60rem;
      color: var(--muted);
    }
    .btn-copy-css {
      background: var(--chip-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 3px 7px;
      border-radius: 4px;
      font-size: 0.64rem;
      font-weight: 600;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s;
      white-space: nowrap;
    }
    .btn-copy-css:hover { border-color: var(--accent); background: var(--panel-hover); transform: translateY(-1px); }
    .btn-copy-css:active { transform: scale(0.96); }

    /* RIGHT COLUMN: SEGMENTED TAB BAR */
    .lib-tab-bar {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
      background: var(--sub-panel);
      padding: 3px;
      border-radius: 7px;
      border: 1px solid var(--border);
      flex-shrink: 0;
      margin-bottom: 6px;
    }
    .lib-tab {
      background: none;
      border: none;
      color: var(--muted);
      padding: 6px 8px;
      border-radius: 5px;
      font-size: 0.74rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
    }
    .lib-tab:hover { color: var(--text); }
    .lib-tab.active {
      background: var(--panel);
      color: var(--text);
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    .lib-tab:active { transform: scale(0.98); }

    .lib-panel {
      flex: 1;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      gap: 6px;
      animation: tabFade 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes tabFade {
      from { opacity: 0; transform: translateY(3px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* CAPES VIEW */
    .cape-top-bar {
      display: flex;
      gap: 5px;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
    }
    .cape-filter-pills { display: flex; gap: 4px; }
    .cape-fetch-bar { display: flex; gap: 4px; flex: 1; min-width: 170px; }
    .cape-fetch-bar input {
      flex: 1;
      background: var(--input-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 4px 7px;
      border-radius: 5px;
      font-size: 0.70rem;
    }
    .cape-fetch-bar button {
      background: var(--accent);
      color: #fff;
      border: none;
      padding: 4px 8px;
      border-radius: 5px;
      font-weight: 600;
      cursor: pointer;
      font-size: 0.70rem;
    }
    .cape-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(95px, 1fr));
      gap: 5px;
      overflow-y: auto;
      flex: 1;
      padding-right: 3px;
    }
    .cape-grid::-webkit-scrollbar { width: 4px; }
    .cape-grid::-webkit-scrollbar-thumb { background: var(--scroll-thumb); border-radius: 4px; }
    .cape-card {
      background: var(--chip-bg);
      border: 1px solid var(--border);
      border-radius: 5px;
      padding: 5px 3px;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 3px;
    }
    .cape-card:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    .cape-card.active {
      border-color: var(--success);
      background: rgba(16, 185, 129, 0.12);
      box-shadow: 0 0 0 1px var(--success);
    }
    .cape-card img {
      width: 38px;
      height: 38px;
      object-fit: contain;
      margin: 0 auto;
      display: block;
      image-rendering: pixelated;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }
    .cape-card-name {
      font-size: 0.65rem;
      font-weight: 600;
      color: var(--text);
      line-height: 1.15;
      max-width: 88px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .cape-badge {
      font-size: 0.58rem;
      padding: 1px 4px;
      border-radius: 3px;
      background: rgba(59, 130, 246, 0.12);
      color: var(--accent);
    }
    .cape-badge.gold {
      background: rgba(245, 158, 11, 0.12);
      color: var(--gold);
    }

    /* PALETTES VIEW */
    .cat-bar {
      display: flex;
      gap: 3px;
      overflow-x: auto;
      padding-bottom: 2px;
      flex-shrink: 0;
    }
    .cat-bar::-webkit-scrollbar { height: 3px; }
    .cat-bar::-webkit-scrollbar-thumb { background: var(--scroll-thumb); border-radius: 3px; }
    .cat-btn {
      background: var(--chip-bg);
      border: 1px solid var(--border);
      color: var(--muted);
      padding: 3px 7px;
      border-radius: 10px;
      font-size: 0.66rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s;
    }
    .cat-btn:hover { color: var(--text); border-color: var(--border-focus); }
    .cat-btn.active {
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }

    .palette-search-bar { display: flex; gap: 5px; flex-shrink: 0; }
    .palette-search-bar input {
      flex: 1;
      background: var(--input-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 4px 7px;
      border-radius: 5px;
      font-size: 0.70rem;
    }
    .palette-search-bar input:focus { border-color: var(--accent); outline: none; }
    .btn-random-palette {
      background: var(--purple);
      color: #fff;
      border: none;
      padding: 4px 9px;
      border-radius: 5px;
      font-size: 0.70rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 3px;
      white-space: nowrap;
      transition: all 0.15s ease;
    }
    .btn-random-palette:hover { filter: brightness(1.1); transform: translateY(-1px); }
    .btn-random-palette:active { transform: scale(0.96); }

    .palette-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
      gap: 5px;
      overflow-y: auto;
      flex: 1;
      padding-right: 3px;
    }
    .palette-grid::-webkit-scrollbar { width: 4px; }
    .palette-grid::-webkit-scrollbar-thumb { background: var(--scroll-thumb); border-radius: 4px; }
    .palette-btn {
      background: var(--chip-bg);
      border: 1px solid var(--border);
      border-radius: 5px;
      padding: 5px;
      cursor: pointer;
      position: relative;
      transition: all 0.15s ease;
      text-align: left;
    }
    .palette-btn:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    .palette-btn.active {
      border-color: var(--accent);
      background: rgba(59, 130, 246, 0.12);
      box-shadow: 0 0 0 1px var(--accent);
    }
    .palette-name {
      font-size: 0.67rem;
      font-weight: 600;
      margin-bottom: 3px;
      display: block;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: var(--text);
    }
    .swatches {
      display: flex;
      height: 11px;
      border-radius: 3px;
      overflow: hidden;
      border: 1px solid var(--border);
    }
    .swatch { flex: 1; }
    .swatch-crown {
      width: 12px;
      height: 11px;
      border-left: 1px solid rgba(0,0,0,0.25);
      position: relative;
    }
    .swatch-crown::after {
      content: '👑';
      font-size: 6px;
      position: absolute;
      top: -2px; left: 1px;
    }
    .swatch-jewel {
      width: 12px;
      height: 11px;
      border-left: 1px solid rgba(0,0,0,0.25);
      position: relative;
    }
    .swatch-jewel::after {
      content: '💎';
      font-size: 6px;
      position: absolute;
      top: -2px; left: 1px;
    }
    .del-palette {
      position: absolute; top: 2px; right: 2px;
      background: rgba(239,68,68,0.2); color: #f87171;
      border: none; border-radius: 3px; padding: 0 3px;
      font-size: 0.62rem; cursor: pointer;
    }

    .custom-save-bar { display: flex; gap: 4px; flex-shrink: 0; }
    .custom-save-bar input {
      flex: 1; background: var(--input-bg); border: 1px solid var(--border);
      color: var(--text); padding: 4px 7px; border-radius: 5px; font-size: 0.68rem;
    }
    .custom-save-bar button {
      background: var(--accent); color: #fff; border: none;
      padding: 4px 8px; border-radius: 5px; font-weight: 600; cursor: pointer; font-size: 0.68rem;
    }
  </style>
</head>
<body>

<!-- TOP BAR -->
<header class="top-header">
  <div class="brand-title">
    <h1>🎮 MC Skin 3D Studio</h1>
    <span class="version-tag">Pro v5 • color-palette MCP</span>
  </div>
  <div class="header-actions">
    <button class="theme-toggle-btn" id="themeToggleBtn" onclick="toggleAppTheme()">
      <span id="themeToggleIcon">☀️</span> <span id="themeToggleText">Açık Mod</span>
    </button>
  </div>
</header>

<!-- 3-PANEL STUDIO -->
<div class="studio-layout">
  
  <!-- PANEL 1: 3D VIEWPORT, DOWNLOAD/UPLOAD & POSE -->
  <div class="studio-card viewer-card">
    <div id="viewer3d">
      <div class="viewer-badge">Sol Tık: Döndür • Tekerlek: Yakınlaştır</div>
      <div class="viewer-mode-badge" id="capeModeBadge" style="display:none;">Pelerin: Aktif</div>
    </div>

    <!-- İNDİR VE YÜKLE DOĞRUDAN 3D GÖRÜNTÜLEYİCİNİN ALTINDA -->
    <div class="tex-preview-bar">
      <canvas id="skinCanvas" width="64" height="64" title="Canlı 64x64 Doku"></canvas>
      <div class="tex-actions">
        <button class="btn-download" id="downloadBtn">⬇ 64x64 PNG İndir</button>
        <label class="btn-upload" title="Farklı bir skin yükle">
          📁 Dosya Yükle <input type="file" id="fileInput" accept="image/png" style="display:none;">
        </label>
      </div>
    </div>

    <div class="inner-scroll">
      <!-- ANİMASYON BUTONLARI -->
      <div class="btn-group" id="animGroup">
        <button class="chip-btn active" data-anim="walk">🚶 Yürü</button>
        <button class="chip-btn" data-anim="run">🏃 Koş</button>
        <button class="chip-btn" data-anim="idle">🧍 Nefes Al</button>
        <button class="chip-btn" data-anim="wave">👋 El Salla</button>
        <button class="chip-btn" data-anim="fly">🦸 Uçuş</button>
        <button class="chip-btn" data-anim="none">⏸ Manuel</button>
      </div>

      <div class="slider-row">
        <div class="slider-header"><span>Animasyon Hızı</span><span id="speedVal">50%</span></div>
        <input type="range" id="speedSlider" min="10" max="250" value="50">
      </div>

      <!-- POZ VE KATMAN AYIRMA SLIDERLARI -->
      <div class="slider-row">
        <div class="slider-header"><span>Katman Patlatma (Explode)</span><span id="explodeVal">0%</span></div>
        <input type="range" id="explodeSlider" min="0" max="100" value="0">
      </div>
      <div class="slider-row">
        <div class="slider-header"><span>Kafa Açısı</span><span id="poseHeadVal">0°</span></div>
        <input type="range" id="poseHead" min="-75" max="75" value="0">
      </div>
      <div class="slider-row">
        <div class="slider-header"><span>Kollar</span><span id="poseArmsVal">0°</span></div>
        <input type="range" id="poseArms" min="-140" max="140" value="0">
      </div>
      <div class="slider-row">
        <div class="slider-header"><span>Bacaklar</span><span id="poseLegsVal">0°</span></div>
        <input type="range" id="poseLegs" min="-80" max="80" value="0">
      </div>
    </div>
  </div>

  <!-- PANEL 2: KATMANLAR, KORUMALAR, RENKLER & COLOR-PALETTE MCP -->
  <div class="studio-card col-mid">
    <div class="inner-scroll">
      
      <!-- KATMAN GÖRÜNÜRLÜĞÜ -->
      <div class="btn-group-layers">
        <button class="chip-btn active" data-layer="hat" title="Dış Katman: Taç">👑 Taç</button>
        <button class="chip-btn active" data-layer="jacket" title="Dış Katman: Ceket">🧥 Ceket</button>
        <button class="chip-btn active" data-layer="arms" title="Dış Katman: Kollar">💪 Kollar</button>
        <button class="chip-btn active" data-layer="pants" title="Dış Katman: Bacaklar">👖 Bacaklar</button>
        <button class="chip-btn active" data-layer="headBase" title="İç Vücut: Baş">🙂 Baş</button>
        <button class="chip-btn active" data-layer="bodyBase" title="İç Vücut: Gövde">👕 Gövde</button>
        <button class="chip-btn active" data-layer="armsBase" title="İç Vücut: Kol">🙌 Kol</button>
        <button class="chip-btn active" data-layer="legsBase" title="İç Vücut: Bacak">🦵 Bacak</button>
      </div>

      <!-- KORUMALAR VE TAVUK GİZLE -->
      <div class="checks-grid">
        <label title="Tacın altın sarısı rengini korur"><input type="checkbox" id="keepCrown" checked> 👑 Tacı Koru</label>
        <label title="Mücevherin taş rengini korur"><input type="checkbox" id="keepJewel"> 💎 Mücevheri Koru</label>
        <label title="1. ve 2. katmandaki saç piksellerini korur"><input type="checkbox" id="keepHair" checked> 💇 Saçı Koru</label>
        <label title="Sırt ceketindeki 28 piksellik tavuğu gizler ve arka kumaşla kaynaştırır"><input type="checkbox" id="hideChicken"> 🐔 Tavuğu Gizle</label>
      </div>

      <!-- RENK SEÇİCİLERİ (2 SÜTUNLU KOMPAKT IZGARA) -->
      <div class="color-grid">
        <div class="color-item">
          <label>👑 Taç</label>
          <div class="color-inputs">
            <input type="color" id="colCrown" value="#eab308">
            <input type="text" class="hex-input" id="hexCrown" value="#EAB308" maxlength="7">
          </div>
        </div>
        <div class="color-item">
          <label>💎 Mücevher</label>
          <div class="color-inputs">
            <input type="color" id="colJewel" value="#2563eb">
            <input type="text" class="hex-input" id="hexJewel" value="#2563EB" maxlength="7">
          </div>
        </div>
        <div class="color-item">
          <label>👕 Üst</label>
          <div class="color-inputs">
            <input type="color" id="colTunic" value="#162d59">
            <input type="text" class="hex-input" id="hexTunic" value="#162D59" maxlength="7">
          </div>
        </div>
        <div class="color-item">
          <label>👖 Alt</label>
          <div class="color-inputs">
            <input type="color" id="colPants" value="#0f1e3d">
            <input type="text" class="hex-input" id="hexPants" value="#0F1E3D" maxlength="7">
          </div>
        </div>
        <div class="color-item">
          <label>🧥 Kollar</label>
          <div class="color-inputs">
            <input type="color" id="colSleeves" value="#2b4c7e">
            <input type="text" class="hex-input" id="hexSleeves" value="#2B4C7E" maxlength="7">
          </div>
        </div>
        <div class="color-item">
          <label>🥾 Ayakkabı</label>
          <div class="color-inputs">
            <input type="color" id="colShoes" value="#091326">
            <input type="text" class="hex-input" id="hexShoes" value="#091326" maxlength="7">
          </div>
        </div>
      </div>

      <!-- SAÇ ÖZEL ALANI (1. VE 2. KATMAN) -->
      <div class="hair-item">
        <div class="hair-top">
          <label>💇 Saç (1. & 2. Katman)</label>
          <div class="color-inputs">
            <input type="color" id="colHair" value="#562a1f">
            <input type="text" class="hex-input" id="hexHair" value="#562A1F" maxlength="7">
          </div>
        </div>
        <div class="hair-presets">
          <div class="hair-dot" style="background:#1c1917" title="Kuzguni Siyah" data-hair="#1c1917"></div>
          <div class="hair-dot" style="background:#3b1e10" title="Koyu Kahve" data-hair="#3b1e10"></div>
          <div class="hair-dot" style="background:#562a1f" title="Kestane Kahve" data-hair="#562a1f"></div>
          <div class="hair-dot" style="background:#854d0e" title="Kumral" data-hair="#854d0e"></div>
          <div class="hair-dot" style="background:#eab308" title="Altın Sarısı" data-hair="#eab308"></div>
          <div class="hair-dot" style="background:#991b1b" title="Kızıl" data-hair="#991b1b"></div>
          <div class="hair-dot" style="background:#e2e8f0" title="Platin Beyaz" data-hair="#e2e8f0"></div>
          <div class="hair-dot" style="background:#3b82f6" title="Neon Mavi" data-hair="#3b82f6"></div>
          <div class="hair-dot" style="background:#ec4899" title="Pastel Pembe" data-hair="#ec4899"></div>
        </div>
      </div>

      <!-- COLOR-PALETTE MCP TON SKALASI -->
      <div class="shade-box">
        <div class="shade-header">
          <span>color-palette MCP (11 Ton Skalası)</span>
          <span class="wcag-badge" id="wcagBadge">WCAG AA 6.8:1</span>
        </div>
        <div class="shade-scale-strip" id="shadeStrip"></div>
        <div class="shade-footer">
          <span class="shade-legend">50 Açık • 500 Ana • 950 Koyu</span>
          <button class="btn-copy-css" id="btnCopyCss" onclick="copyTailwindTokens()">📋 CSS Kopyala</button>
        </div>
      </div>

      <!-- İNCE AYARLAR -->
      <div class="slider-row">
        <div class="slider-header"><span>🥾 Ayakkabı Yüksekliği (Her İki Ayak)</span><span id="shoeHeightVal">3 Piksel</span></div>
        <input type="range" id="shoeHeightSlider" min="0" max="6" value="3">
      </div>
      <div class="slider-row">
        <div class="slider-header"><span>🌗 Gölge & Kontrast Derinliği</span><span id="contrastVal">100%</span></div>
        <input type="range" id="contrastSlider" min="40" max="180" value="100">
      </div>
      <div class="slider-row">
        <div class="slider-header"><span>🎨 Doygunluk Geçişi</span><span id="satKeepVal">85%</span></div>
        <input type="range" id="satKeepSlider" min="0" max="150" value="85">
      </div>

    </div>
  </div>

  <!-- PANEL 3: KÜTÜPHANE (PELERİNLER 46 & RENK PALETLERİ 170) -->
  <div class="studio-card">
    
    <!-- SEGMENTED TABS -->
    <div class="lib-tab-bar">
      <button class="lib-tab active" id="tabCapes" onclick="switchLibTab('capes')">
        🦸 Pelerin Koleksiyonu <span style="font-size:0.68rem; opacity:0.8;">(46)</span>
      </button>
      <button class="lib-tab" id="tabPalettes" onclick="switchLibTab('palettes')">
        🎨 Renk Paletleri <span style="font-size:0.68rem; opacity:0.8;">(170)</span>
      </button>
    </div>

    <!-- PELERİNLER PANELİ -->
    <div class="lib-panel" id="panelCapes">
      <div style="display:flex; gap:5px; align-items:center;">
        <div class="btn-group" style="flex:1;">
          <button class="chip-btn" id="btnModeCape">🦸 Pelerin</button>
          <button class="chip-btn" id="btnModeElytra">🪽 Elytra</button>
          <button class="chip-btn green active" id="btnModeNone">🚫 Gizli</button>
        </div>
      </div>

      <div class="cape-top-bar">
        <div class="cape-filter-pills">
          <button id="btnFilterAll" class="chip-btn green active" style="padding:4px 8px; font-size:0.68rem;" onclick="setCapeFilter('all')">Tüm Pelerinler (46)</button>
          <button id="btnFilterOwned" class="chip-btn" style="padding:4px 8px; font-size:0.68rem;" onclick="setCapeFilter('owned')">Sahip Olunanlar (17)</button>
        </div>
        <div class="cape-fetch-bar">
          <input type="text" id="capeUsernameInput" value="Teknoist" placeholder="Kullanıcı Adı">
          <button id="btnFetchCape">Getir</button>
        </div>
      </div>

      <div class="cape-grid" id="capeGrid"></div>

      <div style="background:var(--sub-panel); padding:5px 7px; border-radius:5px; border:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.68rem; color:var(--muted);">📁 Özel Pelerin (.png 64x32)</span>
        <label class="chip-btn" style="padding:3px 7px; cursor:pointer;">
          Seç <input type="file" id="capeFileInput" accept="image/png" style="display:none;">
        </label>
      </div>
    </div>

    <!-- PALETLER PANELİ -->
    <div class="lib-panel" id="panelPalettes" style="display:none;">
      <div class="cat-bar" id="catBar">
        <button class="cat-btn active" data-cat="all" onclick="filterByCategory('all')">Tümü (170)</button>
        <button class="cat-btn" data-cat="Klasik" onclick="filterByCategory('Klasik')">Klasik</button>
        <button class="cat-btn" data-cat="Canavarlar" onclick="filterByCategory('Canavarlar')">Canavarlar</button>
        <button class="cat-btn" data-cat="Madenler" onclick="filterByCategory('Madenler')">Madenler</button>
        <button class="cat-btn" data-cat="Biyomlar" onclick="filterByCategory('Biyomlar')">Biyomlar</button>
        <button class="cat-btn" data-cat="Cyberpunk" onclick="filterByCategory('Cyberpunk')">Cyberpunk</button>
        <button class="cat-btn" data-cat="Anime" onclick="filterByCategory('Anime')">Anime</button>
        <button class="cat-btn" data-cat="Fantezi" onclick="filterByCategory('Fantezi')">Fantezi</button>
        <button class="cat-btn" data-cat="Pastel" onclick="filterByCategory('Pastel')">Pastel</button>
        <button class="cat-btn" data-cat="Doğa" onclick="filterByCategory('Doğa')">Doğa</button>
        <button class="cat-btn" data-cat="Karanlık" onclick="filterByCategory('Karanlık')">Karanlık</button>
        <button class="cat-btn" data-cat="Ten" onclick="filterByCategory('Ten')">Ten</button>
        <button class="cat-btn" data-cat="Özel" onclick="filterByCategory('Özel')">Özel</button>
      </div>

      <div class="palette-search-bar">
        <input type="text" id="paletteSearch" placeholder="Palet ara (Örn: Elmas, Warden, Sakura...)">
        <button class="btn-random-palette" id="btnRandomPalette">🎲 Rastgele</button>
      </div>

      <div class="palette-grid" id="presetGrid"></div>

      <div class="custom-save-bar">
        <input type="text" id="customPaletteName" placeholder="Özel palet adı">
        <button id="savePaletteBtn">+ Kaydet</button>
      </div>
      <div class="palette-grid" id="customGrid" style="max-height: 80px; flex-shrink:0;"></div>
    </div>

  </div>

</div>

<script>



  // YEREL OLARAK ÖNBELLEKLENMİŞ GERÇEK MİNECRAFT PELERİNLERİ (CORS HATASIZ & ANINDA YÜKLENİR)
  const CACHED_BASE_SKIN = "__SKIN_B64__";

  // 46 PELERİN (Minecraft Wiki Resmi Önizleme Spriteları + 64x32 Dokuları)
  __OFFICIAL_CAPES_JS__;

  // 170+ HAZIR RENK PALETİ
  const PRESET_PALETTES = __PALETTES_JSON__;

  // TEMA YÖNETİMİ (AYDINLIK / KARANLIK MOD)
  function initTheme() {
    const savedTheme = localStorage.getItem('mc_studio_theme') || 'dark';
    if (savedTheme === 'light') {
      document.body.classList.add('light-theme');
      updateThemeUI(true);
    } else {
      document.body.classList.remove('light-theme');
      updateThemeUI(false);
    }
  }

  function toggleAppTheme() {
    const isLight = document.body.classList.toggle('light-theme');
    localStorage.setItem('mc_studio_theme', isLight ? 'light' : 'dark');
    updateThemeUI(isLight);
    updateShadeInspector();
  }

  function updateThemeUI(isLight) {
    const icon = document.getElementById('themeToggleIcon');
    const text = document.getElementById('themeToggleText');
    if (isLight) {
      icon.textContent = '🌙';
      text.textContent = 'Koyu Mod';
    } else {
      icon.textContent = '☀️';
      text.textContent = 'Açık Mod';
    }
  }

  // KÜTÜPHANE SEKMELERİ ARASINDA GEÇİŞ (PELERİNLER / PALETLER)
  function switchLibTab(tab) {
    const isCapes = tab === 'capes';
    document.getElementById('tabCapes').classList.toggle('active', isCapes);
    document.getElementById('tabPalettes').classList.toggle('active', !isCapes);
    document.getElementById('panelCapes').style.display = isCapes ? 'flex' : 'none';
    document.getElementById('panelPalettes').style.display = !isCapes ? 'flex' : 'none';
  }

  // ==========================================
  // color-palette MCP: HSL, 11-SHADE, CONTRAST
  // ==========================================
  function hexToHSL(hex) {
    hex = hex.replace(/^#/, '');
    const r = parseInt(hex.substring(0, 2), 16) / 255;
    const g = parseInt(hex.substring(2, 4), 16) / 255;
    const b = parseInt(hex.substring(4, 6), 16) / 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    const diff = max - min;
    let l = (max + min) / 2;
    let s = 0;
    if (diff !== 0) {
      s = l > 0.5 ? diff / (2 - max - min) : diff / (max + min);
    }
    let h = 0;
    if (diff !== 0) {
      if (max === r) h = ((g - b) / diff + (g < b ? 6 : 0)) / 6;
      else if (max === g) h = ((b - r) / diff + 2) / 6;
      else h = ((r - g) / diff + 4) / 6;
    }
    return { h: Math.round(h * 360), s: Math.round(s * 100), l: Math.round(l * 100) };
  }

  function hslToHex(h, s, l) {
    s = s / 100; l = l / 100;
    const c = (1 - Math.abs(2 * l - 1)) * s;
    const x = c * (1 - Math.abs((h / 60) % 2 - 1));
    const m = l - c / 2;
    let r = 0, g = 0, b = 0;
    if (h >= 0 && h < 60) { r = c; g = x; b = 0; }
    else if (h >= 60 && h < 120) { r = x; g = c; b = 0; }
    else if (h >= 120 && h < 180) { r = 0; g = c; b = x; }
    else if (h >= 180 && h < 240) { r = 0; g = x; b = c; }
    else if (h >= 240 && h < 300) { r = x; g = 0; b = c; }
    else if (h >= 300 && h < 360) { r = c; g = 0; b = x; }
    r = Math.round((r + m) * 255);
    g = Math.round((g + m) * 255);
    b = Math.round((b + m) * 255);
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
  }

  function generate11Shades(hex) {
    const { h, s } = hexToHSL(hex);
    const shadesDef = {
      50:  { l: 97, sMult: 0.8 },
      100: { l: 94, sMult: 0.8 },
      200: { l: 87, sMult: 0.85 },
      300: { l: 75, sMult: 0.9 },
      400: { l: 62, sMult: 0.95 },
      500: { l: 48, sMult: 1.0 },
      600: { l: 40, sMult: 1.0 },
      700: { l: 33, sMult: 1.0 },
      800: { l: 27, sMult: 1.0 },
      900: { l: 20, sMult: 1.0 },
      950: { l: 10, sMult: 1.0 }
    };
    const result = {};
    for (const [shade, { l, sMult }] of Object.entries(shadesDef)) {
      result[shade] = hslToHex(h, Math.round(s * sMult), l);
    }
    return result;
  }

  function getLuminance(hex) {
    hex = hex.replace(/^#/, '');
    const r = parseInt(hex.substring(0, 2), 16) / 255;
    const g = parseInt(hex.substring(2, 4), 16) / 255;
    const b = parseInt(hex.substring(4, 6), 16) / 255;
    const a = [r, g, b].map(v => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2];
  }

  function getContrastRatio(hex1, hex2) {
    const l1 = getLuminance(hex1);
    const l2 = getLuminance(hex2);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }

  function updateShadeInspector() {
    const baseHex = colTunic.value;
    const shades = generate11Shades(baseHex);
    const strip = document.getElementById('shadeStrip');
    if (!strip) return;
    strip.innerHTML = '';

    for (const [num, hex] of Object.entries(shades)) {
      const step = document.createElement('div');
      step.className = 'shade-step';
      step.style.background = hex;
      step.title = `Ton ${num}: ${hex} (Tıkla ve Gövdeye Uygula)`;
      step.addEventListener('click', () => {
        colTunic.value = hex;
        hexTunic.value = hex.toUpperCase();
        renderRecoloredSkin();
      });
      strip.appendChild(step);
    }

    const contrastOnWhite = getContrastRatio(baseHex, '#FFFFFF');
    const contrastOnDark = getContrastRatio(baseHex, '#090D16');
    const bestRatio = Math.max(contrastOnWhite, contrastOnDark);
    const badge = document.getElementById('wcagBadge');
    if (badge) {
      if (bestRatio >= 7.0) {
        badge.textContent = `WCAG AAA ${bestRatio.toFixed(1)}:1`;
        badge.style.color = 'var(--success)';
        badge.style.borderColor = 'rgba(16, 185, 129, 0.4)';
      } else if (bestRatio >= 4.5) {
        badge.textContent = `WCAG AA ${bestRatio.toFixed(1)}:1`;
        badge.style.color = '#38bdf8';
        badge.style.borderColor = 'rgba(56, 189, 248, 0.4)';
      } else {
        badge.textContent = `Kontrast ${bestRatio.toFixed(1)}:1`;
        badge.style.color = 'var(--gold)';
        badge.style.borderColor = 'rgba(245, 158, 11, 0.4)';
      }
    }
  }

  function copyTailwindTokens() {
    const baseHex = colTunic.value;
    const shades = generate11Shades(baseHex);
    const cssCode = `@theme {
  --color-primary-50: ${shades[50]};
  --color-primary-100: ${shades[100]};
  --color-primary-200: ${shades[200]};
  --color-primary-300: ${shades[300]};
  --color-primary-400: ${shades[400]};
  --color-primary-500: ${shades[500]}; /* Brand */
  --color-primary-600: ${shades[600]};
  --color-primary-700: ${shades[700]};
  --color-primary-800: ${shades[800]};
  --color-primary-900: ${shades[900]};
  --color-primary-950: ${shades[950]};

  --color-background: #FFFFFF;
  --color-foreground: ${shades[950]};
  --color-card: #FFFFFF;
  --color-card-foreground: ${shades[900]};
  --color-primary: ${shades[600]};
  --color-primary-foreground: #FFFFFF;
  --color-border: ${shades[200]};
}

.dark {
  --color-background: ${shades[950]};
  --color-foreground: ${shades[50]};
  --color-card: ${shades[900]};
  --color-card-foreground: ${shades[50]};
  --color-primary: ${shades[500]};
  --color-border: ${shades[800]};
}`;

    navigator.clipboard.writeText(cssCode).then(() => {
      const btn = document.getElementById('btnCopyCss');
      const oldText = btn.textContent;
      btn.textContent = '✅ Tailwind v4 CSS Kopyalandı!';
      setTimeout(() => btn.textContent = oldText, 2200);
    });
  }

  // ==========================================
  // PALET LİSTELEME & KATEGORİ FİLTRELEME
  // ==========================================
  let currentCategory = 'all';

  function filterByCategory(cat) {
    currentCategory = cat;
    document.querySelectorAll('.cat-btn').forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-cat') === cat);
    });
    renderPalettes(document.getElementById('paletteSearch').value.trim());
  }

  function createPaletteCard(p, isCustom = false, idx = -1) {
    const div = document.createElement('div');
    div.className = 'palette-btn';
    div.innerHTML = `
      <span class="palette-name">${p.name}</span>
      <div class="swatches">
        <div class="swatch" style="background:${p.tunic}" title="Üst"></div>
        <div class="swatch" style="background:${p.pants}" title="Pantolon"></div>
        <div class="swatch" style="background:${p.sleeves}" title="Kollar"></div>
        <div class="swatch" style="background:${p.shoes || p.pants}" title="Ayakkabı"></div>
        <div class="swatch-crown" style="background:${p.crown || '#eab308'}" title="Taç"></div>
        <div class="swatch-jewel" style="background:${p.jewel || '#2563eb'}" title="Taç Mücevheri (Zıt)"></div>
      </div>
    `;
    div.addEventListener('click', e => {
      if (e.target.classList.contains('del-palette')) return;
      applyPalette(p, div);
    });
    if (isCustom) {
      const del = document.createElement('button');
      del.className = 'del-palette';
      del.textContent = '✕';
      del.addEventListener('click', () => {
        const list = JSON.parse(localStorage.getItem('mc_custom_palettes_v4') || '[]');
        list.splice(idx, 1);
        localStorage.setItem('mc_custom_palettes_v4', JSON.stringify(list));
        renderPalettes();
      });
      div.appendChild(del);
    }
    return div;
  }

  function renderPalettes(filter = '') {
    const presetGrid = document.getElementById('presetGrid');
    presetGrid.innerHTML = '';
    
    const query = filter.toLowerCase();
    const filtered = PRESET_PALETTES.filter(p => {
      const matchesCat = (currentCategory === 'all' || p.cat === currentCategory);
      const matchesQuery = !query || p.name.toLowerCase().includes(query) || (p.cat && p.cat.toLowerCase().includes(query));
      return matchesCat && matchesQuery;
    });

    filtered.forEach((p, i) => {
      const card = createPaletteCard(p, false);
      presetGrid.appendChild(card);
    });

    const customGrid = document.getElementById('customGrid');
    customGrid.innerHTML = '';
    const customList = JSON.parse(localStorage.getItem('mc_custom_palettes_v4') || '[]');
    if (customList.length === 0) {
      customGrid.innerHTML = `<div style="font-size:0.70rem; color:var(--muted); padding:4px;">Özel palet yok.</div>`;
    } else {
      customList.forEach((p, i) => customGrid.appendChild(createPaletteCard(p, true, i)));
    }
  }

  document.getElementById('paletteSearch').addEventListener('input', e => {
    renderPalettes(e.target.value.trim());
  });

  // RASTGELE UYUMLU VE ZIT TAÇ/MÜCEVHER PALETİ ÜRETİCİ
  document.getElementById('btnRandomPalette').addEventListener('click', () => {
    const baseHue = Math.floor(Math.random() * 360);
    const compHue = (baseHue + 180) % 360;
    const splitHue = (baseHue + 150) % 360;
    const crownHue = (baseHue + 40) % 360;
    const jewelHue = (crownHue + 180) % 360; // Zıt komplementer mücevher taşı

    const rgb1 = hslToRgb(baseHue, 65, 30);
    const rgb2 = hslToRgb(baseHue, 50, 15);
    const rgb3 = hslToRgb(compHue, 70, 45);
    const rgb4 = hslToRgb(splitHue, 40, 10);
    const rgbC = hslToRgb(crownHue, 85, 55);
    const rgbJ = hslToRgb(jewelHue, 95, 50);

    const toHex = rgb => '#' + rgb.map(x => x.toString(16).padStart(2, '0')).join('');

    const randomP = {
      name: "🎲 Rastgele Sentez",
      tunic: toHex(rgb1),
      pants: toHex(rgb2),
      sleeves: toHex(rgb3),
      shoes: toHex(rgb4),
      crown: toHex(rgbC),
      jewel: toHex(rgbJ)
    };

    applyPalette(randomP);
  });

  // ÖZEL PALET KAYDETME
  document.getElementById('savePaletteBtn').addEventListener('click', () => {
    const input = document.getElementById('customPaletteName');
    const list = JSON.parse(localStorage.getItem('mc_custom_palettes_v4') || '[]');
    list.push({
      name: input.value.trim() || `Özel Palet #${list.length + 1}`,
      tunic: colTunic.value,
      pants: colPants.value,
      sleeves: colSleeves.value,
      shoes: colShoes.value,
      jewel: colJewel.value,
      crown: colCrown.value
    });
    localStorage.setItem('mc_custom_palettes_v4', JSON.stringify(list));
    input.value = '';
    renderPalettes();
  });

  // DOM ELEMENTLERİ
  const skinCanvas = document.getElementById('skinCanvas');
  const skinCtx = skinCanvas.getContext('2d', { willReadFrequently: true });

  const colCrown = document.getElementById('colCrown'), hexCrown = document.getElementById('hexCrown');
  const colJewel = document.getElementById('colJewel'), hexJewel = document.getElementById('hexJewel');
  const colHair = document.getElementById('colHair'), hexHair = document.getElementById('hexHair');
  const colTunic = document.getElementById('colTunic'), hexTunic = document.getElementById('hexTunic');
  const colPants = document.getElementById('colPants'), hexPants = document.getElementById('hexPants');
  const colSleeves = document.getElementById('colSleeves'), hexSleeves = document.getElementById('hexSleeves');
  const colShoes = document.getElementById('colShoes'), hexShoes = document.getElementById('hexShoes');

  const shoeHeightSlider = document.getElementById('shoeHeightSlider');
  const contrastSlider = document.getElementById('contrastSlider');
  const satKeepSlider = document.getElementById('satKeepSlider');

  // KORUMA & AMBLEM ONAY KUTULARI
  const keepHair = document.getElementById('keepHair');
  const keepCrown = document.getElementById('keepCrown');
  const keepJewel = document.getElementById('keepJewel');
  const hideChicken = document.getElementById('hideChicken');

  let originalImageData = null;
  let pixelClassification = [];
  let groupStats = {
    tunic: { avgS: 50, avgL: 30 },
    pants: { avgS: 30, avgL: 25 },
    sleeves: { avgS: 30, avgL: 50 },
    shoes: { avgS: 30, avgL: 25 },
    jewel: { avgS: 20, avgL: 45 },
    crown: { avgS: 75, avgL: 65 },
    hair: { avgS: 45, avgL: 25 }
  };

  // ========================================================
  // 3D MODELLEME MOTORU (ORİJİNAL MÜKEMMEL ÇALIŞAN VERSİYON)
  // ========================================================
  let scene, camera, renderer, skinTexture;
  let charGroup, headGroup, bodyGroup, rightArmGroup, leftArmGroup, rightLegGroup, leftLegGroup;
  let capePivot, capeMesh;
  let elytraPivot, elytraLeftWing, elytraRightWing, leftWingMesh, rightWingMesh;
  let capeTexture = null;
  let currentCapeMode = 'none'; // Varsayılan olarak PELERİN GİZLİ
  let meshes = {};
  let currentAnim = 'walk';
  let animTime = 0;
  let currentCapeFilter = 'all';
  let activeCapeId = 'cape_46';

  function setBoxUVs(geometry, u, v, w, h, d, texW = 64, texH = 64) {
    const faces = [
      [u + d + w, v + d, d, h],      // right face
      [u, v + d, d, h],              // left face
      [u + d, v, w, d],              // top face
      [u + d + w, v, w, d],          // bottom face
      [u + d, v + d, w, h],          // front face
      [u + d + w + d, v + d, w, h]   // back face
    ];
    const uvAttr = geometry.attributes.uv;
    for (let i = 0; i < 6; i++) {
      let [fx, fy, fw, fh] = faces[i];
      let u0 = fx / texW, u1 = (fx + fw) / texW;
      let v1 = 1 - (fy / texH), v0 = 1 - ((fy + fh) / texH);
      const idx = i * 4;
      if (i === 2) {
        uvAttr.setXY(idx, u0, v1); uvAttr.setXY(idx + 1, u1, v1);
        uvAttr.setXY(idx + 2, u0, v0); uvAttr.setXY(idx + 3, u1, v0);
      } else if (i === 3) {
        uvAttr.setXY(idx, u0, v0); uvAttr.setXY(idx + 1, u1, v0);
        uvAttr.setXY(idx + 2, u0, v1); uvAttr.setXY(idx + 3, u1, v1);
      } else {
        uvAttr.setXY(idx, u0, v1); uvAttr.setXY(idx + 1, u1, v1);
        uvAttr.setXY(idx + 2, u0, v0); uvAttr.setXY(idx + 3, u1, v0);
      }
    }
    uvAttr.needsUpdate = true;
  }

  // PELERİN ÖZEL UV HARİTALAMASI (DIŞ EMBLEM ARKA YÜZDE -Z, İÇ ASTAR ÖN YÜZDE +Z)
  function setCapeBoxUVs(geometry) {
    const texW = 64, texH = 32;
    // Face 0 (+X sağ kenar): [11, 1, 1, 16]
    // Face 1 (-X sol kenar): [0, 1, 1, 16]
    // Face 2 (+Y üst omuz kenarı): [1, 0, 10, 1]
    // Face 3 (-Y alt etek kenarı): [11, 0, 10, 1]
    // Face 4 (+Z gövdeye bakan iç astar): [12, 1, 10, 16]
    // Face 5 (-Z arkadan görünen DIŞ EMBLEM): [1, 1, 10, 16]
    const faces = [
      [11, 1, 1, 16],
      [0, 1, 1, 16],
      [1, 0, 10, 1],
      [11, 0, 10, 1],
      [12, 1, 10, 16],
      [1, 1, 10, 16]
    ];
    const uvAttr = geometry.attributes.uv;
    for (let i = 0; i < 6; i++) {
      let [fx, fy, fw, fh] = faces[i];
      let u0 = fx / texW, u1 = (fx + fw) / texW;
      let v1 = 1 - (fy / texH), v0 = 1 - ((fy + fh) / texH);
      const idx = i * 4;
      if (i === 2) {
        uvAttr.setXY(idx, u0, v1); uvAttr.setXY(idx + 1, u1, v1);
        uvAttr.setXY(idx + 2, u0, v0); uvAttr.setXY(idx + 3, u1, v0);
      } else if (i === 3) {
        uvAttr.setXY(idx, u0, v0); uvAttr.setXY(idx + 1, u1, v0);
        uvAttr.setXY(idx + 2, u0, v1); uvAttr.setXY(idx + 3, u1, v1);
      } else {
        uvAttr.setXY(idx, u0, v1); uvAttr.setXY(idx + 1, u1, v1);
        uvAttr.setXY(idx + 2, u0, v0); uvAttr.setXY(idx + 3, u1, v0);
      }
    }
    uvAttr.needsUpdate = true;
  }

  function createPartMesh(w, h, d, u, v, expand = 0, isOverlay = false) {
    const geom = new THREE.BoxGeometry(w + expand, h + expand, d + expand);
    setBoxUVs(geom, u, v, w, h, d);
    const mat = new THREE.MeshLambertMaterial({
      map: skinTexture,
      transparent: isOverlay,
      alphaTest: isOverlay ? 0.05 : 0,
      side: isOverlay ? THREE.DoubleSide : THREE.FrontSide
    });
    const mesh = new THREE.Mesh(geom, mat);
    mesh.userData = { w, h, d, baseExpand: expand };
    return mesh;
  }

  function init3DViewer() {
    const container = document.getElementById('viewer3d');
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(42, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, 2, 48); // %80 karakter görünümü (1 tık scroll mesafesinde)

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    scene.add(new THREE.AmbientLight(0xffffff, 0.78));
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.45);
    dirLight.position.set(20, 35, 30);
    scene.add(dirLight);

    skinTexture = new THREE.CanvasTexture(skinCanvas);
    skinTexture.magFilter = THREE.NearestFilter;
    skinTexture.minFilter = THREE.NearestFilter;

    capeTexture = new THREE.Texture();
    capeTexture.magFilter = THREE.NearestFilter;
    capeTexture.minFilter = THREE.NearestFilter;

    charGroup = new THREE.Group();
    scene.add(charGroup);

    // KAFA (y=8'de, mesh y=4'te, y: 8..16)
    headGroup = new THREE.Group();
    headGroup.position.set(0, 8, 0);
    meshes.headBase = createPartMesh(8, 8, 8, 0, 0, 0, false);
    meshes.hat = createPartMesh(8, 8, 8, 32, 0, 0.6, true);
    meshes.headBase.position.y = 4;
    meshes.hat.position.y = 4;
    headGroup.add(meshes.headBase, meshes.hat);

    // GÖVDE (y=2'de, mesh y=0'da, y: -4..8)
    bodyGroup = new THREE.Group();
    bodyGroup.position.set(0, 2, 0);
    meshes.bodyBase = createPartMesh(8, 12, 4, 16, 16, 0, false);
    meshes.jacket = createPartMesh(8, 12, 4, 16, 32, 0.5, true);
    bodyGroup.add(meshes.bodyBase, meshes.jacket);

    // SAĞ KOL (y=8'de omuz, mesh y=-6'da, y: -4..8)
    rightArmGroup = new THREE.Group();
    rightArmGroup.position.set(-6, 8, 0);
    meshes.rightArmBase = createPartMesh(4, 12, 4, 40, 16, 0, false);
    meshes.rightSleeve = createPartMesh(4, 12, 4, 40, 32, 0.5, true);
    meshes.rightArmBase.position.y = -6;
    meshes.rightSleeve.position.y = -6;
    rightArmGroup.add(meshes.rightArmBase, meshes.rightSleeve);

    // SOL KOL (y=8'de omuz, mesh y=-6'da, y: -4..8)
    leftArmGroup = new THREE.Group();
    leftArmGroup.position.set(6, 8, 0);
    meshes.leftArmBase = createPartMesh(4, 12, 4, 32, 48, 0, false);
    meshes.leftSleeve = createPartMesh(4, 12, 4, 48, 48, 0.5, true);
    meshes.leftArmBase.position.y = -6;
    meshes.leftSleeve.position.y = -6;
    leftArmGroup.add(meshes.leftArmBase, meshes.leftSleeve);

    // SAĞ BACAK (y=-4'te kalça, mesh y=-6'da, y: -16..-4)
    rightLegGroup = new THREE.Group();
    rightLegGroup.position.set(-2, -4, 0);
    meshes.rightLegBase = createPartMesh(4, 12, 4, 0, 16, 0, false);
    meshes.rightPant = createPartMesh(4, 12, 4, 0, 32, 0.5, true);
    meshes.rightLegBase.position.y = -6;
    meshes.rightPant.position.y = -6;
    rightLegGroup.add(meshes.rightLegBase, meshes.rightPant);

    // SOL BACAK (y=-4'te kalça, mesh y=-6'da, y: -16..-4)
    leftLegGroup = new THREE.Group();
    leftLegGroup.position.set(2, -4, 0);
    meshes.leftLegBase = createPartMesh(4, 12, 4, 16, 48, 0, false);
    meshes.leftPant = createPartMesh(4, 12, 4, 0, 48, 0.5, true);
    meshes.leftLegBase.position.y = -6;
    meshes.leftPant.position.y = -6;
    leftLegGroup.add(meshes.leftLegBase, meshes.leftPant);

    // PELERİN (bodyGroup'a bağlı, y=6, z=-2.1'de; asla gövdeyi delmez!)
    capePivot = new THREE.Group();
    capePivot.position.set(0, 6, -2.1);
    const capeBox = new THREE.BoxGeometry(10, 16, 1);
    setCapeBoxUVs(capeBox);
    const capeMat = new THREE.MeshLambertMaterial({
      map: capeTexture,
      side: THREE.DoubleSide,
      transparent: true,
      alphaTest: 1e-5
    });
    capeMesh = new THREE.Mesh(capeBox, capeMat);
    capeMesh.position.set(0, -8, -0.5);
    capePivot.add(capeMesh);
    capePivot.rotation.x = 0.12;
    capePivot.visible = false;
    bodyGroup.add(capePivot);

    // ELYTRA (bodyGroup'a bağlı, y=6, z=-2.1)
    elytraPivot = new THREE.Group();
    elytraPivot.position.set(0, 6, -2.1);
    const elytraMat = new THREE.MeshLambertMaterial({
      map: capeTexture,
      side: THREE.DoubleSide,
      transparent: true,
      alphaTest: 1e-5
    });
    elytraLeftWing = new THREE.Group();
    elytraLeftWing.position.set(5, 0, 0);
    const leftWingBox = new THREE.BoxGeometry(10, 20, 2);
    setBoxUVs(leftWingBox, 22, 0, 10, 20, 2, 64, 32);
    leftWingMesh = new THREE.Mesh(leftWingBox, elytraMat);
    leftWingMesh.position.set(-5, -10, -1);
    elytraLeftWing.add(leftWingMesh);
    elytraPivot.add(elytraLeftWing);

    elytraRightWing = new THREE.Group();
    elytraRightWing.position.set(-5, 0, 0);
    const rightWingBox = new THREE.BoxGeometry(10, 20, 2);
    setBoxUVs(rightWingBox, 22, 0, 10, 20, 2, 64, 32);
    rightWingMesh = new THREE.Mesh(rightWingBox, elytraMat);
    rightWingMesh.scale.x = -1;
    rightWingMesh.position.set(5, -10, -1);
    elytraRightWing.add(rightWingMesh);
    elytraPivot.add(elytraRightWing);

    elytraLeftWing.rotation.set(0.2618, 0.01, 0.2618);
    elytraRightWing.rotation.set(0.2618, -0.01, -0.2618);
    elytraPivot.visible = false;
    bodyGroup.add(elytraPivot);

    charGroup.add(headGroup, bodyGroup, rightArmGroup, leftArmGroup, rightLegGroup, leftLegGroup);
    charGroup.rotation.y = 0.45;

    // POINTER KONTROLLERİ
    let isDragging = false, prevX = 0, prevY = 0;
    container.addEventListener('pointerdown', e => { isDragging = true; prevX = e.clientX; prevY = e.clientY; });
    window.addEventListener('pointerup', () => isDragging = false);
    window.addEventListener('pointermove', e => {
      if (!isDragging) return;
      charGroup.rotation.y += (e.clientX - prevX) * 0.012;
      charGroup.rotation.x = Math.max(-1.2, Math.min(1.2, charGroup.rotation.x + (e.clientY - prevY) * 0.012));
      prevX = e.clientX; prevY = e.clientY;
    });
    container.addEventListener('wheel', e => {
      e.preventDefault();
      camera.position.z = Math.max(18, Math.min(95, camera.position.z + e.deltaY * 0.03));
    }, { passive: false });

    const update3DSize = () => {
      if (!container || !renderer || !camera) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };
    window.addEventListener('resize', update3DSize);
    if (window.ResizeObserver) {
      new ResizeObserver(update3DSize).observe(container);
    }

    animate3D();
  }

  // ANİMASYON DÖNGÜSÜ (KUSURSUZ DOĞAL HAREKETLER & SERBEST 3D DÖNDÜRME)
  function animate3D() {
    requestAnimationFrame(animate3D);
    const speed = parseFloat(document.getElementById('speedSlider').value) / 100;
    animTime += 0.045 * speed;

    if (currentAnim === 'walk') {
      rightArmGroup.rotation.x = Math.sin(animTime) * 0.65;
      leftArmGroup.rotation.x = -Math.sin(animTime) * 0.65;
      rightLegGroup.rotation.x = -Math.sin(animTime) * 0.65;
      leftLegGroup.rotation.x = Math.sin(animTime) * 0.65;
      rightArmGroup.rotation.z = 0;
      leftArmGroup.rotation.z = 0;
      headGroup.rotation.y = Math.sin(animTime * 0.5) * 0.15;
      headGroup.rotation.x = 0;
      charGroup.position.y = Math.abs(Math.cos(animTime)) * 0.4;
      if (capePivot) capePivot.rotation.x = 0.12 + Math.abs(Math.sin(animTime)) * 0.25;
      if (elytraLeftWing) elytraLeftWing.rotation.z = 0.2618 + Math.abs(Math.sin(animTime)) * 0.12;
      if (elytraRightWing) elytraRightWing.rotation.z = -0.2618 - Math.abs(Math.sin(animTime)) * 0.12;
    } else if (currentAnim === 'run') {
      const t = animTime * 1.8;
      rightArmGroup.rotation.x = Math.sin(t) * 1.2;
      leftArmGroup.rotation.x = -Math.sin(t) * 1.2;
      rightLegGroup.rotation.x = -Math.sin(t) * 1.2;
      leftLegGroup.rotation.x = Math.sin(t) * 1.2;
      rightArmGroup.rotation.z = 0;
      leftArmGroup.rotation.z = 0;
      headGroup.rotation.x = 0;
      headGroup.rotation.y = 0;
      charGroup.position.y = Math.abs(Math.cos(t)) * 0.8;
      if (capePivot) capePivot.rotation.x = 0.45 + Math.abs(Math.sin(t)) * 0.35;
      if (elytraLeftWing) elytraLeftWing.rotation.z = 0.45 + Math.abs(Math.sin(t)) * 0.15;
      if (elytraRightWing) elytraRightWing.rotation.z = -0.45 - Math.abs(Math.sin(t)) * 0.15;
    } else if (currentAnim === 'idle') {
      rightArmGroup.rotation.x = Math.sin(animTime * 0.5) * 0.06;
      leftArmGroup.rotation.x = -Math.sin(animTime * 0.5) * 0.06;
      rightArmGroup.rotation.z = -0.05 - Math.cos(animTime * 0.5) * 0.04;
      leftArmGroup.rotation.z = 0.05 + Math.cos(animTime * 0.5) * 0.04;
      rightLegGroup.rotation.x = 0; leftLegGroup.rotation.x = 0;
      headGroup.rotation.y = Math.sin(animTime * 0.3) * 0.2;
      headGroup.rotation.x = 0;
      charGroup.position.y = 0;
      if (capePivot) capePivot.rotation.x = 0.12 + Math.sin(animTime * 0.5) * 0.03;
      if (elytraLeftWing) elytraLeftWing.rotation.z = 0.2618;
      if (elytraRightWing) elytraRightWing.rotation.z = -0.2618;
    } else if (currentAnim === 'wave') {
      charGroup.position.y = 0;
      headGroup.rotation.y = 0.2;
      headGroup.rotation.x = 0;
      leftArmGroup.rotation.x = 0; leftArmGroup.rotation.z = 0;
      rightArmGroup.rotation.x = -2.6;
      rightArmGroup.rotation.z = -0.3 + Math.sin(animTime * 2.5) * 0.35;
      rightLegGroup.rotation.x = 0; leftLegGroup.rotation.x = 0;
      if (capePivot) capePivot.rotation.x = 0.12;
    } else if (currentAnim === 'fly') {
      // Orijinal hatasız uçuş: charGroup.rotation.x ezilmez, serbestçe döner!
      rightArmGroup.rotation.x = 0.35; leftArmGroup.rotation.x = 0.35;
      rightArmGroup.rotation.z = -0.25; leftArmGroup.rotation.z = 0.25;
      rightLegGroup.rotation.x = 0.25; leftLegGroup.rotation.x = 0.25;
      headGroup.rotation.x = 0;
      headGroup.rotation.y = 0;
      charGroup.position.y = Math.sin(animTime) * 1.2;
      if (capePivot) capePivot.rotation.x = 0.45 + Math.sin(animTime) * 0.1;
      if (elytraLeftWing) elytraLeftWing.rotation.set(0.2618, 0.01, 0.2618);
      if (elytraRightWing) elytraRightWing.rotation.set(0.2618, -0.01, -0.2618);
    } else if (currentAnim === 'none') {
      charGroup.position.y = 0;
      const hDeg = parseFloat(document.getElementById('poseHead').value);
      const aDeg = parseFloat(document.getElementById('poseArms').value);
      const lDeg = parseFloat(document.getElementById('poseLegs').value);
      headGroup.rotation.y = THREE.MathUtils.degToRad(hDeg);
      headGroup.rotation.x = 0;
      rightArmGroup.rotation.x = THREE.MathUtils.degToRad(aDeg);
      leftArmGroup.rotation.x = THREE.MathUtils.degToRad(-aDeg);
      rightLegGroup.rotation.x = THREE.MathUtils.degToRad(lDeg);
      leftLegGroup.rotation.x = THREE.MathUtils.degToRad(-lDeg);
      rightArmGroup.rotation.z = 0;
      leftArmGroup.rotation.z = 0;
      if (capePivot) capePivot.rotation.x = 0.12;
      if (elytraLeftWing) elytraLeftWing.rotation.set(0.2618, 0.01, 0.2618);
      if (elytraRightWing) elytraRightWing.rotation.set(0.2618, -0.01, -0.2618);
    }

    renderer.render(scene, camera);
  }

  // PELERİN GÖRÜNÜRLÜĞÜ MODLARI
  function setCapeMode(mode) {
    currentCapeMode = mode;
    document.getElementById('btnModeCape').classList.toggle('active', mode === 'cape');
    document.getElementById('btnModeElytra').classList.toggle('active', mode === 'elytra');
    document.getElementById('btnModeNone').classList.toggle('active', mode === 'none');

    const badge = document.getElementById('capeModeBadge');
    if (capePivot) capePivot.visible = (mode === 'cape');
    if (elytraPivot) elytraPivot.visible = (mode === 'elytra');

    if (mode === 'cape') {
      badge.textContent = 'Pelerin: Aktif';
      badge.style.display = 'block';
    } else if (mode === 'elytra') {
      badge.textContent = 'Elytra: Aktif';
      badge.style.display = 'block';
    } else {
      badge.style.display = 'none';
    }
  }

  document.getElementById('btnModeCape').addEventListener('click', () => setCapeMode('cape'));
  document.getElementById('btnModeElytra').addEventListener('click', () => setCapeMode('elytra'));
  document.getElementById('btnModeNone').addEventListener('click', () => setCapeMode('none'));

  // ANİMASYON DÜĞMELERİ
  document.querySelectorAll('#animGroup .chip-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#animGroup .chip-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentAnim = btn.getAttribute('data-anim');
    });
  });

  // KATMAN AÇ / KAPAT DÜĞMELERİ
  document.querySelectorAll('[data-layer]').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.classList.toggle('active');
      const layer = btn.getAttribute('data-layer');
      const isVis = btn.classList.contains('active');
      if (layer === 'arms') {
        if (meshes.rightSleeve) meshes.rightSleeve.visible = isVis;
        if (meshes.leftSleeve) meshes.leftSleeve.visible = isVis;
      } else if (layer === 'pants') {
        if (meshes.rightPant) meshes.rightPant.visible = isVis;
        if (meshes.leftPant) meshes.leftPant.visible = isVis;
      } else if (layer === 'armsBase') {
        if (meshes.rightArmBase) meshes.rightArmBase.visible = isVis;
        if (meshes.leftArmBase) meshes.leftArmBase.visible = isVis;
      } else if (layer === 'legsBase') {
        if (meshes.rightLegBase) meshes.rightLegBase.visible = isVis;
        if (meshes.leftLegBase) meshes.leftLegBase.visible = isVis;
      } else if (meshes[layer]) {
        meshes[layer].visible = isVis;
      }
    });
  });

  // EXPLODE (KATMANLARI AYIR)
  document.getElementById('explodeSlider').addEventListener('input', e => {
    const val = parseFloat(e.target.value);
    document.getElementById('explodeVal').textContent = `${val}%`;
    const scale = 1 + (val / 100) * 0.35;
    ['hat', 'jacket', 'rightSleeve', 'leftSleeve', 'rightPant', 'leftPant'].forEach(k => {
      if (meshes[k]) meshes[k].scale.set(scale, scale, scale);
    });
  });

  // SLIDER DEĞERLERİNİ ETİKETE YANSITMA & MANUEL POZ
  document.getElementById('speedSlider').addEventListener('input', e => {
    document.getElementById('speedVal').textContent = e.target.value + '%';
  });
  
  ['poseHead', 'poseArms', 'poseLegs'].forEach(id => {
    document.getElementById(id).addEventListener('input', () => {
      if (currentAnim !== 'none') {
        document.querySelectorAll('#animGroup .chip-btn').forEach(b => b.classList.remove('active'));
        document.querySelector('[data-anim="none"]').classList.add('active');
        currentAnim = 'none';
      }
      document.getElementById('poseHeadVal').textContent = document.getElementById('poseHead').value + '°';
      document.getElementById('poseArmsVal').textContent = document.getElementById('poseArms').value + '°';
      document.getElementById('poseLegsVal').textContent = document.getElementById('poseLegs').value + '°';
    });
  });

  // ==========================================
  // PELERİN YÖNETİMİ & TEKNOİST PROFİL FİLTRESİ
  // ==========================================
  function setCapeFilter(filter) {
    currentCapeFilter = filter;
    document.getElementById('btnFilterAll').classList.toggle('active', filter === 'all');
    document.getElementById('btnFilterOwned').classList.toggle('active', filter === 'owned');
    renderCapeGrid();
  }

  function renderCapeGrid() {
    const grid = document.getElementById('capeGrid');
    grid.innerHTML = '';

    const list = OFFICIAL_CAPES.filter(c => {
      if (currentCapeFilter === 'owned') return c.isOwned === true;
      return true;
    });

    list.forEach(c => {
      const card = document.createElement('div');
      card.className = 'cape-card' + (c.id === activeCapeId ? ' active' : '');
      card.innerHTML = `
        <img src="${c.preview}" alt="${c.name}" loading="lazy">
        <span class="cape-card-name" title="${c.name}">${c.name}</span>
        <span class="cape-badge ${c.isGold ? 'gold' : ''}">${c.badge}</span>
      `;
      card.addEventListener('click', () => {
        activeCapeId = c.id;
        document.querySelectorAll('.cape-card').forEach(el => el.classList.remove('active'));
        card.classList.add('active');
        applyCapeData(c.texture, c.name, true);
      });
      grid.appendChild(card);
    });
  }

  function applyCapeData(dataUri, capeName = 'Özel Pelerin', autoEnable = false) {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      capeTexture.image = img;
      capeTexture.needsUpdate = true;
      if (autoEnable && currentCapeMode === 'none') setCapeMode('cape');
    };
    img.src = dataUri;
  }

  document.getElementById('btnFetchCape').addEventListener('click', () => {
    const username = document.getElementById('capeUsernameInput').value.trim();
    if (!username) return;
    const capeUrl = `https://crafatar.com/capes/${username}`;
    applyCapeData(capeUrl, username + ' Pelerini', true);
  });

  document.getElementById('capeFileInput').addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      applyCapeData(ev.target.result, file.name, true);
      activeCapeId = 'custom';
      document.querySelectorAll('.cape-card').forEach(el => el.classList.remove('active'));
    };
    reader.readAsDataURL(file);
  });

  // ==========================================
  // CİLT PİKSEL ANALİZİ & RENKLENDİRME MOTORU
  // ==========================================
  function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h = 0, s = 0, l = (max + min) / 2;
    if (max !== min) {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      switch (max) {
        case r: h = (g - b) / d + (g < b ? 6 : 0); break;
        case g: h = (b - r) / d + 2; break;
        case b: h = (r - g) / d + 4; break;
      }
      h /= 6;
    }
    return [Math.round(h * 360), Math.round(s * 100), Math.round(l * 100)];
  }

  function hslToRgb(h, s, l) {
    h = ((h % 360) + 360) % 360 / 360;
    s = Math.max(0, Math.min(100, s)) / 100;
    l = Math.max(0, Math.min(100, l)) / 100;
    if (s === 0) {
      const v = Math.round(l * 255);
      return [v, v, v];
    }
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    return [
      Math.round(hue2rgb(p, q, h + 1/3) * 255),
      Math.round(hue2rgb(p, q, h) * 255),
      Math.round(hue2rgb(p, q, h - 1/3) * 255)
    ];
  }

  function hexToHsl(hex) {
    hex = hex.replace('#', '');
    return rgbToHsl(
      parseInt(hex.substring(0, 2), 16),
      parseInt(hex.substring(2, 4), 16),
      parseInt(hex.substring(4, 6), 16)
    );
  }

  const clamp = (v, min, max) => Math.max(min, Math.min(max, v));

  // AYAK VE AYAKKABI TABAN PİKSEL HARİTASI (HER İKİ AYAK İÇİN DE KUSURSUZ ÇALIŞIR)
  function isLegBottomPixel(x, y, shoeH) {
    if (shoeH <= 0) return false;

    // 1. Ayak Tabanları (Soles - Sağ ve Sol, Taban ve Dış Katman):
    const isFootSole = (
      (x >= 8 && x <= 11 && ((y >= 16 && y <= 19) || (y >= 32 && y <= 35) || (y >= 48 && y <= 51))) ||
      (x >= 24 && x <= 27 && (y >= 48 && y <= 51))
    );
    if (isFootSole) return true;

    // 2. Sağ Bacak Taban Üstü (x: 0..15, y in 32-shoeH..31):
    if (x >= 0 && x <= 15 && y >= (32 - shoeH) && y <= 31) return true;

    // 3. Sağ Bacak Dış Katman (x: 0..15, y in 48-shoeH..47):
    if (x >= 0 && x <= 15 && y >= (48 - shoeH) && y <= 47) return true;

    // 4. Sol Bacak Taban Üstü (x: 16..31, y in 64-shoeH..63):
    if (x >= 16 && x <= 31 && y >= (64 - shoeH) && y <= 63) return true;

    // 5. Sol Bacak Dış Katman (x: 0..15, y in 64-shoeH..63):
    if (x >= 0 && x <= 15 && y >= (64 - shoeH) && y <= 63) return true;

    return false;
  }

  // PİKSEL ANALİZİ (MÜCEVHER: 2 YEŞİL PİKSEL, TAÇ: 2. KATTAKİ SARI PİKSELLER, SAÇ: 1. VE 2. KATTAKİ KAHVERENGİ SAÇLAR)
  function analyzeSkinPixels(data) {
    pixelClassification = new Array(4096);
    const shoeH = parseInt(shoeHeightSlider.value, 10);

    const sums = {
      tunic: { s: 0, l: 0, count: 0 },
      pants: { s: 0, l: 0, count: 0 },
      sleeves: { s: 0, l: 0, count: 0 },
      shoes: { s: 0, l: 0, count: 0 },
      jewel: { s: 0, l: 0, count: 0 },
      crown: { s: 0, l: 0, count: 0 },
      hair: { s: 0, l: 0, count: 0 }
    };

    for (let y = 0; y < 64; y++) {
      for (let x = 0; x < 64; x++) {
        const idx = y * 64 + x;
        const i = idx * 4;
        const r = data[i], g = data[i+1], b = data[i+2], a = data[i+3];

        if (a < 10) {
          pixelClassification[idx] = { group: 'none', x, y };
          continue;
        }

        const [h, s, l] = rgbToHsl(r, g, b);
        let group = 'none';

        if (y < 16) {
          // --- KAFA BÖLGESİ (y < 16) ---
          const is_layer2 = (x >= 32);

          if (is_layer2) {
            // 2. KATMAN (Overlay / Hat)
            // Mücevher: SADECE yanyana yeşil 2 piksel (x=43, y=9 ve x=44, y=9)
            const isCrownJewel = ((x === 43 || x === 44) && y === 9);

            // Taç: 2. kattaki sarı/altın renkli pikseller (y=5..9)
            const isCrownGold = !isCrownJewel && (y >= 5 && y <= 9) && (r > 180 && g > 120 && b < 150);

            if (isCrownJewel) {
              group = 'jewel';
            } else if (isCrownGold) {
              group = 'crown';
            } else {
              // 2. kattaki taç ve mücevher dışındaki kahverengi saç parçaları!
              group = 'hair';
            }
          } else {
            // 1. KATMAN (Base Head)
            // Gözler: y=12..13, x in (9,10, 13,14)
            const isEye = (y === 12 || y === 13) && (x === 9 || x === 10 || x === 13 || x === 14);
            // Yüz ve boyun doğal ten rengi
            const isFaceSkin = ((y >= 12 && y <= 15 && x >= 8 && x <= 15 && !isEye && r > 200 && g > 90 && b > 70) ||
                                (y >= 3 && y <= 7 && x >= 16 && x <= 23 && r > 200 && g > 90 && b > 70));

            if (isEye || isFaceSkin) {
              group = 'none'; // Doğal yüz pikselleri korunur
            } else {
              // 1. kattaki saç pikselleri (tepe, yanlar, arka, kaküller, ense)
              group = 'hair';
            }
          }

          pixelClassification[idx] = {
            group, x, y,
            h, s, l, origR: r, origG: g, origB: b,
            isHeadSkin: group === 'none',
            isHair: group === 'hair',
            isCrown: group === 'crown',
            isJewel: group === 'jewel',
            isChickenPixel: false,
            isSkinTone: false,
            isBrownCuff: false
          };

        } else {
          // --- GÖVDE, KOLLAR VE BACAKLAR (y >= 16) ---
          // Ceketin arkasındaki tavuk piksel artı (28 piksel):
          const isChicken = (
            (y === 39 && x >= 34 && x <= 37) ||
            (y === 40 && x >= 34 && x <= 37) ||
            (y === 41 && x >= 33 && x <= 38) ||
            (y === 42 && x >= 33 && x <= 38) ||
            (y === 43 && x >= 34 && x <= 38) ||
            (y === 44 && x === 37) ||
            (y === 45 && (x === 36 || x === 37))
          );
          // Sırt kumaşı bölgesi (tavuğun olduğu ve etrafındaki tüm pikseller):
          const isBackJacketFabric = (x >= 32 && x <= 39 && y >= 37 && y <= 46);

          // Bacak pikselleri (Sağ Bacak Base/Overlay & Sol Bacak Base/Overlay):
          const isLeg = (
            (x >= 0 && x <= 15 && y >= 16 && y <= 47) ||
            (x >= 0 && x <= 31 && y >= 48 && y <= 63)
          );

          // Kol pikselleri (Sağ Kol Base/Overlay & Sol Kol Base/Overlay):
          const isArm = (
            (x >= 40 && x <= 63 && y >= 16 && y <= 47) ||
            (x >= 32 && x <= 63 && y >= 48 && y <= 63)
          );

          if (isLeg) {
            if (isLegBottomPixel(x, y, shoeH)) {
              group = 'shoes';
            } else {
              group = 'pants';
            }
          } else if (isArm) {
            group = 'sleeves';
          } else {
            group = 'tunic';
          }

          const isSkinTone = (r > 195 && g > 125 && b > 100 && (r >= g && g >= b));
          const isBrownCuff = (y >= 60 && y <= 63 && isArm);

          pixelClassification[idx] = {
            group, x, y,
            h, s, l, origR: r, origG: g, origB: b,
            isHeadSkin: false,
            isHair: false,
            isCrown: false,
            isJewel: false,
            isChickenPixel: isChicken,
            isBackJacketFabric: isBackJacketFabric,
            isSkinTone,
            isBrownCuff
          };
        }

        if (group !== 'none' && sums[group]) {
          sums[group].s += s;
          sums[group].l += l;
          sums[group].count++;
        }
      }
    }

    for (const g in sums) {
      if (sums[g].count > 0) {
        groupStats[g] = {
          avgS: Math.round(sums[g].s / sums[g].count),
          avgL: Math.round(sums[g].l / sums[g].count)
        };
      }
    }
  }

  // RENKLENDİRME MOTORU (TAVUK GİZLEMEDE ARKA KUMAŞA UYGUN GRADYAN VE NOISE)
  function renderRecoloredSkin() {
    if (!originalImageData) return;

    const outData = new ImageData(new Uint8ClampedArray(originalImageData.data), 64, 64);
    const data = outData.data;

    const targetColors = {
      tunic: hexToHsl(colTunic.value),
      pants: hexToHsl(colPants.value),
      sleeves: hexToHsl(colSleeves.value),
      shoes: hexToHsl(colShoes.value),
      jewel: hexToHsl(colJewel.value),
      crown: hexToHsl(colCrown.value),
      hair: hexToHsl(colHair.value)
    };

    const contrastMult = parseFloat(contrastSlider.value) / 100;
    const satMult = parseFloat(satKeepSlider.value) / 100;

    for (let idx = 0; idx < 4096; idx++) {
      const info = pixelClassification[idx];
      if (!info || info.group === 'none') continue;

      // 1. Tavuk piksel artı ve etrafındaki sırt kumaşı kontrolü:
      if (info.isChickenPixel && !hideChicken.checked) {
        // Tavuk açıkken: Orijinal 28 piksel art renkleri 100% korunur
        continue;
      }

      if (info.isBackJacketFabric && hideChicken.checked) {
        // Tavuk gizlendiğinde: Tavuk pikselleri ve etrafındaki TÜM sırt kumaşı
        // aynı kesintisiz dikey kumaş gradyanı ve dither/noise ile harmanlanır!
        // Böylece etrafta hiçbir kesiklik veya yama hissi kalmaz!
        const [tH, tS, tL] = targetColors.tunic;
        const verticalProgress = (info.y - 37) / 9.0; // 0.0 (omuz) ile 1.0 (etek)
        const gradientL = (0.5 - verticalProgress) * 6.5; // omuzda hafif aydınlık, etekte derin
        const dither = ((info.x + info.y) % 2 === 0 ? 2.5 : -2.5) * contrastMult;
        const noise = ((((info.x * 19 + info.y * 31) % 7) - 3) * 0.75) * contrastMult;
        
        const newS = clamp(tS, 0, 100);
        const newL = clamp(tL + gradientL + dither + noise, 2, 96);
        const [nR, nG, nB] = hslToRgb(tH, newS, newL);
        const i = idx * 4;
        data[i] = nR; data[i+1] = nG; data[i+2] = nB; data[i+3] = 255;
        continue;
      }

      // 2. Korumalar:
      if (keepHair.checked && info.isHair) continue;
      if (keepCrown.checked && info.isCrown) continue;
      if (keepJewel.checked && info.isJewel) continue;

      // Giysi gruplarında el ve bileklik koruması:
      if (info.group === 'tunic' || info.group === 'sleeves' || info.group === 'pants' || info.group === 'shoes') {
        if (info.isHeadSkin || info.isSkinTone || info.isBrownCuff) continue;
      }

      // 3. ÖZEL ALAN RENKLERİ (SKALA UYGULAMADAN, SEÇİLEN SAF RENKLERLE):
      if (info.isJewel) {
        // Mücevher: SADECE seçili zıt renk uygulanır, skala bozulması yapılmaz!
        const [jH, jS, jL] = targetColors.jewel;
        const facetOffset = (info.x === 44 ? -4 : 0); // Faset derinliği
        const [nR, nG, nB] = hslToRgb(jH, jS, clamp(jL + facetOffset, 5, 95));
        const i = idx * 4;
        data[i] = nR; data[i+1] = nG; data[i+2] = nB;
        continue;
      }

      if (info.isCrown) {
        // Taç: Seçilen taç rengi ve doğal altın parıltısı uygulanır
        const [cH, cS, cL] = targetColors.crown;
        const stats = groupStats.crown || { avgS: 75, avgL: 65 };
        const deltaL = (info.l - stats.avgL) * 0.85;
        const [nR, nG, nB] = hslToRgb(cH, cS, clamp(cL + deltaL, 5, 95));
        const i = idx * 4;
        data[i] = nR; data[i+1] = nG; data[i+2] = nB;
        continue;
      }

      if (info.isHair) {
        // Saç: 1. ve 2. katmandaki tüm saç piksellerine doğal saç telleri korunarak uygulanır
        const [hH, hS, hL] = targetColors.hair;
        const stats = groupStats.hair || { avgS: 45, avgL: 25 };
        const deltaL = (info.l - stats.avgL) * 0.85;
        const [nR, nG, nB] = hslToRgb(hH, hS, clamp(hL + deltaL, 5, 95));
        const i = idx * 4;
        data[i] = nR; data[i+1] = nG; data[i+2] = nB;
        continue;
      }

      // 4. GİYSİ KANALLARI (Tunic, Pants, Sleeves, Shoes):
      const [tH, tS, tL] = targetColors[info.group];
      const stats = groupStats[info.group] || { avgS: 40, avgL: 30 };

      const deltaL = info.l - stats.avgL;
      const deltaS = info.s - stats.avgS;

      const newS = clamp(tS + deltaS * satMult, 0, 100);
      const newL = clamp(tL + deltaL * contrastMult, 2, 96);

      const [nR, nG, nB] = hslToRgb(tH, newS, newL);
      const i = idx * 4;
      data[i] = nR; data[i+1] = nG; data[i+2] = nB;
    }

    skinCtx.clearRect(0, 0, 64, 64);
    skinCtx.putImageData(outData, 0, 0);
    if (skinTexture) skinTexture.needsUpdate = true;
  }

  // PALET UYGULAMA
  function applyPalette(p, btnEl = null) {
    colTunic.value = p.tunic; hexTunic.value = p.tunic.toUpperCase();
    colPants.value = p.pants; hexPants.value = p.pants.toUpperCase();
    colSleeves.value = p.sleeves; hexSleeves.value = p.sleeves.toUpperCase();
    colShoes.value = p.shoes || p.pants; hexShoes.value = (p.shoes || p.pants).toUpperCase();

    if (p.crown) {
      colCrown.value = p.crown;
      hexCrown.value = p.crown.toUpperCase();
    }
    if (p.jewel) {
      colJewel.value = p.jewel;
      hexJewel.value = p.jewel.toUpperCase();
    }

    document.querySelectorAll('.palette-btn').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
    renderRecoloredSkin();
    updateShadeInspector();
  }

  // ÖZEL ALAN ETKİLEŞİMLERİ (SKALA OLMADAN, DOĞRUDAN VE SADECE SEÇİLİ ÖĞEYE)
  function applyHairColor(hex) {
    colHair.value = hex;
    hexHair.value = hex.toUpperCase();
    keepHair.checked = false;
    renderRecoloredSkin();
  }

  colHair.addEventListener('input', () => {
    hexHair.value = colHair.value.toUpperCase();
    keepHair.checked = false;
    renderRecoloredSkin();
  });
  hexHair.addEventListener('input', () => {
    if (/^#[0-9A-Fa-f]{6}$/.test(hexHair.value)) {
      colHair.value = hexHair.value;
      keepHair.checked = false;
      renderRecoloredSkin();
    }
  });

  document.querySelectorAll('.hair-dot').forEach(dot => {
    dot.addEventListener('click', () => applyHairColor(dot.getAttribute('data-hair')));
  });

  colCrown.addEventListener('input', () => {
    hexCrown.value = colCrown.value.toUpperCase();
    keepCrown.checked = false;
    renderRecoloredSkin();
  });
  hexCrown.addEventListener('input', () => {
    if (/^#[0-9A-Fa-f]{6}$/.test(hexCrown.value)) {
      colCrown.value = hexCrown.value;
      keepCrown.checked = false;
      renderRecoloredSkin();
    }
  });

  colJewel.addEventListener('input', () => {
    hexJewel.value = colJewel.value.toUpperCase();
    keepJewel.checked = false;
    renderRecoloredSkin();
  });
  hexJewel.addEventListener('input', () => {
    if (/^#[0-9A-Fa-f]{6}$/.test(hexJewel.value)) {
      colJewel.value = hexJewel.value;
      keepJewel.checked = false;
      renderRecoloredSkin();
    }
  });

  // GİYSİ RENK SEÇİCİ BAĞLANTILARI
  const setupColorSync = (colInput, hexInput) => {
    colInput.addEventListener('input', () => {
      hexInput.value = colInput.value.toUpperCase();
      renderRecoloredSkin();
      updateShadeInspector();
    });
    hexInput.addEventListener('input', () => {
      if (/^#[0-9A-Fa-f]{6}$/.test(hexInput.value)) {
        colInput.value = hexInput.value;
        renderRecoloredSkin();
        updateShadeInspector();
      }
    });
  };

  setupColorSync(colTunic, hexTunic);
  setupColorSync(colPants, hexPants);
  setupColorSync(colSleeves, hexSleeves);
  setupColorSync(colShoes, hexShoes);

  // KORUMA & AYAR DEĞİŞİMİ
  [keepHair, keepCrown, keepJewel, hideChicken].forEach(cb => {
    cb.addEventListener('change', renderRecoloredSkin);
  });

  shoeHeightSlider.addEventListener('input', e => {
    document.getElementById('shoeHeightVal').textContent = e.target.value + ' Piksel';
    if (originalImageData) {
      analyzeSkinPixels(originalImageData.data);
      renderRecoloredSkin();
    }
  });

  contrastSlider.addEventListener('input', e => {
    document.getElementById('contrastVal').textContent = e.target.value + '%';
    renderRecoloredSkin();
  });

  satKeepSlider.addEventListener('input', e => {
    document.getElementById('satKeepVal').textContent = e.target.value + '%';
    renderRecoloredSkin();
  });

  // İNDİR BUTONU (64x64 ŞEFFFAF PNG)
  document.getElementById('downloadBtn').addEventListener('click', () => {
    const link = document.createElement('a');
    link.download = 'mc_skin_custom.png';
    link.href = skinCanvas.toDataURL('image/png');
    link.click();
  });

  // FARKLI PNG YÜKLEME
  document.getElementById('fileInput').addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      const img = new Image();
      img.onload = () => {
        skinCanvas.width = 64; skinCanvas.height = 64;
        skinCtx.clearRect(0, 0, 64, 64);
        skinCtx.drawImage(img, 0, 0, 64, 64);
        originalImageData = skinCtx.getImageData(0, 0, 64, 64);
        analyzeSkinPixels(originalImageData.data);
        renderRecoloredSkin();
      };
      img.src = ev.target.result;
    };
    reader.readAsDataURL(file);
  });

  // BAŞLANGIÇTA BASE CİLDİ YÜKLE (VARSAYILAN: PALET UYGULANMAZ, ORİJİNAL SKİN GÖSTERİLİR)
  function loadBaseSkin() {
    const img = new Image();
    img.onload = () => {
      skinCanvas.width = 64; skinCanvas.height = 64;
      skinCtx.clearRect(0, 0, 64, 64);
      skinCtx.drawImage(img, 0, 0, 64, 64);
      originalImageData = skinCtx.getImageData(0, 0, 64, 64);
      analyzeSkinPixels(originalImageData.data);
      if (skinTexture) skinTexture.needsUpdate = true;
    };
    img.src = CACHED_BASE_SKIN;
  }

  // BAŞLAT
  initTheme();
  init3DViewer();
  renderPalettes();
  renderCapeGrid();
  loadBaseSkin();
  applyCapeData(OFFICIAL_CAPES[0].texture, OFFICIAL_CAPES[0].name, false);
  setCapeMode('none'); // Varsayılan olarak pelerin GİZLİ
  updateShadeInspector();



</script>
</body>
</html>
"""

html_content = html_content.replace('__SKIN_B64__', skin_b64)
html_content = html_content.replace('__OFFICIAL_CAPES_JS__', capes_js)
html_content = html_content.replace('__PALETTES_JSON__', palettes_json)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"index.html basariyla uretildi: {len(html_content)} bayt")
