# 技能树管理系统

一个基于 jsMind 和 Flask 的技能树管理系统，支持多用户、数据库存储、节点编辑和王者荣耀风格的颜色主题。参考[游戏技能树设计文章](https://www.gameres.com/913976.html)实现。

## 核心特性

- **多用户支持**：每个用户有独立的技能树状态，互不影响
- **权限管理**：管理员可以重置所有用户的技能树，普通用户只能管理自己的
- **状态持久化**：用户的节点激活状态独立保存
- **技能点系统**：每个用户有独立的技能点

## 功能特性

### 管理页面（index.html）
1. **技能树管理**
   - 创建、保存、加载技能树
   - 支持多个技能树的管理
   - 自动保存节点数据到数据库
   - 设置初始技能点

2. **节点编辑**
   - 添加子节点和兄弟节点
   - 编辑节点名称、颜色、技能点消耗
   - 删除节点
   - 拖拽移动节点（需要 jsmind.draggable-node.js）

3. **颜色主题**
   - 王者荣耀风格的颜色方案
   - 支持自定义背景色和文字颜色
   - 12种背景颜色 + 5种文字颜色

### 展示页面（view.html）
1. **用户选择**
   - 必须先选择用户才能查看技能树
   - 每个用户看到自己的技能树状态
   - 管理员可以选择查看任意用户的技能树

2. **只读展示模式**
   - 仅用于展示技能树，不可编辑节点内容
   - 支持点击节点激活/点亮（保存到用户状态）
   - 初始状态所有节点都是锁定的（根节点除外）

3. **节点状态管理**
   - **锁定状态**：灰色显示，带锁图标，无法激活
   - **已激活状态**：正常颜色，带高亮动画和✓标记
   - 前置条件检查：只有父节点已激活才能激活子节点
   - 每个用户的状态独立保存

4. **技能点系统**
   - 显示当前用户的可用技能点和总技能点
   - 激活节点消耗技能点（每个用户独立）
   - 重置功能：
     - 普通用户：只能重置自己的技能树
     - 管理员：可以重置所有用户或指定用户的技能树

4. **数据库存储**
   - 使用 SQLite 数据库
   - 自动保存节点结构和状态
   - 支持版本管理

## 项目结构

```
技能树/
├── app.py                      # Flask后端应用
├── requirements.txt            # Python依赖
├── run.bat                     # Windows启动脚本
├── skill_tree.db               # SQLite数据库（自动生成）
├── index.html                  # 管理页面（编辑技能树）
├── view.html                   # 展示页面（只读，可激活节点）
├── libs/                       # 第三方库
│   ├── css/
│   │   └── jsmind.css
│   └── js/
│       ├── jsmind.js
│       └── jsmind.draggable-node.js
└── README.md                   # 项目说明
```

## 安装和运行

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端服务器

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
python app.py
```

服务器将在 `http://localhost:5000` 启动

### 3. 打开前端页面

直接在浏览器中打开 `index.html` 文件，或者使用本地服务器：

```bash
# Python 3
python -m http.server 8000

# 然后访问 http://localhost:8000/index.html
```

## API接口说明

### 获取所有技能树
```
GET /api/trees
```

### 创建新技能树
```
POST /api/trees
Content-Type: application/json

{
  "name": "技能树名称",
  "author": "作者",
  "version": "1.0",
  "data": { ... }  // jsmind格式的数据
}
```

### 获取指定技能树
```
GET /api/trees/{tree_id}
```

### 更新技能树
```
PUT /api/trees/{tree_id}
Content-Type: application/json

{
  "name": "新名称",
  "data": { ... }
}
```

### 删除技能树
```
DELETE /api/trees/{tree_id}
```

### 更新节点
```
PUT /api/trees/{tree_id}/nodes/{node_id}
Content-Type: application/json

{
  "topic": "节点名称",
  "background_color": "#FFD700",
  "foreground_color": "#000000",
  "cost": 1
}
```

### 激活节点
```
POST /api/trees/{tree_id}/nodes/{node_id}/activate
```

### 取消激活节点
```
POST /api/trees/{tree_id}/nodes/{node_id}/deactivate
```

### 重置技能树
```
POST /api/trees/{tree_id}/reset
```

### 创建用户
```
POST /api/users
Content-Type: application/json

{
  "username": "用户名",
  "password": "密码（可选）",
  "is_admin": false
}
```

### 获取用户列表
```
GET /api/users
```

### 重置用户技能树（用户自己）
```
POST /api/users/{user_id}/trees/{tree_id}/reset
```

### 重置技能树（管理员）
```
POST /api/trees/{tree_id}/reset
Content-Type: application/json

{
  "user_id": 管理员ID,
  "target_user_id": 目标用户ID（可选，为空则重置所有用户）
}
```

## 使用说明

### 第一步：创建用户

1. **在管理页面创建用户**
   - 打开 `index.html`
   - 点击"用户管理"按钮
   - 输入用户名、密码（可选）、选择是否为管理员
   - 点击"创建用户"

2. **或使用脚本创建管理员**
   ```bash
   python create_admin.py
   ```
   这会创建一个默认管理员（用户名：admin，密码：admin123）

### 管理页面（index.html）

1. **创建技能树**
   - 在左侧输入技能树名称和初始技能点
   - 点击"新建技能树"按钮
   - 根节点默认已激活，其他节点默认锁定

2. **添加节点**
   - 选择一个节点
   - 点击"添加子节点"或"添加兄弟节点"
   - 输入节点名称
   - 新节点默认锁定状态，消耗1技能点

3. **编辑节点**
   - 点击节点选中
   - 在左侧编辑面板修改名称、颜色、技能点消耗
   - 点击"更新节点"保存

4. **保存技能树**
   - 点击"保存技能树"按钮
   - 系统会自动保存到数据库

5. **加载技能树**
   - 点击"刷新列表"查看已保存的技能树
   - 点击列表中的技能树名称加载

### 展示页面（view.html）

1. **选择用户**
   - 打开 `view.html`
   - 在顶部下拉框选择用户
   - 选择后会自动加载技能树列表

2. **选择技能树**
   - 从技能树下拉框选择要查看的技能树
   - 系统会加载该用户在该技能树中的状态

3. **激活节点**
   - 点击锁定的节点尝试激活
   - 系统会检查：
     - 父节点是否已激活（根节点除外）
     - 技能点是否足够
   - 激活成功后节点会点亮，显示高亮动画
   - 状态会保存到该用户的记录中

4. **重置技能树**
   - **普通用户**：只能重置自己的技能树
   - **管理员**：可以重置所有用户或指定用户的技能树
   - 重置后所有节点恢复锁定状态，技能点全部返还

## 颜色方案

系统提供了12种背景颜色和5种文字颜色，采用王者荣耀风格：

**背景颜色：**
- 金色 (#FFD700) - 默认
- 橙色、红色、紫色、蓝色、青色、绿色、黄色、粉色、深红、深蓝、深绿

**文字颜色：**
- 黑色、白色、金色、红色、蓝色

## 技术栈

- **前端：** HTML5, CSS3, JavaScript, jsMind
- **后端：** Python, Flask, SQLAlchemy
- **数据库：** SQLite

## 注意事项

1. 首次运行会自动创建数据库文件 `skill_tree.db`
2. 确保后端服务器运行在 `http://localhost:5000`
3. 如果遇到跨域问题，确保 Flask-CORS 已正确安装
4. 建议使用现代浏览器（Chrome, Firefox, Edge等）

## 数据库结构

### 用户表 (users)
- `id`: 用户ID
- `username`: 用户名
- `password`: 密码
- `is_admin`: 是否管理员

### 技能树表 (skill_trees)
- `id`: 技能树ID
- `name`: 技能树名称
- `default_skill_points`: 默认技能点

### 技能节点表 (skill_nodes)
- `id`: 节点ID
- `node_id`: 节点标识
- `tree_id`: 所属技能树
- `parent_id`: 父节点ID
- `topic`: 节点标题
- `cost`: 激活消耗的技能点

### 用户技能树状态表 (user_skill_tree_states)
- `id`: 状态ID
- `user_id`: 用户ID
- `tree_id`: 技能树ID
- `node_id`: 节点ID
- `status`: 节点状态（locked/activated）
- `skill_points`: 用户在该技能树中的可用技能点（仅根节点存储）

## 节点状态说明

- **locked（锁定）**：默认状态，灰色显示，带锁图标，无法激活
- **unlocked（解锁）**：已解锁但未激活，半透明显示
- **activated（已激活）**：已点亮，正常颜色，带高亮动画和✓标记

**注意**：每个用户的节点状态是独立保存的，互不影响。

## 开发计划

- [x] 节点状态管理（锁定/解锁/激活）
- [x] 技能点系统
- [x] 前置条件检查
- [x] 只读展示模式
- [ ] 支持节点图标
- [ ] 支持节点链接
- [ ] 导出为图片
- [ ] 导入/导出JSON文件
- [ ] 节点搜索功能
- [ ] 技能树模板

## 许可证

MIT License
