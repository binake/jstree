const fs = require('fs');
const content = fs.readFileSync('view.html', 'utf-8');
const oldPattern = '// ===== Interaction Mode (Hand / Pointer) =====';
const idx = content.indexOf(oldPattern);
if (idx === -1) { console.log('Pattern not found!'); process.exit(1); }
const initMarker = '\u521d\u59cb\u5316';
const initIdx = content.indexOf(initMarker, idx);
if (initIdx === -1) { console.log('Init marker not found!'); process.exit(1); }
const before = content.substring(0, idx);
const after = content.substring(initIdx);
const Q = "'";
const newJsBlock = 
'        // ===== Interaction Mode (Hand / Pointer) =====\n' +
'        var currentInteractionMode = ' + Q + 'pointer' + Q + ';\n' +
'        function setInteractionMode(mode) {\n' +
'            currentInteractionMode = mode;\n' +
'            document.getElementById(' + Q + 'mode_hand' + Q + ').classList.toggle(' + Q + 'active' + Q + ', mode === ' + Q + 'hand' + Q + ');\n' +
'            document.getElementById(' + Q + 'mode_pointer' + Q + ').classList.toggle(' + Q + 'active' + Q + ', mode === ' + Q + 'pointer' + Q + ');\n' +
'            document.body.classList.toggle(' + Q + 'hand-mode-active' + Q + ', mode === ' + Q + 'hand' + Q + ');\n' +
'            if (mode === ' + Q + 'hand' + Q + ') {\n' +
'                if (jm) { try { jm.disable_edit(); } catch(e) {} }\n' +
'                enableCanvasDrag();\n' +
'            } else {\n' +
'                if (jm) { try { jm.enable_edit(); } catch(e) {} }\n' +
'                disableCanvasDrag();\n' +
'            }\n' +
'        }\n' +
"document.addEventListener('keydown', function(e) {\n" +
"if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;\n" +
"if (e.key === 'h' || e.key === 'H') { e.preventDefault(); setInteractionMode('hand'); }\n" +
"else if (e.key === 'v' || e.key === 'V') { e.preventDefault(); setInteractionMode('pointer'); }\n" +
"});\n";
const result = before + newJsBlock + after;
fs.writeFileSync('view.html', result, 'utf-8');
console.log('Done');
