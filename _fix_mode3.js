const fs = require('fs');
let content = fs.readFileSync('view.html', 'utf-8');

// Fix: the init comment line got truncated
// Replace the broken line that starts with the Chinese init comment without leading "// 初始化面板事件"
content = content.replace('鍒濆鍖栭潰鏉夸簨锟?', '        // 鍒濆鍖栭潰鏉夸簨浠');
// Actually, the correct original text should be:
content = content.replace('鍒濆鍖栭潰鏉夸簨锟?', '        // \u521d\u59cb\u5316\u9762\u677f\u4e8b\u4ef6');

fs.writeFileSync('view.html', content, 'utf-8');
console.log('Done');
