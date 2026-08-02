from flask import request, jsonify
from . import api_bp
from ..auth import login_required
from ..models import db
from ..models.todo import Todo


@api_bp.route('/todos')
def get_todos():
    todos = Todo.query.order_by(Todo.done.asc(), Todo.created_at.desc()).all()
    return jsonify({
        'code': 0,
        'message': 'ok',
        'data': [t.to_dict() for t in todos],
    })


@api_bp.route('/todos', methods=['POST'])
@login_required
def create_todo():
    data = request.get_json() or {}
    content = (data.get('content') or '').strip()
    if not content:
        return jsonify({'code': 1, 'message': '内容不能为空'}), 400

    todo = Todo(content=content)
    db.session.add(todo)
    db.session.commit()
    return jsonify({'code': 0, 'message': 'ok', 'data': todo.to_dict()})


@api_bp.route('/todos/<int:todo_id>', methods=['PATCH'])
@login_required
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'code': 1, 'message': '事项不存在'}), 404

    data = request.get_json() or {}
    if 'done' in data:
        todo.done = bool(data['done'])
    db.session.commit()
    return jsonify({'code': 0, 'message': 'ok', 'data': todo.to_dict()})
