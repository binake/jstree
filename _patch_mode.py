<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>技能树展示</title>
    <link type="text/css" rel="stylesheet" href="libs/css/jsmind.css" />
    <link rel="stylesheet" href="libs/css/fonts.css">
    <style>
        /* ===== CSS Variables ===== */
        :root {
            --bg-primary: #060b13;
            --bg-secondary: #0b1221;
            --bg-tertiary: #04070d;
            --surface-0: #eef0f3;
            --surface-1: #f4f5f7;
            --surface-2: #fafafa;
            --surface-3: #e8eaed;

            --text-h: #1a1f2e;
            --text-p: #3d4451;
            --text-s: #6b7280;
            --text-ph: #9ca3af;

            --border: #dde1e7;
            --border-focus: #8b9bbf;

            --accent: #4a5568;
            --accent-hover: #2d3748;
            --accent-light: #edf0f5;

            --ok: #3d6b50;
            --ok-bg: #edf5ef;
            --warn: #7a5c2e;
            --warn-bg: #f5f0e8;
            --err: #7a3040;
            --err-bg: #f5ecee;

            /* Legacy aliases */
            --bg-primary: var(--surface-0);
            --bg-secondary: var(--surface-0);
            --bg-card: var(--surface-1);
            --bg-input: var(--surface-2);
            --cyan: var(--accent);
            --cyan-dim: var(--accent-light);
            --text-primary: var(--text-h);
            --text-secondary: var(--text-s);
            --border-glow: var(--border);
            --border-color: var(--border);
            --red: var(--err);
            --green: var(--ok);
            --gold: var(--warn);
            --font-body: 'Inter', 'Microsoft YaHei', Arial, sans-serif;
            --font-display: 'Inter', 'Microsoft YaHei', sans-serif;
        }

        /* ===== Reset & Global ===== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-body);
            background: var(--bg-primary);
            min-height: 100vh;
            color: var(--text-primary);
            overflow-x: hidden;
        }

        /* Subtle grid background */
        body::before {
            display: none;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: var(--surface-0);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }

        /* ===== Header ===== */
        .header {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 20px;
            text-align: center;
            border-bottom: 1px solid var(--border-glow);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            position: relative;
            z-index: 100;
        }

        /* Header accent line */
        .header::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            right: 0;
            height: 1px;
            background: var(--border-color);
        }

        .header h1 {
            font-size: 36px;
            font-weight: 800;
            color: var(--text-primary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 5px;
        }

        /* ===== Skill Points Display ===== */
        .skill-points {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin-top: 10px;
        }

        .skill-point-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 24px;
            background: #ffffff;
            border-radius: 50px;
            border: 1px solid var(--border-glow);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }

        .skill-point-item:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border-color: var(--cyan);
        }

        .skill-point-item .icon {
            width: 32px;
            height: 32px;
            background: var(--bg-secondary);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: var(--gold);
            font-size: 16px;
        }

        .skill-point-item .text {
            font-size: 16px;
            font-family: var(--font-display);
            letter-spacing: 1px;
            color: var(--text-primary);
        }

        .skill-point-item .text span {
            color: var(--cyan);
            font-size: 20px;
            font-weight: 700;
            margin-left: 6px;
        }

        /* ===== Toolbar Controls ===== */
        .toolbar {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 16px;
            margin-top: 24px;
            flex-wrap: wrap;
        }

        select.btn {
            appearance: none;
            padding: 10px 36px 10px 16px;
            background: var(--surface-1);
            border: 1px solid var(--border);
            border-radius: 7px;
            font-family: var(--font-body);
            font-size: 13.5px;
            color: var(--text-p);
            cursor: pointer;
            transition: border-color 0.15s;
            min-width: 200px;
        }

        select.btn:hover,
        select.btn:focus {
            border-color: var(--border-focus);
            outline: none;
        }

        button.btn {
            padding: 9px 22px;
            border-radius: 7px;
            cursor: pointer;
            font-size: 13.5px;
            font-family: var(--font-body);
            font-weight: 600;
            transition: background 0.15s ease, transform 0.1s ease;
            border: 1px solid transparent;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        button.btn-primary {
            background: var(--accent);
            color: #ffffff;
            border-color: var(--accent);
        }

        button.btn-primary:hover {
            background: var(--accent-hover);
        }

        button.btn-danger {
            background: var(--err-bg);
            color: var(--err);
            border-color: color-mix(in srgb, var(--err) 20%, transparent);
        }

        button.btn-danger:hover {
            background: var(--err);
            color: #fff;
        }

        button.btn:hover {
            transform: translateY(-1px);
        }

        /* ===== jsMind Container ===== */
        #jsmind_container {
            width: calc(100% - 40px);
            height: calc(100vh - 240px);
            background: var(--surface-3);
            background-image:
                radial-gradient(circle at 1px 1px, var(--border) 1px, transparent 0);
            background-size: 28px 28px;
            margin: 20px auto;
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.04);
            position: relative;
            overflow: auto;
            cursor: grab;
        }

        #jsmind_container:active {
            cursor: grabbing;
        }

        /* jsMind inner */
        .jsmind-inner {
            min-width: 200%;
            min-height: 200%;
            position: relative;
            transition: none;
        }

        /* Root node styles */
        jmnode[data-is-root="true"] {
            cursor: grab !important;
        }

        jmnode[data-is-root="true"]:active {
            cursor: grabbing !important;
        }

        #jsmind_container canvas {
            display: block;
        }

        /* Node base styles */
        .jsmind-inner jmnode {
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-family: var(--font-body);
            border-radius: 6px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            white-space: normal !important;
            /* 允许换行 */
            min-width: 100px !important;
            /* 增加最小宽�?*/
            max-width: 320px !important;
            /* 增加最大宽�?*/
            line-height: 1.5 !important;
            padding: 10px 14px !important;
            word-wrap: break-word;
            word-break: break-word;
            display: flex;
            align-items: center;
        }

        /* Locked Node */
        jmnode[data-status="locked"] {
            opacity: 0.6 !important;
            filter: grayscale(100%) brightness(0.9);
            cursor: not-allowed;
            background: #f1f5f9 !important;
            color: #94a3b8 !important;
            border: 1px solid #cbd5e1 !important;
        }

        jmnode[data-status="locked"]::before {
            content: '🔒';
            position: absolute;
            top: -10px;
            right: -10px;
            width: 22px;
            height: 22px;
            background: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            z-index: 10;
        }

        /* Unlocked Node (Available) */
        jmnode[data-status="unlocked"] {
            opacity: 1;
            cursor: pointer;
            border: 1.5px dashed var(--cyan);
            background: #ffffff !important;
            box-shadow: 0 4px 10px rgba(2, 132, 199, 0.05);
        }

        @keyframes breathe {

            0%,
            100% {
                opacity: 0.8;
                box-shadow: 0 0 5px var(--cyan-dim);
            }

            50% {
                opacity: 1;
                box-shadow: 0 0 15px var(--cyan-glow);
            }
        }

        /* Activated Node */
        jmnode[data-status="activated"] {
            opacity: 1;
            cursor: pointer;
            border: 1px solid var(--cyan);
            background: var(--cyan) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            z-index: 5;
        }

        @keyframes activePulse {
            from {
                box-shadow: 0 0 10px rgba(255, 215, 0, 0.4);
            }

            to {
                box-shadow: 0 0 25px rgba(255, 215, 0, 0.7), 0 0 40px rgba(255, 215, 0, 0.3);
            }
        }

        jmnode[data-status="activated"]::after {
            content: '�?;
            position: absolute;
            top: -10px;
            right: -10px;
            width: 24px;
            height: 24px;
            background: var(--green);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: #000;
            font-weight: 900;
            z-index: 10;
            box-shadow: 0 0 10px var(--green);
            animation: checkPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes checkPop {
            0% {
                transform: scale(0);
                opacity: 0;
            }

            100% {
                transform: scale(1);
                opacity: 1;
            }
        }

        /* Ensure icons placed outside the node bounds are visible */
        jmnode {
            overflow: visible !important;
        }

        /*
         * 覆盖 libs/css/jsmind.css �?theme-orange 的默认色�?
         * - jmnode.selected 使用 #11f（近�?#1111ff）饱和度过高
         * - jmnode:hover 使用 #f39c12 也较�?
         * 以下规则与页�?slate 风格统一，并保留节点自身背景的可读性（hover 用滤镜柔化）
         */
        #jsmind_container jmnodes.theme-orange jmnode:hover {
            filter: saturate(0.68) brightness(1.04);
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.14);
        }

        #jsmind_container jmnodes.theme-orange jmnode.selected {
            background-color: #5a6a85 !important;
            color: #f8fafc !important;
            filter: none;
            border: 1px solid rgba(51, 65, 85, 0.45) !important;
            box-shadow: 0 4px 14px rgba(30, 41, 59, 0.22);
        }

        #jsmind_container jmnodes.theme-orange jmnode.selected:hover {
            background-color: #677899 !important;
            color: #f8fafc !important;
        }

        /* Node Info Icon - MindManager Style */
        .node-info-icon {
            position: absolute;
            top: 50%;
            left: 100%;
            transform: translateY(-50%);
            margin-left: 6px;
            padding: 2px 6px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            font-size: 13px;
            cursor: pointer;
            z-index: 20;
            transition: all 0.2s ease;
            border: 1px solid rgba(0, 0, 0, 0.08);
            color: #4b5563 !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            pointer-events: auto;
            line-height: 1;
            white-space: nowrap;
        }

        .node-info-icon:hover {
            transform: translateY(-50%) scale(1.05);
            background: #ffffff;
            border-color: var(--cyan);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }

        .node-info-icon .node-info-glyph {
            display: inline-block;
            line-height: 1;
            user-select: none;
        }

        /* ===== Tooltip ===== */
        .node-tooltip {
            position: absolute;
            /* background: rgba(13, 13, 43, 0.95);
             */
             background: #797979;
            backdrop-filter: blur(10px);
            color: var(--text-primary);
            padding: 16px;
            border-radius: 12px;
            font-size: 14px;
            pointer-events: none;
            z-index: 1000;
            border: 1px solid var(--border-glow);
            box-shadow: 0 0 30px rgba(0, 240, 255, 0.15);
            display: none;
            max-width: 320px;
            line-height: 1.6;
        }

        .node-tooltip .tooltip-title {
            font-family: var(--font-display);
            font-weight: 700;
            font-size: 16px;
            color: var(--cyan);
            margin-bottom: 8px;
            border-bottom: 1px solid var(--border-glow);
            padding-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .node-tooltip .tooltip-status {
            color: var(--gold);
            font-weight: 600;
            margin: 6px 0;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .node-tooltip .tooltip-description {
            margin-top: 10px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 6px;
            font-size: 13px;
            max-height: 80px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            line-clamp: 4;
            -webkit-box-orient: vertical;
            border-left: 2px solid var(--cyan-dim);
        }

        .node-tooltip .tooltip-link {
            margin-top: 10px;
            padding: 6px 12px;
            /* background: rgba(0, 240, 255, 0.1); */
            background: rgb(50, 205, 50);
            border-radius: 4px;
            display: inline-block;
            /* color: var(--cyan); */
            color: #000;
            text-decoration: none;
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
            border: 1px solid var(--cyan-dim);
        }

        /* ===== Detail Panel ===== */
        .node-detail-panel {
            position: fixed;
            right: -420px;
            top: 0;
            width: 400px;
            height: 100vh;
            background: var(--surface-1);
            border-left: 1px solid var(--border);
            padding: 30px;
            overflow-y: auto;
            transition: right 0.4s cubic-bezier(0.19, 1, 0.22, 1);
            z-index: 2000;
            box-shadow: -4px 0 20px rgba(0, 0, 0, 0.08);
        }

        .node-detail-panel.show {
            right: 0;
        }

        .node-detail-panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(to bottom, transparent, var(--cyan), var(--purple), transparent);
            box-shadow: 0 0 15px var(--cyan);
        }

        .node-detail-panel .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-glow);
        }

        .node-detail-panel .panel-title {
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            color: var(--cyan);
            margin: 0;
            line-height: 1.2;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        }

        .node-detail-panel .panel-close {
            width: 32px;
            height: 32px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glow);
            border-radius: 50%;
            color: var(--text-primary);
            font-size: 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
            flex-shrink: 0;
            margin-left: 15px;
        }

        .node-detail-panel .panel-close:hover {
            background: var(--red);
            border-color: var(--red);
            color: #fff;
            transform: rotate(90deg) scale(1.1);
            box-shadow: 0 0 15px var(--red);
        }

        .node-detail-panel .panel-section {
            margin-bottom: 24px;
            animation: slideInRight 0.4s ease-out forwards;
            opacity: 0;
            transform: translateX(20px);
        }

        .node-detail-panel .panel-section:nth-child(2) {
            animation-delay: 0.1s;
        }

        .node-detail-panel .panel-section:nth-child(3) {
            animation-delay: 0.2s;
        }

        .node-detail-panel .panel-section:nth-child(4) {
            animation-delay: 0.3s;
        }

        .node-detail-panel .panel-section:nth-child(5) {
            animation-delay: 0.4s;
        }

        @keyframes slideInRight {
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .node-detail-panel .section-label {
            font-family: var(--font-display);
            font-size: 12px;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .node-detail-panel .section-label::after {
            content: '';
            flex: 1;
            height: 1px;
            background: rgba(255, 255, 255, 0.1);
        }

        .node-detail-panel .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 600;
            border: 1px solid transparent;
        }

        .node-detail-panel .status-badge.locked {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            border-color: rgba(255, 255, 255, 0.1);
        }

        .node-detail-panel .status-badge.unlocked {
            background: var(--cyan-dim);
            color: var(--cyan);
            border-color: var(--cyan);
            box-shadow: 0 0 10px var(--cyan-dim);
        }

        .node-detail-panel .status-badge.activated {
            background: var(--green-dim);
            color: var(--green);
            border-color: var(--green);
            box-shadow: 0 0 10px var(--green-dim);
        }

        .node-detail-panel .description-content {
            background: rgba(255, 255, 255, 0.03);
            padding: 20px;
            border-radius: 12px;
            border-left: 3px solid var(--cyan);
            line-height: 1.8;
            font-size: 14px;
            color: var(--text-primary);
            white-space: pre-wrap;
            word-wrap: break-word;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .node-detail-panel .description-content ul {
            margin: 10px 0;
            padding-left: 20px;
        }

        .node-detail-panel .description-content li {
            margin-bottom: 5px;
        }

        .node-detail-panel .description-content strong {
            color: var(--cyan);
            font-weight: 700;
        }

        .node-detail-panel .link-button {
            display: block;
            width: 100%;
            padding: 14px 20px;
            background: linear-gradient(135deg, var(--cyan-dim) 0%, rgba(168, 85, 247, 0.15) 100%);
            color: var(--cyan);
            text-decoration: none;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s;
            border: 1px solid var(--cyan-glow);
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }

        .node-detail-panel .link-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .node-detail-panel .link-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 20px var(--cyan-dim);
            border-color: var(--cyan);
            background: rgba(0, 240, 255, 0.2);
        }

        .node-detail-panel .link-button:hover::before {
            left: 100%;
        }

        /* Overlay */
        .panel-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
            z-index: 1999;
            display: none;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .panel-overlay.show {
            display: block;
            opacity: 1;
        }

        /* ===== Loader & Messages ===== */
        .loading {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: var(--font-display);
            font-size: 24px;
            color: var(--cyan);
            text-transform: uppercase;
            letter-spacing: 4px;
            text-shadow: 0 0 20px var(--cyan);
        }

        .loading::after {
            content: '';
            display: block;
            width: 60px;
            height: 60px;
            margin: 20px auto;
            border: 2px solid transparent;
            border-top-color: var(--cyan);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        .loading::before {
            content: '';
            position: absolute;
            top: calc(100% + 25px);
            left: 50%;
            transform: translateX(-50%);
            width: 40px;
            height: 40px;
            border: 2px solid transparent;
            border-bottom-color: var(--purple);
            border-radius: 50%;
            animation: spinReverse 1.5s linear infinite;
        }

        @keyframes spin {
            100% {
                transform: rotate(360deg);
            }
        }

        @keyframes spinReverse {
            100% {
                transform: translateX(-50%) rotate(-360deg);
            }
        }

        .message {
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 14px 20px;
            background: var(--surface-1);
            color: var(--text-h);
            border-radius: 8px;
            border-left: 4px solid var(--accent);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            display: none;
            z-index: 3000;
            font-size: 14px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            border: 1px solid var(--border);
            border-left-width: 4px;
        }

        .message.show {
            display: block;
            transform: translateX(0);
        }

        .message.error {
            border-left-color: var(--err);
            color: var(--err);
        }

        .message.success {
            border-left-color: var(--ok);
            color: var(--ok);
        }

        #tree_select {
            min-width: 200px;
            margin-right: 15px;
        }

        #tree_select option {
            background: var(--surface-2);
            color: var(--text-p);
            padding: 10px;
        }

        /* ===== Progress Dashboard Panel ===== */
        .progress-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(4px);
            z-index: 3000;
            display: none;
        }

        .progress-overlay.show {
            display: block;
        }

        .progress-panel {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.92);
            width: min(90vw, 780px);
            max-height: 80vh;
            background: var(--surface-1);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 32px;
            overflow-y: auto;
            z-index: 3100;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
            opacity: 0;
            pointer-events: none;
            visibility: hidden;
            transition: all 0.3s ease;
        }

        .progress-panel.show {
            opacity: 1;
            pointer-events: auto;
            visibility: visible;
            transform: translate(-50%, -50%) scale(1);
        }

        .progress-panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-glow);
        }

        .progress-panel-header h2 {
            font-family: var(--font-display);
            color: var(--cyan);
            font-size: 20px;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
            margin: 0;
        }

        .progress-panel-close {
            width: 32px;
            height: 32px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glow);
            border-radius: 50%;
            color: var(--text-primary);
            font-size: 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }

        .progress-panel-close:hover {
            background: var(--red);
            border-color: var(--red);
            color: #fff;
            transform: rotate(90deg);
        }

        .progress-user-block {
            background: var(--surface-0);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px 18px;
            margin-bottom: 14px;
        }

        .progress-username {
            font-family: var(--font-display);
            font-size: 15px;
            letter-spacing: 1px;
            color: var(--cyan);
            margin-bottom: 14px;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }

        .mod-tag {
            background: var(--accent-light);
            color: var(--accent);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            border: 1px solid var(--border);
            white-space: nowrap;
        }

        .progress-username .admin-badge {
            font-size: 10px;
            background: rgba(168, 85, 247, 0.2);
            border: 1px solid var(--purple);
            color: var(--purple);
            padding: 2px 8px;
            border-radius: 20px;
            letter-spacing: 1px;
        }

        /* 右键菜单 */
        .context-menu {
            position: fixed;
            background: var(--surface-1);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 5px 0;
            z-index: 5000;
            display: none;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            min-width: 140px;
        }

        .context-menu-item {
            padding: 10px 20px;
            color: var(--text-p);
            cursor: pointer;
            font-size: 13.5px;
            transition: background 0.15s;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .context-menu-item:hover {
            background: var(--surface-3);
            color: var(--text-h);
        }

        .context-menu-item.disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        /* 激活按钮样�?*/
        .btn-activate-main {
            width: 100%;
            padding: 13px;
            margin-top: 10px;
            background: var(--ok);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            font-size: 15px;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: background 0.15s ease, transform 0.1s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            letter-spacing: 0.5px;
        }

        .btn-activate-main:hover {
            background: #2d5a3d;
            transform: translateY(-1px);
        }

        .btn-activate-main:active {
            transform: translateY(0);
        }

        .btn-activate-main.disabled {
            background: var(--border);
            color: var(--text-s);
            cursor: not-allowed;
            box-shadow: none;
            opacity: 0.7;
        }

        .btn-activate-main.deactivate {
            background: var(--err);
        }

        /* 视图切换器样�?*/
        .view-mode-selector {
            display: flex;
            background: var(--surface-3);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 3px;
            margin-right: 15px;
            gap: 3px;
        }

        .view-mode-btn {
            padding: 6px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.15s;
            color: var(--text-s);
            border: none;
            background: transparent;
            font-family: var(--font-display);
        }

        .view-mode-btn.active {
            background: var(--accent);
            color: #ffffff;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
        }

        .view-mode-btn:hover:not(.active) {
            background: var(--surface-1);
            color: var(--text-h);
        }

        /* 画布缩放（jsMind view.zoom），固定于视窗右下角以便独立模式仍可�?*/
        .zoom-controls {
            position: fixed;
            right: 20px;
            bottom: 24px;
            z-index: 1200;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 6px 10px;
            background: var(--surface-1);
            border: 1px solid var(--border);
            border-radius: 10px;
            font-family: var(--font-display);
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.12);
        }

        body.standalone-mode .zoom-controls {
            bottom: 20px;
            right: 20px;
        }

        .zoom-controls .btn-zoom {
            min-width: 32px;
            height: 30px;
            padding: 0 8px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: #ffffff;
            color: var(--text-h);
            font-size: 16px;
            font-weight: 700;
            line-height: 1;
            cursor: pointer;
            transition: background 0.15s ease, border-color 0.15s ease;
        }

        .zoom-controls .btn-zoom:hover {
            background: var(--accent-light);
            border-color: var(--accent);
        }

        .zoom-controls .btn-zoom-reset {
            font-size: 11px;
            font-weight: 600;
            min-width: auto;
            padding: 0 10px;
        }

        #zoom_percent_label {
            min-width: 48px;
            text-align: center;
            font-size: 13px;
            font-weight: 700;
            color: var(--text-primary);
            user-select: none;
        }

        /* 节点状态图标与样式 */
        .status-icon {
            position: absolute;
            top: -8px;
            right: -8px;
            width: 18px;
            height: 18px;
            background: var(--surface-1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9px;
            border: 1px solid var(--border);
            z-index: 10;
            pointer-events: none;
        }

        .lock-icon {
            border-color: var(--err);
            color: var(--err);
        }

        .unlock-icon {
            border-color: var(--accent);
            color: var(--accent);
        }

        .active-icon {
            border-color: var(--ok);
            color: var(--ok);
        }

        .node-locked {
            opacity: 0.5;
            filter: grayscale(0.8);
            border-style: dashed !important;
            cursor: not-allowed !important;
        }

        .node-unlocked {
            border-color: var(--cyan) !important;
            box-shadow: 0 0 15px var(--cyan-glow) !important;
            cursor: pointer !important;
            animation: pulse-border 2s infinite;
        }

        @keyframes pulse-border {
            0% {
                box-shadow: 0 0 5px var(--cyan-glow);
            }

            50% {
                box-shadow: 0 0 20px var(--cyan-glow);
            }

            100% {
                box-shadow: 0 0 5px var(--cyan-glow);
            }
        }

        .node-activated {
            border-width: 2px !important;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.4) !important;
            cursor: pointer !important;
        }

        .progress-tree-row {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 12px;
        }

        .progress-tree-name {
            font-size: 13px;
            color: var(--text-secondary);
            min-width: 120px;
            flex-shrink: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .progress-bar-wrap {
            flex: 1;
            height: 10px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            background: linear-gradient(90deg, var(--cyan), var(--green));
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
        }

        .progress-bar-fill.full {
            background: linear-gradient(90deg, var(--green), #00ffa3);
            box-shadow: 0 0 12px rgba(0, 255, 136, 0.6);
        }

        .progress-stat {
            font-size: 12px;
            color: var(--text-secondary);
            min-width: 120px;
            text-align: right;
            white-space: nowrap;
        }

        .progress-stat .pct {
            font-family: var(--font-display);
            font-size: 14px;
            color: var(--gold);
            margin-left: 6px;
        }

        .progress-empty {
            text-align: center;
            color: var(--text-dim);
            padding: 30px;
            font-size: 14px;
        }

        .btn-progress {
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(0, 240, 255, 0.1) 100%);
            color: var(--purple);
            border-color: rgba(168, 85, 247, 0.5);
        }

        .btn-progress:hover {
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
            border-color: var(--purple);
            transform: translateY(-2px);
        }

        /* ===== Standalone Mode (Progress View) ===== */
        body.standalone-mode .header {
            display: none !important;
        }

        body.standalone-mode #jsmind_container {
            top: 0 !important;
            height: 100vh !important;
            margin-top: 0 !important;
        }

        body.standalone-mode .btn-standalone-close {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            background: rgba(0, 240, 255, 0.1);
            border: 1px solid var(--cyan);
            color: var(--cyan);
            padding: 8px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-family: var(--font-display);
            font-size: 13px;
            font-weight: 600;
            backdrop-filter: blur(8px);
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
            transition: all 0.3s ease;
        }

        body.standalone-mode .btn-standalone-close:hover {
            background: var(--cyan);
            color: #000;
            box-shadow: 0 0 25px var(--cyan-glow);
        }

        /* ===== Task Board Styles ===== */
        .task-board-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 15, 20, 0.85);
            backdrop-filter: blur(12px);
            z-index: 10000;
            display: none;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.4s ease;
        }

        .task-board-overlay.show {
            display: flex;
        }

        .task-board {
            width: 95%;
            max-width: 900px;
            /* 竖版布局，宽度收�?*/
            max-height: 85vh;
            background: var(--surface-1);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 30px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            box-shadow: 0 40px 100px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }

        .task-board::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, var(--cyan), var(--purple), var(--gold));
        }

        .task-board-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .task-board-header h2 {
            font-size: 28px;
            font-weight: 800;
            color: var(--text-h);
            margin: 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .task-grid {
            display: flex;
            flex-direction: column;
            /* 改为纵向垂直排列 */
            gap: 24px;
            overflow-y: auto;
            padding-right: 15px;
            margin-bottom: 20px;
        }

        .task-column {
            background: rgba(0, 0, 0, 0.15);
            border-radius: 20px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }

        .task-column-header {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 700;
            color: var(--text-s);
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .task-card {
            background: var(--surface-2);
            border-radius: 12px;
            padding: 12px;
            border-left: 3px solid var(--cyan);
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }

        .task-card:hover {
            transform: translateY(-2px);
            background: var(--surface-3);
            box-shadow: 0 4px 12px rgba(0, 240, 255, 0.1);
        }

        .task-card-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-h);
            margin-bottom: 6px;
            line-height: 1.5;
            word-break: break-all;
            white-space: normal;
        }

        .task-card-tree {
            font-size: 12px;
            color: var(--cyan);
            opacity: 0.8;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .task-card-tree::before {
            content: '📂';
            font-size: 10px;
        }

        .task-empty {
            font-size: 12px;
            color: var(--text-dim);
            text-align: center;
            margin-top: 20px;
            font-style: italic;
        }

        .task-board-close {
            background: var(--surface-3);
            border: none;
            color: var(--text-h);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            transition: all 0.2s;
        }

        .task-board-close:hover {
            background: var(--err);
            color: white;
            transform: rotate(90deg);
        }

        /* 审核相关状�?*/
        .status-badge.pending {
            background: rgba(255, 165, 0, 0.1);
            color: #ffa500;
            border: 1px solid rgba(255, 165, 0, 0.3);
        }

        .node-pending {
            border-color: #ffa500 !important;
            box-shadow: 0 0 15px rgba(255, 165, 0, 0.3) !important;
            cursor: wait !important;
        }

        .pending-icon {
            border-color: #ffa500;
            color: #ffa500;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }
    </style>
    <script type="text/javascript" src="libs/js/jsmind.js"></script>
    <script type="text/javascript" src="libs/js/jsmind.draggable-node.js"></script>
</head>

<body>
    <script>
        // 极早检测独立模式，防止 UI 闪烁
        (function () {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('standalone') === 'true') {
                document.body.classList.add('standalone-mode');
            }
        })();
    </script>
    <div class="header">
        <h1 id="tree_name">技能树</h1>
        <div class="skill-points" style="display: none;">
            <div class="skill-point-item">
                <div class="icon">�?/div>
                <div class="text">可用技能点: <span id="skill_points">0</span></div>
            </div>
            <div class="skill-point-item">
                <div class="icon">💎</div>
                <div class="text">总技能点: <span id="total_skill_points">0</span></div>
            </div>
        </div>
        <div class="toolbar">
            <div id="user_info" style="margin-right: 15px; color: var(--cyan); font-weight: bold;"></div>

            <div class="view-mode-selector">
                <button id="btn_view_tree" class="view-mode-btn active" onclick="switchViewMode('tree')">🌳
                    树状视图</button>
                <button id="btn_view_path" class="view-mode-btn" onclick="switchViewMode('path')">�?进阶路径</button>
            </div>

            <button class="btn btn-primary" onclick="logout()" style="margin-right: 15px;">登出</button>
            <button class="btn btn-progress" onclick="loadTaskBoard(true)" style="margin-right: 15px;">🎯 学习任务</button>
            <button class="btn btn-progress" onclick="showProgress()" style="margin-right: 15px;">📊 学习进度</button>
            <select id="tree_select" class="btn">
                <option value="">-- 请选择技能树 --</option>
            </select>
            <button class="btn btn-danger" onclick="resetTree()" id="reset_btn" style="display: none;">重置技能树</button>
        </div>
    </div>

    <div class="zoom-controls" title="滚轮在画布上滚动也可缩放">
        <button type="button" class="btn-zoom" onclick="mindZoomOut()" aria-label="缩小" title="缩小">�?/button>
        <span id="zoom_percent_label">100%</span>
        <button type="button" class="btn-zoom" onclick="mindZoomIn()" aria-label="放大" title="放大">+</button>
        <button type="button" class="btn-zoom btn-zoom-reset" onclick="mindZoomReset100()" title="恢复 100% 比例">100%</button>
    </div>

    <div id="jsmind_container"></div>

    <div class="node-tooltip" id="node_tooltip"></div>
    <div class="message" id="message"></div>
    <div class="loading" id="loading" style="display: none;">加载�?..</div>

    <!-- 节点详细信息面板 -->
    <div class="panel-overlay" id="panel_overlay"></div>
    <div id="context_menu" class="context-menu"></div>
    <div class="node-detail-panel" id="node_detail_panel">
        <div class="panel-header">
            <h2 class="panel-title" id="panel_node_title">节点信息</h2>
            <div class="panel-close" id="panel_close">×</div>
        </div>
        <div class="panel-section">
            <div class="section-label">状�?/div>
            <div id="panel_node_status"></div>
        </div>
        <div class="panel-section" style="display: none;">
            <div class="section-label">消耗技能点</div>
            <div style="color: var(--gold); font-size: 18px; font-weight: bold; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);"
                id="panel_node_cost">0</div>
        </div>
        <div class="panel-section" style="display: flex; gap: 20px;">
            <div style="flex: 1;">
                <div class="section-label">节点等级</div>
                <div id="panel_node_level" style="color: var(--cyan); font-weight: bold;"></div>
            </div>
            <div style="flex: 1;">
                <div class="section-label">所属模�?/div>
                <div id="panel_node_module" style="color: var(--cyan); font-weight: bold;"></div>
            </div>
        </div>
        <div class="panel-section" id="panel_description_section" style="display: none;">
            <div class="section-label">技能说�?/div>
            <div class="description-content" id="panel_node_description"></div>
        </div>
        <div class="panel-section" id="panel_link_section" style="display: none;">
            <div class="section-label">EDM SOP</div>
            <a href="#" target="_blank" class="link-button" id="panel_node_link">🔗 查看相关链接</a>
        </div>

        <div class="panel-section" id="panel_activate_section">
            <button id="btn_panel_activate" class="btn-activate-main">
                <span>�?/span> 点亮此技�?
            </button>
        </div>
    </div>

    <!-- 学习进度面板 -->
    <div class="progress-overlay" id="progress_overlay" onclick="hideProgress()"></div>
    <div class="progress-panel" id="progress_panel">
        <div class="progress-panel-header">
            <h2>📊 学习进度</h2>
            <div class="progress-panel-close" onclick="hideProgress()">×</div>
        </div>
        <div id="progress_content">
            <div class="progress-empty">加载�?..</div>
        </div>
    </div>

    <!-- 学习任务看板 (登录后弹�? -->
    <div class="task-board-overlay" id="task_board_overlay">
        <div class="task-board">
            <div class="task-board-header">
                <h2><span>🎯</span> 学习任务主页</h2>
                <button class="task-board-close" onclick="closeTaskBoard()">×</button>
            </div>
            <div class="task-grid">
                <div class="task-column">
                    <div class="task-column-header"><span>📅</span> 当日任务</div>
                    <div id="tasks_daily" class="task-list"></div>
                </div>
                <div class="task-column">
                    <div class="task-column-header"><span>🗓�?/span> 本周计划</div>
                    <div id="tasks_weekly" class="task-list"></div>
                </div>
                <div class="task-column">
                    <div class="task-column-header"><span>📊</span> 本月目标</div>
                    <div id="tasks_monthly" class="task-list"></div>
                </div>
                <div class="task-column">
                    <div class="task-column-header"><span>🏆</span> 本季�?�?/div>
                    <div id="tasks_high" class="task-list"></div>
                </div>
            </div>
            <div style="text-align: center; color: var(--text-dim); font-size: 13px;">
                * 点击任务卡片即可快速定位至对应的技能节�?
            </div>
        </div>
    </div>

    <script type="text/javascript">
        const API_BASE = '/api';
        let jm = null;
        let currentTreeId = null;
        let currentNodeUserId = null;  // 当前查看的用户ID
        let currentUser = null;  // 当前登录的用户信�?
        let nodeStatusMap = {}; // 节点状态映�?
        let originalMindData = null; // 原始树状数据备份
        let currentViewMode = 'tree'; // 当前视图模式：tree �?path

        // 事件监听器函�?
        let eventListener = null;

        // 初始化jsMind（只读模式）
        function initMindMap() {
            // 如果已存在，先清�?
            if (jm) {
                try {
                    if (eventListener) {
                        jm.clear_event_listener();
                    }
                } catch (e) {
                    console.warn('清理事件监听器失败：', e);
                }
            }

            const options = {
                container: 'jsmind_container',
                theme: 'orange',
                editable: false, // 只读模式
                view: {
                    engine: 'canvas',
                    hmargin: 120,    // 增加水平边距
                    vmargin: 60,     // 增加垂直边距
                    line_width: 3,
                    line_color: '#8B4513',
                    line_style: 'curved',
                    draggable: true,
                    hide_scrollbars_when_draggable: true,
                    node_overflow: 'wrap', // 修改�?wrap 以支持换行显�?
                    zoom: {
                        min: 0.25,
                        max: 2.5,
                        step: 0.1,
                    },
                },
                shortcut: {
                    enable: true,
                    handles: {},
                    mapping: {
                        addchild: 45,      // Insert
                        addbrother: 13,    // Enter
                        editnode: 113,     // F2
                        delnode: 46,       // Delete
                        toggle: 32,        // Space
                        left: 37,          // Left
                        up: 38,            // Up
                        right: 39,         // Right
                        down: 40           // Down
                    }
                },
                layout: {
                    hspace: 60, // 增加水平间距防止重叠
                    vspace: 40, // 增加垂直间距防止重叠
                    pspace: 15,
                    cousin_space: 0
                },
            };

            jm = new jsMind(options);

            // 创建新的事件监听�?
            eventListener = function (type, data) {
                try {
                    if (type === jsMind.event_type.select && data && data.node) {
                        const nodeId = data.node;
                        const node = jm.get_node(nodeId);
                        // 如果选中的是根节点，启用拖动功能
                        if (node && node.isroot) {
                            enableRootNodeDrag();
                        } else {
                            disableRootNodeDrag();
                        }
                        handleNodeClick(nodeId);
                    }
                } catch (error) {
                    console.error('事件处理错误�?, error);
                }
            };

            // 监听节点点击事件
            jm.add_event_listener(eventListener);

            patchJsmindZoomAgainstInflatedPanel();
        }

        /**
         * jsMind 缩小�?e_panel.getBoundingClientRect 判断「缩略图是否已小于面板」�?
         * 本页 .jsmind-inner 设了 min-width/min-height: 200%，e_panel �?rect 远大于可视区域，
         * 会误判为已够小，导致无法缩到 100% 以下。改为用 #jsmind_container 可视区判断，
         * 缩放时的滚动与锚点也以该容器为准（与空白拖动画布一致）�?
         */
        function patchJsmindZoomAgainstInflatedPanel() {
            if (!jm || !jm.view || jm.view._zoomViewportGuardPatched) return;
            const view = jm.view;
            view._zoomViewportGuardPatched = true;
            view.set_zoom = function (e, t) {
                if (e < this.opts.zoom.min || e > this.opts.zoom.max) return false;
                const outer = document.getElementById('jsmind_container');
                const vp = outer ? outer.getBoundingClientRect() : this.e_panel.getBoundingClientRect();
                if (e < 1 && e < this.zoom_current && this.size.w * e < vp.width && this.size.h * e < vp.height) {
                    return false;
                }
                const scrEl = outer || this.e_panel;
                const panelRect = this.e_panel.getBoundingClientRect();
                let n;
                if (t && typeof t.clientX === 'number') {
                    if (outer) {
                        const r = outer.getBoundingClientRect();
                        n = { x: t.clientX - r.left, y: t.clientY - r.top };
                    } else {
                        n = { x: t.clientX - panelRect.left, y: t.clientY - panelRect.top };
                    }
                } else if (t && typeof t.x === 'number') {
                    n = { x: t.x - panelRect.left, y: t.y - panelRect.top };
                } else {
                    n = { x: scrEl.clientWidth / 2, y: scrEl.clientHeight / 2 };
                }
                const sl = scrEl.scrollLeft;
                const st = scrEl.scrollTop;
                const o = (sl + n.x) * e / this.zoom_current - n.x;
                const s = (st + n.y) * e / this.zoom_current - n.y;
                this.zoom_current = e;
                for (let r = 0; r < this.e_panel.children.length; r++) {
                    this.e_panel.children[r].style.zoom = e;
                }
                this._show();
                scrEl.scrollLeft = o;
                scrEl.scrollTop = s;
                if (outer && scrEl !== this.e_panel) {
                    this.e_panel.scrollLeft = 0;
                    this.e_panel.scrollTop = 0;
                }
                return true;
            };
        }

        // 根节点拖动状�?
        let rootNodeDragEnabled = false;
        let rootDragState = {
            isDragging: false,
            startX: 0,
            startY: 0,
            startLeft: 0,
            startTop: 0
        };

        // 画布拖动（空白区域拖动，使用 scrollLeft/scrollTop，节点和连线不会分离�?
        let canvasDragEnabled = false;
        function enableCanvasDrag() {
            if (canvasDragEnabled) return;
            canvasDragEnabled = true;

            const container = document.getElementById('jsmind_container');
            if (!container) {
                canvasDragEnabled = false;
                setTimeout(() => enableCanvasDrag(), 100);
                return;
            }

            let isDragging = false;
            let startX = 0;
            let startY = 0;
            let startScrollLeft = 0;
            let startScrollTop = 0;

            const shouldDrag = (target) => {
                if (!target) return false;
                // 点击在节点上/节点内容上，不触发画布拖动（避免影响节点点击�?
                if (target.closest && target.closest('jmnode')) return false;
                if (target.closest && target.closest('.node-detail-panel')) return false;
                if (target.closest && target.closest('.panel-overlay')) return false;
                // 允许在容器、内部容器、canvas 上拖�?
                if (target === container) return true;
                if (target.classList && target.classList.contains('jsmind-inner')) return true;
                if (target.tagName && target.tagName.toLowerCase() === 'canvas') return true;
                if (target.closest && target.closest('#jsmind_container')) return true;
                return false;
            };

            function onMouseDown(e) {
                if (e.button !== 0) return; // 仅左�?
                if (!shouldDrag(e.target)) return;
                // 根节点拖动开启时，优先根节点拖动（避免两个拖动逻辑打架�?
                if (rootNodeDragEnabled) return;

                isDragging = true;
                startX = e.pageX;
                startY = e.pageY;
                startScrollLeft = container.scrollLeft;
                startScrollTop = container.scrollTop;
                container.style.cursor = 'grabbing';
                document.body.style.userSelect = 'none';
                e.preventDefault();
            }

            function onMouseMove(e) {
                if (!isDragging) return;
                const dx = e.pageX - startX;
                const dy = e.pageY - startY;
                container.scrollLeft = startScrollLeft - dx;
                container.scrollTop = startScrollTop - dy;
                e.preventDefault();
            }

            function onMouseUp() {
                if (!isDragging) return;
                isDragging = false;
                container.style.cursor = 'grab';
                document.body.style.userSelect = '';
            }

            // 防止重复绑定
            if (container._canvasDragHandlers) {
                container.removeEventListener('mousedown', container._canvasDragHandlers.mousedown);
                document.removeEventListener('mousemove', container._canvasDragHandlers.mousemove);
                document.removeEventListener('mouseup', container._canvasDragHandlers.mouseup);
            }

            container._canvasDragHandlers = { mousedown: onMouseDown, mousemove: onMouseMove, mouseup: onMouseUp };
            container.addEventListener('mousedown', onMouseDown, { passive: false });
            document.addEventListener('mousemove', onMouseMove, { passive: false });
            document.addEventListener('mouseup', onMouseUp);

            if (!container._zoomWheelLabelBound) {
                container._zoomWheelLabelBound = true;
                container.addEventListener('wheel', () => {
                    requestAnimationFrame(updateZoomLabel);
                }, { passive: true });
            }
        }

        function updateZoomLabel() {
            const el = document.getElementById('zoom_percent_label');
            if (!el) return;
            if (!jm || !jm.view) {
                el.textContent = '�?;
                return;
            }
            el.textContent = Math.round(jm.view.zoom_current * 100) + '%';
        }

        function mindZoomIn() {
            if (!jm || !jm.view) {
                showMessage('请先加载技能树', 'warning');
                return;
            }
            const ok = jm.view.zoom_in();
            updateZoomLabel();
            if (!ok) showMessage('已达到最大缩�?, 'warning');
        }

        function mindZoomOut() {
            if (!jm || !jm.view) {
                showMessage('请先加载技能树', 'warning');
                return;
            }
            const ok = jm.view.zoom_out();
            updateZoomLabel();
            if (!ok) showMessage('已达到最小缩放（整棵树已能完整放入视窗时无法继续缩小�?, 'warning');
        }

        function mindZoomReset100() {
            if (!jm || !jm.view) {
                showMessage('请先加载技能树', 'warning');
                return;
            }
            jm.view.set_zoom(1);
            updateZoomLabel();
        }

        // 重置视图并尽量居中（兼容大技能树 + scroll 容器�?
        function resetAndCenterView() {
            const container = document.getElementById('jsmind_container');
            if (!container || !jm) return;

            const inner = container.querySelector('.jsmind-inner');
            if (inner) {
                // 清掉上次拖动留下�?transform，避免初始落在角�?
                inner.style.transform = 'translate(0px, 0px)';
            }

            // 先把 scroll 移到容器“中间”，避免初始停在右下�?左上�?
            const maxScrollLeft = Math.max(0, container.scrollWidth - container.clientWidth);
            const maxScrollTop = Math.max(0, container.scrollHeight - container.clientHeight);
            container.scrollLeft = Math.floor(maxScrollLeft / 2);
            container.scrollTop = Math.floor(maxScrollTop / 2);

            // 再用 jsMind �?API 居中根节点（如果可用�?
            try {
                if (jm.mind && jm.mind.root && jm.view && typeof jm.view.center_root === 'function') {
                    jm.view.center_root(jm.mind.root);
                }
            } catch (e) {
                console.warn('resetAndCenterView: center_root failed', e);
            }
        }

        // 启用根节点拖动功能（选中根节点后，拖动整个技能树�?
        function enableRootNodeDrag() {
            if (rootNodeDragEnabled) return;

            rootNodeDragEnabled = true;
            const container = document.getElementById('jsmind_container');
            if (!container) return;

            // 查找 jsMind 的内部容器（包含 canvas 和节点的容器�?
            const jsmindInner = container.querySelector('.jsmind-inner');
            if (!jsmindInner) {
                setTimeout(() => enableRootNodeDrag(), 100);
                return;
            }

            // 确保内部容器可以移动
            if (!jsmindInner.style.position || jsmindInner.style.position === 'static') {
                jsmindInner.style.position = 'relative';
            }

            // 鼠标按下（在根节点上�?
            function handleRootMouseDown(e) {
                const selectedNode = jm.get_selected_node();
                if (!selectedNode || !selectedNode.isroot) {
                    return;
                }

                // 检查是否点击在根节点上（包括节点本身和其子元素�?
                const nodeElement = selectedNode._data && selectedNode._data.view && selectedNode._data.view.element;
                if (!nodeElement) {
                    return;
                }

                // 检查点击目标是否是根节点或其子元素（排除图标）
                const target = e.target;
                if (!nodeElement.contains(target) || target.closest('.node-info-icon')) {
                    return;
                }

                rootDragState.isDragging = true;
                rootDragState.startX = e.clientX;
                rootDragState.startY = e.clientY;

                // 获取当前内部容器的位置（�?transform �?left/top 获取�?
                let currentLeft = 0;
                let currentTop = 0;

                // 尝试�?transform 获取
                const transform = jsmindInner.style.transform;
                if (transform && transform !== 'none') {
                    const match = transform.match(/translate\(([^,]+)px,\s*([^)]+)px\)/);
                    if (match) {
                        currentLeft = parseFloat(match[1]) || 0;
                        currentTop = parseFloat(match[2]) || 0;
                    }
                } else {
                    // 如果没有 transform，尝试从 left/top 获取
                    currentLeft = parseInt(jsmindInner.style.left) || 0;
                    currentTop = parseInt(jsmindInner.style.top) || 0;
                }

                rootDragState.startLeft = currentLeft;
                rootDragState.startTop = currentTop;

                container.style.cursor = 'grabbing';
                document.body.style.userSelect = 'none';
                e.preventDefault();
                e.stopPropagation();
            }

            // 鼠标移动
            function handleRootMouseMove(e) {
                if (!rootDragState.isDragging) return;

                const deltaX = e.clientX - rootDragState.startX;
                const deltaY = e.clientY - rootDragState.startY;

                // 移动内部容器（整个技能树�?
                const newLeft = rootDragState.startLeft + deltaX;
                const newTop = rootDragState.startTop + deltaY;

                // 使用 transform 移动，性能更好
                jsmindInner.style.transform = `translate(${newLeft}px, ${newTop}px)`;

                e.preventDefault();
            }

            // 鼠标释放
            function handleRootMouseUp(e) {
                if (rootDragState.isDragging) {
                    rootDragState.isDragging = false;
                    const container = document.getElementById('jsmind_container');
                    if (container) {
                        container.style.cursor = 'grab';
                    }
                    document.body.style.userSelect = '';
                }
            }

            // 保存事件处理�?
            container._rootDragHandlers = {
                mousedown: handleRootMouseDown,
                mousemove: handleRootMouseMove,
                mouseup: handleRootMouseUp
            };

            // 添加事件监听�?
            container.addEventListener('mousedown', handleRootMouseDown, { passive: false });
            document.addEventListener('mousemove', handleRootMouseMove, { passive: false });
            document.addEventListener('mouseup', handleRootMouseUp);

            // 更新根节点样式，显示可拖动提�?
            updateRootNodeDragStyle(true);
        }

        // 禁用根节点拖动功�?
        function disableRootNodeDrag() {
            if (!rootNodeDragEnabled) return;

            rootNodeDragEnabled = false;
            rootDragState.isDragging = false;

            const container = document.getElementById('jsmind_container');
            if (container && container._rootDragHandlers) {
                container.removeEventListener('mousedown', container._rootDragHandlers.mousedown);
                container.removeEventListener('mousemove', container._rootDragHandlers.mousemove);
                container.removeEventListener('mouseup', container._rootDragHandlers.mouseup);
                delete container._rootDragHandlers;
            }

            // 更新根节点样�?
            updateRootNodeDragStyle(false);
        }

        // 更新根节点拖动样�?
        function updateRootNodeDragStyle(enabled) {
            if (!jm || !jm.mind || !jm.mind.root) return;

            const rootNode = jm.get_node(jm.mind.root.id);
            if (!rootNode || !rootNode._data || !rootNode._data.view || !rootNode._data.view.element) {
                setTimeout(() => updateRootNodeDragStyle(enabled), 100);
                return;
            }

            const element = rootNode._data.view.element;
            if (enabled) {
                element.style.cursor = 'grab';
                element.setAttribute('data-is-root', 'true');
                element.title = '拖动根节点可移动整个技能树';
                // 添加视觉提示
                element.style.border = '2px dashed rgba(255, 215, 0, 0.5)';
            } else {
                element.style.cursor = 'pointer';
                element.removeAttribute('data-is-root');
                element.title = '';
                element.style.border = '';
            }
        }

        // 处理节点点击
        async function handleNodeClick(nodeId) {
            if (!currentTreeId) {
                showMessage('请先选择一个技能树', 'error');
                return;
            }

            if (!jm || !jm.mind) {
                showMessage('技能树未加�?, 'error');
                return;
            }

            const node = jm.get_node(nodeId);
            if (!node) {
                console.warn('节点不存在：', nodeId);
                return;
            }

            // 根节点不弹出详情面板
            if (node.isroot) {
                return;
            }

            // 【优化】左键点击统一改为显示详情面板，不再直接尝试激�?
            showNodeDetailPanel(node);
        }

        // 激活节�?
        async function activateNode(nodeId) {
            if (!currentNodeUserId) {
                showMessage('请先选择用户', 'error');
                return;
            }

            try {
                const response = await fetch(`${API_BASE}/trees/${currentTreeId}/nodes/${nodeId}/activate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: currentNodeUserId
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    if (result.status === 'pending_approval') {
                        nodeStatusMap[nodeId] = 'pending_approval';
                        updateNodeStyle(nodeId, 'pending_approval');
                        showMessage('申请已提交，等待管理员或组长审核', 'info');
                    } else {
                        nodeStatusMap[nodeId] = 'activated';
                        updateNodeStyle(nodeId, 'activated');
                        updateSkillPoints(result.skill_points);
                        showMessage('节点激活成功！', 'success');
                    }
                    // 刷新详情面板状�?
                    if (jm) {
                        const node = jm.get_node(nodeId);
                        if (node) showNodeDetailPanel(node);
                    }
                    // 刷新显示
                    refreshTree();
                } else {
                    showMessage(result.error || '激活失�?, 'error');
                }
            } catch (error) {
                showMessage('网络错误�? + error.message, 'error');
            }
        }

        // ===== 学习任务系统逻辑 =====
        async function loadTaskBoard() {
            if (!currentUser) return;

            try {
                const resp = await fetch(`${API_BASE}/tasks/my?user_id=${currentUser.id}`);
                if (!resp.ok) return;

                const data = await resp.json();

                const renderTasks = (listId, tasks) => {
                    const list = document.getElementById(listId);
                    if (!list) return;

                    if (!tasks || tasks.length === 0) {
                        list.innerHTML = '<div class="task-empty">暂无任务</div>';
                        return;
                    }

                    list.innerHTML = tasks.map(t => `
                        <div class="task-card" onclick="jumpToTaskNode(${t.tree_id}, '${t.node_id}')">
                            <div class="task-card-title">${t.node_topic}</div>
                            <div class="task-card-tree">${t.tree_name}</div>
                        </div>
                    `).join('');
                };

                renderTasks('tasks_daily', data.daily);
                renderTasks('tasks_weekly', data.weekly);
                renderTasks('tasks_monthly', data.monthly);

                // 季度和年度合并显�?
                const highTasks = [...(data.quarterly || []), ...(data.yearly || [])];
                renderTasks('tasks_high', highTasks);

                // 如果有任务，则显示看�?
                const totalTasks = (data.daily?.length || 0) + (data.weekly?.length || 0) + (data.monthly?.length || 0) + highTasks.length;
                if (totalTasks > 0) {
                    showTaskBoard();
                }
            } catch (e) {
                console.warn('加载任务看板失败:', e);
            }
        }

        function showTaskBoard() {
            document.getElementById('task_board_overlay').style.display = 'flex';
        }

        function closeTaskBoard() {
            document.getElementById('task_board_overlay').style.display = 'none';
        }

        async function jumpToTaskNode(treeId, nodeId) {
            closeTaskBoard();
            // 如果已经在该树下，直接查找并跳转
            if (currentTreeId == treeId) {
                jm.select_node(nodeId);
                const node = jm.get_node(nodeId);
                if (node) showNodeDetailPanel(node);
            } else {
                // 加载新树
                document.getElementById('tree_select').value = treeId;
                await loadTree(treeId, currentUser.id);
                setTimeout(() => {
                    jm.select_node(nodeId);
                    const node = jm.get_node(nodeId);
                    if (node) showNodeDetailPanel(node);
                }, 500);
            }
        }

        // 重置技能树
        async function resetTree() {
            if (!currentTreeId || !currentUser) {
                showMessage('请先选择用户和技能树', 'error');
                return;
            }

            if (!currentUser.is_admin) {
                // 普通用户只能重置自己的
                if (!confirm('确定要重置您的技能树吗？所有已激活的节点将恢复锁定状态�?)) {
                    return;
                }

                try {
                    const response = await fetch(`${API_BASE}/users/${currentNodeUserId}/trees/${currentTreeId}/reset`, {
                        method: 'POST'
                    });

                    const result = await response.json();

                    if (response.ok) {
                        // 重置所有节点状�?
                        for (let nodeId in nodeStatusMap) {
                            nodeStatusMap[nodeId] = 'locked';
                        }
                        updateSkillPoints(result.skill_points);
                        showMessage('技能树已重�?, 'success');
                        refreshTree();
                    } else {
                        showMessage('重置失败', 'error');
                    }
                } catch (error) {
                    showMessage('网络错误�? + error.message, 'error');
                }
                return;
            }

            // 管理员可以重置所有用户或指定用户
            const resetAll = confirm('是否重置所有用户的技能树？\n点击"确定"重置所有用户，点击"取消"只重置当前用�?);

            try {
                const response = await fetch(`${API_BASE}/trees/${currentTreeId}/reset`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: currentUser.id,
                        target_user_id: resetAll ? null : currentNodeUserId
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    // 重置所有节点状�?
                    for (let nodeId in nodeStatusMap) {
                        nodeStatusMap[nodeId] = 'locked';
                    }
                    updateSkillPoints(result.skill_points);
                    showMessage('技能树已重�?, 'success');
                    refreshTree();
                } else {
                    showMessage('重置失败', 'error');
                }
            } catch (error) {
                showMessage('网络错误�? + error.message, 'error');
            }
        }

        // 使用当前登录用户的身�?
        async function loadUserList() {
            const currentUserStr = localStorage.getItem('currentUser');
            if (!currentUserStr) {
                window.location.href = '/login.html?redirect=/view.html';
                return;
            }

            currentUser = JSON.parse(currentUserStr);
            currentNodeUserId = currentUser.id;

            // 显示用户信息
            const userInfoEl = document.getElementById('user_info');
            if (userInfoEl) {
                let role = '';
                if (currentUser.is_admin) role = ' (管理�?';
                else if (currentUser.is_leader) role = ' (组长)';
                userInfoEl.textContent = '👤 ' + currentUser.username + role;
            }

            // 显示/隐藏重置按钮（只有管理员可以重置所有用户）
            const resetBtn = document.getElementById('reset_btn');
            if (resetBtn) resetBtn.style.display = currentUser.is_admin ? 'inline-block' : 'none';

            // 加载技能树列表
            await loadTreeList();
        }

        // 登出
        function logout() {
            localStorage.removeItem('currentUser');
            window.location.href = '/login.html?redirect=/view.html';
        }


        // 加载技能树列表到下拉框
        async function loadTreeList() {
            if (!currentUser) {
                showMessage('请先选择用户', 'error');
                return;
            }

            try {
                const response = await fetch(`${API_BASE}/trees?user_id=${currentUser.id}`);
                const trees = await response.json();

                const select = document.getElementById('tree_select');
                select.innerHTML = '<option value="">-- 请选择技能树 --</option>';

                if (trees.length === 0) {
                    select.innerHTML = '<option value="">暂无技能树，请先在管理页面创建</option>';
                    showMessage('暂无技能树，请先在管理页面创建', 'error');
                    return;
                }

                trees.forEach(tree => {
                    const option = document.createElement('option');
                    option.value = tree.id;
                    // 在名称后标注权限
                    const suffix = tree.can_activate ? '' : ' (🔒只读)';
                    option.textContent = tree.name + suffix;
                    if (!tree.can_activate) {
                        option.style.color = 'var(--text-dim)';
                    }
                    select.appendChild(option);
                });

                // 监听选择变化
                select.onchange = function () {
                    const treeId = parseInt(this.value);
                    if (treeId && currentNodeUserId) {
                        loadTree(treeId, currentNodeUserId);
                    }
                };

            } catch (error) {
                showMessage('加载列表失败�? + error.message, 'error');
            }
        }

        // 加载指定技能树
        async function loadTree(treeId, userId = null) {
            if (!userId && !currentNodeUserId) {
                showMessage('请先选择用户', 'error');
                return;
            }

            userId = userId || currentNodeUserId;
            document.getElementById('loading').style.display = 'block';

            try {
                const response = await fetch(`${API_BASE}/trees/${treeId}?user_id=${userId}`);
                if (!response.ok) {
                    throw new Error('加载失败�? + response.statusText);
                }

                const mindData = await response.json();

                // 为节点添加等级星号展示（仅前端显示用，不修改后台数据库）
                // function decorateNodesWithStars(node) {
                //     if (node && node.topic) {
                //         // 如果节点�?level 属性，�?topic 前面还没有星星（防止重复添加�?
                //         if (node.level && !node.topic.startsWith("�?)) {
                //             const level = parseInt(node.level) || 1;
                //             const stars = "�?.repeat(Math.min(level, 5));
                //             node.topic = stars + node.topic;
                //         }
                //     }
                //     if (node.children && Array.isArray(node.children)) {
                //         node.children.forEach(decorateNodesWithStars);
                //     }
                // }

                // 为节点添加等级星号展示并确保保留描述/链接字段
                // 修改 view.html 中的这个函数
                function decorateNodesWithStars(node) {
                    if (node) {
                        // 1. 处理星星标题
                        if (node.topic && node.level && !node.topic.startsWith("�?)) {
                            const level = parseInt(node.level) || 1;
                            const stars = "�?.repeat(Math.min(level, 5));
                            node.topic = stars + node.topic;
                        }

                        // 2. 确保 description / link 等在 jsMind �?node.data 中（与后�?index 一致，供图标读取）
                        if (!node.data) node.data = {};
                        const extraFields = ['description', 'link', 'link2', 'level', 'module', 'cost'];
                        extraFields.forEach(field => {
                            const fromTop = node[field];
                            const fromData = node.data[field];
                            if (fromTop !== undefined && fromTop !== null && String(fromTop).trim() !== '') {
                                node.data[field] = fromTop;
                            } else if (fromData !== undefined && fromData !== null) {
                                node.data[field] = fromData;
                            }
                        });
                    }
                    if (node.children && Array.isArray(node.children)) {
                        node.children.forEach(decorateNodesWithStars);
                    }
                }

                if (mindData && mindData.data) {
                    decorateNodesWithStars(mindData.data);
                }

                // 记录当前技能树是否可激�?
                window.currentTreeCanActivate = mindData.meta ? mindData.meta.can_activate : true;

                // 如果是只读，显示提示
                if (window.currentTreeCanActivate === false) {
                    showMessage('当前技能树为只读模�?, 'info');
                }

                if (!mindData || !mindData.data) {
                    throw new Error('技能树数据格式错误：缺�?data 字段');
                }

                // 统计节点数量
                function countNodes(node) {
                    let count = 1;
                    if (node.children && Array.isArray(node.children)) {
                        node.children.forEach(child => {
                            count += countNodes(child);
                        });
                    }
                    return count;
                }
                const nodeCount = countNodes(mindData.data);
                console.log(`接收到的节点总数�?{nodeCount}`);

                // 保存节点状�?
                nodeStatusMap = {};
                function collectStatus(node) {
                    if (node && node.id) {
                        nodeStatusMap[node.id] = node.status || 'locked';
                    }
                    if (node && node.children && Array.isArray(node.children)) {
                        node.children.forEach(collectStatus);
                    }
                }
                collectStatus(mindData.data);
                console.log('节点状态映射：', nodeStatusMap);

                // 确保 jm 已初始化
                if (!jm) {
                    initMindMap();
                }

                // 验证数据格式
                if (!mindData.data || !mindData.data.id || !mindData.data.topic) {
                    throw new Error('技能树数据格式错误：缺少根节点信息');
                }

                // 清理并重置（避免之前的数据干扰）
                if (jm && jm.mind) {
                    try {
                        // 先清除事件监听器
                        jm.clear_event_listener();
                        // 重置
                        jm._reset();
                        // 重新添加事件监听�?
                        if (eventListener) {
                            jm.add_event_listener(eventListener);
                        }
                    } catch (resetError) {
                        console.warn('重置失败，重新初始化�?, resetError);
                        // 如果重置失败，重新初始化
                        initMindMap();
                    }
                }

                // 显示技能树
                try {
                    // 备份原始数据
                    originalMindData = JSON.parse(JSON.stringify(mindData));

                    let displayData = mindData;
                    // 如果当前是进阶模式，转换数据
                    if (currentViewMode === 'path') {
                        displayData = getLinearMindData(mindData);
                    }

                    // 显示数据
                    jm.show(displayData, true);
                    currentTreeId = treeId;
                    currentNodeUserId = userId;

                    // 预留一些时间让浏览器渲染文字换行和星星装饰
                    setTimeout(() => {
                        if (jm) {
                            jm.resize(); // 核心：强制重新计算每个节点的大小和位�?
                            applyNodeStyles(); // 应用解锁图标等样�?
                            resetAndCenterView(); // 居中
                            updateZoomLabel();
                        }
                    }, 50);

                    // 前台交互：启用空白处拖动画布，并�?show 后重�?居中视图
                    enableCanvasDrag();
                    resetAndCenterView();
                    updateZoomLabel();

                    // 等待一帧确保渲染完�?
                    requestAnimationFrame(() => {
                        // 再次保障性调�?
                        if (jm) jm.resize();
                        updateZoomLabel();

                        // 检查渲染结�?
                        if (jm && jm.mind && jm.mind.nodes) {
                            const renderedNodeCount = Object.keys(jm.mind.nodes).length;
                            console.log(`渲染后的节点数：${renderedNodeCount}`);
                        }

                        // 更新UI
                        document.getElementById('tree_name').textContent = mindData.meta.name || '技能树';
                        updateSkillPoints(mindData.meta.skill_points || 0, mindData.meta.total_skill_points || 0);

                        // 应用节点样式（延迟执行，确保DOM已稳定）
                        setTimeout(() => {
                            if (jm && jm.mind && jm.mind.nodes) {
                                jm.resize();
                                applyNodeStyles();
                            }
                        }, 500);

                        // 再次应用样式，确保颜色正确显�?
                        setTimeout(() => {
                            if (jm && jm.mind && jm.mind.nodes) {
                                jm.resize();
                                applyNodeStyles();
                            }
                        }, 1200);

                        // 最终兜底，确保所有图标都能显�?(针对大数据量或慢速加�?
                        setTimeout(() => {
                            if (jm && jm.mind && jm.mind.nodes) {
                                applyNodeStyles();
                            }
                        }, 2500);
                    });
                } catch (showError) {
                    console.error('显示技能树错误�?, showError);
                    console.error('错误堆栈�?, showError.stack);
                    console.error('数据内容�?, JSON.stringify(mindData, null, 2));
                    throw new Error('显示技能树失败�? + showError.message);
                }

                showMessage('技能树加载成功', 'success');
            } catch (error) {
                console.error('加载技能树错误�?, error);
                showMessage('加载失败�? + error.message, 'error');
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }

        // 应用节点样式
        function applyNodeStyles() {
            // jsMind canvas 引擎的画布在 view.graph.e_canvas，不存在 view.canvas；误判断会导致整段逻辑从不执行
            if (!jm || !jm.view || !jm.mind || !jm.mind.nodes) {
                console.warn('技能树未加载，无法应用样式');
                return;
            }

            try {
                const nodes = jm.mind.nodes;
                Object.keys(nodes).forEach(nodeId => {
                    const status = nodeStatusMap[nodeId] || 'locked';
                    updateNodeStyle(nodeId, status);
                    addNodeInfoIcon(nodeId);
                });

                // 图标�?absolute，勿在逐节�?addNodeInfoIcon 内调�?resize（会重排 DOM 导致图标丢失�?
                if (jm && typeof jm.resize === 'function') {
                    requestAnimationFrame(() => jm.resize());
                }

                // 渲染扩展元素（外框和联系线）
                renderMindMapExtras();
            } catch (error) {
                console.error('应用节点样式错误�?, error);
                setTimeout(() => {
                    if (jm && jm.mind && jm.mind.nodes) {
                        applyNodeStyles();
                    }
                }, 500);
            }
        }

        // 渲染扩展元素 (外框、联系线)
        function renderMindMapExtras() {
            if (!jm || !jm.view || currentViewMode === 'path') return;

            const canvas = jm.view.graph?.e_canvas || jm.view.canvas;
            const ctx = jm.view.graph?.canvas_ctx || (canvas ? canvas.getContext('2d') : null);
            if (!canvas || !ctx) return;

            let extraData = {};
            try {
                const rawExtra = originalMindData?.meta?.extra_data;
                if (rawExtra) {
                    extraData = typeof rawExtra === 'string' ? JSON.parse(rawExtra) : rawExtra;
                }
            } catch (e) {
                console.warn('解析扩展数据失败:', e);
            }

            // 在这一步，我们不执�?clearRect，因�?jsMind 的连线也在这�?canvas �?
            // 我们只需要叠加绘制即�?

            // 1. 自动外框 (基于 module 属�?
            if (extraData.autoBoundaries !== false) { // 默认开�?
                const moduleGroups = {};
                if (jm.mind && jm.mind.nodes) {
                    Object.values(jm.mind.nodes).forEach(node => {
                        const mod = node.data.module;
                        if (mod && mod !== '默认模块') {
                            if (!moduleGroups[mod]) moduleGroups[mod] = [];
                            moduleGroups[mod].push(node.id);
                        }
                    });

                    Object.keys(moduleGroups).forEach(mod => {
                        drawBoundary(ctx, {
                            nodes: moduleGroups[mod],
                            topic: mod,
                            color: 'rgba(128, 128, 128, 0.4)',
                            bgColor: 'rgba(128, 128, 128, 0.02)'
                        });
                    });
                }
            }

            // 2. 手动外框渲染
            if (extraData.boundaries && Array.isArray(extraData.boundaries)) {
                extraData.boundaries.forEach(b => drawBoundary(ctx, b));
            }

            // 3. 联系线渲�?
            if (extraData.relationships && Array.isArray(extraData.relationships)) {
                extraData.relationships.forEach(r => drawRelationship(ctx, r));
            }
        }

        // 渲染循环 (View 页面)
        function initRenderLoop() {
            const loop = () => {
                if (jm && jm.mind && currentViewMode !== 'path') {
                    renderMindMapExtras();
                }
                requestAnimationFrame(loop);
            };
            loop();
        }

        // 在适当位置启动循环
        setTimeout(initRenderLoop, 2000);

        // 绘制外框
        function drawBoundary(ctx, boundary) {
            if (!boundary.nodes || boundary.nodes.length === 0) return;

            let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
            let found = false;

            boundary.nodes.forEach(id => {
                const node = jm.get_node(id);
                if (node) {
                    const loc = node.get_location();
                    const size = node.get_size();
                    minX = Math.min(minX, loc.x);
                    minY = Math.min(minY, loc.y);
                    maxX = Math.max(maxX, loc.x + size.w);
                    maxY = Math.max(maxY, loc.y + size.h);
                    found = true;
                }
            });

            if (!found) return;

            const padding = 15;
            minX -= padding;
            minY -= padding;
            maxX += padding;
            maxY += padding;
            const w = maxX - minX;
            const h = maxY - minY;

            if (boundary.style === 'brace' || boundary.style === 'bracket' || boundary.style === 'curved') {
                // 绘制概要大括�?方括�?(Summary Style)
                ctx.save();
                ctx.strokeStyle = boundary.color || 'rgba(168, 85, 247, 0.8)';
                ctx.lineWidth = 2.5;
                ctx.lineCap = 'round';

                const midY = (minY + maxY) / 2;
                const braceX = maxX + 4;
                const tipX = braceX + 10;

                ctx.beginPath();
                if (boundary.style === 'brace') {
                    // Curly Brace �?
                    ctx.moveTo(maxX, minY + 5);
                    ctx.quadraticCurveTo(braceX, minY + 5, braceX, minY + 20);
                    ctx.lineTo(braceX, midY - 15);
                    ctx.quadraticCurveTo(braceX, midY, tipX, midY);
                    ctx.quadraticCurveTo(braceX, midY, braceX, midY + 15);
                    ctx.lineTo(braceX, maxY - 20);
                    ctx.quadraticCurveTo(braceX, maxY - 5, maxX, maxY - 5);
                } else if (boundary.style === 'bracket') {
                    // Square Bracket �?
                    ctx.moveTo(maxX, minY + 5);
                    ctx.lineTo(braceX, minY + 5);
                    ctx.lineTo(braceX, maxY - 5);
                    ctx.lineTo(maxX, maxY - 5);
                    // 加上中间的突�?tip
                    ctx.moveTo(braceX, midY);
                    ctx.lineTo(tipX, midY);
                } else {
                    // Curved Bracket �?
                    ctx.moveTo(maxX, minY + 5);
                    ctx.quadraticCurveTo(tipX, midY, maxX, maxY - 5);
                }
                ctx.stroke();

                if (boundary.topic) {
                    ctx.save();
                    const fontSize = boundary.fontSize || 14;
                    ctx.font = `bold ${fontSize}px "Inter", sans-serif`;
                    const textWidth = ctx.measureText(boundary.topic).width;
                    const textHeight = fontSize;

                    // 绘制文字背景 (Pill Shape)
                    ctx.fillStyle = 'rgba(20, 20, 20, 0.7)';
                    const bgX = tipX + 8;
                    const bgY = midY - textHeight / 2 - 6;
                    const bgW = textWidth + 16;
                    const bgH = textHeight + 10;
                    const radius = bgH / 2;

                    ctx.beginPath();
                    ctx.moveTo(bgX + radius, bgY);
                    ctx.arcTo(bgX + bgW, bgY, bgX + bgW, bgY + bgH, radius);
                    ctx.arcTo(bgX + bgW, bgY + bgH, bgX, bgY + bgH, radius);
                    ctx.arcTo(bgX, bgY + bgH, bgX, bgY, radius);
                    ctx.arcTo(bgX, bgY, bgX + bgW, bgY, radius);
                    ctx.closePath();
                    ctx.fill();

                    // 绘制文字
                    ctx.fillStyle = boundary.color || 'rgb(168, 85, 247)';
                    ctx.fillText(boundary.topic, bgX + 8, midY + textHeight / 2 - 2);
                    ctx.restore();
                }
                ctx.restore();
                return;
            }

            if (boundary.style === 'cloud') {
                // 绘制云朵外框 (Cloud/Scalloped style)
                ctx.save();
                ctx.beginPath();
                ctx.setLineDash([]);
                ctx.strokeStyle = boundary.color || 'rgba(236, 72, 153, 0.6)';
                ctx.lineWidth = 2;

                const step = 20; // 弧线的宽�?
                for (let x = minX; x < maxX; x += step) ctx.arc(x + step / 2, minY, step / 2 + 2, Math.PI, 0, false);
                for (let y = minY; y < maxY; y += step) ctx.arc(maxX, y + step / 2, step / 2 + 2, -Math.PI / 2, Math.PI / 2, false);
                for (let x = maxX; x > minX; x -= step) ctx.arc(x - step / 2, maxY, step / 2 + 2, 0, Math.PI, false);
                for (let y = maxY; y > minY; y -= step) ctx.arc(minX, y - step / 2, step / 2 + 2, Math.PI / 2, -Math.PI / 2, false);

                ctx.stroke();

                // 使用 destination-over 确保背景在连线下�?
                ctx.save();
                ctx.globalCompositeOperation = 'destination-over';
                ctx.fillStyle = boundary.bgColor || 'rgba(236, 72, 153, 0.12)';
                ctx.fill();
                ctx.restore();

                if (boundary.topic) {
                    ctx.save();
                    const fontSize = boundary.fontSize || 14;
                    ctx.font = `bold ${fontSize}px "Inter", sans-serif`;
                    const textWidth = ctx.measureText(boundary.topic).width;
                    const textHeight = fontSize;

                    // 绘制文字背景 (Pill Shape)
                    ctx.fillStyle = 'rgba(20, 20, 20, 0.7)';
                    const bgX = minX + 8;
                    const bgY = minY - textHeight - 12;
                    const bgW = textWidth + 16;
                    const bgH = textHeight + 8;
                    const radius = bgH / 2;

                    ctx.beginPath();
                    ctx.moveTo(bgX + radius, bgY);
                    ctx.arcTo(bgX + bgW, bgY, bgX + bgW, bgY + bgH, radius);
                    ctx.arcTo(bgX + bgW, bgY + bgH, bgX, bgY + bgH, radius);
                    ctx.arcTo(bgX, bgY + bgH, bgX, bgY, radius);
                    ctx.arcTo(bgX, bgY, bgX + bgW, bgY, radius);
                    ctx.closePath();
                    ctx.fill();

                    // 绘制文字
                    ctx.fillStyle = boundary.color || '#EC4899';
                    ctx.fillText(boundary.topic, bgX + 8, bgY + textHeight + 2);
                    ctx.restore();
                }
                ctx.restore();
                return;
            }

            // 默认为矩形外�?
            ctx.save();
            ctx.beginPath();
            ctx.setLineDash([6, 4]);
            ctx.strokeStyle = boundary.color || 'rgba(255, 127, 39, 0.8)';
            ctx.lineWidth = 2.5;

            const r = 20; // 增大圆角
            ctx.moveTo(minX + r, minY);
            ctx.arcTo(maxX, minY, maxX, maxY, r);
            ctx.arcTo(maxX, maxY, minX, maxY, r);
            ctx.arcTo(minX, maxY, minX, minY, r);
            ctx.arcTo(minX, minY, maxX, minY, r);
            ctx.closePath();
            ctx.stroke();

            // 使用 destination-over 确保背景在连线下�?
            ctx.save();
            ctx.globalCompositeOperation = 'destination-over';
            ctx.fillStyle = boundary.bgColor || 'rgba(255, 127, 39, 0.12)';
            ctx.fill();
            ctx.restore();

            // 绘制标题 (优化设计：气�?药丸形状背景)
            if (boundary.topic && boundary.style !== 'cloud') {
                ctx.save();
                ctx.setLineDash([]);
                const fontSize = boundary.fontSize || 14;
                ctx.font = `bold ${fontSize}px "Inter", sans-serif`;

                const textWidth = ctx.measureText(boundary.topic).width;
                const textHeight = fontSize;

                // 绘制文字背景 (Pill Shape)
                ctx.fillStyle = 'rgba(20, 20, 20, 0.7)';
                const bgX = minX + 8;
                const bgY = minY - textHeight - 12;
                const bgW = textWidth + 16;
                const bgH = textHeight + 8;
                const radius = bgH / 2;

                ctx.beginPath();
                ctx.moveTo(bgX + radius, bgY);
                ctx.arcTo(bgX + bgW, bgY, bgX + bgW, bgY + bgH, radius);
                ctx.arcTo(bgX + bgW, bgY + bgH, bgX, bgY + bgH, radius);
                ctx.arcTo(bgX, bgY + bgH, bgX, bgY, radius);
                ctx.arcTo(bgX, bgY, bgX + bgW, bgY, radius);
                ctx.closePath();
                ctx.fill();

                // 绘制文字
                ctx.fillStyle = boundary.color || 'rgb(207, 77, 12)';
                ctx.fillText(boundary.topic, bgX + 8, bgY + textHeight + 2);
                ctx.restore();
            }
            ctx.restore();
        }

        // 绘制联系�?
        function drawRelationship(ctx, rel) {
            const nodeFrom = jm.get_node(rel.from);
            const nodeTo = jm.get_node(rel.to);
            if (!nodeFrom || !nodeTo) return;

            const locFrom = nodeFrom.get_location();
            const sizeFrom = nodeFrom.get_size();
            const locTo = nodeTo.get_location();
            const sizeTo = nodeTo.get_size();

            const p1 = { x: locFrom.x + sizeFrom.w / 2, y: locFrom.y + sizeFrom.h / 2 };
            const p2 = { x: locTo.x + sizeTo.w / 2, y: locTo.y + sizeTo.h / 2 };

            ctx.save();
            ctx.beginPath();
            ctx.strokeStyle = rel.color || 'rgba(168, 85, 247, 0.6)';
            ctx.lineWidth = 2;
            ctx.setLineDash([4, 3]);

            // 使用三次贝塞尔曲线，显得更专�?
            const dist = Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
            const cp1 = { x: p1.x + (p2.x - p1.x) * 0.2, y: p1.y - dist * 0.2 };
            const cp2 = { x: p1.x + (p2.x - p1.x) * 0.8, y: p2.y - dist * 0.2 };

            ctx.moveTo(p1.x, p1.y);
            ctx.bezierCurveTo(cp1.x, cp1.y, cp2.x, cp2.y, p2.x, p2.y);
            ctx.stroke();

            // 绘制箭头
            const angle = Math.atan2(p2.y - cp2.y, p2.x - cp2.x);
            ctx.beginPath();
            ctx.setLineDash([]);
            ctx.fillStyle = rel.color || 'rgba(168, 85, 247, 0.8)';
            ctx.moveTo(p2.x, p2.y);
            ctx.lineTo(p2.x - 12 * Math.cos(angle - Math.PI / 8), p2.y - 12 * Math.sin(angle - Math.PI / 8));
            ctx.lineTo(p2.x - 12 * Math.cos(angle + Math.PI / 8), p2.y - 12 * Math.sin(angle + Math.PI / 8));
            ctx.closePath();
            ctx.fill();

            // 绘制关系名称标签 (Pill Shape)
            if (rel.topic) {
                const midX = (cp1.x + cp2.x) / 2;
                const midY = (cp1.y + cp2.y) / 2;
                ctx.save();
                ctx.font = 'bold 12px "Inter", sans-serif';
                const textWidth = ctx.measureText(rel.topic).width;
                const textHeight = 12;

                // 绘制文字背景 (Premium Pill Shape)
                ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
                const bgX = midX - textWidth / 2 - 10;
                const bgY = midY - textHeight / 2 - 6;
                const bgW = textWidth + 20;
                const bgH = textHeight + 12;
                const radius = bgH / 2;

                ctx.beginPath();
                ctx.moveTo(bgX + radius, bgY);
                ctx.arcTo(bgX + bgW, bgY, bgX + bgW, bgY + bgH, radius);
                ctx.arcTo(bgX + bgW, bgY + bgH, bgX, bgY + bgH, radius);
                ctx.arcTo(bgX, bgY + bgH, bgX, bgY, radius);
                ctx.arcTo(bgX, bgY, bgX + bgW, bgY, radius);
                ctx.closePath();
                ctx.fill();

                // 增加精细边框
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.lineWidth = 1;
                ctx.stroke();

                ctx.fillStyle = rel.color || 'rgb(168, 85, 247)';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(rel.topic, midX, midY);
                ctx.restore();
            }
            ctx.restore();
        }

        /** 用于移除重复�?tooltip 监听（避免多�?applyNodeStyles 叠加�?*/
        const VIEW_NODE_TOOLTIP_KEY = '__viewMindNodeTooltipHandlers';

        function addNodeInfoIcon(nodeId) {
            if (!jm || !jm.mind) return;

            const node = jm.get_node(nodeId);
            if (!node || !node._data || !node._data.view || !node._data.view.element) {
                setTimeout(() => addNodeInfoIcon(nodeId), 100);
                return;
            }

            const element = node._data.view.element;
            const n = node;
            const d = node.data || {};

            const desc = (d.description || n.description || '').toString().trim();
            const l1 = (d.link || n.link || '').toString().trim();
            const l2 = (d.link2 || n.link2 || '').toString().trim();

            const hasDescription = desc.length > 0;
            const hasLink = l1.length > 0 || l2.length > 0;

            const oldIcon = element.querySelector('.node-info-icon');
            if (oldIcon) oldIcon.remove();

            if (element[VIEW_NODE_TOOLTIP_KEY]) {
                const h = element[VIEW_NODE_TOOLTIP_KEY];
                element.removeEventListener('mouseenter', h.enter);
                element.removeEventListener('mouseleave', h.leave);
                element.removeEventListener('mousemove', h.move);
                delete element[VIEW_NODE_TOOLTIP_KEY];
            }

            if (!hasDescription && !hasLink) {
                return;
            }

            const iconElement = document.createElement('div');
            iconElement.className = 'node-info-icon';
            iconElement.setAttribute('role', 'img');
            iconElement.setAttribute('aria-label', (hasDescription ? '含技能说�?' : '') + (hasLink ? '含相关链�? : ''));

            let inner = '';
            if (hasDescription) {
                inner += '<span class="node-info-glyph" title="有技能说�?>📝</span>';
            }
            if (hasLink) {
                inner += '<span class="node-info-glyph" title="有相关链�?>🔗</span>';
            }
            iconElement.innerHTML = inner;
            iconElement.title = (hasDescription ? '有技能说明\n' : '') + (hasLink ? '有链接信�? : '');

            element.appendChild(iconElement);

            let tooltipTimer = null;
            const enterFn = function (e) {
                if (tooltipTimer) clearTimeout(tooltipTimer);
                tooltipTimer = setTimeout(() => {
                    showTooltip(node, e);
                }, 300);
            };
            const leaveFn = function () {
                if (tooltipTimer) clearTimeout(tooltipTimer);
                hideTooltip();
            };
            const moveFn = function (e) {
                if (tooltipTimer) {
                    updateTooltipPosition(e);
                }
            };

            element.addEventListener('mouseenter', enterFn);
            element.addEventListener('mouseleave', leaveFn);
            element.addEventListener('mousemove', moveFn);
            element[VIEW_NODE_TOOLTIP_KEY] = { enter: enterFn, leave: leaveFn, move: moveFn };
        }


        // 显示 Tooltip
        function showTooltip(node, event) {
            const tooltip = document.getElementById('node_tooltip');
            if (!tooltip) return;

            const nodeData = node.data || {};
            const status = nodeStatusMap[node.id] || 'locked';
            const cost = nodeData.cost || node.cost || 1;
            const description = (nodeData.description || node.description || '').toString();
            const link = (nodeData.link || node.link || '').toString();
            const level = nodeData.level || node.level || 1;
            const moduleStr = nodeData.module || node.module || '默认模块';

            let statusText = '';
            if (status === 'locked') statusText = '🔒 锁定';
            else if (status === 'unlocked') statusText = '🔓 已解�?;
            else if (status === 'activated') statusText = '�?已激�?;

            const stars = '�?.repeat(level);

            let html = `
                <div class="tooltip-title">${node.topic}</div>
                <div class="tooltip-status">${statusText}</div>
                <div style="font-size: 12px; color: var(--cyan-dim); margin: 6px 0;">等级: ${stars} (${level}�? | 模块: ${moduleStr}</div>
            `;

            if (description) {
                html += `<div class="tooltip-description">${description}</div>`;
            }

            if (link) {
                // 确保链接格式正确
                let formattedLink = link.trim();
                if (!formattedLink.match(/^https?:\/\//i)) {
                    formattedLink = 'http://' + formattedLink;
                }
                const safeLink = formattedLink.replace(/</g, '&lt;').replace(/>/g, '&gt;');
                html += `<a href="${safeLink}" target="_blank" class="tooltip-link" onclick="event.stopPropagation();">🔗 链接 1</a>`;
            }

            const link2 = (nodeData.link2 || node.link2 || '').toString();
            if (link2) {
                let formattedLink = link2.trim();
                if (!formattedLink.match(/^https?:\/\//i)) {
                    formattedLink = 'http://' + formattedLink;
                }
                const safeLink = formattedLink.replace(/</g, '&lt;').replace(/>/g, '&gt;');
                html += `<a href="${safeLink}" target="_blank" class="tooltip-link" style="margin-left: 8px;" onclick="event.stopPropagation();">🔗 链接 2</a>`;
            }

            tooltip.innerHTML = html;
            tooltip.style.display = 'block';
            updateTooltipPosition(event);
        }

        // 更新 Tooltip 位置
        function updateTooltipPosition(event) {
            const tooltip = document.getElementById('node_tooltip');
            if (!tooltip || tooltip.style.display === 'none') return;

            const x = event.clientX + 15;
            const y = event.clientY + 15;

            tooltip.style.left = x + 'px';
            tooltip.style.top = y + 'px';

            // 检查是否超出屏幕，自动调整位置
            const rect = tooltip.getBoundingClientRect();
            if (rect.right > window.innerWidth) {
                tooltip.style.left = (event.clientX - rect.width - 15) + 'px';
            }
            if (rect.bottom > window.innerHeight) {
                tooltip.style.top = (event.clientY - rect.height - 15) + 'px';
            }
        }

        // 隐藏 Tooltip
        function hideTooltip() {
            const tooltip = document.getElementById('node_tooltip');
            if (tooltip) {
                tooltip.style.display = 'none';
            }
        }

        // 更新节点样式
        function updateNodeStyle(nodeId, status) {
            if (!jm || !jm.mind) return;

            const node = jm.get_node(nodeId);
            if (!node) return;

            // 安全检查：确保 _data �?view 存在
            if (!node._data || !node._data.view || !node._data.view.element) {
                // 如果元素还未创建，稍后重�?
                setTimeout(() => updateNodeStyle(nodeId, status), 100);
                return;
            }

            const element = node._data.view.element;
            if (!element) return;

            // 清理旧状态类
            element.classList.remove('node-locked', 'node-unlocked', 'node-activated');

            // 清理旧状态图�?
            const oldIcons = element.querySelectorAll('.status-icon');
            oldIcons.forEach(icon => icon.remove());

            // 获取节点数据中的颜色信息
            const nodeData = node.data || {};
            const displayBgColor = nodeData['background-color'] || '#666666';
            const displayFgColor = nodeData['foreground-color'] || '#999999';

            // 根据状态设置颜色和样式
            if (status === 'activated') {
                element.classList.add('node-activated');
                element.style.backgroundColor = displayBgColor;
                element.style.color = displayFgColor;
                element.style.opacity = '1';
                element.style.filter = 'none';
                element.style.setProperty('background-color', element.style.backgroundColor, 'important');

                const activeIcon = document.createElement('div');
                activeIcon.className = 'status-icon active-icon';
                activeIcon.innerHTML = '�?;
                element.appendChild(activeIcon);
            } else if (status === 'unlocked') {
                element.classList.add('node-unlocked');
                element.style.backgroundColor = '#444444';
                element.style.color = '#cccccc';
                element.style.opacity = '0.8';

                const unlockIcon = document.createElement('div');
                unlockIcon.className = 'status-icon unlock-icon';
                unlockIcon.innerHTML = '🔓';
                element.appendChild(unlockIcon);
            } else if (status === 'pending_approval') {
                element.classList.add('node-pending');
                // 更加突出的琥珀�?橙色视觉，增加脉动或明显边框
                element.style.backgroundColor = '#4d3b00'; // 深琥珀色背�?
                element.style.border = '2px solid #ffcc00'; // 亮橙色边�?
                element.style.color = '#ffcc00';
                element.style.opacity = '1';
                element.style.boxShadow = '0 0 15px rgba(255, 204, 0, 0.4)';

                const pendingIcon = document.createElement('div');
                pendingIcon.className = 'status-icon pending-icon';
                pendingIcon.innerHTML = '�?;
                element.appendChild(pendingIcon);
            } else {
                // 默认视为锁定
                element.classList.add('node-locked');
                element.style.backgroundColor = '#333333';
                element.style.color = '#666666';
                element.style.opacity = '0.5';

                const lockIcon = document.createElement('div');
                lockIcon.className = 'status-icon lock-icon';
                lockIcon.innerHTML = '🔒';
                element.appendChild(lockIcon);
            }
        }

        // 刷新技能树显示
        function refreshTree() {
            if (currentTreeId && currentNodeUserId) {
                loadTree(currentTreeId, currentNodeUserId);
            }
        }

        // 更新技能点显示
        function updateSkillPoints(points, total) {
            document.getElementById('skill_points').textContent = points || 0;
            if (total !== undefined) {
                document.getElementById('total_skill_points').textContent = total || 0;
            }
        }

        // 格式化描述内容（支持�?Markdown 语法�?
        function formatDescription(text) {
            if (!text) return '';

            // 1. 基础 HTML 转义
            let html = text
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;');

            // 2. 加粗 **text**
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

            // 3. 斜体 *text*
            html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

            // 4. 自定义颜�?[color:red](text)
            html = html.replace(/\[color:(.*?)\]\((.*?)\)/g, '<span style="color:$1;">$2</span>');

            // 5. 自定义字�?[size:18px](text)
            html = html.replace(/\[size:(.*?)\]\((.*?)\)/g, '<span style="font-size:$1;">$2</span>');

            // 6. 自定义缩�?[indent:20](text)
            html = html.replace(/\[indent:(.*?)\]\((.*?)\)/g, '<div style="margin-left:$1px;">$2</div>');

            // 7. 链接 [text](url)
            html = html.replace(/\[(.*?)\]\((https?:\/\/.*?)\)/g, '<a href="$2" target="_blank" style="color:var(--cyan); text-decoration: underline;">$1</a>');

            // 8. 列表处理（每行开头的 - �?* �?
            const lines = html.split('\n');
            let inList = false;
            const processedLines = lines.map(line => {
                const listMatch = line.match(/^[\s]*[-*][\s]+(.*)/);
                if (listMatch) {
                    let result = '';
                    if (!inList) {
                        result = '<ul style="margin: 8px 0; padding-left: 20px;">';
                        inList = true;
                    }
                    result += `<li style="margin-bottom: 4px;">${listMatch[1]}</li>`;
                    return result;
                } else {
                    let result = '';
                    if (inList) {
                        result = '</ul>';
                        inList = false;
                    }
                    return result + line;
                }
            });
            if (inList) processedLines.push('</ul>');

            html = processedLines.join('\n');

            // 9. 换行处理（保�?pre-wrap 但转换一些显式换行）
            html = html.replace(/\n\n/g, '<div style="height: 10px;"></div>');

            return html;
        }

        // 显示节点信息
        // 显示节点详细信息面板
        function showNodeDetailPanel(node) {
            const panel = document.getElementById('node_detail_panel');
            const overlay = document.getElementById('panel_overlay');
            if (!panel || !overlay) return;

            const nodeData = node.data || {};
            const status = nodeStatusMap[node.id] || 'locked';
            const cost = nodeData.cost || node.cost || 1;
            const description = (nodeData.description || node.description || '').toString();
            const link = (nodeData.link || node.link || '').toString();
            const link2 = (nodeData.link2 || node.link2 || '').toString();
            const level = nodeData.level || node.level || 1;
            const moduleStr = nodeData.module || node.module || '默认模块';

            // 记录点击日志
            if (typeof logNodeClick === 'function') {
                logNodeClick(currentTreeId, node.id);
            }

            // 设置节点标题
            document.getElementById('panel_node_title').textContent = node.topic;

            // 设置等级和模�?
            document.getElementById('panel_node_level').textContent = '�?.repeat(level) + ` (${level}�?`;
            document.getElementById('panel_node_module').textContent = moduleStr;

            // 设置状�?
            let statusText = '';
            let statusClass = '';
            if (status === 'locked') {
                statusText = '🔒 锁定';
                statusClass = 'locked';
            } else if (status === 'unlocked') {
                statusText = '🔓 已解�?;
                statusClass = 'unlocked';
            } else if (status === 'activated') {
                statusText = '�?已激�?;
                statusClass = 'activated';
            } else if (status === 'pending_approval') {
                statusText = '�?已申请，待审�?;
                statusClass = 'pending';
            }
            const statusElement = document.getElementById('panel_node_status');
            statusElement.innerHTML = `<span class="status-badge ${statusClass}">${statusText}</span>`;

            // 更新激活按钮状�?
            const activateBtn = document.getElementById('btn_panel_activate');
            const activateSection = document.getElementById('panel_activate_section');
            const canActivate = window.currentTreeCanActivate !== false;

            if (activateBtn && activateSection) {
                // 记录当前操作的节点ID，以便按钮点击时使用
                activateBtn.dataset.nodeId = node.id;

                if (status === 'activated') {
                    // 已点亮：根据用户要求，暂时屏蔽“取消点亮”功能，隐藏按钮
                    activateSection.style.display = 'none';
                    activateBtn.innerHTML = '<span>�?/span> 已点�?;
                    activateBtn.classList.add('activated-state');
                    activateBtn.onclick = null;
                } else if (status === 'pending_approval') {
                    // 审核中：禁用按钮或者提�?
                    activateSection.style.display = 'block';
                    activateBtn.innerHTML = '<span>�?/span> 已申请，待审�?;
                    activateBtn.classList.add('disabled');
                    activateBtn.classList.remove('activated-state');
                    activateBtn.onclick = () => showMessage('您的申请正在等待组长或管理员审核', 'info');
                } else {
                    // 未点亮：显示点亮按钮
                    activateSection.style.display = 'block';
                    activateBtn.innerHTML = '<span>�?/span> 点亮此技�?;
                    activateBtn.classList.remove('activated-state');
                    activateBtn.classList.remove('deactivate');
                    activateBtn.onclick = () => activateNode(node.id);
                }

                // 权限检�?
                if (!canActivate) {
                    activateBtn.classList.add('disabled');
                    activateBtn.title = '您没有权限对此模块进行操�?;
                    activateBtn.onclick = () => showMessage('只读模式，无法操�?, 'warning');
                } else if (status !== 'activated') {
                    activateBtn.classList.remove('disabled');
                    activateBtn.title = '';
                }
            }

            // 设置消�?
            document.getElementById('panel_node_cost').textContent = cost;

            // 设置描述
            const descriptionSection = document.getElementById('panel_description_section');
            const descriptionContent = document.getElementById('panel_node_description');
            if (description && description.trim()) {
                descriptionContent.innerHTML = formatDescription(description);
                descriptionSection.style.display = 'block';
            } else {
                descriptionSection.style.display = 'none';
            }

            // 设置链接 1
            const linkSection = document.getElementById('panel_link_section');
            const linkButton = document.getElementById('panel_node_link');
            if (link && link.trim()) {
                let fl = link.trim();
                if (!fl.match(/^https?:\/\//i)) fl = 'http://' + fl;
                linkButton.href = fl;
                linkButton.textContent = '🔗 相关链接 1';
                linkSection.style.display = 'block';
            } else {
                linkSection.style.display = 'none';
            }

            // 设置链接 2
            let link2Section = document.getElementById('panel_link2_section');
            if (!link2Section) {
                link2Section = document.createElement('div');
                link2Section.id = 'panel_link2_section';
                link2Section.className = 'panel-section';
                link2Section.style.marginTop = '10px';
                link2Section.innerHTML = `<div class="section-label">相关链接 2</div><a id="panel_node_link2" class="link-button" target="_blank">🔗 相关链接 2</a>`;
                linkSection.parentNode.insertBefore(link2Section, linkSection.nextSibling);
            }
            const link2Button = document.getElementById('panel_node_link2');
            if (link2 && link2.trim()) {
                let fl2 = link2.trim();
                if (!fl2.match(/^https?:\/\//i)) fl2 = 'http://' + fl2;
                link2Button.href = fl2;
                link2Section.style.display = 'block';
            } else {
                link2Section.style.display = 'none';
            }

            // 显示面板和遮�?
            panel.classList.add('show');
            overlay.classList.add('show');

            // 隐藏 Tooltip
            hideTooltip();
        }

        // 关闭节点详细信息面板
        function closeNodeDetailPanel() {
            const panel = document.getElementById('node_detail_panel');
            const overlay = document.getElementById('panel_overlay');
            if (panel) panel.classList.remove('show');
            if (overlay) overlay.classList.remove('show');
        }

        // 异步记录节点点击
        async function logNodeClick(treeId, nodeId) {
            if (!treeId || !nodeId) return;
            try {
                await fetch(`${API_BASE}/trees/${treeId}/nodes/${nodeId}/click`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: currentUser ? currentUser.id : null })
                });
            } catch (e) {
                console.warn('记录点击失败:', e);
            }
        }

        // ===== 视图切换逻辑 =====
        async function switchViewMode(mode) {
            if (!originalMindData || !currentTreeId) {
                showMessage('请先选择一个技能树', 'warning');
                return;
            }

            if (currentViewMode === mode) return;

            currentViewMode = mode;

            // 更新按钮状�?
            document.getElementById('btn_view_tree').classList.toggle('active', mode === 'tree');
            document.getElementById('btn_view_path').classList.toggle('active', mode === 'path');
            document.getElementById('progress_panel').classList.remove('active');
            document.body.style.overflow = 'auto'; // 恢复滚动

            try {
                // 将模式同步到服务�?
                const response = await fetch(`${API_BASE}/trees/${currentTreeId}/mode`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode: mode })
                });

                if (!response.ok) {
                    console.warn('同步模式到服务器失败');
                }

                // 重新从服务器加载数据，以获取最新计算的状�?
                await loadTree(currentTreeId, currentNodeUserId);

                showMessage(`切换�?{mode === 'tree' ? '树状模式（自下而上解锁�? : '进阶路径模式（线性等级解锁）'}`, 'success');

            } catch (error) {
                console.error('切换模式异常�?, error);
                // 如果失败，回退本地渲染
                renderCurrentMode();
            }
        }

        function renderCurrentMode() {
            if (!jm || !originalMindData) return;

            document.getElementById('loading').style.display = 'block';

            try {
                // 深度克隆原始数据
                const mindData = JSON.parse(JSON.stringify(originalMindData));
                let displayData = mindData;

                if (currentViewMode === 'path') {
                    displayData = getLinearMindData(mindData);
                }

                // 重新加载数据
                jm.show(displayData);

                // 应用样式
                setTimeout(() => {
                    applyNodeStyles();
                    resetAndCenterView();
                    updateZoomLabel();
                }, 200);

            } catch (error) {
                console.error('切换视图失败�?, error);
                showMessage('切换视图失败�? + error.message, 'error');
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }

        // 重新组织数据为线性进阶模�?(5 -> 4 -> 3 -> 2 -> 1)
        function getLinearMindData(originalData) {
            const nodes = [];
            // 递归提取所有节�?
            function flatten(node) {
                // 确保业务属性被提取
                const extraData = {
                    level: node.level || (node.data && node.data.level) || 1,
                    module: node.module || (node.data && node.data.module) || '默认模块',
                    cost: node.cost || (node.data && node.data.cost) || 1,
                    description: node.description || (node.data && node.data.description) || '',
                    link: node.link || (node.data && node.data.link) || '',
                    link2: node.link2 || (node.data && node.data.link2) || '',
                };
                const bgColor = node['background-color'] || (node.data && node.data['background-color']);
                const fgColor = node['foreground-color'] || (node.data && node.data['foreground-color']);

                nodes.push({
                    id: node.id,
                    topic: node.topic,
                    direction: node.direction,
                    expanded: node.expanded,
                    'background-color': bgColor,
                    'foreground-color': fgColor,
                    // 将这些属性直接放在顶层，与后端返回的结构保持一致，确保 jsMind 能正确将其放�?node.data
                    level: extraData.level,
                    module: extraData.module,
                    cost: extraData.cost,
                    description: extraData.description,
                    link: extraData.link,
                    link2: extraData.link2
                });
                if (node.children) {
                    node.children.forEach(flatten);
                }
            }

            flatten(originalData.data);

            // 提取根节点（通常是第一个或�?id='root'�?
            const root = nodes.find(n => n.id === originalData.data.id);
            const otherNodes = nodes.filter(n => n.id !== root.id);

            // 按等级分�?(�?�?)
            const levels = { 5: [], 4: [], 3: [], 2: [], 1: [], 0: [] };
            otherNodes.forEach(node => {
                const lv = parseInt(node.level) || 0;
                if (levels[lv]) levels[lv].push(node);
                else levels[0].push(node);
            });

            // 重建层级关系: Root -> Lv5 -> Lv4 -> Lv3 -> Lv2 -> Lv1 -> Others
            const levelSequence = [5, 4, 3, 2, 1, 0];
            const resultRoot = { ...root, children: [] };

            let lastLevelNodes = [resultRoot];

            levelSequence.forEach(lv => {
                const currentLevelNodes = levels[lv];
                if (currentLevelNodes && currentLevelNodes.length > 0) {
                    // 分派当前层级的节点到上一层级的节点下
                    currentLevelNodes.forEach((node, index) => {
                        const parent = lastLevelNodes[index % lastLevelNodes.length];
                        if (!parent.children) parent.children = [];
                        parent.children.push(node);
                    });
                    lastLevelNodes = currentLevelNodes;
                }
            });

            return {
                meta: originalData.meta,
                format: originalData.format,
                data: resultRoot
            };
        }

        // 初始化面板关闭事�?
        function initPanelEvents() {
            const closeBtn = document.getElementById('panel_close');
            const overlay = document.getElementById('panel_overlay');

            if (closeBtn) {
                closeBtn.addEventListener('click', closeNodeDetailPanel);
            }

            if (overlay) {
                overlay.addEventListener('click', closeNodeDetailPanel);
            }

            // 初始化右键菜�?
            document.addEventListener('contextmenu', function (e) {
                const nodeItem = e.target.closest('jmnode');
                if (nodeItem) {
                    e.preventDefault();
                    const nodeId = nodeItem.getAttribute('nodeid');
                    showContextMenu(e.clientX, e.clientY, nodeId);
                } else {
                    hideContextMenu();
                }
            });

            document.addEventListener('click', function () {
                hideContextMenu();
            });
        }

        // ===== 右键菜单功能 =====
        function showContextMenu(x, y, nodeId) {
            const menu = document.getElementById('context_menu');
            if (!menu) return;

            const node = jm.get_node(nodeId);
            if (!node || node.isroot) return;

            const status = nodeStatusMap[nodeId] || 'locked';
            const canActivate = window.currentTreeCanActivate !== false;

            let html = '';
            if (status === 'activated') {
                // 已点亮：根据要求移除“取消点亮”选项
                html = `<div class="context-menu-item disabled">
                            <span>�?/span> 已点�?
                        </div>`;
            } else {
                html = `<div class="context-menu-item ${!canActivate ? 'disabled' : ''}" onclick="${canActivate ? `activateNode('${nodeId}')` : `showMessage('只读模式无法操作', 'warning')`}">
                            <span>�?/span> 点亮此技�?
                        </div>`;
            }

            html += `<div class="context-menu-item" onclick="showNodeDetailPanel(jm.get_node('${nodeId}'))">
                        <span>ℹ️</span> 详情信息
                    </div>`;

            menu.innerHTML = html;
            menu.style.display = 'block';

            // 确保不超出屏�?
            const rect = menu.getBoundingClientRect();
            let finalX = x;
            let finalY = y;
            if (x + rect.width > window.innerWidth) finalX = x - rect.width;
            if (y + rect.height > window.innerHeight) finalY = y - rect.height;

            menu.style.left = finalX + 'px';
            menu.style.top = finalY + 'px';
        }

        function hideContextMenu() {
            const menu = document.getElementById('context_menu');
            if (menu) menu.style.display = 'none';
        }

        // 显示消息
        function showMessage(text, type = 'success') {
            const message = document.getElementById('message');
            message.textContent = text;
            message.className = 'message show ' + (type || '');

            setTimeout(() => {
                message.classList.remove('show');
            }, 3000);
        }

        // ===== 学习进度面板 =====
        function showProgress() {
            const overlay = document.getElementById('progress_overlay');
            const panel = document.getElementById('progress_panel');
            overlay.classList.add('show');
            // 触发动画（延迟一帧）
            requestAnimationFrame(() => {
                panel.classList.add('show');
            });
            loadProgress();
        }

        function hideProgress() {
            const overlay = document.getElementById('progress_overlay');
            const panel = document.getElementById('progress_panel');
            panel.classList.remove('show');
            overlay.classList.remove('show');
        }

        async function loadProgress() {
            const content = document.getElementById('progress_content');
            content.innerHTML = '<div class="progress-empty">加载�?..</div>';

            if (!currentUser) {
                content.innerHTML = '<div class="progress-empty">请先登录</div>';
                return;
            }

            try {
                // 管理员获取全体进度，普通用户只获取自己
                const isAdmin = currentUser.is_admin;
                const url = isAdmin
                    ? `${API_BASE}/progress?user_id=${currentUser.id}&all=true`
                    : `${API_BASE}/progress?user_id=${currentUser.id}`;

                const resp = await fetch(url);
                if (!resp.ok) {
                    const err = await resp.json();
                    content.innerHTML = `<div class="progress-empty">加载失败�?{err.error || resp.status}</div>`;
                    return;
                }

                const data = await resp.json();

                if (!data || data.length === 0) {
                    content.innerHTML = '<div class="progress-empty">暂无进度数据</div>';
                    return;
                }

                let html = '';

                // 管理员时显示切换标签
                if (isAdmin) {
                    html += `
                    <div style="margin-bottom:20px;display:flex;gap:10px;flex-wrap:wrap;">
                        <button onclick="renderProgress(progressData, false)" id="btn_all"
                            style="padding:8px 18px;border-radius:8px;border:1px solid var(--border-glow);
                                   background:rgba(0,240,255,0.1);color:var(--cyan);cursor:pointer;font-size:13px;">
                            👥 全员进度
                        </button>
                        <button onclick="renderProgress(progressData, true)" id="btn_self"
                            style="padding:8px 18px;border-radius:8px;border:1px solid var(--border-glow);
                                   background:rgba(0,240,255,0.05);color:var(--text-secondary);cursor:pointer;font-size:13px;">
                            👤 我的进度
                        </button>
                    </div>
                    <div id="progress_list"></div>`;
                    content.innerHTML = html;
                    window.progressData = data;
                    renderProgress(data, false);
                } else {
                    content.innerHTML = html + '<div id="progress_list"></div>';
                    window.progressData = data;
                    renderProgress(data, false);
                }

            } catch (e) {
                content.innerHTML = `<div class="progress-empty">网络错误�?{e.message}</div>`;
            }
        }

        function renderProgress(data, selfOnly) {
            const list = document.getElementById('progress_list');
            if (!list) return;

            const filtered = selfOnly
                ? data.filter(u => u.user_id === currentUser.id)
                : data;

            if (filtered.length === 0) {
                list.innerHTML = '<div class="progress-empty">暂无数据</div>';
                return;
            }

            let html = '';
            for (const u of filtered) {
                const adminBadge = u.is_admin
                    ? '<span class="admin-badge">管理�?/span>' : '';

                let modulesHtml = '';
                if (u.module) {
                    const mods = u.module.split(',');
                    mods.forEach(m => {
                        const t = m.trim();
                        if (t) {
                            modulesHtml += `<span class="mod-tag">${t}</span>`;
                        }
                    });
                }

                let treesHtml = '';
                if (!u.trees || u.trees.length === 0) {
                    treesHtml = '<div style="color:var(--text-dim);font-size:13px;padding:6px 0;">暂未参与任何技能树</div>';
                } else {
                    for (const t of u.trees) {
                        const isFull = t.percent >= 100;
                        const treeNodes = t.activated_node_details || [];
                        const nodesListHtml = treeNodes.length > 0
                            ? `<div class="nodes-detail-list" id="nodes_detail_${u.user_id}_${t.tree_id}" style="display:none; margin-top:8px; padding:10px; background:rgba(0,0,0,0.2); border-radius:6px; border-left:2px solid var(--cyan-dim);">
                                <div style="font-size:11px; color:var(--text-dim); margin-bottom:5px; text-transform:uppercase;">已激活技能详�?</div>
                                <div style="display:flex; flex-wrap:wrap; gap:6px;">
                                    ${treeNodes.map(n => `<span style="font-size:12px; color:var(--cyan); background:rgba(0,216,255,0.1); padding:2px 8px; border-radius:4px; border:1px solid rgba(0,216,255,0.2);">${n.topic}</span>`).join('')}
                                </div>
                               </div>`
                            : '';

                        treesHtml += `
                        <div class="progress-tree-row">
                            <div class="progress-tree-header" style="display:flex; justify-content:space-between; align-items:center;">
                                <div class="progress-tree-name" title="${t.tree_name}" onclick="toggleNodeDetails('${u.user_id}_${t.tree_id}')" style="cursor: pointer;">${t.tree_name}</div>
                                <div class="progress-stat">
                                    <button class="btn-detail" onclick="viewTreeProgress(${t.tree_id}, '${t.tree_name.replace(/'/g, "\\'")}', ${u.user_id})" 
                                            style="background: var(--purple-dim); color: var(--purple); border: 1px solid var(--purple-dim); padding: 2px 8px; border-radius: 4px; font-size: 10px; cursor: pointer; margin-right: 10px;">🔍 树图</button>
                                    ${t.activated_nodes}/${t.total_nodes} 节点 <span class="pct">${t.percent}%</span>
                                </div>
                            </div>
                            <div class="progress-bar-wrap" style="cursor: pointer;" onclick="toggleNodeDetails('${u.user_id}_${t.tree_id}')">
                                <div class="progress-bar-fill ${isFull ? 'full' : ''}"
                                     style="width:${t.percent}%"></div>
                            </div>
                            ${nodesListHtml}
                        </div>`;
                    }
                }

                html += `
                    <div class="progress-username">
                        👤 ${u.username} ${adminBadge} ${u.is_leader ? '<span class="admin-badge" style="background:#f59e0b">组长</span>' : ''} ${modulesHtml}
                    </div>
                    ${treesHtml}
                </div>`;
            }

            list.innerHTML = html;
        }

        function toggleNodeDetails(id) {
            const el = document.getElementById('nodes_detail_' + id);
            if (el) {
                el.style.display = el.style.display === 'none' ? 'block' : 'none';
            }
        }

        // --- 进度树图跳转独立页面 ---
        function viewTreeProgress(treeId, treeName, userId) {
            const url = `view.html?tree_id=${treeId}&user_id=${userId}&standalone=true`;
            window.open(url, '_blank');
        }
        // --- 学习任务看板管理 ---
        async function loadTaskBoard(force = false) {
            if (!currentUser) return;
            try {
                const resp = await fetch(`${API_BASE}/tasks/my?user_id=${currentUser.id}`);
                const tasks = await resp.json();

                const daily = document.getElementById('tasks_daily');
                const weekly = document.getElementById('tasks_weekly');
                const monthly = document.getElementById('tasks_monthly');
                const high = document.getElementById('tasks_high');

                daily.innerHTML = renderTasks(tasks.daily);
                weekly.innerHTML = renderTasks(tasks.weekly);
                monthly.innerHTML = renderTasks(tasks.monthly);
                high.innerHTML = renderTasks([...tasks.quarterly, ...tasks.yearly]);

                const totalTasks = tasks.daily.length + tasks.weekly.length + tasks.monthly.length + tasks.quarterly.length + tasks.yearly.length;
                if (totalTasks > 0 || force) {
                    document.getElementById('task_board_overlay').classList.add('show');
                }
            } catch (e) {
                console.error('加载任务看板失败:', e);
            }
        }

        function renderTasks(list) {
            if (!list || list.length === 0) return '<div class="task-empty">🎉 暂无任务</div>';
            return list.map(t => `
                <div class="task-card" onclick="showTaskNode(${t.tree_id}, '${t.node_id}')">
                    <div class="task-card-title">${t.node_path || t.node_topic}</div>
                    <div class="task-card-tree">${t.tree_name}</div>
                </div>
            `).join('');
        }

        function closeTaskBoard() {
            document.getElementById('task_board_overlay').classList.remove('show');
        }

        async function showTaskNode(treeId, nodeId) {
            closeTaskBoard();
            if (currentTreeId != treeId) {
                await loadTree(treeId, currentUser.id);
            }
            // 延时等待渲染
            setTimeout(() => {
                jm.select_node(nodeId);
                const node = jm.get_node(nodeId);
                if (node) {
                    jm.view.center_root(node);
                    showNodeDetailPanel(node);
                }
            }, 500);
        }

        // 根据 URL 参数加载
        async function checkUrlParams() {
            const urlParams = new URLSearchParams(window.location.search);
            const treeId = urlParams.get('tree_id');
            const targetUserId = urlParams.get('user_id');
            const standalone = urlParams.get('standalone');

            if (treeId && targetUserId) {
                if (standalone === 'true') {
                    // 注入关闭按钮
                    if (!document.querySelector('.btn-standalone-close')) {
                        const closeBtn = document.createElement('button');
                        closeBtn.className = 'btn-standalone-close';
                        closeBtn.innerHTML = '关闭进度视图';
                        closeBtn.onclick = () => window.close();
                        document.body.appendChild(closeBtn);
                    }
                }

                // 加载指定的技能树和用户状�?
                currentNodeUserId = targetUserId;
                currentTreeId = treeId;

                try {
                    document.getElementById('loading').style.display = 'block';
                    await loadTree(treeId, targetUserId);
                    // 渲染完成后强制居�?
                    setTimeout(resetAndCenterView, 500);
                } catch (e) {
                    console.error('自动加载树失�?', e);
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }
        }

        // 初始�?
        window.onload = async function () {
            // 初始化面板事�?
            initPanelEvents();
            initMindMap();
            try {
                // 加载参数
                const up = new URLSearchParams(window.location.search);
                // 先加载用户列表和权限基础
                await loadUserList();
                // 检查是否有 URL 参数需要自动加载特定视�?
                await checkUrlParams();

                // 如果不是由其他页面重定向过来看进度的，弹出任务看�?
                if (!up.get('standalone')) {
                    loadTaskBoard();
                }
            } catch (e) {
                console.error('初始化失�?', e);
            }
        };
    </script>
</body>

</html>
