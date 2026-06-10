"""
创建管理员用户的脚本
运行此脚本可以快速创建一个管理员用户
"""
from app import app, db, User

def create_admin():
    with app.app_context():
        # 检查是否已存在管理员
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"管理员已存在：{admin.username} (ID: {admin.id})")
            return admin
        
        # 创建管理员
        admin = User(
            username='admin',
            password='admin123',  # 简单密码，实际应该加密
            is_admin=True,
            group='Office'
        )
        db.session.add(admin)
        db.session.commit()
        print(f"管理员创建成功：{admin.username} (ID: {admin.id})")
        return admin

if __name__ == '__main__':
    create_admin()

