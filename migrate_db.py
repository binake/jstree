"""
数据库迁移脚本
用于更新现有数据库结构，添加新字段
"""
from app import app, db
from sqlalchemy import text

def migrate_database():
    """迁移数据库结构"""
    with app.app_context():
        try:
            # 检查 skill_trees 表是否存在 default_skill_points 字段
            inspector = db.inspect(db.engine)
            if 'skill_trees' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('skill_trees')]
                
                if 'default_skill_points' not in columns:
                    print("正在添加 default_skill_points 字段...")
                    db.session.execute(text('ALTER TABLE skill_trees ADD COLUMN default_skill_points INTEGER DEFAULT 10'))
                    db.session.execute(text('UPDATE skill_trees SET default_skill_points = 10 WHERE default_skill_points IS NULL'))
                    db.session.commit()
                    print("✓ default_skill_points 字段添加成功")
                else:
                    print("✓ default_skill_points 字段已存在")
            
            # 创建新表（如果不存在）
            db.create_all()
            print("\n数据库迁移完成！")
            
        except Exception as e:
            print(f"迁移失败：{e}")
            print("\n如果迁移失败，可以删除数据库文件重新创建：")
            print("1. 停止 Flask 服务器")
            print("2. 删除 instance/skill_tree.db 文件")
            print("3. 重新启动服务器，系统会自动创建新数据库")
            raise

if __name__ == '__main__':
    migrate_database()

