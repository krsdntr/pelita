import re

# 1. Read HTML
with open('d:/app/alkitab/scratch/extracted_header.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove data-astro-cid attributes
html = re.sub(r'\s*data-astro-cid-[a-z0-9]+\s*', ' ', html)
html = html.replace(' >', '>').replace(' >', '>')

# 2. Extract CSS
with open('d:/app/alkitab/dist/_astro/Footer.BOIXFHvA.css', 'r', encoding='utf-8') as f:
    css_full = f.read()

match = re.search(r'(\.sacred-topbar.*?)(\.sacred-footer.*)', css_full)
if match:
    css = match.group(1)
    css = re.sub(r'\[data-astro-cid-[a-z0-9]+\]', '', css)
    # Add newlines after } for better readability
    css = css.replace('}', '}\n')
else:
    css = "/* Failed to extract CSS */"

# 3. Create the JS logic
js_logic = """
    // Search Overlay Logic
    const searchBtn = document.getElementById('headerSearchBtn');
    const closeSearchBtn = document.getElementById('closeSearchBtn');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchInput = document.getElementById('globalSearchInput');
    const searchResultsDropdown = document.getElementById('searchResultsDropdown');
    const searchResultsGrid = document.getElementById('searchResultsGrid');
    
    // Settings Drawer Logic
    const settingsBtn = document.getElementById('headerSettingsBtn');
    const closeSettingsBtn = document.getElementById('closeGlobalSettings');
    const settingsDrawer = document.getElementById('globalSettingsDrawer');
    const settingsBackdrop = document.getElementById('settingsDrawerBackdrop');
    
    const themeOptions = document.querySelectorAll('.theme-option');
    const textSizeSlider = document.getElementById('globalTextSizeSlider');
    const textSizeVal = document.getElementById('globalTextSizeVal');

    // Open/Close functions
    function openSearch() {
        if(searchOverlay) {
            searchOverlay.classList.add('active');
            setTimeout(() => { if(searchInput) searchInput.focus(); }, 100);
        }
    }
    function closeSearch() {
        if(searchOverlay) searchOverlay.classList.remove('active');
    }
    function openSettings() {
        if(settingsDrawer) settingsDrawer.classList.add('active');
        if(settingsBackdrop) settingsBackdrop.classList.add('active');
    }
    function closeSettings() {
        if(settingsDrawer) settingsDrawer.classList.remove('active');
        if(settingsBackdrop) settingsBackdrop.classList.remove('active');
    }

    if(searchBtn) searchBtn.addEventListener('click', openSearch);
    if(closeSearchBtn) closeSearchBtn.addEventListener('click', closeSearch);
    if(settingsBtn) settingsBtn.addEventListener('click', openSettings);
    if(closeSettingsBtn) closeSettingsBtn.addEventListener('click', closeSettings);
    if(settingsBackdrop) settingsBackdrop.addEventListener('click', closeSettings);

    // Theme Switcher
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeOptions.forEach(opt => {
        if(opt.getAttribute('data-theme') === savedTheme) opt.classList.add('active');
        opt.addEventListener('click', () => {
            themeOptions.forEach(o => o.classList.remove('active'));
            opt.classList.add('active');
            const theme = opt.getAttribute('data-theme');
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        });
    });

    // Text Size
    const sizeMap = {
        12: 'Sangat Kecil', 14: 'Kecil', 16: 'Sedang',
        18: 'Besar', 20: 'Sangat Besar', 22: 'Ekstra Besar', 24: 'Maksimal'
    };
    const savedSize = localStorage.getItem('textSize') || '16';
    if(textSizeSlider) {
        textSizeSlider.value = savedSize;
        if(textSizeVal) textSizeVal.textContent = sizeMap[savedSize] || savedSize + 'px';
        
        textSizeSlider.addEventListener('input', (e) => {
            const val = e.target.value;
            if(textSizeVal) textSizeVal.textContent = sizeMap[val] || val + 'px';
            document.documentElement.style.setProperty('--type-body-lg', (val / 16) + 'rem');
            localStorage.setItem('textSize', val);
        });
        document.documentElement.style.setProperty('--type-body-lg', (savedSize / 16) + 'rem');
    }
"""

astro_content = f"""---
// StatsHeader.astro Rebuilt
---

{html}

<style>
{css}
</style>

<script>
try {{
{js_logic}
}} catch (err) {{
  console.error("StatsHeader logic error:", err);
}}
</script>
"""

with open('d:/app/alkitab/src/components/StatsHeader.astro', 'w', encoding='utf-8') as f:
    f.write(astro_content)

print("Rebuilt StatsHeader.astro without external modules")
