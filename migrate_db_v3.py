"""
数据库迁移脚本 V3
用于添加 is_leader 字段并创建 learning_tasks 表
"""
from app import app, db, User, LearningTask
from sqlalchemy import text

def migrate_database():
    """迁移数据库结构"""
    with app.app_context():
        try:
            # 检查 users 表是否存在 is_leader 字段
            inspector = db.inspect(db.engine)
            if 'users' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('users')]
                
                if 'is_leader' not in columns:
                    print("正在为 users 表添加 is_leader 字段...")
                    db.session.execute(text('ALTER TABLE users ADD COLUMN is_leader BOOLEAN DEFAULT 0'))
                    db.session.commit()
                    print("✓ is_leader 字段添加成功")
                else:
                    print("✓ is_leader 字段已存在")
            
            # 创建新表（如果不存在）
            db.create_all()
            print("\n数据库迁移完成！")
            
        except Exception as e:
            print(f"迁移失败：{e}")
            raise

if __name__ == '__main__':
    migrate_database()
