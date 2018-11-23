from app import limiter, api
from flask_restful import reqparse, Resource, fields, marshal

from flask_jwt_extended import (
jwt_required
)

from app.helpers.httpResponses import (
    Res200,
    Res201,
    Abort
)

TODOS = {
    '1': {'task': 'build an API'},
    '2': {'task': '?????'},
    '3': {'task': 'three!'},
    '4': {'task': 'empat!'},
    '5': {'task': 'lima!'},
    '6': {'task': 'enam!'},
    '7': {'task': 'tujuh!'},
    '8': {'task': 'profit!'},
    '9': {'task': 'asdasd!'},
}

global_parser = reqparse.RequestParser(bundle_errors=True)
global_parser.add_argument('task', help="Missing field", required=True)


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        Abort(404, "Todo for '{}' doesn't exist.".format(todo_id))


class AllCapsString(fields.Raw):
    def format(self, value):
        return value.upper()


todos_fields = {
    "task": AllCapsString
}


# shows a single todo item and lets you delete a todo item
class Todo(Resource):

    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return Res200(TODOS[todo_id])

    @jwt_required
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return Res200({}, "Todo for '{}' deleted".format(todo_id))

    @jwt_required
    def put(self, todo_id):
        parser = global_parser.copy()
        parser.add_argument('blabla', help='Test err msg. {error_msg}', required=True)

        args = parser.parse_args()
        task = marshal({'task': args['task']}, todos_fields)
        TODOS[todo_id] = task
        return Res201(dict(task), "Todo for '{}' changed".format(todo_id))


# shows a list of all todos, and lets you POST to add new tasks
class Todos(Resource):
    decorators = [
        # limiter.limit("2/minute") # custom limiter
        limiter.exempt,
    ]

    def get(self):
        return Res200(TODOS)

    @jwt_required
    def post(self):
        parser = global_parser.copy()

        args = parser.parse_args()
        todo_id = max(map(int, TODOS.keys())) + 1
        todo_id = '%i' % todo_id

        task = marshal({'task': args['task']}, todos_fields)
        TODOS[todo_id] = task
        return Res201(dict(TODOS[todo_id]))


# Api resource routing
api.add_resource(Todos, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')