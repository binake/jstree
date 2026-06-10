const fs = require('fs');
let content = fs.readFileSync('view.html', 'utf-8');
// Fix garbled comment line before initPanelEvents()
content = content.replace('初始化面板事�?', '        // \u521d\u59cb\u5316\u9762\u677f\u4e8b\u4ef6');
fs.writeFileSync('view.html', content, 'utf-8');
console.log('Done');
