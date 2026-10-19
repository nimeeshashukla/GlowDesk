import http.server
import json
import os
import pathlib
from datetime import datetime

PORT = 8080
BASE_DIR = pathlib.Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def atomic_write(filepath: pathlib.Path, data):
    tmp_path = filepath.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, filepath)

def read_json(filename: str, default=None):
    p = DATA_DIR / filename
    if not p.exists():
        return default if default is not None else []
    try:
        with open(p, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default if default is not None else []
            return json.loads(content)
    except Exception:
        return default if default is not None else []

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>GlowDesk // Beauty, Wellness & Lifestyle OS</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;1,600&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #FAF7F5; color: #2D2424; }
    .font-serif-clean { font-family: 'Playfair Display', serif; }
    .card-aesthetic { background: #FFFFFF; border: 1px solid #F0E6E1; box-shadow: 0 4px 20px -2px rgba(226, 199, 191, 0.25); border-radius: 16px; }
    .nav-btn-active { background-color: #E11D48 !important; color: #FFFFFF !important; }
  </style>
</head>
<body class="p-5 md:p-8">

  <!-- Header -->
  <header class="flex flex-col md:flex-row justify-between items-start md:items-center pb-6 border-b border-[#F0E6E1] mb-6">
    <div>
      <div class="flex items-center gap-3">
        <h1 class="text-3xl font-extrabold tracking-tight text-[#4A3933] font-serif-clean">GlowDesk ✨</h1>
        <span class="px-3 py-1 text-xs font-bold rounded-full bg-[#FFE4E6] text-[#E11D48] tracking-wider uppercase">Self-Care Hub</span>
      </div>
      <p class="text-sm text-[#8C7A74] mt-1">Smart vanity, wellness tracking, budget management & advisor 🌸</p>
    </div>

    <!-- Navigation Bar -->
    <div class="flex flex-wrap items-center gap-2 mt-4 md:mt-0">
      <button onclick="switchView('menu')" id="btn-nav-menu" class="px-3.5 py-1.5 bg-white text-[#785950] border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-[#FAF4F0] transition nav-btn-active">🏠 Menu</button>
      <button onclick="switchView('skincare')" id="btn-nav-skincare" class="px-3.5 py-1.5 bg-white text-[#785950] border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-[#FAF4F0] transition">🧴 Vanity</button>
      <button onclick="switchView('routines')" id="btn-nav-routines" class="px-3.5 py-1.5 bg-white text-[#785950] border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-[#FAF4F0] transition">🌸 Routines</button>
      <button onclick="switchView('fitness')" id="btn-nav-fitness" class="px-3.5 py-1.5 bg-white text-[#785950] border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-[#FAF4F0] transition">🥗 Fitness</button>
      <button onclick="switchView('budget')" id="btn-nav-budget" class="px-3.5 py-1.5 bg-white text-[#785950] border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-[#FAF4F0] transition">💳 Budget</button>
      <button onclick="switchView('travel')" id="btn-nav-travel" class="px-3.5 py-1.5 bg-white text-[#785950] border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-[#FAF4F0] transition">🧳 Travel</button>
      <button onclick="switchView('advisor')" id="btn-nav-advisor" class="px-3.5 py-1.5 bg-white text-[#785950] border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-[#FAF4F0] transition">☀️ Advisor</button>
    </div>
  </header>

  <!-- ============================================================== -->
  <!-- 1. MAIN MENU                                                   -->
  <!-- ============================================================== -->
  <section id="view-menu" class="space-y-6">
    <div class="text-center max-w-xl mx-auto my-4">
      <h2 class="text-2xl font-extrabold text-[#4A3933] font-serif-clean">Self-Care Services Directory 🪞</h2>
      <p class="text-xs text-[#8C7A74] mt-1">Pick a service to open your customized dashboard 💕</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div onclick="switchView('skincare')" class="card-aesthetic p-6 cursor-pointer hover:scale-[1.02] transition-transform border-t-4 border-[#E11D48] flex flex-col justify-between">
        <div>
          <div class="w-12 h-12 rounded-2xl bg-rose-50 flex items-center justify-center text-2xl mb-3">🧴</div>
          <h3 class="text-base font-bold text-[#4A3933]">Skincare Vanity</h3>
          <p class="text-xs text-[#8C7A74] mt-1">Track bottle opening dates, PAO expiry, and stock alerts.</p>
        </div>
        <div class="mt-4 pt-3 border-t border-[#FAF4F0] flex justify-between items-center">
          <span class="text-xs font-bold text-[#E11D48]">Open Vanity ➔</span>
          <span id="badge-menu-prods" class="text-[10px] px-2 py-0.5 rounded bg-rose-50 text-rose-600 font-bold">0 Items</span>
        </div>
      </div>

      <div onclick="switchView('routines')" class="card-aesthetic p-6 cursor-pointer hover:scale-[1.02] transition-transform border-t-4 border-amber-400 flex flex-col justify-between">
        <div>
          <div class="w-12 h-12 rounded-2xl bg-amber-50 flex items-center justify-center text-2xl mb-3">🌸</div>
          <h3 class="text-base font-bold text-[#4A3933]">AM / PM Routines</h3>
          <p class="text-xs text-[#8C7A74] mt-1">Daily morning & night steps with progress counters.</p>
        </div>
        <div class="mt-4 pt-3 border-t border-[#FAF4F0] flex justify-between items-center">
          <span class="text-xs font-bold text-amber-600">Open Routines ➔</span>
          <span class="text-[10px] px-2 py-0.5 rounded bg-amber-50 text-amber-700 font-bold">Checklist</span>
        </div>
      </div>

      <div onclick="switchView('fitness')" class="card-aesthetic p-6 cursor-pointer hover:scale-[1.02] transition-transform border-t-4 border-emerald-400 flex flex-col justify-between">
        <div>
          <div class="w-12 h-12 rounded-2xl bg-emerald-50 flex items-center justify-center text-2xl mb-3">🥗</div>
          <h3 class="text-base font-bold text-[#4A3933]">Fitness & Wellness</h3>
          <p class="text-xs text-[#8C7A74] mt-1">Track daily calories, interactive water glasses, and body vitals.</p>
        </div>
        <div class="mt-4 pt-3 border-t border-[#FAF4F0] flex justify-between items-center">
          <span class="text-xs font-bold text-emerald-600">Open Fitness ➔</span>
          <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-bold">Vitals</span>
        </div>
      </div>

      <div onclick="switchView('budget')" class="card-aesthetic p-6 cursor-pointer hover:scale-[1.02] transition-transform border-t-4 border-purple-400 flex flex-col justify-between">
        <div>
          <div class="w-12 h-12 rounded-2xl bg-purple-50 flex items-center justify-center text-2xl mb-3">💳</div>
          <h3 class="text-base font-bold text-[#4A3933]">Beauty Budget & Hauls</h3>
          <p class="text-xs text-[#8C7A74] mt-1">Track monthly spending limits, new purchases, and spending charts in ₹.</p>
        </div>
        <div class="mt-4 pt-3 border-t border-[#FAF4F0] flex justify-between items-center">
          <span class="text-xs font-bold text-purple-600">Open Budget ➔</span>
          <span id="badge-menu-budget" class="text-[10px] px-2 py-0.5 rounded bg-purple-50 text-purple-700 font-bold">₹0 Spent</span>
        </div>
      </div>

      <div onclick="switchView('travel')" class="card-aesthetic p-6 cursor-pointer hover:scale-[1.02] transition-transform border-t-4 border-blue-400 flex flex-col justify-between">
        <div>
          <div class="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center text-2xl mb-3">🧳</div>
          <h3 class="text-base font-bold text-[#4A3933]">Travel Bag & TSA Check</h3>
          <p class="text-xs text-[#8C7A74] mt-1">Smart packing assistant with 100ml liquid cabin safety rules.</p>
        </div>
        <div class="mt-4 pt-3 border-t border-[#FAF4F0] flex justify-between items-center">
          <span class="text-xs font-bold text-blue-600">Open Travel ➔</span>
          <span id="badge-menu-travel" class="text-[10px] px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-bold">Packing List</span>
        </div>
      </div>

      <div onclick="switchView('advisor')" class="card-aesthetic p-6 cursor-pointer hover:scale-[1.02] transition-transform border-t-4 border-sky-400 flex flex-col justify-between">
        <div>
          <div class="w-12 h-12 rounded-2xl bg-sky-50 flex items-center justify-center text-2xl mb-3">☀️</div>
          <h3 class="text-base font-bold text-[#4A3933]">Sun, Air & Skin Cycling</h3>
          <p class="text-xs text-[#8C7A74] mt-1">UV radiation, pollution alerts & 4-night skin cycle guide.</p>
        </div>
        <div class="mt-4 pt-3 border-t border-[#FAF4F0] flex justify-between items-center">
          <span class="text-xs font-bold text-sky-600">Open Advisor ➔</span>
          <span class="text-[10px] px-2 py-0.5 rounded bg-sky-50 text-sky-700 font-bold">UV, AQI & Cycling</span>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================================================== -->
  <!-- 2. BUDGET VIEW (IN RUPEES ₹)                                    -->
  <!-- ============================================================== -->
  <section id="view-budget" class="hidden space-y-6">
    <div class="flex justify-between items-center">
      <button onclick="switchView('menu')" class="px-3.5 py-1.5 bg-white border border-[#E8DCD5] rounded-xl text-xs font-bold text-[#785950] hover:bg-[#FAF4F0] flex items-center gap-1.5 shadow-sm">
        <span>←</span> <span>Back to Main Menu</span>
      </button>
      <button onclick="document.getElementById('modal-haul').classList.remove('hidden')" class="px-4 py-1.5 bg-purple-600 text-white rounded-xl text-xs font-bold shadow-md hover:bg-purple-700 transition">+ Log Beauty Haul</button>
    </div>

    <!-- Budget Status Cards in ₹ -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card-aesthetic p-4 border-l-4 border-purple-500">
        <span class="text-[10px] uppercase font-bold text-[#8C7A74]">Monthly Allowance</span>
        <h3 id="budget-limit-val" class="text-2xl font-black text-[#4A3933] mt-1">₹5,000</h3>
        <p class="text-[11px] text-purple-600 font-semibold mt-1">Monthly Beauty Cap</p>
      </div>
      <div class="card-aesthetic p-4 border-l-4 border-rose-500">
        <span class="text-[10px] uppercase font-bold text-[#8C7A74]">Total Spent This Month</span>
        <h3 id="budget-spent-val" class="text-2xl font-black text-rose-600 mt-1">₹0</h3>
        <p id="budget-pct-text" class="text-[11px] text-[#8C7A74] font-semibold mt-1">0% utilized</p>
      </div>
      <div class="card-aesthetic p-4 border-l-4 border-emerald-500">
        <span class="text-[10px] uppercase font-bold text-[#8C7A74]">Remaining Safe Buffer</span>
        <h3 id="budget-left-val" class="text-2xl font-black text-emerald-600 mt-1">₹5,000</h3>
        <p class="text-[11px] text-emerald-600 font-semibold mt-1">Available to spend ✨</p>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="card-aesthetic p-4">
      <div class="flex justify-between text-xs font-bold mb-1">
        <span class="text-[#4A3933]">Monthly Spending Gauge</span>
        <span id="budget-progress-label" class="text-purple-600">0%</span>
      </div>
      <div class="w-full bg-[#FAF7F5] rounded-full h-3 border border-[#F0E6E1] overflow-hidden">
        <div id="budget-progress-bar" class="bg-purple-500 h-3 rounded-full transition-all duration-500" style="width: 0%"></div>
      </div>
    </div>

    <!-- Hauls Table & Spending Chart -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="card-aesthetic p-5">
        <h4 class="text-xs font-bold text-[#4A3933] uppercase tracking-wider mb-2">Recent Beauty Purchases 🛍️</h4>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="border-b border-[#F5ECE8] uppercase font-bold text-[#8C7A74]">
                <th class="py-2">Item</th>
                <th class="py-2">Category</th>
                <th class="py-2">Date</th>
                <th class="py-2 text-right">Cost (₹)</th>
              </tr>
            </thead>
            <tbody id="haul-rows"></tbody>
          </table>
        </div>
      </div>

      <div class="card-aesthetic p-5">
        <h4 class="text-xs font-bold text-[#4A3933] uppercase tracking-wider mb-2">Category Spend Breakdown 📊</h4>
        <div class="h-56 flex justify-center">
          <canvas id="chart-budget"></canvas>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================================================== -->
  <!-- 3. EXPANDED ADVISOR VIEW                                       -->
  <!-- ============================================================== -->
  <section id="view-advisor" class="hidden space-y-6">
    <div class="flex justify-between items-center">
      <button onclick="switchView('menu')" class="px-3.5 py-1.5 bg-white border border-[#E8DCD5] rounded-xl text-xs font-bold text-[#785950] hover:bg-[#FAF4F0] flex items-center gap-1.5 shadow-sm">
        <span>←</span> <span>Back to Main Menu</span>
      </button>
      <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 font-bold border border-amber-200">Environmental Telemetry</span>
    </div>

    <div class="p-5 rounded-2xl bg-gradient-to-r from-amber-50 via-rose-50 to-orange-50 border border-amber-200 flex flex-col md:flex-row justify-between items-center gap-4">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-amber-400/20 flex items-center justify-center text-2xl">☀️</div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold uppercase tracking-wider text-amber-800">Campus Solar Guide</span>
            <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-amber-200 text-amber-900">UV 7.4 (High Exposure)</span>
          </div>
          <p class="text-xs text-[#785950] mt-0.5">High sun hours active! Reapply sunscreen every 2 hours when outside.</p>
        </div>
      </div>
      <button onclick="reapplySPF()" class="px-4 py-2 bg-amber-600 text-white rounded-xl text-xs font-bold shadow hover:bg-amber-700 transition">🧴 Reapplied SPF Now</button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="card-aesthetic p-5 border-t-4 border-slate-400">
        <div class="flex justify-between items-start mb-2">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500">Environmental Barrier Alert</span>
            <h4 class="text-base font-bold text-[#4A3933]">Air Quality & Pollution Shield 🌫️</h4>
          </div>
          <span id="aqi-badge" class="px-2 py-0.5 rounded text-[10px] font-bold bg-orange-100 text-orange-800">AQI 118 (Moderate Smog)</span>
        </div>
        <p class="text-xs text-[#785950] mt-1">Particulate matter clogs open pores and weakens lipid barriers.</p>
        <div class="p-3 bg-[#FAF7F5] rounded-xl border border-[#F0E6E1] mt-3">
          <span class="text-[11px] font-bold text-[#4A3933]">🛡️ Recommended Barrier Defense:</span>
          <p id="aqi-tip" class="text-xs text-[#785950] mt-0.5">Double cleanse tonight with an oil/cleansing balm to dissolve micro-dust, and apply an antioxidant Vitamin C serum tomorrow morning!</p>
        </div>
        <div class="flex gap-2 mt-3">
          <button onclick="setAQI('Clean', 35)" class="px-2.5 py-1 bg-white border rounded text-[11px] font-semibold hover:bg-gray-50">Clean Campus Air 🌿</button>
          <button onclick="setAQI('Smog', 165)" class="px-2.5 py-1 bg-white border rounded text-[11px] font-semibold hover:bg-gray-50">High Smog / Dust ⚠️</button>
        </div>
      </div>

      <div class="card-aesthetic p-5 border-t-4 border-indigo-400">
        <div class="flex justify-between items-start mb-2">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-500">Dermatologist Cadence</span>
            <h4 class="text-base font-bold text-[#4A3933]">4-Night Skin Cycling Guide 🌙</h4>
          </div>
          <span id="cycle-badge" class="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-800">Night 2: Retinoid 🧴</span>
        </div>
        <p class="text-xs text-[#785950] mt-1">Prevents over-exfoliation and barrier burns by spacing potent actives.</p>
        <div class="p-3 bg-[#FAF7F5] rounded-xl border border-[#F0E6E1] mt-3">
          <span id="cycle-step-name" class="text-[11px] font-bold text-indigo-700">Tonight's Step: Cell Turnover & Retinol</span>
          <p id="cycle-step-desc" class="text-xs text-[#785950] mt-0.5">Use your 0.5% Encapsulated Retinol on clean dry skin, then sandwich with a rich barrier moisturizer. No acids tonight!</p>
        </div>
        <div class="flex justify-between items-center mt-3 pt-2">
          <span class="text-[11px] text-[#8C7A74]">Rotate to tomorrow night:</span>
          <button onclick="nextSkinCycle()" class="px-3 py-1 bg-indigo-600 text-white rounded-lg text-xs font-bold hover:bg-indigo-700 transition">Next Night ➔</button>
        </div>
      </div>
    </div>

    <div class="card-aesthetic p-5">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 mb-2">
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-teal-800">Weather & Seasonal Advice 🌡️</span>
          <h3 id="climate-badge" class="text-base font-bold text-[#4A3933] mt-0.5">Dry Air / AC (32% Humidity)</h3>
          <p id="climate-recommendation" class="text-xs text-[#785950] mt-1">Air is crisp and dry. Layer a hyaluronic mist and seal with a rich ceramide cream.</p>
        </div>
        <div class="flex gap-2">
          <button onclick="setClimate('Dry Air')" class="px-3 py-1.5 bg-white border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-gray-50">Dry Air 🏜️</button>
          <button onclick="setClimate('Humid')" class="px-3 py-1.5 bg-white border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-gray-50">Humid 🌧️</button>
          <button onclick="setClimate('Cold Winter')" class="px-3 py-1.5 bg-white border border-[#E8DCD5] rounded-xl text-xs font-bold hover:bg-gray-50">Cold ❄️</button>
        </div>
      </div>
    </div>

    <div class="card-aesthetic p-5">
      <h4 class="text-xs font-bold text-[#4A3933] uppercase tracking-wider mb-1">Hourly Campus UV Radiation Curve</h4>
      <div class="h-56"><canvas id="chart-uv"></canvas></div>
    </div>
  </section>

  <!-- ============================================================== -->
  <!-- 4. SKINCARE VANITY VIEW                                        -->
  <!-- ============================================================== -->
  <section id="view-skincare" class="hidden space-y-6">
    <div class="flex justify-between items-center">
      <button onclick="switchView('menu')" class="px-3.5 py-1.5 bg-white border border-[#E8DCD5] rounded-xl text-xs font-bold text-[#785950] hover:bg-[#FAF4F0] flex items-center gap-1.5 shadow-sm">
        <span>←</span> <span>Back to Main Menu</span>
      </button>
      <button onclick="document.getElementById('modal-add').classList.remove('hidden')" class="px-4 py-1.5 bg-[#E11D48] text-white rounded-xl text-xs font-bold shadow-md hover:bg-[#BE123C]">+ New Product</button>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="card-aesthetic p-4 border-l-4 border-[#E11D48]">
        <p class="text-[11px] uppercase font-bold text-[#8C7A74]">Total Products</p>
        <h2 id="kpi-total" class="text-2xl font-black text-[#4A3933] mt-1">0</h2>
      </div>
      <div class="card-aesthetic p-4 border-l-4 border-amber-400">
        <p class="text-[11px] uppercase font-bold text-[#8C7A74]">Needs Attention</p>
        <h2 id="kpi-expiring" class="text-2xl font-black text-amber-600 mt-1">0</h2>
      </div>
      <div class="card-aesthetic p-4 border-l-4 border-emerald-400">
        <p class="text-[11px] uppercase font-bold text-[#8C7A74]">Skin Glow</p>
        <h2 class="text-2xl font-black text-emerald-600 mt-1">92 / 100</h2>
      </div>
      <div class="card-aesthetic p-4 border-l-4 border-purple-400">
        <p class="text-[11px] uppercase font-bold text-[#8C7A74]">Restock Low</p>
        <h2 class="text-2xl font-black text-purple-600 mt-1">2</h2>
      </div>
    </div>

    <div class="card-aesthetic p-5">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 mb-4">
        <h3 class="text-base font-bold text-[#4A3933]">Skincare Shelf & Expiry Status 🧴</h3>
        <div class="flex items-center gap-1.5 bg-[#FAF7F5] p-1 rounded-xl border border-[#F0E6E1] text-xs">
          <span class="text-[10px] font-bold text-[#8C7A74] px-2 uppercase">Filter:</span>
          <button onclick="filterShelf('All')" class="filter-btn px-2.5 py-1 rounded-lg font-bold bg-[#E11D48] text-white">All</button>
          <button onclick="filterShelf('Hydration')" class="filter-btn px-2.5 py-1 rounded-lg font-semibold text-[#785950] hover:bg-white">Dry</button>
          <button onclick="filterShelf('Actives')" class="filter-btn px-2.5 py-1 rounded-lg font-semibold text-[#785950] hover:bg-white">Oily</button>
          <button onclick="filterShelf('Sun Protection')" class="filter-btn px-2.5 py-1 rounded-lg font-semibold text-[#785950] hover:bg-white">Sunscreen</button>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="border-b border-[#F5ECE8] uppercase font-bold text-[#8C7A74]">
              <th class="py-2.5 px-3">Name</th>
              <th class="py-2.5 px-3">Brand</th>
              <th class="py-2.5 px-3">Category</th>
              <th class="py-2.5 px-3">Shelf Left</th>
              <th class="py-2.5 px-3">Status</th>
              <th class="py-2.5 px-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody id="product-rows"></tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- ============================================================== -->
  <!-- 5. ROUTINES VIEW                                               -->
  <!-- ============================================================== -->
  <section id="view-routines" class="hidden space-y-6">
    <div class="flex justify-between items-center">
      <button onclick="switchView('menu')" class="px-3.5 py-1.5 bg-white border border-[#E8DCD5] rounded-xl text-xs font-bold text-[#785950] hover:bg-[#FAF4F0] flex items-center gap-1.5 shadow-sm">
        <span>←</span> <span>Back to Main Menu</span>
      </button>
      <span id="routine-status-badge" class="text-xs px-3 py-1 rounded-full bg-rose-50 text-rose-600 font-bold border border-rose-200">0% Done</span>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="card-aesthetic p-5 border-t-4 border-amber-400">
        <span class="text-xs font-bold text-amber-700 uppercase">☀️ Morning Routine (AM)</span>
        <div class="space-y-2 mt-3 text-xs">
          <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg bg-[#FAF7F5] border"><input type="checkbox" onchange="updateRoutineProgress()" class="am-step rounded accent-rose-500 w-4 h-4"><span>1. Gentle Foam Cleanser</span></label>
          <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg bg-[#FAF7F5] border"><input type="checkbox" onchange="updateRoutineProgress()" class="am-step rounded accent-rose-500 w-4 h-4"><span>2. Vitamin C Glow Serum</span></label>
          <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg bg-[#FAF7F5] border"><input type="checkbox" onchange="updateRoutineProgress()" class="am-step rounded accent-rose-500 w-4 h-4"><span>3. Barrier Moisturizer</span></label>
          <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg bg-[#FAF7F5] border"><input type="checkbox" onchange="updateRoutineProgress()" class="am-step rounded accent-rose-500 w-4 h-4"><span>4. Sunscreen (SPF 50+)</span></label>
        </div>
      </div>
      <div class="card-aesthetic p-5 border-t-4 border-indigo-400">
        <span class="text-xs font-bold text-indigo-700 uppercase">🌙 Night Routine (PM)</span>
        <div class="space-y-2 mt-3 text-xs">
          <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg bg-[#FAF7F5] border"><input type="checkbox" onchange="updateRoutineProgress()" class="pm-step rounded accent-rose-500 w-4 h-4"><span>1. Micellar Cleanser</span></label>
          <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg bg-[#FAF7F5] border"><input type="checkbox" onchange="updateRoutineProgress()" class="pm-step rounded accent-rose-500 w-4 h-4"><span>2. Hydrating Face Wash</span></label>
          <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg bg-[#FAF7F5] border"><input type="checkbox" onchange="updateRoutineProgress()" class="pm-step rounded accent-rose-500 w-4 h-4"><span>3. Treatment Retinol</span></label>
          <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg bg-[#FAF7F5] border"><input type="checkbox" onchange="updateRoutineProgress()" class="pm-step rounded accent-rose-500 w-4 h-4"><span>4. Deep Night Balm</span></label>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================================================== -->
  <!-- 6. FITNESS VIEW                                                -->
  <!-- ============================================================== -->
  <section id="view-fitness" class="hidden space-y-6">
    <div class="flex justify-between items-center">
      <button onclick="switchView('menu')" class="px-3.5 py-1.5 bg-white border border-[#E8DCD5] rounded-xl text-xs font-bold text-[#785950] hover:bg-[#FAF4F0] flex items-center gap-1.5 shadow-sm">
        <span>←</span> <span>Back to Main Menu</span>
      </button>
      <button onclick="document.getElementById('modal-wellness').classList.remove('hidden')" class="px-4 py-1.5 bg-[#E11D48] text-white rounded-xl text-xs font-bold">+ Log Vitals</button>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card-aesthetic p-5 border-t-4 border-sky-400">
        <h3 class="text-base font-bold text-[#4A3933]">Daily Water 💧</h3>
        <span id="water-display-ml" class="text-xs text-sky-600 font-bold">1500 / 2000 ml</span>
        <div class="w-full bg-[#FAF7F5] rounded-full h-3 border my-3 overflow-hidden">
          <div id="water-progress-bar" class="bg-sky-400 h-3 rounded-full" style="width: 75%"></div>
        </div>
        <div class="flex justify-between items-center text-xs">
          <span id="water-glasses-text" class="font-bold">6 of 8 Glasses</span>
          <div class="flex gap-1.5">
            <button onclick="adjustWater(-1)" class="px-2 py-1 bg-white border rounded">-1</button>
            <button onclick="adjustWater(1)" class="px-3 py-1 bg-sky-500 text-white rounded font-bold">+1 Glass</button>
          </div>
        </div>
      </div>
      <div class="card-aesthetic p-5 border-t-4 border-emerald-400">
        <h3 class="text-base font-bold text-[#4A3933]">Today's Calories 🥗</h3>
        <p id="net-cal-badge" class="text-xs font-bold text-emerald-600 mt-1">1,450 Net kcal</p>
        <div class="grid grid-cols-2 gap-2 mt-3 text-center text-xs">
          <div class="p-2 bg-[#FAF7F5] rounded border"><span class="text-[10px] text-[#8C7A74]">Intake</span><p id="cal-intake-val" class="font-bold">1850</p></div>
          <div class="p-2 bg-[#FAF7F5] rounded border"><span class="text-[10px] text-[#8C7A74]">Burned</span><p id="cal-burned-val" class="font-bold text-rose-500">-400</p></div>
        </div>
      </div>
      <div class="card-aesthetic p-5 border-t-4 border-rose-400">
        <h3 class="text-base font-bold text-[#4A3933]">Measurements 📏</h3>
        <div class="grid grid-cols-2 gap-2 mt-3 text-center text-xs">
          <div class="p-2 bg-[#FAF7F5] rounded border"><span class="text-[10px] text-[#8C7A74]">Weight</span><p id="body-weight-val" class="font-bold">53.7 kg</p></div>
          <div class="p-2 bg-[#FAF7F5] rounded border"><span class="text-[10px] text-[#8C7A74]">Waist</span><p id="body-waist-val" class="font-bold">26.2 in</p></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================================================== -->
  <!-- 7. TRAVEL VIEW                                                 -->
  <!-- ============================================================== -->
  <section id="view-travel" class="hidden space-y-6">
    <div class="flex justify-between items-center">
      <button onclick="switchView('menu')" class="px-3.5 py-1.5 bg-white border border-[#E8DCD5] rounded-xl text-xs font-bold text-[#785950] hover:bg-[#FAF4F0] flex items-center gap-1.5 shadow-sm">
        <span>←</span> <span>Back to Main Menu</span>
      </button>
      <button onclick="document.getElementById('modal-travel-item').classList.remove('hidden')" class="px-4 py-1.5 bg-blue-600 text-white rounded-xl text-xs font-bold">+ Add Bottle</button>
    </div>
    <div class="card-aesthetic p-5">
      <h3 class="text-base font-bold text-[#4A3933] mb-4">Travel Vanity Bag Checklist 🧳</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead><tr class="border-b uppercase font-bold text-[#8C7A74]"><th class="py-2 px-3">Status</th><th class="py-2 px-3">Item</th><th class="py-2 px-3">Volume</th><th class="py-2 px-3">TSA Rule</th><th class="py-2 px-3 text-right">Action</th></tr></thead>
          <tbody id="travel-rows"></tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- MODALS -->
  <div id="modal-add" class="hidden fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl">
      <h3 class="text-base font-bold text-[#4A3933] mb-4">Add Product 🧴</h3>
      <form onsubmit="submitProduct(event)" class="space-y-3 text-xs">
        <input type="text" id="p-name" placeholder="Product Name" required class="w-full border rounded-lg p-2">
        <input type="text" id="p-brand" placeholder="Brand Name" required class="w-full border rounded-lg p-2">
        <select id="p-category" class="w-full border rounded-lg p-2">
          <option value="Hydration">Hydration</option>
          <option value="Actives">Actives</option>
          <option value="Sun Protection">Sun Protection</option>
          <option value="Cleanser">Cleanser</option>
          <option value="Barrier Cream">Barrier Cream</option>
        </select>
        <input type="number" id="p-pao" value="6" placeholder="PAO (Months)" required class="w-full border rounded-lg p-2">
        <div class="flex justify-end gap-2 pt-2">
          <button type="button" onclick="document.getElementById('modal-add').classList.add('hidden')" class="px-3 py-1.5">Cancel</button>
          <button type="submit" class="px-4 py-1.5 bg-[#E11D48] text-white rounded-lg font-bold">Save</button>
        </div>
      </form>
    </div>
  </div>

  <div id="modal-haul" class="hidden fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl">
      <h3 class="text-base font-bold text-[#4A3933] mb-4">Log Beauty Purchase 🛍️</h3>
      <form onsubmit="submitHaul(event)" class="space-y-3 text-xs">
        <input type="text" id="h-item" placeholder="Product / Haul Item" required class="w-full border rounded-lg p-2">
        <select id="h-category" class="w-full border rounded-lg p-2">
          <option value="Skincare">Skincare</option>
          <option value="Makeup">Makeup</option>
          <option value="Sunscreen">Sunscreen</option>
          <option value="Lip Care">Lip Care</option>
        </select>
        <input type="number" id="h-cost" step="1" placeholder="Cost in ₹ (e.g. 495)" required class="w-full border rounded-lg p-2">
        <div class="flex justify-end gap-2 pt-2">
          <button type="button" onclick="document.getElementById('modal-haul').classList.add('hidden')" class="px-3 py-1.5">Cancel</button>
          <button type="submit" class="px-4 py-1.5 bg-purple-600 text-white rounded-lg font-bold">Log Haul</button>
        </div>
      </form>
    </div>
  </div>

  <div id="modal-travel-item" class="hidden fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl">
      <h3 class="text-base font-bold text-[#4A3933] mb-4">Add Travel Bottle 🧳</h3>
      <form onsubmit="submitTravelItem(event)" class="space-y-3 text-xs">
        <input type="text" id="t-item" placeholder="Bottle Name" required class="w-full border rounded-lg p-2">
        <input type="number" id="t-volume" placeholder="Volume in ml (e.g. 50 or 150)" required class="w-full border rounded-lg p-2">
        <div class="flex justify-end gap-2 pt-2">
          <button type="button" onclick="document.getElementById('modal-travel-item').classList.add('hidden')" class="px-3 py-1.5">Cancel</button>
          <button type="submit" class="px-4 py-1.5 bg-blue-600 text-white rounded-lg font-bold">Add</button>
        </div>
      </form>
    </div>
  </div>

  <div id="modal-wellness" class="hidden fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl">
      <h3 class="text-base font-bold text-[#4A3933] mb-4">Log Today's Vitals 🥗</h3>
      <form onsubmit="submitWellness(event)" class="space-y-3 text-xs">
        <input type="number" id="w-calories-in" placeholder="Calories Eaten" value="1850" required class="w-full border rounded-lg p-2">
        <input type="number" id="w-calories-burned" placeholder="Calories Burned" value="400" required class="w-full border rounded-lg p-2">
        <input type="number" step="0.1" id="w-weight" placeholder="Weight (kg)" value="53.7" required class="w-full border rounded-lg p-2">
        <input type="number" step="0.1" id="w-waist" placeholder="Waist (in)" value="26.2" required class="w-full border rounded-lg p-2">
        <div class="flex justify-end gap-2 pt-2">
          <button type="button" onclick="document.getElementById('modal-wellness').classList.add('hidden')" class="px-3 py-1.5">Cancel</button>
          <button type="submit" class="px-4 py-1.5 bg-[#E11D48] text-white rounded-lg font-bold">Save</button>
        </div>
      </form>
    </div>
  </div>

  <script>
    let globalProducts = [], globalWellness = [], globalBudget = {}, globalTravel = [];
    let activeFilter = 'All';
    let currentGlasses = 6;
    let chartBudget = null, chartUV = null;

    const cycleSteps = [
      { name: "Night 1: Exfoliation & Acid Resurfacing 🧪", desc: "Use AHA/BHA chemical exfoliant to dissolve dead skin cells. Follow with light hydration. No retinoids tonight!", badge: "Night 1: Exfoliate" },
      { name: "Night 2: Cell Turnover & Retinoid 🧴", desc: "Use your encapsulated retinol on dry skin to stimulate collagen. Sandwich with a ceramide cream.", badge: "Night 2: Retinoid" },
      { name: "Night 3: Barrier Recovery & Ceramides 💧", desc: "No actives tonight! Rest your moisture barrier with hydrating essence and cica soothing cream.", badge: "Night 3: Recovery" },
      { name: "Night 4: Deep Moisture Seal & Sleep Mask 😴", desc: "Gentle hydration plus slugging or rich barrier balm to lock in complete recovery.", badge: "Night 4: Recovery" }
    ];
    let currentCycleIndex = 1;

    function nextSkinCycle() {
      currentCycleIndex = (currentCycleIndex + 1) % cycleSteps.length;
      document.getElementById('cycle-badge').innerText = cycleSteps[currentCycleIndex].badge;
      document.getElementById('cycle-step-name').innerText = cycleSteps[currentCycleIndex].name;
      document.getElementById('cycle-step-desc').innerText = cycleSteps[currentCycleIndex].desc;
    }

    function setAQI(type, score) {
      const b = document.getElementById('aqi-badge');
      const t = document.getElementById('aqi-tip');
      if (type === 'Clean') {
        b.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800";
        b.innerText = `AQI ${score} (Pure & Clean Air)`;
        t.innerText = "Air is fresh and clear! Standard gentle foam wash and hydration are all you need today.";
      } else {
        b.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800";
        b.innerText = `AQI ${score} (High Dust / Smog)`;
        t.innerText = "High particulate pollution! Micro-dust oxidizes skin lipids. Double cleanse with cleansing balm immediately upon returning home!";
      }
    }

    function switchView(viewName) {
      ['menu', 'skincare', 'routines', 'fitness', 'budget', 'travel', 'advisor'].forEach(v => {
        const el = document.getElementById(`view-${v}`);
        const btn = document.getElementById(`btn-nav-${v}`);
        if (el) el.classList.add('hidden');
        if (btn) btn.classList.remove('nav-btn-active');
      });
      const targetView = document.getElementById(`view-${viewName}`);
      const targetBtn = document.getElementById(`btn-nav-${viewName}`);
      if (targetView) targetView.classList.remove('hidden');
      if (targetBtn) targetBtn.classList.add('nav-btn-active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    async function refreshData() {
      const res = await fetch('/api/data');
      const data = await res.json();
      globalProducts = data.products || [];
      globalWellness = data.wellness || [];
      globalBudget = data.budget || { monthly_limit: 5000, hauls: [] };
      globalTravel = data.travel || [];

      document.getElementById('badge-menu-prods').innerText = `${globalProducts.length} Items`;
      
      const totalSpent = (globalBudget.hauls || []).reduce((acc, h) => acc + h.cost, 0);
      document.getElementById('badge-menu-budget').innerText = `₹${totalSpent.toFixed(0)} Spent`;
      
      const packedCount = globalTravel.filter(t => t.packed).length;
      document.getElementById('badge-menu-travel').innerText = `${packedCount}/${globalTravel.length} Packed`;

      renderSkincare();
      renderFitness();
      renderBudget(totalSpent);
      renderTravel();
      renderAdvisorCharts(data);
    }

    function renderSkincare() {
      document.getElementById('kpi-total').innerText = globalProducts.length;
      document.getElementById('kpi-expiring').innerText = globalProducts.filter(p => p.days_left <= 7).length;
      const tb = document.getElementById('product-rows');
      tb.innerHTML = '';
      const list = activeFilter === 'All' ? globalProducts : globalProducts.filter(p => p.category === activeFilter);
      list.forEach(p => {
        let badgeColor = 'bg-emerald-50 text-emerald-600 border border-emerald-200';
        if (p.priority === 'P1-Toss Out') badgeColor = 'bg-rose-50 text-rose-600 border border-rose-200';
        if (p.priority === 'P2-Expiring') badgeColor = 'bg-amber-50 text-amber-600 border border-amber-200';

        tb.innerHTML += `
          <tr class="border-b border-[#FAF4F0] hover:bg-[#FAF7F5]">
            <td class="py-2.5 px-3 font-bold text-[#4A3933]">${p.name}</td>
            <td class="py-2.5 px-3 text-[#785950]">${p.brand}</td>
            <td class="py-2.5 px-3 text-xs text-[#8C7A74]">${p.category}</td>
            <td class="py-2.5 px-3 font-semibold ${p.days_left < 0 ? 'text-rose-500 font-bold' : ''}">${p.days_left < 0 ? 'Expired' : p.days_left + ' Days'}</td>
            <td class="py-2.5 px-3"><span class="px-2 py-0.5 text-[11px] font-bold rounded-md ${badgeColor}">${p.status}</span></td>
            <td class="py-2.5 px-3 text-right"><button onclick="cycleProduct('${p.id}')" class="px-2 py-1 bg-white border rounded text-xs hover:border-rose-300">Advance ➔</button></td>
          </tr>
        `;
      });
    }

    function filterShelf(category) {
      activeFilter = category;
      document.querySelectorAll('.filter-btn').forEach(b => {
        b.className = b.innerText.toLowerCase().includes(category.toLowerCase()) || (category === 'All' && b.innerText === 'All')
          ? 'filter-btn px-2.5 py-1 rounded-lg font-bold bg-[#E11D48] text-white'
          : 'filter-btn px-2.5 py-1 rounded-lg font-semibold text-[#785950] hover:bg-white';
      });
      renderSkincare();
    }

    function renderFitness() {
      if (globalWellness.length > 0) {
        const latest = globalWellness[globalWellness.length - 1];
        currentGlasses = latest.water_glasses || 6;
        document.getElementById('cal-intake-val').innerText = `${latest.calories_in} kcal`;
        document.getElementById('cal-burned-val').innerText = `-${latest.calories_burned} kcal`;
        document.getElementById('net-cal-badge').innerText = `${latest.calories_in - latest.calories_burned} Net kcal`;
        document.getElementById('body-weight-val').innerText = `${latest.weight_kg} kg`;
        document.getElementById('body-waist-val').innerText = `${latest.waist_in} in`;
      }
      const ml = currentGlasses * 250;
      const pct = Math.min(100, Math.round((currentGlasses / 8) * 100));
      document.getElementById('water-display-ml').innerText = `${ml} / 2000 ml`;
      document.getElementById('water-glasses-text').innerText = `${currentGlasses} of 8 Glasses`;
      document.getElementById('water-progress-bar').style.width = `${pct}%`;
    }

    async function adjustWater(delta) {
      currentGlasses = Math.max(0, currentGlasses + delta);
      await fetch('/api/wellness/water', { method: 'POST', body: JSON.stringify({ glasses: currentGlasses }) });
      refreshData();
    }

    function setClimate(type) {
      const b = document.getElementById('climate-badge');
      const r = document.getElementById('climate-recommendation');
      if (type === 'Dry Air') {
        b.innerText = "Dry Air / AC (32% Humidity)";
        r.innerText = "Air is crisp and dry. Layer a hyaluronic mist and seal with a rich ceramide cream.";
      } else if (type === 'Humid') {
        b.innerText = "Humid Monsoon (85% Humidity)";
        r.innerText = "Pores clog faster in high humidity! Use an oil-free gel moisturizer and double cleanse.";
      } else {
        b.innerText = "Cold Winter (12°C Chill)";
        r.innerText = "Skin barrier needs heavy lip repair and barrier balms to prevent wind-burn flaking.";
      }
    }

    function renderBudget(totalSpent) {
      const limit = globalBudget.monthly_limit || 5000;
      const left = Math.max(0, limit - totalSpent);
      const pct = Math.min(100, Math.round((totalSpent / limit) * 100));

      document.getElementById('budget-limit-val').innerText = `₹${limit.toLocaleString('en-IN')}`;
      document.getElementById('budget-spent-val').innerText = `₹${totalSpent.toLocaleString('en-IN')}`;
      document.getElementById('budget-left-val').innerText = `₹${left.toLocaleString('en-IN')}`;
      document.getElementById('budget-pct-text').innerText = `${pct}% of limit used`;
      document.getElementById('budget-progress-label').innerText = `${pct}%`;
      document.getElementById('budget-progress-bar').style.width = `${pct}%`;

      const hr = document.getElementById('haul-rows');
      hr.innerHTML = '';
      (globalBudget.hauls || []).forEach(h => {
        hr.innerHTML += `
          <tr class="border-b border-[#FAF4F0]">
            <td class="py-2 font-bold text-[#4A3933]">${h.item}</td>
            <td class="py-2 text-[#8C7A74]">${h.category}</td>
            <td class="py-2 text-[#8C7A74]">${h.date}</td>
            <td class="py-2 font-mono font-bold text-right text-purple-700">₹${h.cost}</td>
          </tr>
        `;
      });

      const cats = {};
      (globalBudget.hauls || []).forEach(h => { cats[h.category] = (cats[h.category] || 0) + h.cost; });
      if (chartBudget) chartBudget.destroy();
      const el = document.getElementById('chart-budget');
      if (el) {
        chartBudget = new Chart(el, {
          type: 'doughnut',
          data: {
            labels: Object.keys(cats),
            datasets: [{ data: Object.values(cats), backgroundColor: ['#FDA4AF', '#C084FC', '#38BDF8', '#FDE047'], borderWidth: 0 }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }
    }

    function renderTravel() {
      const tr = document.getElementById('travel-rows');
      tr.innerHTML = '';
      globalTravel.forEach(t => {
        const isTsaOk = t.volume_ml <= 100;
        tr.innerHTML += `
          <tr class="border-b border-[#FAF4F0] hover:bg-[#FAF7F5]">
            <td class="py-2.5 px-3"><input type="checkbox" onchange="togglePacked('${t.id}')" ${t.packed ? 'checked' : ''} class="rounded accent-blue-600 w-4 h-4 cursor-pointer"></td>
            <td class="py-2.5 px-3 font-bold ${t.packed ? 'line-through text-[#8C7A74]' : 'text-[#4A3933]'}">${t.item}</td>
            <td class="py-2.5 px-3 font-mono text-xs font-semibold">${t.volume_ml} ml</td>
            <td class="py-2.5 px-3"><span class="px-2 py-0.5 text-[10px] font-bold rounded-md ${isTsaOk ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'}">${isTsaOk ? '✅ TSA Safe' : '⚠️ Checked Bag'}</span></td>
            <td class="py-2.5 px-3 text-right"><button onclick="removeTravel('${t.id}')" class="text-xs text-rose-500 hover:font-bold">Remove</button></td>
          </tr>
        `;
      });
    }

    function renderAdvisorCharts(data) {
      if (data.uv && data.uv.hourly_uv) {
        if (chartUV) chartUV.destroy();
        const elUv = document.getElementById('chart-uv');
        if (elUv) {
          chartUV = new Chart(elUv, {
            type: 'bar',
            data: {
              labels: data.uv.hourly_uv.map(u => u.time),
              datasets: [{
                label: 'Campus UV Index',
                data: data.uv.hourly_uv.map(u => u.uv),
                backgroundColor: data.uv.hourly_uv.map(u => u.uv > 6 ? '#F43F5E' : (u.uv > 3 ? '#FBBF24' : '#34D399')),
                borderRadius: 6
              }]
            },
            options: { responsive: true, maintainAspectRatio: false }
          });
        }
      }
    }

    async function togglePacked(id) {
      await fetch('/api/travel/toggle', { method: 'POST', body: JSON.stringify({ id }) });
      refreshData();
    }

    async function removeTravel(id) {
      await fetch('/api/travel/remove', { method: 'POST', body: JSON.stringify({ id }) });
      refreshData();
    }

    function updateRoutineProgress() {
      const am = document.querySelectorAll('.am-step:checked').length;
      const pm = document.querySelectorAll('.pm-step:checked').length;
      const pct = Math.round(((am + pm) / 8) * 100);
      document.getElementById('routine-status-badge').innerText = `${pct}% Done`;
    }

    async function cycleProduct(id) {
      await fetch('/api/products/cycle', { method: 'POST', body: JSON.stringify({ id }) });
      refreshData();
    }

    async function reapplySPF() {
      await fetch('/api/spf/reapply', { method: 'POST' });
      alert("SPF Reset! Next application in 2 hours ☀️🧴");
    }

    async function submitHaul(e) {
      e.preventDefault();
      const payload = {
        item: document.getElementById('h-item').value,
        category: document.getElementById('h-category').value,
        cost: parseFloat(document.getElementById('h-cost').value),
        date: new Date().toISOString().split('T')[0]
      };
      await fetch('/api/budget/add', { method: 'POST', body: JSON.stringify(payload) });
      document.getElementById('modal-haul').classList.add('hidden');
      refreshData();
    }

    async function submitTravelItem(e) {
      e.preventDefault();
      const payload = {
        item: document.getElementById('t-item').value,
        volume_ml: parseInt(document.getElementById('t-volume').value)
      };
      await fetch('/api/travel/add', { method: 'POST', body: JSON.stringify(payload) });
      document.getElementById('modal-travel-item').classList.add('hidden');
      refreshData();
    }

    async function submitProduct(e) {
      e.preventDefault();
      const payload = {
        name: document.getElementById('p-name').value,
        brand: document.getElementById('p-brand').value,
        category: document.getElementById('p-category').value,
        pao: parseInt(document.getElementById('p-pao').value)
      };
      await fetch('/api/products/add', { method: 'POST', body: JSON.stringify(payload) });
      document.getElementById('modal-add').classList.add('hidden');
      refreshData();
    }

    async function submitWellness(e) {
      e.preventDefault();
      const payload = {
        day: "Today",
        calories_in: parseInt(document.getElementById('w-calories-in').value),
        calories_burned: parseInt(document.getElementById('w-calories-burned').value),
        water_glasses: currentGlasses,
        weight_kg: parseFloat(document.getElementById('w-weight').value),
        waist_in: parseFloat(document.getElementById('w-waist').value)
      };
      await fetch('/api/wellness/add', { method: 'POST', body: JSON.stringify(payload) });
      document.getElementById('modal-wellness').classList.add('hidden');
      refreshData();
    }

    refreshData();
  </script>
</body>
</html>"""

class GlowDeskHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/api/data":
            payload = {
                "products": read_json("products.json"),
                "inventory": read_json("inventory.json"),
                "routines": read_json("routines.json"),
                "wellness": read_json("wellness.json"),
                "budget": read_json("budget.json", default={"monthly_limit": 5000, "hauls": []}),
                "travel": read_json("travel.json", default=[]),
                "uv": read_json("uv_telemetry.json", default={})
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        if self.path == "/api/budget/add":
            b = read_json("budget.json", default={"monthly_limit": 5000, "hauls": []})
            body["id"] = f"H-{len(b.get('hauls', [])) + 1}"
            b.setdefault("hauls", []).append(body)
            atomic_write(DATA_DIR / "budget.json", b)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"success": true}')

        elif self.path == "/api/travel/add":
            t = read_json("travel.json", default=[])
            body["id"] = f"TRV-{len(t) + 1}"
            body["packed"] = False
            t.append(body)
            atomic_write(DATA_DIR / "travel.json", t)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"success": true}')

        elif self.path == "/api/travel/toggle":
            t = read_json("travel.json", default=[])
            for item in t:
                if item["id"] == body.get("id"): item["packed"] = not item["packed"]
            atomic_write(DATA_DIR / "travel.json", t)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"success": true}')

        elif self.path == "/api/travel/remove":
            t = read_json("travel.json", default=[])
            t = [item for item in t if item["id"] != body.get("id")]
            atomic_write(DATA_DIR / "travel.json", t)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"success": true}')

        elif self.path == "/api/wellness/water":
            w = read_json("wellness.json")
            if w: w[-1]["water_glasses"] = body.get("glasses", 6)
            atomic_write(DATA_DIR / "wellness.json", w)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"success": true}')

        elif self.path == "/api/wellness/add":
            w = read_json("wellness.json")
            w.append(body)
            if len(w) > 7: w.pop(0)
            atomic_write(DATA_DIR / "wellness.json", w)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"success": true}')

        elif self.path == "/api/spf/reapply":
            uv = read_json("uv_telemetry.json", default={})
            uv["spf_reapply_timer_mins"] = 120
            atomic_write(DATA_DIR / "uv_telemetry.json", uv)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"success": true}')

        elif self.path == "/api/products/cycle":
            prods = read_json("products.json")
            for p in prods:
                if p["id"] == body.get("id"):
                    if p["priority"] == "P1-Toss Out":
                        p["status"] = "Fresh ✨"; p["priority"] = "P3-Safe"; p["days_left"] = 180
                    else:
                        p["priority"] = "P1-Toss Out"; p["status"] = "Expired"; p["days_left"] = -1
            atomic_write(DATA_DIR / "products.json", prods)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"success": true}')

        elif self.path == "/api/products/add":
            prods = read_json("products.json")
            prods.append({
                "id": f"GLOW-{len(prods) + 101}",
                "name": body.get("name"),
                "brand": body.get("brand"),
                "category": body.get("category"),
                "days_left": body.get("pao", 6) * 30,
                "status": "Fresh ✨",
                "priority": "P3-Safe"
            })
            atomic_write(DATA_DIR / "products.json", prods)
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"success": true}')

def run():
    server = http.server.HTTPServer(("0.0.0.0", PORT), GlowDeskHandler)
    print(f"✨ GlowDesk engine listening on http://127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == "__main__":
    run()