"""
技能树后端API - Flask应用
支持技能树的保存、加载、更新和删除
"""
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

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
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 关联用户技能树状态
    skill_tree_states = db.relationship('UserSkillTreeState', backref='user', lazy=True, cascade='all, delete-orphan')


class SkillTree(db.Model):
    """技能树表"""
    __tablename__ = 'skill_trees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50))
    version = db.Column(db.String(20))
    default_skill_points = db.Column(db.Integer, default=10)  # 默认技能点
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
    background_color = db.Column(db.String(20), default='#FFD700')  # 默认金色
    foreground_color = db.Column(db.String(20), default='#000000')
    
    # 技能内容：说明文字和链接
    description = db.Column(db.Text)  # 技能说明文字
    link = db.Column(db.String(500))  # 技能相关链接（如教程、文档等）
    
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


@app.route('/api/users', methods=['POST'])
def create_user():
    """创建用户"""
    data = request.json
    username = data.get('username')
    password = data.get('password', '')
    is_admin = data.get('is_admin', False)
    
    if not username:
        return jsonify({'error': '用户名不能为空'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    user = User(username=username, password=password, is_admin=is_admin)
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
        'created_at': user.created_at.isoformat()
    } for user in users])


@app.route('/api/trees', methods=['GET'])
def get_all_trees():
    """获取所有技能树列表"""
    trees = SkillTree.query.all()
    return jsonify([{
        'id': tree.id,
        'name': tree.name,
        'author': tree.author,
        'version': tree.version,
        'created_at': tree.created_at.isoformat(),
        'updated_at': tree.updated_at.isoformat()
    } for tree in trees])


@app.route('/api/trees', methods=['POST'])
def create_tree():
    """创建新的技能树"""
    data = request.json
    default_points = data.get('default_skill_points', 10)
    
    tree = SkillTree(
        name=data.get('name', '未命名技能树'),
        author=data.get('author', 'system'),
        version=data.get('version', '1.0'),
        default_skill_points=default_points
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
    nodes = SkillNode.query.filter_by(tree_id=tree_id).all()
    
    # 构建jsmind格式的数据
    mind_data = build_jsmind_data(tree, nodes, user_id)
    
    return jsonify(mind_data)


@app.route('/api/trees/<int:tree_id>', methods=['PUT'])
def update_tree(tree_id):
    """更新整个技能树"""
    tree = SkillTree.query.get_or_404(tree_id)
    data = request.json
    
    tree.name = data.get('name', tree.name)
    tree.author = data.get('author', tree.author)
    tree.version = data.get('version', tree.version)
    if 'default_skill_points' in data:
        tree.default_skill_points = data.get('default_skill_points', tree.default_skill_points)
    tree.updated_at = datetime.now()
    
    # 先获取现有节点的颜色信息，以便在更新时保留
    existing_nodes = SkillNode.query.filter_by(tree_id=tree_id).all()
    color_map = {}
    for node in existing_nodes:
        color_map[node.node_id] = {
            'background_color': node.background_color,
            'foreground_color': node.foreground_color
        }
    
    # 删除旧节点
    SkillNode.query.filter_by(tree_id=tree_id).delete()
    db.session.flush()  # 确保删除操作完成
    
    # 保存新节点
    if 'data' in data and data['data']:
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


@app.route('/api/trees/<int:tree_id>/nodes/<node_id>', methods=['PUT'])
def update_node(tree_id, node_id):
    """更新单个节点"""
    node = SkillNode.query.filter_by(tree_id=tree_id, node_id=node_id).first_or_404()
    data = request.json
    
    node.topic = data.get('topic', node.topic)
    node.direction = data.get('direction', node.direction)
    node.expanded = data.get('expanded', node.expanded)
    node.background_color = data.get('background_color', node.background_color)
    node.foreground_color = data.get('foreground_color', node.foreground_color)
    node.cost = data.get('cost', node.cost)
    node.description = data.get('description', node.description)
    node.link = data.get('link', node.link)
    
    # 不再通过 extra_data 保存颜色信息，颜色只通过 background_color 和 foreground_color 保存
    # 如果还有其他额外数据需要保存，可以在这里处理
    # if 'extra_data' in data:
    #     node.extra_data = json.dumps(data['extra_data'])
    
    node.updated_at = datetime.now()
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
    node = SkillNode.query.filter_by(tree_id=tree_id, node_id=node_id).first_or_404()
    tree = SkillTree.query.get_or_404(tree_id)
    
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
    
    # 检查前置条件：所有的子节点必须已激活才能激活此节点 (叶子节点可以直接激活)
    children = SkillNode.query.filter_by(tree_id=tree_id, parent_id=node.node_id).all()
    if children:
        for child in children:
            child_state = UserSkillTreeState.query.filter_by(
                user_id=user_id, tree_id=tree_id, node_id=child.node_id
            ).first()
            if not child_state or child_state.status != 'activated':
                return jsonify({'error': '所有的子节点全部点亮才能激活此节点'}), 400
    
    # 检查节点状态
    if user_state.status == 'activated':
        return jsonify({'error': '节点已激活'}), 400
    
    # 获取用户在该技能树中的技能点
    root_state = UserSkillTreeState.query.filter_by(
        user_id=user_id, tree_id=tree_id, node_id='root'
    ).first()
    
    if not root_state:
        init_user_tree_state(user_id, tree_id, tree.default_skill_points)
        root_state = UserSkillTreeState.query.filter_by(
            user_id=user_id, tree_id=tree_id, node_id='root'
        ).first()
    
    # 检查技能点是否足够
    if root_state.skill_points < node.cost:
        return jsonify({'error': f'技能点不足，需要 {node.cost} 点，当前 {root_state.skill_points} 点'}), 400
    
    # 激活节点
    user_state.status = 'activated'
    root_state.skill_points -= node.cost
    user_state.updated_at = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        'message': '节点激活成功',
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


def save_nodes(tree_id, node_data, parent_id=None):
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
        link=node_data.get('link', '')
    )
    
    # 保存额外数据（排除颜色相关字段，颜色只通过 background_color 和 foreground_color 保存）
    extra = {}
    excluded_keys = ['id', 'topic', 'direction', 'expanded', 'children', 
                     'background-color', 'foreground-color', 
                     'original-background-color', 'original-foreground-color',
                     'status', 'cost', 'description', 'link']
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
            for child in node_data['children']:
                if child and isinstance(child, dict) and 'id' in child:
                    save_nodes(tree_id, child, node_data['id'])
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
            'link': node.link or '',  # 技能链接
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
                if root:
                    if 'children' not in root:
                        root['children'] = []
                    root['children'].append(node_map[node.node_id])
    
    # 确保根节点存在
    if not root:
        # 如果没有根节点，创建一个默认的
        root = {
            'id': 'root',
            'topic': tree.name or '技能树',
            'direction': None,
            'expanded': True,
            'status': 'activated',
            'cost': 0,
            'background-color': '#FFD700',
            'foreground-color': '#000000',
            'children': []
        }
    
    # 确保所有节点都有必要的字段
    def ensure_node_fields(node):
        if not isinstance(node, dict):
            return node
        # 确保有必要的字段
        if 'id' not in node:
            node['id'] = 'node_' + str(hash(str(node)))
        if 'topic' not in node:
            node['topic'] = '未命名节点'
        if 'expanded' not in node:
            node['expanded'] = True
        if 'status' not in node:
            node['status'] = 'locked'
        if 'cost' not in node:
            node['cost'] = 1
        if 'children' not in node:
            node['children'] = []
        # 递归处理子节点
        if node['children']:
            node['children'] = [ensure_node_fields(child) for child in node['children']]
        return node
    
    root = ensure_node_fields(root)
    
    return {
        'meta': {
            'name': tree.name,
            'author': tree.author,
            'version': tree.version,
            'skill_points': user_skill_points if user_id else tree.default_skill_points,
            'total_skill_points': tree.default_skill_points
        },
        'format': 'node_tree',
        'data': root
    }


# 提供静态文件服务
@app.route('/')
def index():
    """首页 - 管理页面"""
    return send_file('index.html')

@app.route('/view.html')
def view():
    """展示页面"""
    return send_file('view.html')

@app.route('/<path:filename>')
def static_files(filename):
    """提供静态文件（CSS、JS等）"""
    if filename.startswith('libs/'):
        return send_from_directory('.', filename)
    return send_file(filename)


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
                    print("检测到数据库结构需要更新...")
                    print("正在迁移数据库...")
                    try:
                        from sqlalchemy import text
                        # 添加新字段
                        db.session.execute(text('ALTER TABLE skill_trees ADD COLUMN default_skill_points INTEGER DEFAULT 10'))
                        # 更新现有记录的默认值
                        db.session.execute(text('UPDATE skill_trees SET default_skill_points = 10 WHERE default_skill_points IS NULL'))
                        db.session.commit()
                        print("✓ 数据库迁移完成！")
                    except Exception as e:
                        print(f"迁移失败：{e}")
                        print("建议：删除 instance/skill_tree.db 文件后重新启动")
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
        print("管理页面: http://localhost:5000/")
        print("展示页面: http://localhost:5000/view.html")
        print("API文档: http://localhost:5000/api/trees")
        print("="*50 + "\n")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000, host='0.0.0.0')

