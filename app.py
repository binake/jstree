"""
技能树后端API - Flask应用
支持技能树的保存、加载、更新和删除
"""
from flask import Flask, request, jsonify, send_from_directory, send_file,render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

import csv
import io
import uuid


app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skill_tree.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  # 允许跨域请求

db = SQLAlchemy(app)


class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100))  # 简单密码，实际应该加密
    is_admin = db.Column(db.Boolean, default=False)  # 是否管理员
    is_leader = db.Column(db.Boolean, default=False)  # 是否组长
    module = db.Column(db.String(100), default='默认模块')  # 所属模块/权限范围
    group = db.Column(db.String(20), default='A')  # 用户组别: A/B/C/D
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 关联用户技能树状态
    skill_tree_states = db.relationship('UserSkillTreeState', backref='user', lazy=True, cascade='all, delete-orphan')


class SkillTree(db.Model):
    """技能树表"""
    __tablename__ = 'skill_trees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(100), default='默认模块')  # 所属模块
    author = db.Column(db.String(50))
    version = db.Column(db.String(20))
    default_skill_points = db.Column(db.Integer, default=10)  # 默认技能点
    mode = db.Column(db.String(20), default='tree')  # 激活规则模式：tree（树状自下而上）或 path（进阶等级线性）
    extra_data = db.Column(db.Text)  # 存储外框、联系线、概要等扩展数据 (JSON)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联节点
    nodes = db.relationship('SkillNode', backref='tree', lazy=True, cascade='all, delete-orphan')
    # 关联用户状态
    user_states = db.relationship('UserSkillTreeState', backref='tree', lazy=True, cascade='all, delete-orphan')


class SkillNode(db.Model):
    """技能节点表"""
    __tablename__ = 'skill_nodes'
    
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String(50), nullable=False)  # jsmind中的节点ID
    tree_id = db.Column(db.Integer, db.ForeignKey('skill_trees.id'), nullable=False)
    parent_id = db.Column(db.String(50), nullable=True)  # 父节点ID，root节点为None
    topic = db.Column(db.Text, nullable=False)  # 节点标题
    direction = db.Column(db.String(10))  # left/right
    expanded = db.Column(db.Boolean, default=True)
    
    # 节点状态：locked(锁定) / unlocked(解锁但未激活) / activated(已激活/点亮)
    status = db.Column(db.String(20), default='locked')
    
    # 技能点消耗
    cost = db.Column(db.Integer, default=1)  # 激活此节点需要的技能点
    
    # 颜色和样式
    background_color = db.Column(db.String(20), default='#f4f5f7')  # surface-1: 统一板岩系背景
    foreground_color = db.Column(db.String(20), default='#3d4451')  # text-p: 统一板岩系文字
    
    # 技能内容：说明文字和链接
    description = db.Column(db.Text)  # 技能说明文字
    link = db.Column(db.String(500))  # 技能相关链接 1
    link2 = db.Column(db.String(500)) # 技能相关链接 2
    
    # 节点属性：等级和模块
    level = db.Column(db.Integer, default=1)  # 等级属性：1=初级, 2=中级, 3=高级等
    module = db.Column(db.String(100), default='默认模块')  # 所属模块
    sort_index = db.Column(db.Integer, default=0)  # 排序索引
    
    # 其他自定义数据（JSON格式）
    extra_data = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 索引
    __table_args__ = (db.Index('idx_tree_node', 'tree_id', 'node_id'),)


class UserSkillTreeState(db.Model):
    """用户技能树状态表"""
    __tablename__ = 'user_skill_tree_states'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tree_id = db.Column(db.Integer, db.ForeignKey('skill_trees.id'), nullable=False)
    node_id = db.Column(db.String(50), nullable=False)  # 节点ID
    status = db.Column(db.String(20), default='locked')  # locked/activated
    skill_points = db.Column(db.Integer, default=0)  # 用户在该技能树中的可用技能点
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 唯一索引：一个用户在一个技能树中，每个节点只能有一条记录
    __table_args__ = (
        db.Index('idx_user_tree_node', 'user_id', 'tree_id', 'node_id'),
        db.UniqueConstraint('user_id', 'tree_id', 'node_id', name='uq_user_tree_node')
    )


class NodeEditHistory(db.Model):
    """节点编辑历史表"""
    __tablename__ = 'node_edit_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer, db.ForeignKey('skill_trees.id'), nullable=False)
    node_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # 修改者ID
    username = db.Column(db.String(50)) # 记录当时的用户名，冗余存储方便查询
    
    # 记录变更详情（JSON格式）
    change_details = db.Column(db.Text) 
    
    created_at = db.Column(db.DateTime, default=datetime.now)


class NodeClickHistory(db.Model):
    """节点点击历史表"""
    __tablename__ = 'node_click_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer, db.ForeignKey('skill_trees.id'), nullable=False)
    node_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # 点击者ID
    username = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.now)


class LearningTask(db.Model):
    """学习任务表"""
    __tablename__ = 'learning_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tree_id = db.Column(db.Integer, db.ForeignKey('skill_trees.id'), nullable=False)
    node_id = db.Column(db.String(50), nullable=False)
    
    # 任务类型: daily, weekly, monthly, quarterly, yearly
    task_type = db.Column(db.String(20), nullable=False)
    
    # 任务状态: assigned(已分配), pending(待审核), completed(已完成)
    status = db.Column(db.String(20), default='assigned')
    
    assigner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # 分配者ID
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # 建立关联
    user_rel = db.relationship('User', foreign_keys=[user_id], backref='tasks')
    assigner_rel = db.relationship('User', foreign_keys=[assigner_id])



# 假设已经有 db, SkillTree, SkillNode 定义


@app.route('/api/skill-trees/list', methods=['GET']) # 修改了路径，避免路径也冲突
def get_tree_list_for_import(): # 修改了函数名
    """获取所有技能树供下拉框选择"""
    trees = SkillTree.query.order_by(SkillTree.updated_at.desc()).all()
    return jsonify([{"id": t.id, "name": t.name} for t in trees])

@app.route('/admin/skill/import-preview', methods=['POST'])
def import_preview():
    """解析上传的文件并返回 JSON 用于前端表格预览"""
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "未发现文件"}), 400

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)
    
    preview_data = []
    for row in csv_input:
        preview_data.append(row)
        
    return jsonify({"data": preview_data})

import uuid
from flask import request, jsonify

@app.route('/admin/skill/import-submit', methods=['POST'])
def import_submit():
    data = request.json.get('nodes')
    tree_id = request.json.get('tree_id')
    
    try:
        # 1. 建立临时 ID 映射表 (针对 CSV 内部的 1, 2, 3)
        temp_to_real_map = {}
        for item in data:
            t_id = str(item.get('temp_id', '')).strip()
            if t_id:
                # 正常节点依然生成 UUID，除非该节点本身就是 root（根据业务判断）
                temp_to_real_map[t_id] = f"node_{uuid.uuid4().hex[:8]}"

        # 2. 构建节点对象
        new_nodes = []
        for item in data:
            t_id = str(item.get('temp_id', '')).strip()
            p_t_id = str(item.get('parent_temp_id', '')).strip().lower()
            
            # --- 【核心修正点】 ---
            if p_t_id == 'root':
                # 如果模板里写的是 root，数据库 parent_id 字段直接存字符串 "root"
                real_parent_id = "root"
            elif p_t_id in temp_to_real_map:
                # 如果指向的是 CSV 里的其他数字 ID，则使用映射出的 UUID
                real_parent_id = temp_to_real_map[p_t_id]
            else:
                # 其他情况（如真的为空）才存 None
                real_parent_id = None
            # ----------------------

            # 处理布尔值
            is_expanded = str(item.get('expanded', 'true')).lower() == 'true'
            
            # 特殊处理：如果当前节点本身就是 root 节点
            # (虽然你图片里 root 是作为父节点出现的，但预防万一你要导入 root 节点)
            current_node_id = temp_to_real_map[t_id]
            # 如果你希望 temp_id 为 1 的节点 node_id 直接就是 "root"，可以加这个判断：
            # if t_id == "1" and p_t_id == "": current_node_id = "root"

            node = SkillNode(
                node_id=current_node_id,
                tree_id=tree_id,
                parent_id=real_parent_id, # 这里会存入 "root" 字符串
                topic=item.get('topic', '未命名'),
                direction=item.get('direction', 'right'),
                expanded=is_expanded,
                status=item.get('status', 'locked'),
                background_color=item.get('background_color', '#f4f5f7'),
                foreground_color=item.get('foreground_color', '#3d4451'),
                description=item.get('description', ''),
                link=item.get('link', ''),
                link2=item.get('link2', ''),
                level=int(item.get('level', 1) or 1),
                module=item.get('module', '默认模块'),
                sort_index=int(item.get('sort_index', 0) or 0)
            )
            new_nodes.append(node)
        
        db.session.bulk_save_objects(new_nodes)
        db.session.commit()
        return jsonify({"message": f"成功导入 {len(new_nodes)} 个节点，已关联至 root"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500





@app.route('/api/users', methods=['POST'])
def create_user():
    """创建用户"""
    data = request.json
    username = data.get('username')
    password = data.get('password', '')
    is_admin = data.get('is_admin', False)
    is_leader = data.get('is_leader', False)
    module = data.get('module', '默认模块')
    group = data.get('group', 'A')
    
    if not username:
        return jsonify({'error': '用户名不能为空'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    user = User(username=username, password=password, is_admin=is_admin, is_leader=is_leader, module=module, group=group)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'id': user.id, 'username': user.username, 'message': '用户创建成功'}), 201


@app.route('/api/users', methods=['GET'])
def get_users():
    """获取所有用户列表"""
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin,
        'is_leader': user.is_leader,
        'module': user.module,
        'group': user.group,
        'created_at': user.created_at.isoformat()
    } for user in users])

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户"""
    user = User.query.get_or_404(user_id)
    data = request.json
    
    username = data.get('username')
    if username is not None:
        existing = User.query.filter_by(username=username).first()
        if existing and existing.id != user_id:
            return jsonify({'error': '用户名已存在'}), 400
        user.username = username
        
    password = data.get('password')
    if password is not None and password != '':
        user.password = password
        
    is_admin = data.get('is_admin')
    if is_admin is not None:
        user.is_admin = is_admin
        
    is_leader = data.get('is_leader')
    if is_leader is not None:
        user.is_leader = is_leader
        
    module = data.get('module')
    if module is not None:
        user.module = module
        
    group = data.get('group')
    if group is not None:
        user.group = group
        
    db.session.commit()
    return jsonify({'message': '用户更新成功'})


@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    username = data.get('username')
    password = data.get('password', '')
    
    if not username:
        return jsonify({'error': '用户名不能为空'}), 400
        
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404
        
    # 简单密码校验，实际情况需加密并安全校验
    if user.password != password:
        return jsonify({'error': '密码错误'}), 401
        
    return jsonify({
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin,
        'is_leader': user.is_leader,
        'module': user.module,
        'group': user.group,
        'message': '登录成功'
    }), 200


@app.route('/api/trees', methods=['GET'])
def get_all_trees():
    """获取技能树列表（带有权限标记）"""
    user_id = request.args.get('user_id', type=int)
    
    trees = SkillTree.query.all()
    user = User.query.get(user_id) if user_id else None
    
    result = []
    for tree in trees:
        can_activate = True
        if user and not user.is_admin:
            user_modules = set([m.strip() for m in user.module.split(',')] if user.module else [])
            tree_modules = set([m.strip() for m in tree.module.split(',')] if tree.module else [])
            can_activate = bool(user_modules.intersection(tree_modules))
            
        result.append({
            'id': tree.id,
            'name': tree.name,
            'module': tree.module,
            'author': tree.author,
            'version': tree.version,
            'can_activate': can_activate,
            'created_at': tree.created_at.isoformat(),
            'updated_at': tree.updated_at.isoformat()
        })
            
    return jsonify(result)


@app.route('/api/trees', methods=['POST'])
def create_tree():
    """创建新的技能树"""
    data = request.json
    default_points = data.get('default_skill_points', 10)
    
    tree = SkillTree(
        name=data.get('name', '未命名技能树'),
        module=data.get('module', '默认模块'),
        author=data.get('author', 'system'),
        version=data.get('version', '1.0'),
        default_skill_points=default_points,
        extra_data=data.get('extra_data')
    )
    db.session.add(tree)
    db.session.commit()
    
    # 如果有节点数据，保存节点
    if 'data' in data and data['data']:
        save_nodes(tree.id, data['data'])
        db.session.commit()  # 关键：提交节点数据
        node_count = SkillNode.query.filter_by(tree_id=tree.id).count()
        print(f"技能树 {tree.id} 创建完成，保存节点数：{node_count}")
    
    return jsonify({'id': tree.id, 'message': '创建成功'}), 201


@app.route('/api/trees/<int:tree_id>', methods=['GET'])
def get_tree(tree_id):
    """获取指定技能树（包含所有节点）"""
    user_id = request.args.get('user_id', type=int)  # 可选的用户ID
    
    tree = SkillTree.query.get_or_404(tree_id)
    nodes = SkillNode.query.filter_by(tree_id=tree_id).order_by(SkillNode.sort_index.asc()).all()
    
    # 构建jsmind格式的数据
    mind_data = build_jsmind_data(tree, nodes, user_id)
    
    return jsonify(mind_data)


@app.route('/api/trees/<int:tree_id>', methods=['PUT'])
def update_tree(tree_id):
    """更新整个技能树"""
    tree = SkillTree.query.get_or_404(tree_id)
    data = request.json
    
    tree.name = data.get('name', tree.name)
    tree.module = data.get('module', tree.module)
    tree.author = data.get('author', tree.author)
    tree.version = data.get('version', tree.version)
    if 'default_skill_points' in data:
        tree.default_skill_points = data.get('default_skill_points', tree.default_skill_points)
    if 'extra_data' in data:
        tree.extra_data = data.get('extra_data')
    tree.updated_at = datetime.now()
    
    # 只有当请求中包含节点数据时，才更新节点
    if 'data' in data and data['data']:
        # 先获取现有节点的颜色信息，以便在更新时保留
        existing_nodes = SkillNode.query.filter_by(tree_id=tree_id).all()
        color_map = {}
        for node in existing_nodes:
            color_map[node.node_id] = {
                'background_color': node.background_color,
                'foreground_color': node.foreground_color
            }
        
        # 尝试在保存前记录历史（如果数据发生了变化）
        user_id = data.get('user_id')
        user = User.query.get(user_id) if user_id else None
        
        # 递归查找所有发生变更的节点
        def track_bulk_changes(node_list, parent_id=None):
            if not node_list: return
            for n_data in node_list:
                n_id = n_data.get('id')
                if n_id in color_map: # 说明是旧节点
                    old_node = SkillNode.query.filter_by(tree_id=tree_id, node_id=n_id).first()
                    if old_node:
                        bulk_changes = {}
                        if old_node.topic != n_data.get('topic', old_node.topic):
                            bulk_changes['topic'] = {'old': old_node.topic, 'new': n_data.get('topic')}
                        # ... 其他字段比对暂略或按需添加 ...
                        if bulk_changes:
                            history = NodeEditHistory(
                                tree_id=tree_id,
                                node_id=n_id,
                                user_id=user_id,
                                username=user.username if user else '批量保存',
                                change_details=json.dumps(bulk_changes, ensure_ascii=False)
                            )
                            db.session.add(history)
                if 'children' in n_data:
                    track_bulk_changes(n_data['children'], n_id)

        track_bulk_changes([data['data']])

        # 删除旧节点
        SkillNode.query.filter_by(tree_id=tree_id).delete()
        db.session.flush()
        
        try:
            # 在保存节点时，如果新节点没有颜色信息，使用旧节点的颜色信息
            def preserve_colors(node_data):
                """保留现有节点的颜色信息"""
                if not node_data or 'id' not in node_data:
                    return
                
                node_id = node_data['id']
                # 如果新节点没有颜色信息，但旧节点有，则使用旧节点的颜色
                if node_id in color_map:
                    if 'background-color' not in node_data or not node_data.get('background-color'):
                        node_data['background-color'] = color_map[node_id]['background_color']
                    if 'foreground-color' not in node_data or not node_data.get('foreground-color'):
                        node_data['foreground-color'] = color_map[node_id]['foreground_color']
                
                # 递归处理子节点
                if 'children' in node_data and node_data['children']:
                    if isinstance(node_data['children'], list):
                        for child in node_data['children']:
                            preserve_colors(child)
            
            # 保留颜色信息
            preserve_colors(data['data'])
            
            save_nodes(tree_id, data['data'])
            # 统计保存的节点数
            node_count = SkillNode.query.filter_by(tree_id=tree_id).count()
            print(f"技能树 {tree_id} 更新成功，共保存 {node_count} 个节点")
        except Exception as e:
            print(f"保存节点时出错：{e}")
            db.session.rollback()
            return jsonify({'error': f'保存节点失败：{str(e)}'}), 500
    
    db.session.commit()
    return jsonify({'message': '更新成功'})


@app.route('/api/trees/<int:tree_id>', methods=['DELETE'])
def delete_tree(tree_id):
    """删除技能树"""
    tree = SkillTree.query.get_or_404(tree_id)
    db.session.delete(tree)
    db.session.commit()
    return jsonify({'message': '删除成功'})

@app.route('/api/trees/<int:tree_id>/nodes', methods=['POST'])
def add_node(tree_id):
    """快速添加单个节点"""
    tree = SkillTree.query.get_or_404(tree_id)
    payload = request.json.get('data', {})
    
    node_id = payload.get('id')
    if not node_id:
        return jsonify({'error': '节点ID不能为空'}), 400
        
    # 检查节点是否已存在
    existing = SkillNode.query.filter_by(tree_id=tree_id, node_id=node_id).first()
    if existing:
        return jsonify({'error': '节点ID已存在'}), 400
        
    node = SkillNode(
        tree_id=tree_id,
        node_id=node_id,
        parent_id=payload.get('parent_id') or None,
        topic=payload.get('topic', '新节点'),
        direction=payload.get('direction', 'right'),
        level=payload.get('level', 1),
        module=payload.get('module', '默认模块'),
        cost=payload.get('cost', 1),
        description=payload.get('description', ''),
        link=payload.get('link', ''),
        link2=payload.get('link2', '')
    )
    db.session.add(node)
    
    # 记录节点添加历史
    user_id = payload.get('user_id')
    user = User.query.get(user_id) if user_id else None
    history = NodeEditHistory(
        tree_id=tree_id,
        node_id=node_id,
        user_id=user_id,
        username=user.username if user else '快速添加',
        change_details=json.dumps({'action': 'added_node', 'topic': node.topic}, ensure_ascii=False)
    )
    db.session.add(history)
    
    db.session.commit()
    
    return jsonify({'message': '节点添加成功', 'node_id': node.node_id}), 201

@app.route('/api/trees/<int:tree_id>/nodes/batch', methods=['POST'])
def batch_add_nodes(tree_id):
    """批量导入节点（CSV导入专用）"""
    tree = SkillTree.query.get_or_404(tree_id)
    data = request.json
    nodes_data = data.get('nodes', [])

    if not nodes_data:
        return jsonify({'error': '节点数据不能为空'}), 400

    results = []
    success_count = 0
    error_count = 0

    for idx, payload in enumerate(nodes_data):
        row_num = idx + 2  # CSV第1行是表头，数据从第2行开始
        topic = payload.get('topic', '').strip()

        if not topic:
            results.append({'row': row_num, 'topic': '(空)', 'status': 'error', 'message': '标题不能为空'})
            error_count += 1
            continue

        # 生成唯一节点ID
        node_id = payload.get('id') or ('node_' + __import__('uuid').uuid4().hex[:8])

        # 检查节点ID是否已存在
        existing = SkillNode.query.filter_by(tree_id=tree_id, node_id=node_id).first()
        if existing:
            node_id = 'node_' + __import__('uuid').uuid4().hex[:8]

        try:
            node = SkillNode(
                tree_id=tree_id,
                node_id=node_id,
                parent_id=payload.get('parent_id') or None,
                topic=topic,
                direction=payload.get('direction', 'right'),
                level=int(payload.get('level', 1)),
                module=payload.get('module', '默认模块'),
                cost=int(payload.get('cost', 1)),
                description=payload.get('description', ''),
                link=payload.get('link', ''),
                link2=payload.get('link2', '')
            )
            db.session.add(node)

            # 记录历史
            history = NodeEditHistory(
                tree_id=tree_id,
                node_id=node_id,
                user_id=None,
                username='CSV批量导入',
                change_details=json.dumps({'action': 'csv_import', 'topic': topic}, ensure_ascii=False)
            )
            db.session.add(history)
            db.session.flush()  # 单条刷新，不提交

            results.append({'row': row_num, 'topic': topic, 'status': 'success', 'node_id': node_id})
            success_count += 1

        except Exception as e:
            db.session.rollback()
            results.append({'row': row_num, 'topic': topic, 'status': 'error', 'message': str(e)})
            error_count += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'批量提交失败：{str(e)}'}), 500

    return jsonify({
        'message': f'导入完成，成功 {success_count} 条，失败 {error_count} 条',
        'success_count': success_count,
        'error_count': error_count,
        'results': results
    }), 200 if error_count == 0 else 207


@app.route('/api/trees/<int:tree_id>/mode', methods=['PUT'])

def update_tree_mode(tree_id):
    """更新技能树的激活模式"""
    tree = SkillTree.query.get_or_404(tree_id)
    data = request.json
    mode = data.get('mode')
    
    # 建立映射关系，兼容前端可能传入的 'linear' 关键字
    mode_map = {
        'tree': 'tree',
        'path': 'path',
        'linear': 'path'
    }
    
    if mode not in mode_map:
        return jsonify({'error': '无效的模式'}), 400
        
    normalized_mode = mode_map[mode]
    tree.mode = normalized_mode
    db.session.commit()
    return jsonify({'message': f'模式已更新为 {normalized_mode}', 'mode': normalized_mode})


@app.route('/api/trees/<int:tree_id>/nodes/<node_id>', methods=['PUT'])
def update_node(tree_id, node_id):
    """更新单个节点"""
    node = SkillNode.query.filter_by(tree_id=tree_id, node_id=node_id).first_or_404()
    data = request.json
    
    # 记录变更详情
    changes = {}
    
    def normalize(val):
        if val is None: return ""
        return str(val).strip()

    req_topic = normalize(data.get('topic'))
    req_desc = normalize(data.get('description'))
    req_link = normalize(data.get('link'))
    req_link2 = normalize(data.get('link2'))
    
    if normalize(node.topic) != req_topic:
        changes['topic'] = {'old': node.topic, 'new': req_topic}
    if normalize(node.description) != req_desc:
        changes['description'] = {'old': node.description, 'new': req_desc}
    if normalize(node.link) != req_link:
        changes['link'] = {'old': node.link, 'new': req_link}
    if normalize(node.link2) != req_link2:
        changes['link2'] = {'old': node.link2, 'new': req_link2}
    if node.level != int(data.get('level', node.level)):
        changes['level'] = {'old': node.level, 'new': int(data.get('level'))}
    if normalize(node.module) != normalize(data.get('module')):
        changes['module'] = {'old': node.module, 'new': data.get('module')}

    print(f"DEBUG: Node {node_id} changes: {changes}")

    node.topic = req_topic
    node.direction = data.get('direction', node.direction)
    node.expanded = data.get('expanded', node.expanded)
    node.background_color = data.get('background_color', node.background_color)
    node.foreground_color = data.get('foreground_color', node.foreground_color)
    node.cost = data.get('cost', node.cost)
    node.description = data.get('description', node.description)
    node.link = data.get('link', node.link)
    node.link2 = data.get('link2', node.link2)
    node.level = data.get('level', node.level)
    node.module = data.get('module', node.module)
    
    node.updated_at = datetime.now()

    # 如果有变更，保存历史记录
    if changes:
        user_id = data.get('user_id')
        user = User.query.get(user_id) if user_id else None
        history = NodeEditHistory(
            tree_id=tree_id,
            node_id=node_id,
            user_id=user_id,
            username=user.username if user else '未知用户',
            change_details=json.dumps(changes, ensure_ascii=False)
        )
        db.session.add(history)
    
    db.session.commit()
    
    return jsonify({'message': '节点更新成功'})


@app.route('/api/trees/<int:tree_id>/nodes/<node_id>/activate', methods=['POST'])
def activate_node(tree_id, node_id):
    """激活/点亮节点（用户操作）"""
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': '需要用户ID'}), 400
    
    user = User.query.get_or_404(user_id)
    tree = SkillTree.query.get_or_404(tree_id)
    node = SkillNode.query.filter_by(tree_id=tree_id, node_id=node_id).first_or_404()
    
    # 权限校验：非管理员只能在自己所属模块的技能树中激活节点
    if not user.is_admin:
        user_modules = set([m.strip() for m in user.module.split(',')] if user.module else [])
        tree_modules = set([m.strip() for m in tree.module.split(',')] if tree.module else [])
        if not user_modules.intersection(tree_modules):
            return jsonify({'error': '您没有权限激活该模块的技能节点'}), 403
    
    # 获取或创建用户技能树状态
    user_state = UserSkillTreeState.query.filter_by(
        user_id=user_id, tree_id=tree_id, node_id=node_id
    ).first()
    
    if not user_state:
        # 初始化用户技能树状态（如果是第一次）
        init_user_tree_state(user_id, tree_id, tree.default_skill_points)
        user_state = UserSkillTreeState.query.filter_by(
            user_id=user_id, tree_id=tree_id, node_id=node_id
        ).first()
    
    # 检查解锁条件（根据当前树的模式）
    if tree.mode == 'path':
        # 进阶模式校验
        if node.level > 1:
            # 找到该模块下小于当前等级的最大等级（最近的前有序等级）
            prev_levels = db.session.query(SkillNode.level).filter(
                SkillNode.tree_id == tree_id,
                SkillNode.module == node.module,
                SkillNode.level < node.level
            ).distinct().all()
            
            if prev_levels:
                # 取得最大的前序等级
                target_prev_level = max(l[0] for l in prev_levels)
                
                # 获取该等级的所有节点
                prev_nodes = SkillNode.query.filter_by(
                    tree_id=tree_id, module=node.module, level=target_prev_level
                ).all()
                
                # 检查是否全部激活
                for p_node in prev_nodes:
                    p_state = UserSkillTreeState.query.filter_by(
                        user_id=user_id, tree_id=tree_id, node_id=p_node.node_id
                    ).first()
                    if not p_state or p_state.status != 'activated':
                        return jsonify({'error': f'必须先完成该模块下所有 {target_prev_level} 级的技能才能解锁当前等级'}), 400
    else:
        # 树状模式校验（自下而上）
        children = SkillNode.query.filter_by(tree_id=tree_id, parent_id=node.node_id).all()
        if children:
            for child in children:
                child_state = UserSkillTreeState.query.filter_by(
                    user_id=user_id, tree_id=tree_id, node_id=child.node_id
                ).first()
                if not child_state or child_state.status != 'activated':
                    return jsonify({'error': '必须先完成所有子技能才能激活此技能'}), 400
    
    # 检查节点状态
    if user_state.status == 'activated':
        return jsonify({'error': '节点已激活'}), 400
    if user_state.status == 'pending_approval':
        return jsonify({'error': '节点正在审核中'}), 400
    
    # 获取用户在该技能树中的技能点 (用于校验)
    root_state = UserSkillTreeState.query.filter_by(
        user_id=user_id, tree_id=tree_id, node_id='root'
    ).first()
    
    if not root_state:
        init_user_tree_state(user_id, tree_id, tree.default_skill_points)
        root_state = UserSkillTreeState.query.filter_by(
            user_id=user_id, tree_id=tree_id, node_id='root'
        ).first()

    # 逻辑：如果是管理员或组长（激活本人的），直接点亮；普通用户则进入待审核
    if user.is_admin or user.is_leader:
        user_state.status = 'activated'
        
        # 如果该节点有关联的任务，同步标记为完成
        task = LearningTask.query.filter_by(user_id=user_id, tree_id=tree_id, node_id=node_id, status='assigned').first()
        if task:
            task.status = 'completed'
            task.completed_at = datetime.now()
            
        message = '节点激活成功'
    else:
        user_state.status = 'pending_approval'
        # 查找或创建一个 pending 状态的任务记录，方便管理追踪
        task = LearningTask.query.filter_by(user_id=user_id, tree_id=tree_id, node_id=node_id).first()
        if not task:
            # 创建一个临时的“自发申请”任务
            task = LearningTask(
                user_id=user_id,
                tree_id=tree_id,
                node_id=node_id,
                task_type='self_apply',
                status='pending'
            )
            db.session.add(task)
        else:
            task.status = 'pending'
            
        message = '申请已提交，等待管理员或组长审核'
    
    user_state.updated_at = datetime.now()
    db.session.commit()
    
    return jsonify({
        'message': message,
        'status': user_state.status,
        'skill_points': root_state.skill_points
    })


@app.route('/api/trees/<int:tree_id>/nodes/<node_id>/deactivate', methods=['POST'])
def deactivate_node(tree_id, node_id):
    """取消激活节点（重置）"""
    node = SkillNode.query.filter_by(tree_id=tree_id, node_id=node_id).first_or_404()
    tree = SkillTree.query.get_or_404(tree_id)
    
    if node.status != 'activated':
        return jsonify({'error': '节点未激活'}), 400
    
    # 检查是否有子节点已激活
    children = SkillNode.query.filter_by(tree_id=tree_id, parent_id=node.node_id).all()
    activated_children = [c for c in children if c.status == 'activated']
    if activated_children:
        return jsonify({'error': '存在已激活的子节点，无法取消激活'}), 400
    
    # 取消激活
    node.status = 'locked'
    tree.skill_points += node.cost
    node.updated_at = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        'message': '节点已重置',
        'skill_points': tree.skill_points
    })


@app.route('/api/trees/<int:tree_id>/skill-points', methods=['PUT'])
def update_skill_points(tree_id):
    """更新技能点"""
    tree = SkillTree.query.get_or_404(tree_id)
    data = request.json
    
    tree.skill_points = data.get('skill_points', tree.skill_points)
    tree.total_skill_points = data.get('total_skill_points', tree.total_skill_points)
    db.session.commit()
    
    return jsonify({
        'skill_points': tree.skill_points,
        'total_skill_points': tree.total_skill_points
    })


@app.route('/api/trees/<int:tree_id>/reset', methods=['POST'])
def reset_tree(tree_id):
    """重置技能树（管理员操作，重置所有用户的状态）"""
    data = request.json
    user_id = data.get('user_id')  # 操作者ID
    target_user_id = data.get('target_user_id')  # 目标用户ID，如果为空则重置所有用户
    
    if not user_id:
        return jsonify({'error': '需要用户ID'}), 400
    
    user = User.query.get_or_404(user_id)
    
    # 检查是否是管理员
    if not user.is_admin:
        return jsonify({'error': '只有管理员可以重置技能树'}), 403
    
    tree = SkillTree.query.get_or_404(tree_id)
    
    if target_user_id:
        # 重置指定用户的状态
        user_states = UserSkillTreeState.query.filter_by(
            user_id=target_user_id, tree_id=tree_id
        ).all()
        
        for state in user_states:
            if state.status == 'activated' and state.node_id != 'root':
                # 返还技能点
                root_state = UserSkillTreeState.query.filter_by(
                    user_id=target_user_id, tree_id=tree_id, node_id='root'
                ).first()
                if root_state:
                    node = SkillNode.query.filter_by(tree_id=tree_id, node_id=state.node_id).first()
                    if node:
                        root_state.skill_points += node.cost
                state.status = 'locked'
        
        # 重置根节点的技能点
        root_state = UserSkillTreeState.query.filter_by(
            user_id=target_user_id, tree_id=tree_id, node_id='root'
        ).first()
        if root_state:
            root_state.skill_points = tree.default_skill_points
        
        db.session.commit()
        return jsonify({
            'message': f'用户 {target_user_id} 的技能树已重置',
            'skill_points': root_state.skill_points if root_state else tree.default_skill_points
        })
    else:
        # 重置所有用户的状态
        user_states = UserSkillTreeState.query.filter_by(tree_id=tree_id).all()
        reset_count = 0
        
        for state in user_states:
            if state.status == 'activated' and state.node_id != 'root':
                state.status = 'locked'
                reset_count += 1
        
        # 重置所有用户的技能点
        root_states = UserSkillTreeState.query.filter_by(tree_id=tree_id, node_id='root').all()
        for root_state in root_states:
            root_state.skill_points = tree.default_skill_points
        
        db.session.commit()
        return jsonify({
            'message': f'所有用户的技能树已重置，共重置 {reset_count} 个节点',
            'reset_count': reset_count
        })


@app.route('/api/users/<int:user_id>/trees/<int:tree_id>/reset', methods=['POST'])
def reset_user_tree(user_id, tree_id):
    """重置指定用户的技能树（用户自己重置）"""
    tree = SkillTree.query.get_or_404(tree_id)
    
    # 重置用户状态
    user_states = UserSkillTreeState.query.filter_by(
        user_id=user_id, tree_id=tree_id
    ).all()
    
    for state in user_states:
        if state.status == 'activated' and state.node_id != 'root':
            # 返还技能点
            root_state = UserSkillTreeState.query.filter_by(
                user_id=user_id, tree_id=tree_id, node_id='root'
            ).first()
            if root_state:
                node = SkillNode.query.filter_by(tree_id=tree_id, node_id=state.node_id).first()
                if node:
                    root_state.skill_points += node.cost
            state.status = 'locked'
    
    # 重置技能点
    root_state = UserSkillTreeState.query.filter_by(
        user_id=user_id, tree_id=tree_id, node_id='root'
    ).first()
    if root_state:
        root_state.skill_points = tree.default_skill_points
    
    db.session.commit()
    
    return jsonify({
        'message': '技能树已重置',
        'skill_points': root_state.skill_points if root_state else tree.default_skill_points
    })


def init_user_tree_state(user_id, tree_id, skill_points):
    """初始化用户的技能树状态"""
    nodes = SkillNode.query.filter_by(tree_id=tree_id).all()
    
    for node in nodes:
        # 检查是否已存在
        existing = UserSkillTreeState.query.filter_by(
            user_id=user_id, tree_id=tree_id, node_id=node.node_id
        ).first()
        
        if not existing:
            state = UserSkillTreeState(
                user_id=user_id,
                tree_id=tree_id,
                node_id=node.node_id,
                status='activated' if node.node_id == 'root' else 'locked',
                skill_points=skill_points if node.node_id == 'root' else 0
            )
            db.session.add(state)
    
    db.session.commit()


def save_nodes(tree_id, node_data, parent_id=None, index=0):
    """递归保存节点数据"""
    if not node_data or 'id' not in node_data:
        print(f"警告：跳过无效节点数据，parent_id={parent_id}")
        return None
    
    node = SkillNode(
        tree_id=tree_id,
        node_id=node_data['id'],
        parent_id=parent_id,
        topic=node_data.get('topic', ''),
        direction=node_data.get('direction'),
        expanded=node_data.get('expanded', True),
        status=node_data.get('status', 'locked'),  # 默认锁定
        cost=node_data.get('cost', 1),  # 默认消耗1点
        background_color=node_data.get('background-color', '#FFD700'),
        foreground_color=node_data.get('foreground-color', '#000000'),
        description=node_data.get('description', ''),
        link=node_data.get('link', ''),
        link2=node_data.get('link2', ''),
        level=int(node_data.get('level', 1)),
        module=node_data.get('module', '默认模块'),
        sort_index=index
    )
    
    # 保存额外数据（排除颜色相关字段，颜色只通过 background_color 和 foreground_color 保存）
    extra = {}
    excluded_keys = ['id', 'topic', 'direction', 'expanded', 'children', 
                     'background-color', 'foreground-color', 
                     'original-background-color', 'original-foreground-color',
                     'status', 'cost', 'description', 'link', 'link2', 'level', 'module']
    for key in node_data:
        if key not in excluded_keys:
            extra[key] = node_data[key]
    if extra:
        node.extra_data = json.dumps(extra)
    
    db.session.add(node)
    db.session.flush()
    
    # 递归保存子节点
    children_count = 0
    if 'children' in node_data and node_data['children']:
        if isinstance(node_data['children'], list):
            for i, child in enumerate(node_data['children']):
                if child and isinstance(child, dict) and 'id' in child:
                    save_nodes(tree_id, child, node_data['id'], i)
                    children_count += 1
                else:
                    print(f"警告：跳过无效子节点，parent={node_data['id']}")
        else:
            print(f"警告：children 不是列表，parent={node_data['id']}")
    
    if children_count > 0:
        print(f"节点 {node_data['id']} 保存了 {children_count} 个子节点")
    
    return node


def build_jsmind_data(tree, nodes, user_id=None):
    """构建jsmind格式的数据"""
    # 获取用户状态（如果提供了user_id）
    user_states = {}
    user_skill_points = tree.default_skill_points
    
    if user_id:
        states = UserSkillTreeState.query.filter_by(user_id=user_id, tree_id=tree.id).all()
        for state in states:
            user_states[state.node_id] = state
            if state.node_id == 'root':
                user_skill_points = state.skill_points
        
        # 如果用户状态不存在，初始化
        if not states:
            init_user_tree_state(user_id, tree.id, tree.default_skill_points)
            states = UserSkillTreeState.query.filter_by(user_id=user_id, tree_id=tree.id).all()
            for state in states:
                user_states[state.node_id] = state
                if state.node_id == 'root':
                    user_skill_points = state.skill_points
    
    # 创建节点映射
    node_map = {}
    for node in nodes:
        # 根据用户状态设置颜色和样式
        # 获取节点保存的原始颜色（如果为None或空，则视为未配置）
        # 注意：这里要保留原始值，不要立即设置默认值，以便后续判断
        original_bg_color = node.background_color if node.background_color else None
        original_fg_color = node.foreground_color if node.foreground_color else None
        
        # 用于显示的背景色和前景色（会设置默认值）
        bg_color = original_bg_color if original_bg_color else '#FFD700'  # 默认金色
        fg_color = original_fg_color if original_fg_color else '#000000'  # 默认黑色
        
        node_status = 'locked'
        
        if user_id and node.node_id in user_states:
            node_status = user_states[node.node_id].status
        elif not user_id:
            # 如果没有用户，使用节点默认状态
            node_status = node.status
        
        # 根据状态调整显示效果，但保留原始颜色信息
        # 如果是后台编辑模式（没有user_id），直接使用数据库中的颜色，不根据状态改变
        if not user_id:
            # 后台编辑模式：直接使用数据库中的颜色，不根据状态改变
            display_bg_color = bg_color
            display_fg_color = fg_color
        else:
            # 前台查看模式：根据节点状态显示颜色
            if node_status == 'locked':
                # 锁定状态（未点亮）：使用灰色
                display_bg_color = '#666666'
                display_fg_color = '#999999'
            elif node_status == 'activated':
                # 已激活（已点亮）：如果数据库中的颜色是默认金色，则显示绿色，否则显示数据库中的颜色
                if bg_color == '#FFD700':  # 如果是默认金色，显示绿色
                    display_bg_color = '#32CD32'  # 绿色
                    display_fg_color = '#000000'  # 黑色文字
                else:
                    # 如果有自定义颜色，使用数据库中的颜色
                    display_bg_color = bg_color
                    display_fg_color = fg_color
            else:
                # 其他状态（如unlocked）：使用灰色（未点亮状态）
                display_bg_color = '#666666'
                display_fg_color = '#999999'
        
        node_map[node.node_id] = {
            'id': node.node_id,
            'topic': node.topic,
            'direction': node.direction,
            'expanded': node.expanded,
            'status': node_status,
            'cost': node.cost,
            'background-color': display_bg_color,  # 使用显示颜色
            'foreground-color': display_fg_color,   # 使用显示颜色
            # 原始颜色：始终使用数据库中的实际颜色值（用于前端判断和显示）
            'original-background-color': original_bg_color if original_bg_color else bg_color,
            'original-foreground-color': original_fg_color if original_fg_color else fg_color,
            'description': node.description or '',  # 技能说明
            'link': node.link or '',  # 技能链接 1
            'link2': node.link2 or '', # 技能链接 2
            'level': node.level or 1,  # 等级属性
            'module': node.module or '默认模块',  # 所属模块
            'children': []
        }
        
        # 添加额外数据（但不覆盖颜色字段，颜色只从 background_color 和 foreground_color 读取）
        if node.extra_data:
            extra = json.loads(node.extra_data)
            # 排除颜色相关字段，确保颜色只从数据库的标准字段读取
            color_keys = ['background-color', 'foreground-color', 
                         'original-background-color', 'original-foreground-color']
            for key in color_keys:
                if key in extra:
                    del extra[key]
            if extra:
                node_map[node.node_id].update(extra)
    
    # 构建树形结构
    root = None
    for node in nodes:
        if node.parent_id is None or node.parent_id == '':
            root = node_map[node.node_id]
        else:
            if node.parent_id in node_map:
                if 'children' not in node_map[node.parent_id]:
                    node_map[node.parent_id]['children'] = []
                node_map[node.parent_id]['children'].append(node_map[node.node_id])
            else:
                # 如果父节点不存在，将其作为根节点的子节点
                print(f"警告：节点 {node.node_id} 的父节点 {node.parent_id} 不存在，将作为根节点的子节点")
    # ================= 动态状态计算逻辑 =================
    
    # 获取用户激活状态和待审核状态数据
    user_activated_ids = set()
    user_pending_ids = set()
    if user_id:
        u_states = UserSkillTreeState.query.filter_by(user_id=user_id, tree_id=tree.id).filter(UserSkillTreeState.status.in_(['activated', 'pending_approval'])).all()
        for s in u_states:
            if s.status == 'activated':
                user_activated_ids.add(s.node_id)
            elif s.status == 'pending_approval':
                user_pending_ids.add(s.node_id)

    # 预处理进阶路径数据：按 module 聚合所有已激活等级
    path_groups = {} # {module: set(activated_levels)}
    for node in nodes:
        if node.node_id in user_activated_ids:
            if node.module not in path_groups:
                path_groups[node.module] = set()
            path_groups[node.module].add(node.level)
    
    # 统计每个等级的所有节点总数，用于校验“全部完成”规则
    level_node_counts = {} # {module: {level: total_count}}
    for node in nodes:
        if node.module not in level_node_counts:
            level_node_counts[node.module] = {}
        level_node_counts[node.module][node.level] = level_node_counts[node.module].get(node.level, 0) + 1
    
    # 统计每个等级已完成的节点数
    level_activated_counts = {} # {module: {level: count}}
    for node in nodes:
        if node.node_id in user_activated_ids:
            if node.module not in level_activated_counts:
                level_activated_counts[node.module] = {}
            level_activated_counts[node.module][node.level] = level_activated_counts[node.module].get(node.level, 0) + 1

    # 计算最终显示状态
    def get_calculated_status(node_data, mode):
        node_id = node_data['id']
        if node_id == 'root':
            return 'activated'
        
        # 1. 如果已激活，保持已激活
        if node_id in user_activated_ids:
            return 'activated'
        if node_id in user_pending_ids:
            return 'pending_approval'
        
        # 2. 根据模式计算解锁逻辑
        if mode == 'path':
            # 进阶模式：同一 module 下，比当前 level 小的所有等级节点必须全部完成
            current_level = node_data.get('level', 1)
            current_module = node_data.get('module', '默认模块')
            
            if current_level <= 1:
                return 'unlocked' # 第一级默认解锁
            
            # 找到该模块下存在的、比当前等级小的、最大的等级（即最近的前序等级）
            current_module = node_data.get('module', '默认模块')
            existing_lower_levels = [lvl for lvl in level_node_counts.get(current_module, {}).keys() if lvl < current_level]
            
            if not existing_lower_levels:
                return 'unlocked' # 如果前面没有任何等级，则视为起点，解锁
            
            prev_level = max(existing_lower_levels)
            
            # 检查该前序等级是否全部完成
            total_required = level_node_counts.get(current_module, {}).get(prev_level, 0)
            activated_count = level_activated_counts.get(current_module, {}).get(prev_level, 0)
            
            if total_required > 0 and activated_count >= total_required:
                return 'unlocked'
            return 'locked'
            
        else:
            # 树状模式 (Tree Mode)：自下而上。所有子节点必须点亮。
            children = node_data.get('children', [])
            if not children:
                return 'unlocked' # 叶子节点默认解锁
            
            # 检查子节点是否全量激活
            # 注意：此处需要递归检查所有后代，或者仅检查直属子级
            # 根据需求：“一节点的所有子节点均已完成时，该节点才可被激活”
            def all_children_activated(n_data):
                if not n_data.get('children'):
                    return n_data['id'] in user_activated_ids
                
                # 如果有子级，检查所有子级是否已激活
                return all(child['id'] in user_activated_ids for child in n_data['children'])

            if all_children_activated(node_data):
                return 'unlocked'
            return 'locked'

    # 为所有节点注入计算后的状态
    def inject_status(node_data, tree_mode):
        node_data['status'] = get_calculated_status(node_data, tree_mode)
        if 'children' in node_data and node_data['children']:
            for child in node_data['children']:
                inject_status(child, tree_mode)
        return node_data

    root = inject_status(root, tree.mode)
    
    # 确定当前用户是否有激活权限
    can_activate = True
    if user_id:
        user = User.query.get(user_id)
        if user and not user.is_admin:
            user_modules = set([m.strip() for m in user.module.split(',')] if user.module else [])
            tree_modules = set([m.strip() for m in tree.module.split(',')] if tree.module else [])
            can_activate = bool(user_modules.intersection(tree_modules))

    return {
        'meta': {
            'name': tree.name,
            'module': tree.module,
            'author': tree.author,
            'version': tree.version,
            'extra_data': tree.extra_data,
            'can_activate': can_activate,
            'skill_points': user_skill_points if user_id else tree.default_skill_points,
            'total_skill_points': tree.default_skill_points,
            'default_skill_points': tree.default_skill_points
        },
        'format': 'node_tree',
        'data': root
    }


@app.route('/api/modules', methods=['GET'])
def get_modules():
    """获取分离的各维度模块列表"""
    try:
        from sqlalchemy import text
        tree_records = db.session.query(SkillTree.module).distinct().all()
        node_records = db.session.query(SkillNode.module).distinct().all()
        user_records = db.session.query(User.module).distinct().all()
        
        def parse_modules(records):
            mods = set()
            for rec in records:
                if rec[0]:
                    for m in rec[0].split(','):
                        if m.strip(): mods.add(m.strip())
            if not mods: mods.add('默认模块')
            return sorted(list(mods))
            
        return jsonify({
            'tree': parse_modules(tree_records),
            'node': parse_modules(node_records),
            'user': parse_modules(user_records)
        })
    except Exception as e:
        return jsonify({'tree': ['默认模块'], 'node': ['默认模块'], 'user': ['默认模块']})


@app.route('/api/progress', methods=['GET'])
def get_progress():
    """获取用户进度信息"""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': '需要用户ID'}), 400
        
    user = User.query.get_or_404(user_id)
    
    get_all = request.args.get('all', 'false').lower() == 'true'
    
    users_to_query = []
    if get_all:
        all_users = User.query.all()
        if user.is_admin:
            users_to_query = all_users
        else:
            # 普通用户：过滤出自己，以及拥有交集模块的小伙伴
            user_modules = set([m.strip() for m in user.module.split(',')] if user.module else [])
            for u in all_users:
                if u.id == user.id:
                    users_to_query.append(u)
                    continue
                u_modules = set([m.strip() for m in u.module.split(',')] if u.module else [])
                if user_modules.intersection(u_modules):
                    users_to_query.append(u)
    else:
        # 非 get_all 模式，只查询目标用户（通常是当前用户自己）
        users_to_query = [user]

    # 获取发起请求的用户信息，用于进度过滤
    requester_id = request.args.get('user_id', type=int)
    requester = db.session.get(User, requester_id) if requester_id else None
    requester_modules = set([m.strip() for m in requester.module.split(',')] if requester and requester.module else [])
    
    all_trees = SkillTree.query.all()
    
    result = []
    for u in users_to_query:
        user_progress = {
            'user_id': u.id,
            'username': u.username,
            'is_admin': u.is_admin,
            'is_leader': u.is_leader,
            'module': u.module,
            'group': u.group,
            'trees': []
        }
        
        for tree in all_trees:
            # 权限过滤：非管理员查看别人进度时，只看与自己模块有交集的技能树
            if requester and not requester.is_admin:
                tree_modules = set([m.strip() for m in tree.module.split(',')] if tree.module else [])
                if not requester_modules.intersection(tree_modules):
                    continue

            # 统计总节点数（不包含root节点）
            nodes = [n for n in SkillNode.query.filter_by(tree_id=tree.id).all() if n.node_id != 'root']
            total_nodes = len(nodes)
            if total_nodes == 0:
                continue
                
            # 获取用户在该技能树上激活的节点
            user_states = UserSkillTreeState.query.filter_by(user_id=u.id, tree_id=tree.id, status='activated').all()
            activated_node_ids = set(state.node_id for state in user_states if state.node_id != 'root')
            
            # 由于可能包含废弃节点的进度，与当前真实节点做交集才是真实的已激活节点
            actual_activated_count = len([n for n in nodes if n.node_id in activated_node_ids])
            
            percent = int((actual_activated_count / total_nodes) * 100) if total_nodes > 0 else 0
            
            user_progress['trees'].append({
                'tree_id': tree.id,
                'tree_name': tree.name,
                'module': tree.module,
                'total_nodes': total_nodes,
                'activated_nodes': actual_activated_count,
                'percent': percent,
                # 添加具体激活节点的列表
                'activated_node_details': [
                    {'node_id': n.node_id, 'topic': n.topic} 
                    for n in nodes if n.node_id in activated_node_ids
                ]
            })
            
        result.append(user_progress)
        
    return jsonify(result)


@app.route('/api/trees/<int:tree_id>/nodes/<node_id>/click', methods=['POST'])
def log_node_click(tree_id, node_id):
    """记录节点点击事件"""
    data = request.json
    user_id = data.get('user_id')
    user = User.query.get(user_id) if user_id else None
    
    click = NodeClickHistory(
        tree_id=tree_id,
        node_id=node_id,
        user_id=user_id,
        username=user.username if user else '访客'
    )
    db.session.add(click)
    db.session.commit()
    
    return jsonify({'message': '点击已记录'})


@app.route('/api/trees/<int:tree_id>/nodes/<node_id>/history', methods=['GET'])
def get_node_history(tree_id, node_id):
    """获取节点的操作历史和点击统计"""
    # 编辑历史
    edit_histories = NodeEditHistory.query.filter_by(
        tree_id=tree_id, node_id=node_id
    ).order_by(NodeEditHistory.created_at.desc()).all()
    
    # 点击统计
    click_count = NodeClickHistory.query.filter_by(
        tree_id=tree_id, node_id=node_id
    ).count()
    
    # 最近点击
    recent_clicks = NodeClickHistory.query.filter_by(
        tree_id=tree_id, node_id=node_id
    ).order_by(NodeClickHistory.created_at.desc()).limit(1).all()
    
    return jsonify({
        'edit_history': [{
            'username': h.username,
            'changes': json.loads(h.change_details),
            'created_at': h.created_at.isoformat()
        } for h in edit_histories],
        'click_stats': {
            'total_clicks': click_count,
            'last_click': recent_clicks[0].created_at.isoformat() if recent_clicks else None,
            'last_click_user': recent_clicks[0].username if recent_clicks else None
        }
    })


@app.route('/api/history/global/clicks', methods=['GET'])
def get_global_click_history():
    """获取全局点击统计和最近点击记录"""
    # 获取参数
    ranking_limit = request.args.get('ranking_limit', 5, type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # 1. 统计各技能树的总点击量
    tree_stats_query = db.session.query(
        SkillTree.name,
        db.func.count(NodeClickHistory.id).label('click_count')
    ).join(NodeClickHistory, SkillTree.id == NodeClickHistory.tree_id)\
     .group_by(SkillTree.id).order_by(db.desc('click_count')).limit(ranking_limit).all()
    
    tree_stats = [{'tree_name': name, 'count': count} for name, count in tree_stats_query]
    
    # 2. 统计点击最多的节点
    node_stats_query = db.session.query(
        SkillTree.name,
        NodeClickHistory.node_id,
        db.func.count(NodeClickHistory.id).label('click_count')
    ).join(SkillTree, SkillTree.id == NodeClickHistory.tree_id)\
     .group_by(NodeClickHistory.tree_id, NodeClickHistory.node_id)\
     .order_by(db.desc('click_count')).limit(ranking_limit).all()
    
    # 获取节点标题
    node_stats = []
    for tree_name, node_id, count in node_stats_query:
        node = SkillNode.query.filter_by(node_id=node_id).first()
        node_stats.append({
            'tree_name': tree_name,
            'node_id': node_id,
            'node_topic': node.topic if node else '未知节点',
            'count': count
        })
        
    # 3. 统计点亮最多的技能树 (按已激活节点数统计)
    tree_activation_query = db.session.query(
        SkillTree.name,
        db.func.count(UserSkillTreeState.id).label('activation_count')
    ).join(UserSkillTreeState, SkillTree.id == UserSkillTreeState.tree_id)\
     .filter(UserSkillTreeState.status == 'activated')\
     .group_by(SkillTree.id).order_by(db.desc('activation_count')).limit(ranking_limit).all()
    
    tree_activation_stats = [{'tree_name': name, 'count': count} for name, count in tree_activation_query]

    # 4. 统计点亮最多的单个技能点 (热门学习节点)
    node_activation_query = db.session.query(
        SkillTree.name.label('tree_name'),
        UserSkillTreeState.tree_id,
        UserSkillTreeState.node_id,
        db.func.count(UserSkillTreeState.id).label('activation_count')
    ).join(SkillTree, SkillTree.id == UserSkillTreeState.tree_id)\
     .filter(UserSkillTreeState.status == 'activated')\
     .group_by(UserSkillTreeState.tree_id, UserSkillTreeState.node_id)\
     .order_by(db.desc('activation_count')).limit(ranking_limit).all()
    
    node_activation_stats = []
    for tree_name, t_id, node_id, count in node_activation_query:
        node = SkillNode.query.filter_by(node_id=node_id, tree_id=t_id).first()
        node_activation_stats.append({
            'tree_name': tree_name,
            'node_id': node_id,
            'node_topic': node.topic if node else '未知节点',
            'count': count
        })

    # 5. 点击记录分页
    total_clicks = NodeClickHistory.query.count()
    
    recent_clicks_query = db.session.query(
        NodeClickHistory.id,
        NodeClickHistory.username,
        NodeClickHistory.created_at,
        SkillTree.name.label('tree_name'),
        NodeClickHistory.node_id
    ).join(SkillTree, SkillTree.id == NodeClickHistory.tree_id)\
     .order_by(NodeClickHistory.created_at.desc())\
     .offset((page - 1) * per_page).limit(per_page).all()
     
    click_log = []
    for c in recent_clicks_query:
        try:
            node = SkillNode.query.filter_by(node_id=c.node_id).first()
            click_log.append({
                'username': c.username,
                'tree_name': c.tree_name,
                'node_topic': node.topic if node else c.node_id,
                'created_at': c.created_at.isoformat()
            })
        except Exception:
            continue

    return jsonify({
        'tree_stats': tree_stats,
        'node_stats': node_stats,
        'tree_activation_stats': tree_activation_stats,
        'node_activation_stats': node_activation_stats,
        'recent_clicks': click_log,
        'total_clicks': total_clicks,
        'page': page,
        'per_page': per_page
    })


@app.route('/api/history/global/edits', methods=['GET'])
def get_global_edit_history():
    """获取全局编辑历史记录"""
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    try:
        total_edits = NodeEditHistory.query.count()
        
        histories = db.session.query(
            NodeEditHistory.id,
            NodeEditHistory.username,
            NodeEditHistory.change_details,
            NodeEditHistory.created_at,
            SkillTree.name.label('tree_name'),
            NodeEditHistory.node_id
        ).join(SkillTree, SkillTree.id == NodeEditHistory.tree_id)\
         .order_by(NodeEditHistory.created_at.desc())\
         .offset((page - 1) * per_page).limit(per_page).all()
        
        result = []
        for h in histories:
            try:
                # 获取节点标题
                node = SkillNode.query.filter_by(node_id=h.node_id).first()
                # 容错处理 JSON 解析
                changes = {}
                if h.change_details:
                    try:
                        changes = json.loads(h.change_details)
                    except json.JSONDecodeError:
                        changes = {"error": "解析失败", "raw": h.change_details}
                
                result.append({
                    'username': h.username,
                    'tree_name': h.tree_name,
                    'node_topic': node.topic if node else h.node_id,
                    'changes': changes,
                    'created_at': h.created_at.isoformat()
                })
            except Exception as e:
                print(f"处理历史记录 {h.id} 时出错: {e}")
                continue
                
        return jsonify({
            'edits': result,
            'total_edits': total_edits,
            'page': page,
            'per_page': per_page
        })
    except Exception as e:
        print(f"获取全局编辑历史时发生重大错误: {e}")
        return jsonify({'error': str(e)}), 500


# 提供静态文件服务
@app.route('/')
def index():
    """首页 - 管理页面"""
    return send_file('index.html')

@app.route('/view.html')
def view():
    """展示页面"""
    return send_file('view.html')

@app.route('/login.html')
def login_page():
    """登录页面"""
    return send_file('login.html')

@app.route('/users.html')
def users_page():
    """用户管理页面"""
    return send_file('users.html')

@app.route('/<path:filename>')
def static_files(filename):
    """提供静态文件（CSS、JS等）"""
    if filename.startswith('libs/'):
        return send_from_directory('.', filename)
    return send_file(filename)


@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """获取大盘统计数据"""
    total_users = User.query.count()
    total_trees = SkillTree.query.count()
    # 过滤掉root节点
    total_nodes = SkillNode.query.filter(SkillNode.node_id != 'root').count()
    total_activations = UserSkillTreeState.query.filter(UserSkillTreeState.status == 'activated', UserSkillTreeState.node_id != 'root').count()
    
    # 获取各组别的激活率 (Group progress)
    groups = ['A', 'B', 'C', 'D','Office']
    group_stats = []
    
    for g in groups:
        g_users = User.query.filter_by(group=g).all()
        gu_ids = [u.id for u in g_users]
        if not gu_ids:
            continue
        g_activations = UserSkillTreeState.query.filter(UserSkillTreeState.user_id.in_(gu_ids), UserSkillTreeState.status == 'activated', UserSkillTreeState.node_id != 'root').count()
        g_possible_activations = len(gu_ids) * total_nodes
        g_progress = (g_activations / g_possible_activations * 100) if g_possible_activations > 0 else 0
        group_stats.append({
            'group': g,
            'user_count': len(gu_ids),
            'activations': g_activations,
            'progress': round(g_progress, 1)
        })
    
    # 模块激活统计 (Tree Module progress)
    # 先获取所有去重后的模块名称列表
    tree_modules_raw = db.session.query(SkillTree.module).distinct().all()
    user_modules_raw = db.session.query(User.module).distinct().all()
    
    unique_modules = set()
    for row in tree_modules_raw + user_modules_raw:
        if row[0]:
            for m in row[0].split(','):
                if m.strip(): unique_modules.add(m.strip())
    
    tree_module_stats = []
    for mod_name in sorted(list(unique_modules)):
        # 匹配包含该模块名称的所有技能树
        t_ids = [t.id for t in SkillTree.query.filter(SkillTree.module.ilike(f"%{mod_name}%")).all()]
        if not t_ids: continue
        
        # 确定属于该模块的用户
        m_users = User.query.filter(User.module.ilike(f"%{mod_name}%")).all()
        mu_ids = [u.id for u in m_users]
        if not mu_ids: continue
        
        # 该模块下的所有节点总数
        tm_nodes = SkillNode.query.filter(SkillNode.tree_id.in_(t_ids), SkillNode.node_id != 'root').count()
        if tm_nodes == 0: continue
        
        # 统计该模块对应的用户在这些技能树上的实际激活总数
        tm_activations = UserSkillTreeState.query.filter(
            UserSkillTreeState.user_id.in_(mu_ids),
            UserSkillTreeState.tree_id.in_(t_ids), 
            UserSkillTreeState.status == 'activated', 
            UserSkillTreeState.node_id != 'root'
        ).count()
        
        tm_possible = len(mu_ids) * tm_nodes
        tm_progress = (tm_activations / tm_possible * 100) if tm_possible > 0 else 0
        
        tree_module_stats.append({
            'module': mod_name,
            'tree_count': len(t_ids),
            'node_count': tm_nodes,
            'user_count': len(mu_ids),
            'progress': round(tm_progress, 1)
        })

    # 最活跃用户 (按点亮节点数量排行)
    top_users_query = db.session.query(
        User.username,
        User.group,
        User.module,
        db.func.count(UserSkillTreeState.id).label('activated_count')
    ).join(UserSkillTreeState, User.id == UserSkillTreeState.user_id)\
     .filter(UserSkillTreeState.status == 'activated', UserSkillTreeState.node_id != 'root')\
     .group_by(User.id).order_by(db.desc('activated_count')).limit(10).all()
     
    top_users = [{
        'username': u.username,
        'group': u.group,
        'module': u.module,
        'activated_nodes': u.activated_count,
        'progress': round((u.activated_count / total_nodes * 100), 1) if total_nodes > 0 else 0
    } for u in top_users_query]
    
    return jsonify({
        'overview': {
            'total_users': total_users,
            'total_trees': total_trees,
            'total_nodes': total_nodes,
            'total_activations': total_activations
        },
        'group_stats': group_stats,
        'module_stats': tree_module_stats,
        'top_users': top_users
    })

@app.route('/api/tasks/assign', methods=['POST'])
def assign_task():
    """管理员或组长分配学习任务"""
    data = request.json
    assigner_id = data.get('assigner_id')
    user_id = data.get('user_id')
    tree_id = data.get('tree_id')
    
    # 支持单选和多选
    node_id = data.get('node_id')
    node_ids = data.get('node_ids', [])
    if node_id and node_id not in node_ids:
        node_ids.append(node_id)
        
    task_type = data.get('task_type', 'weekly')
    
    if not all([assigner_id, user_id, tree_id]) or len(node_ids) == 0:
        return jsonify({'error': '缺少必要参数 (用户、技能树或技能点)'}), 400
        
    assigner = User.query.get_or_404(assigner_id)
    user = User.query.get_or_404(user_id)
    
    # 权限检查
    if not assigner.is_admin:
        if not assigner.is_leader:
            return jsonify({'error': '无权限分配任务'}), 403
        if assigner.group != user.group:
            return jsonify({'error': '组长只能给本组员分配任务'}), 403
            
    # 批量处理节点
    assigned_count = 0
    for nid in node_ids:
        # 检查是否已分配过且未完成
        existing = LearningTask.query.filter_by(
            user_id=user_id, tree_id=tree_id, node_id=nid, status='assigned'
        ).first()
        if existing:
            existing.task_type = task_type
            existing.assigner_id = assigner_id
        else:
            task = LearningTask(
                user_id=user_id,
                tree_id=tree_id,
                node_id=nid,
                task_type=task_type,
                assigner_id=assigner_id,
                status='assigned'
            )
            db.session.add(task)
        assigned_count += 1
        
    db.session.commit()
    return jsonify({'message': f'成功分配 {assigned_count} 个任务', 'count': assigned_count})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """管理员或组长取消分配的任务"""
    user_id = request.args.get('user_id', type=int) # 当前操作者ID
    if not user_id:
        return jsonify({'error': '缺少操作者ID'}), 400
        
    operator = User.query.get_or_404(user_id)
    task = LearningTask.query.get_or_404(task_id)
    
    # 权限检查
    if not operator.is_admin:
        if not operator.is_leader:
            return jsonify({'error': '无权限操作'}), 403
        if operator.group != task.user.group:
            return jsonify({'error': '组长只能撤回本组员的任务'}), 403
            
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': '任务已撤回'})

@app.route('/api/tasks/my', methods=['GET'])
def get_my_tasks():
    """获取用户的学习任务列表"""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': '需要用户ID'}), 400
        
    # 获取已分配但未完成的任务
    tasks = LearningTask.query.filter_by(user_id=user_id, status='assigned').all()
    
    result = {
        'daily': [],
        'weekly': [],
        'monthly': [],
        'quarterly': [],
        'yearly': []
    }
    
    # 定义获取层级路径的内部函数
    def get_path(tid, nid):
        path = []
        curr = nid
        # 限制循环次数防止死循环
        limit = 20
        while curr and curr != 'root' and limit > 0:
            limit -= 1
            node = SkillNode.query.filter_by(tree_id=tid, node_id=curr).first()
            if not node: break
            path.append(node.topic)
            curr = node.parent_id
        path.reverse()
        return ' > '.join(path)
    
    for t in tasks:
        tree = SkillTree.query.get(t.tree_id)
        node = SkillNode.query.filter_by(tree_id=t.tree_id, node_id=t.node_id).first()
        
        task_data = {
            'id': t.id,
            'tree_id': t.tree_id,
            'tree_name': tree.name if tree else '未知',
            'node_id': t.node_id,
            'node_topic': node.topic if node else t.node_id,
            'node_path': get_path(t.tree_id, t.node_id), # 新增层级路径
            'created_at': t.created_at.isoformat()
        }
        
        if t.task_type in result:
            result[t.task_type].append(task_data)
        else:
            # 默认为周计划
            result['weekly'].append(task_data)
            
    return jsonify(result)

@app.route('/api/tasks/pending', methods=['GET'])
def get_pending_approvals():
    """获取待审核列表"""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': '需要用户ID'}), 400
        
    currentUser = User.query.get_or_404(user_id)
    
    # 只有管理员和组长可以审核
    if not (currentUser.is_admin or currentUser.is_leader):
        return jsonify({'error': '无权限访问'}), 403
        
    # 查询待审核的任务/状态
    pending_states = UserSkillTreeState.query.filter_by(status='pending_approval').all()
    
    result = []
    # 定义获取路径的函数
    def get_path(tid, nid):
        path = []
        curr = nid
        limit = 20
        while curr and curr != 'root' and limit > 0:
            limit -= 1
            node = SkillNode.query.filter_by(tree_id=tid, node_id=curr).first()
            if not node: break
            path.append(node.topic)
            curr = node.parent_id
        path.reverse()
        return ' > '.join(path)

    for state in pending_states:
        user = User.query.get(state.user_id)
        # 如果是组长，只能看到所属组员的申请
        if currentUser.is_leader and not currentUser.is_admin:
            if not user or user.group != currentUser.group:
                continue
                
        tree = SkillTree.query.get(state.tree_id)
        node = SkillNode.query.filter_by(tree_id=state.tree_id, node_id=state.node_id).first()
        
        result.append({
            'user_id': user.id if user else state.user_id,
            'username': user.username if user else '未知用户',
            'group': user.group if user else 'A',
            'tree_id': tree.id if tree else state.tree_id,
            'tree_name': tree.name if tree else '未知',
            'node_id': node.node_id if node else state.node_id,
            'node_topic': node.topic if node else state.node_id,
            'node_path': get_path(state.tree_id, state.node_id),
            'cost': node.cost if node else 0,
            'requested_at': state.updated_at.isoformat()
        })
        
    return jsonify(result)

@app.route('/api/tasks/approve', methods=['POST'])
def approve_task():
    """审核通过任务"""
    data = request.json
    approver_id = data.get('approver_id')
    target_user_id = data.get('user_id')
    tree_id = data.get('tree_id')
    node_id = data.get('node_id')
    
    if not all([approver_id, target_user_id, tree_id, node_id]):
        return jsonify({'error': '缺少必要参数'}), 400
        
    approver = User.query.get_or_404(approver_id)
    targetUser = User.query.get_or_404(target_user_id)
    
    # 权限检查
    if not approver.is_admin:
        if not approver.is_leader:
            return jsonify({'error': '无权限审核'}), 403
        if approver.group != targetUser.group:
            return jsonify({'error': '组长只能审核本组成员的请求'}), 403
            
    # 获取状态记录
    user_state = UserSkillTreeState.query.filter_by(
        user_id=target_user_id, tree_id=tree_id, node_id=node_id
    ).first()
    
    if not user_state or user_state.status != 'pending_approval':
        return jsonify({'error': '未找到待审核的记录'}), 404
        
    # 获取根节点状态用于扣分
    root_state = UserSkillTreeState.query.filter_by(
        user_id=target_user_id, tree_id=tree_id, node_id='root'
    ).first()
    
    node = SkillNode.query.filter_by(tree_id=tree_id, node_id=node_id).first()
    cost = node.cost if node else 0
    
    # 正式激活
    user_state.status = 'activated'
        
    # 同步更新任务记录
    task = LearningTask.query.filter_by(
        user_id=target_user_id, tree_id=tree_id, node_id=node_id
    ).filter(LearningTask.status.in_(['assigned', 'pending'])).first()
    if task:
        task.status = 'completed'
        task.completed_at = datetime.now()
        
    db.session.commit()
    return jsonify({'message': '审核通过，已正式点亮节点'})

@app.route('/api/modules', methods=['GET'])
def get_all_modules():
    """获取所有已存在的模块列表（用于下拉选择）"""
    # 从 SkillNode 和 User 中提取去重后的模块
    node_modules = db.session.query(SkillNode.module).distinct().all()
    user_modules = db.session.query(User.module).distinct().all()
    
    all_nodes = set()
    for m in node_modules:
        if m[0]:
            mods = m[0].split(',')
            for mod in mods:
                all_nodes.add(mod.strip())
                
    all_users = set()
    for m in user_modules:
        if m[0]:
            mods = m[0].split(',')
            for mod in mods:
                all_users.add(mod.strip())
                
    return jsonify({
        'node': sorted(list(all_nodes)),
        'user': sorted(list(all_users))
    })


# 初始化数据库
def init_db():
    with app.app_context():
        try:
            # 尝试检查表是否存在
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            # 如果表已存在，检查是否需要迁移
            if 'skill_trees' in existing_tables:
                # 检查是否有新字段
                columns = [col['name'] for col in inspector.get_columns('skill_trees')]
                if 'default_skill_points' not in columns:
                    print("检测到数据库结构需要更新 (SkillTree 添加 default_skill_points)...")
                    try:
                        from sqlalchemy import text
                        db.session.execute(text('ALTER TABLE skill_trees ADD COLUMN default_skill_points INTEGER DEFAULT 10'))
                        db.session.commit()
                        print("✓ SkillTree.default_skill_points 更新完成！")
                    except Exception as e:
                        print(f"SkillTree 迁移失败：{e}")
                        db.session.rollback()
                
                # 更新 module 字段
                columns = [col['name'] for col in inspector.get_columns('skill_trees')]
                if 'module' not in columns:
                    print("检测到数据库结构需要更新 (SkillTree 添加 module)...")
                    try:
                        from sqlalchemy import text
                        db.session.execute(text('ALTER TABLE skill_trees ADD COLUMN module VARCHAR(100) DEFAULT "默认模块"'))
                        db.session.commit()
                        print("✓ SkillTree.module 更新完成！")
                    except Exception as e:
                        print(f"SkillTree.module 更新失败：{e}")
                        db.session.rollback()
            
            if 'users' in existing_tables:
                columns = [col['name'] for col in inspector.get_columns('users')]
                if 'module' not in columns:
                    print("检测到 users 表结构需要更新 (添加 module)...")
                    try:
                        from sqlalchemy import text
                        db.session.execute(text('ALTER TABLE users ADD COLUMN module VARCHAR(100) DEFAULT "默认模块"'))
                        db.session.commit()
                        print("✓ User.module 更新完成！")
                    except Exception as e:
                        print(f"User 表更新失败：{e}")
                        db.session.rollback()
                        
                if 'group' not in columns:
                    print("检测到 users 表结构需要更新 (添加 group)...")
                    try:
                        from sqlalchemy import text
                        db.session.execute(text('ALTER TABLE users ADD COLUMN "group" VARCHAR(20) DEFAULT "A"'))
                        db.session.commit()
                        print("✓ User.group 更新完成！")
                    except Exception as e:
                        print(f"User.group 更新失败：{e}")
                        db.session.rollback()

            if 'skill_nodes' in existing_tables:
                columns = [col['name'] for col in inspector.get_columns('skill_nodes')]
                if 'level' not in columns:
                    print("检测到 skill_nodes 表结构需要更新 (添加 level 和 module)...")
                    try:
                        from sqlalchemy import text
                        db.session.execute(text('ALTER TABLE skill_nodes ADD COLUMN level INTEGER DEFAULT 1'))
                        db.session.execute(text('ALTER TABLE skill_nodes ADD COLUMN module VARCHAR(100) DEFAULT "默认模块"'))
                        db.session.commit()
                        print("✓ skill_nodes 表更新完成 (level, module)！")
                    except Exception as e:
                        print(f"skill_nodes 表更新失败：{e}")
                        db.session.rollback()
                
                # 重新获取列名以检查 link2
                columns = [col['name'] for col in inspector.get_columns('skill_nodes')]
                if 'link2' not in columns:
                    print("检测到 skill_nodes 表结构需要更新 (添加 link2)...")
                    try:
                        from sqlalchemy import text
                        db.session.execute(text('ALTER TABLE skill_nodes ADD COLUMN link2 VARCHAR(500)'))
                        db.session.commit()
                        print("✓ skill_nodes 表更新完成 (link2)！")
                    except Exception as e:
                        print(f"skill_nodes 表（link2）更新失败：{e}")
                        db.session.rollback()
                
                # 添加 sort_index
                columns = [col['name'] for col in inspector.get_columns('skill_nodes')]
                if 'sort_index' not in columns:
                    print("检测到 skill_nodes 表结构需要更新 (添加 sort_index)...")
                    try:
                        from sqlalchemy import text
                        db.session.execute(text('ALTER TABLE skill_nodes ADD COLUMN sort_index INTEGER DEFAULT 0'))
                        db.session.commit()
                        print("✓ skill_nodes 表更新完成 (sort_index)！")
                    except Exception as e:
                        print(f"skill_nodes 表（sort_index）更新失败：{e}")
                        db.session.rollback()
            
            # 创建所有表（如果不存在）
            db.create_all()
            print("数据库初始化完成！")
        except Exception as e:
            print(f"数据库初始化警告：{e}")
            # 如果迁移失败，尝试重新创建
            print("尝试重新创建数据库...")
            db.drop_all()
            db.create_all()
            print("数据库重新创建完成！")
        
        print("\n" + "="*50)
        print("技能树系统已启动！")
        print("="*50)
        print("管理页面: http://localhost:5003/")
        print("展示页面: http://localhost:5003/view.html")
        print("API文档: http://localhost:5003/api/trees")
        print("="*50 + "\n")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5003, host='0.0.0.0')

