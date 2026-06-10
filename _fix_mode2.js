const fs = require('fs');
let content = fs.readFileSync('view.html', 'utf-8');
const lines = content.split('\n');

// 1. Modify shouldDrag in enableCanvasDrag to allow node dragging in hand mode
// Find "if (target.closest && target.closest('jmnode')) return false;"
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes("target.closest('jmnode')")) {
        const indent = lines[i].match(/^\s*/)[0];
        lines[i] = indent + "// 手型模式下允许在节点上拖拽平移";
        lines.splice(i+1, 0, indent + "if (target.closest && target.closest('jmnode')) {");
        lines.splice(i+2, 0, indent + "    if (currentInteractionMode !== 'hand') return false;");
        lines.splice(i+3, 0, indent + "    // hand mode: 允许拖拽节点来平移画布");
        lines.splice(i+4, 0, indent + "}");
        break;
    }
}

// 2. Format the mode toggle JS block (fix indentation)
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('var currentInteractionMode')) {
        lines[i] = '        var currentInteractionMode = ' + "'pointer'" + ';';
    }
}

// 3. Add disableCanvasDrag function between enableCanvasDrag and updateZoomLabel
// Find the closing of enableCanvasDrag and updateZoomLabel
let enableEndIdx = -1;
let updateLabelIdx = -1;
for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() === 'function updateZoomLabel() {') {
        updateLabelIdx = i;
        break;
    }
}

// Find the blank line before updateZoomLabel
for (let i = updateLabelIdx - 1; i >= 0; i--) {
    if (lines[i].trim() === '}') {
        enableEndIdx = i;
        // Look back for the function's closing
        // Go back a bit and insert after the } plus one blank line
        break;
    }
}

if (enableEndIdx > 0 && updateLabelIdx > 0) {
    const disableFn = [
        '        function disableCanvasDrag() {',
        '            if (!canvasDragEnabled) return;',
        '            canvasDragEnabled = false;',
        '',
        '            const container = document.getElementById(' + "'jsmind_container'" + ');',
        '            if (container && container._canvasDragHandlers) {',
        '                container.removeEventListener(' + "'mousedown'" + ', container._canvasDragHandlers.mousedown);',
        '                document.removeEventListener(' + "'mousemove'" + ', container._canvasDragHandlers.mousemove);',
        '                document.removeEventListener(' + "'mouseup'" + ', container._canvasDragHandlers.mouseup);',
        '                delete container._canvasDragHandlers;',
        '            }',
        '        }',
        ''
    ];
    // Insert after the blank line following enableCanvasDrag's closing }
    // Find the first empty line after enableEndIdx
    let insertAfter = enableEndIdx;
    while (insertAfter < lines.length - 1 && lines[insertAfter + 1].trim() === '') {
        insertAfter++;
    }
    lines.splice(insertAfter + 1, 0, ...disableFn);
}

// 4. Fix mode JS block indentation - find the keydown listener lines
for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() === "document.addEventListener('keydown', function(e) {") {
        // This and following 3 lines need proper indentation
        const baseIndent = '        ';
        for (let j = i; j < Math.min(i + 5, lines.length); j++) {
            let trimmed = lines[j].trimStart();
            if (trimmed.startsWith('document.addEventListener')) {
                lines[j] = baseIndent + trimmed;
            } else if (trimmed.startsWith('if (e.target.tagName')) {
                lines[j] = baseIndent + '    ' + trimmed;
            } else if (trimmed.startsWith('if (e.key') || trimmed.startsWith('else if')) {
                lines[j] = baseIndent + '    ' + trimmed;
            } else if (trimmed.startsWith('});')) {
                lines[j] = baseIndent + trimmed;
            }
        }
        break;
    }
}

// 5. Fix the switchViewMode function to reset to pointer mode when switching views
// (We'll leave this as-is for now - the mode is independent of view mode)

content = lines.join('\n');
fs.writeFileSync('view.html', content, 'utf-8');
console.log('Done');
