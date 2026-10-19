import re

file_path = "C:/Users/IDC/Desktop/laboratorio de neuromarketing/SISTEMA ESTADISTICO CORRELACIONES/ESTADISTICA JV.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject HTML for presets
html_target = r'(<div class="border-t border-teal-200 pt-3">\s*<label class="block text-\[10px\] font-bold text-teal-700 uppercase mb-1">Escala Likert / Rango</label>)'
preset_html = """<div class="border-t border-teal-200 pt-3">
                        <label class="block text-[10px] font-bold text-teal-700 uppercase mb-1">Preajustes de Escala</label>
                        <select id="scale-preset" class="w-full border border-teal-300 rounded px-2 py-1 text-[10px] mb-2 text-slate-700 font-semibold bg-teal-50 focus:outline-none focus:ring-1 focus:ring-teal-400">
                            <option value="custom">-- Personalizado --</option>
                            <option value="likert4">Ordinal: Likert 4 pts (TD a TA)</option>
                            <option value="likert5">Ordinal: Likert 5 pts (TD a TA)</option>
                            <option value="nominal12">Nominal: Dicotómica (1=Sí, 2=No)</option>
                            <option value="nominal01">Nominal: Dicotómica (0=No, 1=Sí)</option>
                        </select>
                        <label class="block text-[10px] font-bold text-teal-700 uppercase mb-1">Rango Personalizado</label>"""
content = re.sub(html_target, preset_html, content)

# 2. Inject JS for logic
js_target = r'(minInput\.addEventListener\(\'change\', generateLabelInputs\); maxInput\.addEventListener\(\'change\', generateLabelInputs\);)'
js_replacement = """
        const scalePreset = document.getElementById('scale-preset');
        scalePreset.addEventListener('change', () => {
            const val = scalePreset.value;
            if (val === 'likert4') {
                minInput.value = 1; maxInput.value = 4; generateLabelInputs();
                document.getElementById('label-val-1').value = "Totalmente en desacuerdo";
                document.getElementById('label-val-2').value = "En desacuerdo";
                document.getElementById('label-val-3').value = "De acuerdo";
                document.getElementById('label-val-4').value = "Totalmente de acuerdo";
            } else if (val === 'likert5') {
                minInput.value = 1; maxInput.value = 5; generateLabelInputs();
                document.getElementById('label-val-1').value = "Totalmente en desacuerdo";
                document.getElementById('label-val-2').value = "En desacuerdo";
                document.getElementById('label-val-3').value = "Ni de acuerdo ni en desacuerdo";
                document.getElementById('label-val-4').value = "De acuerdo";
                document.getElementById('label-val-5').value = "Totalmente de acuerdo";
            } else if (val === 'nominal12') {
                minInput.value = 1; maxInput.value = 2; generateLabelInputs();
                document.getElementById('label-val-1').value = "Sí";
                document.getElementById('label-val-2').value = "No";
            } else if (val === 'nominal01') {
                minInput.value = 0; maxInput.value = 1; generateLabelInputs();
                document.getElementById('label-val-0').value = "No";
                document.getElementById('label-val-1').value = "Sí";
            } else {
                generateLabelInputs();
            }
        });

        minInput.addEventListener('change', () => { scalePreset.value = 'custom'; generateLabelInputs(); });
        maxInput.addEventListener('change', () => { scalePreset.value = 'custom'; generateLabelInputs(); });
"""
content = re.sub(js_target, js_replacement, content)

# Remove the redundant old listeners to prevent double firing if needed, but the regex replaces them directly so it's clean.
# Also fix the keyup listeners so they reset to custom
keyup_target = r'(minInput\.addEventListener\(\'keyup\', generateLabelInputs\); maxInput\.addEventListener\(\'keyup\', generateLabelInputs\);)'
keyup_replacement = """minInput.addEventListener('keyup', () => { scalePreset.value = 'custom'; generateLabelInputs(); }); maxInput.addEventListener('keyup', () => { scalePreset.value = 'custom'; generateLabelInputs(); });"""
content = re.sub(keyup_target, keyup_replacement, content)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Scale presets added successfully.")
